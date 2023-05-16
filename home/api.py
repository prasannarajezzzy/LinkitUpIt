import re
from collections import defaultdict
from nltk.corpus import stopwords
import openai
import spacy
import re

max_tokens = 1024
model_engine = "text-davinci-003"
openai.api_key = "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"

def get_keywords(job_description):

    professional_keywords = {
        'Programming languages': {'Java', 'Python', 'C++', 'C#', 'JavaScript', 'TypeScript', 'PHP', 'Ruby', 'Swift', 'Objective-C', 'Kotlin', 'Scala', 'Go', 'R', 'Perl', 'SQL', 'NoSQL'},
        'Web development': {'HTML', 'CSS', 'React', 'Angular', 'Vue.js', 'jQuery', 'Bootstrap', 'Sass', 'Less', 'Webpack', 'Gatsby', 'Jekyll', 'WordPress'},
        'Frameworks and libraries': {'Spring', 'Hibernate', 'Django', 'Flask', 'Ruby on Rails', 'Express.js', 'Nest.js', 'Laravel', 'Symfony', 'CakePHP', 'CodeIgniter', 'Node.js', 'Express', 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn'},
        'Database technologies': {'MySQL', 'PostgreSQL', 'Oracle', 'SQL Server', 'MongoDB', 'Redis', 'Cassandra', 'Elasticsearch', 'Firebase', 'Amazon RDS', 'Amazon DynamoDB'},
        'Cloud technologies': {'AWS', 'Azure', 'Google Cloud', 'Kubernetes', 'Docker', 'Ansible', 'Terraform', 'Puppet', 'Chef'},
        'DevOps tools': {'Jenkins', 'GitLab', 'GitHub', 'Travis CI', 'CircleCI', 'Bitbucket', 'SonarQube', 'New Relic', 'AppDynamics'},
        'Methodologies and processes': {'Agile', 'Scrum', 'Kanban', 'Waterfall', 'Continuous Integration', 'Continuous Delivery', 'Test-Driven Development', 'Behavior-Driven Development', 'Pair Programming'},
        'Other skills': {'Algorithms', 'Data Structures', 'Object-Oriented Programming', 'Functional Programming', 'RESTful APIs', 'GraphQL', 'Microservices', 'Serverless', 'Linux', 'Windows', 'Networking', 'Security'}
    }

    job_description = job_description.lower()

    words = re.findall(r'\b\w+\b', job_description)

    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    word_count = defaultdict(int)
    for word in words:
        word_count[word] += 1

    keywords = sorted(word_count, key=word_count.get, reverse=True)

    categorized_keywords = {}
    for category in professional_keywords:
        categorized_keywords[category] = set()
        for keyword in professional_keywords[category]:
            if keyword.lower() in word_count:
                categorized_keywords[category].add(keyword)
    result_keywords=[]
    for key in categorized_keywords:
        if(categorized_keywords[key]!=set()):
            # print(f"The value of key '{key}' is: {categorized_keywords[key]}")
            for i in categorized_keywords[key]:
                result_keywords.append(i)

    return result_keywords

def resume_parse(resume_text, job_description):
   
    nlp = spacy.load("en_core_web_sm")

   
    resume_doc = nlp(resume_text)
    print(resume_doc)

    candidate_name = None
    candidate_email = None
    candidate_phone = None
    for ent in resume_doc.ents:
        if ent.label_ == "PERSON" and not candidate_name:
            candidate_name = ent.text
        elif ent.label_ == "EMAIL" and not candidate_email:
            candidate_email = ent.text
        elif ent.label_ == "PHONE_NUMBER" and not candidate_phone:
            candidate_phone = ent.text

  
    candidate_experience = []
    candidate_education = []
    candidate_skills = []
    for section in resume_doc.noun_chunks:
        if "experience" in section.text.lower():
            candidate_experience.append(section.text)
        elif "education" in section.text.lower():
            candidate_education.append(section.text)
        elif "skills" in section.text.lower():
            candidate_skills.append(section.text)
            
    experience_match_score = 0
    education_match_score = 0
    skills_match_score = 0
    for section in job_description.split("\n"):
        if "experience" in section.lower():
            for experience in candidate_experience:
                if experience.lower() in section.lower():
                    experience_match_score += 1
        elif "education" in section.lower():
            for education in candidate_education:
                if education.lower() in section.lower():
                    education_match_score += 1
        elif "skills" in section.lower():
            for skill in candidate_skills:
                if skill.lower() in section.lower():
                    skills_match_score += 1


    match_score = (
        (experience_match_score * 0.6)
        + (education_match_score * 0.3)
        + (skills_match_score * 0.1)
    )


    return match_score

def getResponse(prompt):
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return completion.choices[0].text



def calculate_matching_score(job_description, resume):
    # Convert both inputs to lowercase for case-insensitive matching
    job_description = job_description.lower()
    resume = resume.lower()

    # Remove non-alphanumeric characters and split into individual words
    job_description_words = re.findall(r'\w+', job_description)
    resume_words = re.findall(r'\w+', resume)

    # Calculate the matching score by counting the common words
    common_words = set(job_description_words) & set(resume_words)
    matching_score = len(common_words) / len(job_description_words) * 100

    return matching_score

def suggest_keywords(job_description, resume):
    job_description = job_description.lower()
    resume = resume.lower()

    # Initialize a set of professional keywords for a software engineer
    professional_keywords = {
        'python',
        'java',
        'c++',
        'javascript',
        'web development',
        'software development',
        'object-oriented programming',
        'algorithm',
        'data structures',
        'database',
        'problem-solving',
        'agile methodology',
        'version control',
        'debugging',
        'testing',
        'software architecture',
        'framework',
        'API',
        'cloud computing',
        'full-stack development',
        'front-end development',
        'back-end development',
        'mobile app development',
        'machine learning',
        'data analysis',
        'teamwork',
        'communication',
        'documentation'
    }

    # Remove non-alphanumeric characters and split job description into individual words
    job_description_words = re.findall(r'\w+', job_description)

    # Find professional keywords from job description that are missing in the resume
    missing_keywords = [keyword for keyword in professional_keywords if keyword in job_description_words and keyword not in resume]

    return missing_keywords


