import json
import pdfplumber
from docx import Document
 
 
def find_candidates_with_skills(skill_list, neo4j_handler):
    query = """
    MATCH (a:Applicant)-[:HAS_SKILL]->(s:Skill)
    WHERE ANY(skill IN $skills WHERE TOLOWER(s.name) CONTAINS TOLOWER(skill))
    RETURN a.name AS applicant, COLLECT(s.name) AS matched_skills
    """
    with neo4j_handler.driver.session() as session:
        result = session.run(query, skills=skill_list)
        return [record for record in result]
    
    

def get_candidate(query,neo4j_handler, vector_index,skill_extraction_chain, skill_list=None):
    
    if not skill_list:
        skill_list = []
        
    # Perform similarity search
    response = vector_index.similarity_search(query)
    vector_search_candidates = {res.metadata['name'] for res in response}
    
    # Extract skills from the query
    output = skill_extraction_chain.run({"text": query})
    output = output.strip('```json\n').strip('```')

    # Convert JSON string to a Python dictionary
    skills_data = json.loads(output)
    
    # Combine all skills
    for skill in skills_data['Skills']:
        if skill not in skill_list:
            skill_list.append(skill)

    # Perform skill-based search
    skill_search_results = find_candidates_with_skills(skill_list, neo4j_handler)
    skill_search_candidates = {record['applicant'] for record in skill_search_results}

    # Find common candidates
    common_candidates = vector_search_candidates.intersection(skill_search_candidates)
    
    # Prepare the result details
    result_details = []

    # Add common candidates first (highest priority)
    for record in skill_search_results:
        if record['applicant'] in common_candidates:
            result_details.append({
                'Applicant': record['applicant'],
                'Matched_skills': record['matched_skills'],
                'Source': ['both']
            })

    # Add skill-based candidates who are not in the common list
    for record in skill_search_results:
        if record['applicant'] not in common_candidates:
            result_details.append({
                'Applicant': record['applicant'],
                'Matched_skills': record['matched_skills'],
                'Source': ['skills']
            })

    # Add vector-based candidates who are not in the common list or skill list
    for res in response:
        if res.metadata['name'] not in skill_search_candidates and res.metadata['name'] not in common_candidates:
            result_details.append({
                'Applicant': res.metadata['name'],
                'Matched_skills': [],
                'Source': ['vector']
            })

    return result_details


def parse_resume(file_path):
    # Extract text from the resume
    if file_path.endswith(".pdf"):
        with pdfplumber.open(file_path) as pdf:
            text = " ".join([page.extract_text() for page in pdf.pages])
    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        text = " ".join([p.text for p in doc.paragraphs])
    else:
        raise ValueError("Unsupported file format")
    
    return text