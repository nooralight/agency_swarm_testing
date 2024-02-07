from agency_swarm import set_openai_key
import os
from dotenv import load_dotenv
load_dotenv()

openai_key = os.getenv('OPENAI_KEY')
set_openai_key(openai_key)

from agency_swarm import Agency, Agent

intro_manager = Agent(name="Intro Manager",
            description="This helper bot asks for username, and their birthday",
            instructions="As a personal bot, you will ask user for their full name. Later after receiving the name, you will ask for their brith year. Later if user want to know this age, you will talk with the AGE CALCULATOR AGENT for that."
)
print(intro_manager)

age_calculator = Agent(name="AGE CALCULATOR AGENT",
            description="This helper bot calculate users age",
            instructions = "you will get the user's age from the Intro Manager, and will calculate the age. Send reply with a message like this: I am the AFE CALCULATOR AGENT, let me know if you need anything later"
)



agency = Agency([intro_manager,
                 [intro_manager, age_calculator]],shared_instructions="You all are a part of the team who will help me")

print(agency)

while True:
    question = input("Ask me questions : ")
    completion_output = agency.get_completion(question, yield_messages=False)
    print(type(completion_output))
    print(completion_output)

