from glob import glob
from tqdm import tqdm
import json
import sys
sys.path.append("..")
from utils import parse_resume
from chains import parse_resume_chain
from Neo4jHandler.initialize_neo4j_handler import neo4j_handler



resume_files = glob(r"D:\Reflex\Resumes_2022_24\*")

for resume_file in tqdm(resume_files, desc="Processing Resumes"):
    try:
        resume_text = parse_resume(resume_file)
        output = parse_resume_chain.run({"text": resume_text})
        output = output.strip('```json\n').strip('```')

        # Convert JSON string to a Python dictionary
        resume_data = json.loads(output)
        
        # Add applicant data to Neo4j
        neo4j_handler.add_applicant(
            name=resume_data["Name"],
            email = resume_data['Email'],
            phone_number = resume_data['Phone number'],
            summary = resume_data['Summary'],
            skills=resume_data["Skills"],
            education=resume_data["Education"],
            work_experience=resume_data["Work experience"],
            internship_experience= resume_data['Internship'],
        )
    
    except Exception as e:
        print(f"Error processing {resume_file}: {e}")
        continue
    
    