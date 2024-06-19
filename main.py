from crewai import Agent, Crew, Process
from crewai_tools import SerperDevTool
from crewai import Task
from dotenv import load_dotenv
import os

# environment variable `OPENAI_API_KEY` and 'SERPER_API_KEY'

search_tool = SerperDevTool()
load_dotenv()

researcher = Agent(
  role='Company Researcher',
  goal='Gain insights about the company {company}, exploring its focused field, main products, '
       'core values, history, and development goals, and evaluate if it is a good fit for a CS student '
       'who wants to work and learn from an internship.',
  verbose=True,
  memory=True,
  backstory=(
    "With a keen eye for important detail and excellent judgement, and enthusiastic in helping "
    "undergraduate student finding internship, you are skilled at evaluating what "
    "a company is looking for in its interns, and what it can offer a potential intern, and can give "
    "good advice for a job-searching student regarding this company."
  ),
  tools=[search_tool],
  allow_delegation=True,
)

# # Creating a writer agent with custom tools and delegation capability
# resumeWriter = Agent(
#   role='Expert Resume Writer',
#   goal='Create an excellent resume tailor made for company {company} that displays what the company is looking for',
#   verbose=True,
#   memory=True,
#   backstory=(
#     "You are a resume writer and editor with many years of experience, and are skilled at editing succinct,"
#     "readable, one-page resume that are tailor fit to a role. "
#   ),
#   tools=[search_tool],
#   allow_delegation=False
# )

research_task = Task(
  description=(
    "Provide a short, succinct 200 word summary on the provided company, introducing the "
    "the company to the audience: what kind of company is it? what area does it specialize in?"
    "what products do it produce? what is its culture and values?"
    "Further more, list out what it is looking for in its employees (what skills and qualifications), "
    "think of what learning opportunities it offers its employees, and finally end with a "
    "suggestion on whether you think the company is a good fit for a CS student"
  ),
  expected_output='A 100 to 200 word summary highlighting your evaluation of a company',
  tools=[search_tool],
  agent=researcher,
)

# resume_task = Task(
#   description=(
#     "Given a long resume {resume} containing all of a student's past experiences, and "
#     "given a role description {role}, edit the resume "
#     "so that it becomes only 1 page long, and make sure relevant experiences are kept "
#     "and highlighted, while not so relevant ones are cut. Tailor the language of the resume"
#     "to the role. Make sure the resume is clear, succinct, professional."
#   ),
#   expected_output='A shortened one-page resume tailored to the role.',
#   tools=[search_tool],
#   agent=resumeWriter,
#   async_execution=False,
#   output_file='new-resume.md'
# )

crew = Crew(
  agents=[researcher],
  tasks=[research_task],
  process=Process.sequential,
  memory=True,
  cache=True,
  max_rpm=100,
  share_crew=True
)

result = crew.kickoff(inputs={'company': 'Oracle'})
print(result)