from neo4j import GraphDatabase

# Neo4j handler class
class Neo4jHandler:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_applicant(self, name, email, phone_number, summary, skills, education, work_experience, internship_experience):
        """
        Add an applicant with their details to the Neo4j database.
        :param name: Name of the applicant
        :param email: Email id of the applicant
        :param phone_number: Phone No. of the applicant
        :param summary: Profile summary of the applicant
        :param skills: List of skills
        :param education: List of dictionaries, each containing degree and institution
        :param work_experience: List of dictionaries, each containing company and duration
        :param internship_experience: List of dictionaries, each containing company and duration

        """
        # Filter out empty or None values for lists
        summary = summary if summary else None
        skills = skills if skills else None
        education = education if education else None
        work_experience = work_experience if work_experience else None
        internship_experience = internship_experience if internship_experience else None

        with self.driver.session() as session:
            session.execute_write(
                self._add_applicant_transaction, name, email, phone_number, summary, skills, education, work_experience, internship_experience
            )

    @staticmethod
    def _add_applicant_transaction(tx, name, email, phone_number, summary, skills, education, work_experience, internship_experience):
        # Build the query with checks to avoid empty lists being processed
        query = """
        CREATE (a:Applicant {name: $name, email: $email, phone_number: $phone_number, summary: $summary})
        """

        if skills:
            query += """
            FOREACH (skill IN $skills | 
                MERGE (s:Skill {name: skill}) 
                MERGE (a)-[:HAS_SKILL]->(s))
            """
        if education:
            query += """
            FOREACH (edu IN $education | 
                MERGE (e:Education {degree: edu.degree, institution: edu.institution}) 
                MERGE (a)-[:HAS_EDUCATION]->(e))
            """
        if work_experience:
            query += """
            FOREACH (exp IN $work_experience | 
                MERGE (c:Company {name: exp.company}) 
                MERGE (a)-[:WORKED_AT {duration: exp.duration}]->(c))
            """
        if internship_experience:
            query += """
            FOREACH (exp IN $internship_experience | 
                MERGE (c:Company {name: exp.company}) 
                MERGE (a)-[:INTERNED_AT {duration: exp.duration}]->(c))
            """
        
        # Execute the query with the passed parameters
        tx.run(query, name=name, email=email, phone_number=phone_number, 
               summary=summary, skills=skills, education=education, work_experience=work_experience, internship_experience=internship_experience)

    def get_applicant_data(self, name):
        with self.driver.session() as session:
            result = session.execute_read(self._get_applicant_data_transaction, name)  # Updated to execute_read
        return result

    @staticmethod
    def _get_applicant_data_transaction(tx, name):
        query = """
        MATCH (a:Applicant {name: $name})-[r]->(n)
        RETURN type(r) AS Relationship, labels(n) AS NodeType, n AS NodeDetails
        """
        return list(tx.run(query, name=name))
