
from crewai import Crew, Task, Agent
from crewai_tools import SerperDevTool
from ListenerTool import Listener
from CustomerTool import CustomerTalker
from DealerTool import DealerTalker
from langchain import OpenAI
from dotenv import load_dotenv
import os
import warnings
warnings.filterwarnings("ignore")

load_dotenv()
api_key = os.environ["OPENAI_API_KEY"]

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", max_tokens=1000, openai_api_key = api_key)
function_calling_llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", max_tokens=1000, openai_api_key = api_key)


listen = Listener()
talker = CustomerTalker()
dealer = DealerTalker()

telemetry_agent = Agent(
    llm=llm,
    function_calling_llm=function_calling_llm,
    role="Vehicle Telemetry tracker",
    goal="Find the vehicle that have reached the threshold value specified",
    backstory="You are a tracker that has access to vehicle telemetry data that can be used to check the status of those vehicles and report those that are above the threshold ",
    allow_delegation=False,
    tools=[listen],
    max_iter = 3,
    verbose=1,
)

task1 = Task(
    description="Check vehicle telemetry data and report vehicles that have exceeded the threshold of 40,000 kilometers driven.",
    expected_output="A list of vehicle numbers and UINs for vehicles that have exceeded the threshold, formatted as bullet points.",
    output_file="task1output.txt",
    agent=telemetry_agent,  # Use the telemetry_agent instead of researcher
)


customer_interaction_agent = Agent(
    llm=llm,
    function_calling_llm=function_calling_llm,
    role="Customer Interaction Specialist",
    goal="Gather customer details including preferred Locations, Dates, and timeslot for service appointments.",
    backstory="You are a friendly and efficient agent tasked with collecting customer preferences for service scheduling.",
    allow_delegation=False,
    tools=[talker],  # Assuming customer_tool is a tool for interacting with customers
    max_iter=3,
    verbose=1
)

task2 = Task(
    description="Interact with customers to collect their preferred Locations, Dates, and timeslots for service appointments.",
    expected_output="A list of customer preferences including Locations, Dates, and timeslots, formatted as bullet points.",
    output_file="customer_details.txt",
    agent=customer_interaction_agent,  # Use the customer_interaction_agent
)

dealer_interaction_agent = Agent(
    llm=llm,
    function_calling_llm=function_calling_llm,
    role="Dealer Engagement Specialist",
    goal="Engage with dealers to verify availability of service slots based on customer preferences.",
    backstory="You are a proactive agent tasked with confirming service slot availability with dealers using customer-provided details.",
    allow_delegation=False,
    tools=[dealer],  # Assuming dealer_talker is a tool for interacting with dealers
    max_iter=3,
    verbose=1,
)

task3 = Task(
    description="Engage with dealers to verify the availability of service slots based on customer preferences for city, date, and time.",
    expected_output="A confirmation of slot availability status for the customer's preferred city, date, and time.",
    output_file="slot_status.txt",
    agent=dealer_interaction_agent,  # Use the dealer_interaction_agent
)

crew = Crew(agents=[telemetry_agent,customer_interaction_agent,dealer_interaction_agent], tasks=[task1,task2,task3], verbose=1)
print(crew.kickoff())




