extract_skills_prompt_template = """
Extract the Skills from the given query:

Query Text:
{text}

Important:
Return the output in JSON format.
Skills will be a list always.

"""


parse_resume_prompt_template = """
Extract the following information from this resume text:
- Name
- Email
- Phone number
- Skills
- Education (degree and institution)
- Internship (company and duration)
- Work experience (company and duration)

Generate a Summary of the profile mentionning all the skills the candidate has and describing the projects and relevant work experiences.

Resume Text:
{text}

Important:
Return the output in JSON format.
If any field is not found, leave it empty.
Education, Internship and Work experience will be a list of dictionaries always.
Skills will be a list always.
Summary will always be a string.

"""