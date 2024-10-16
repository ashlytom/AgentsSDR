
from crewai import Crew, Task, Agent
from crewai_tools import SerperDevTool
from langchain import OpenAI
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", max_tokens=1000, openai_api_key = api_key)
function_calling_llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", max_tokens=500, openai_api_key = api_key)


search = SerperDevTool()

researcher = Agent(
    llm=llm,
    function_calling_llm=function_calling_llm,
    role="Senior AI Researcher",
    goal="Find promising research in the field of AI Research.",
    backstory="You are a veteran AI Researcher writer with a background in modern Artificial intelligence.",
    allow_delegation=False,
    tools=[search],
    max_iter = 3,
    verbose=1,
)

task1 = Task(
    description="Search the internet and find 5 examples of promising AI Agentic implementation in Automobile Industry in India.",
    expected_output="A detailed bullet point summary on each of the topics. Each bullet point should cover the topic, background and why the innovation is useful.",
    output_file="task1output.txt",
    agent=researcher,
)

writer = Agent(
    llm=llm,
    role="Senior Blog Writer",
    goal="Write technical articles from provided research.",
    backstory="You are a veteran AI writer with a background in modern Artificial intelligence.",
    allow_delegation=False,
    verbose=1,
)



task2 = Task(
    description="Write an notion post on next breakthroughs in AI research.",
    expected_output="A detailed blog speech with an intro, body and conclusion.",
    output_file="task2output.txt",
    agent=writer,
)

crew = Crew(agents=[researcher, writer], tasks=[task1, task2], verbose=1)
print(crew.kickoff())




