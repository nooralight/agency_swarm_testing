from flask import Flask, render_template, request, jsonify,session
from datetime import timedelta
import time
from threading import Thread

import os
from dotenv import load_dotenv
load_dotenv()

openai_key = os.getenv('OPENAI_KEY')

app = Flask(__name__)
app.secret_key = '5800d5d9e4405020d527f0587538abbe'


messages = []

agency_arr =[]

from agency_swarm import set_openai_key
set_openai_key(openai_key)
from agency_swarm import Agency, Agent



@app.route('/')
def index():
    session.clear()
    session['messages'] = []
    
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form.get('message')
    if message:
        session['messages'].append(message)

        if "agency" not in agency_arr:
            intro_manager = Agent(name="Intro Manager",
                description="You have the main role to talk with the customers",
                instructions='''You are a personal assistant of mine who is ready to serve me anytime I want, anything I want'''
            )
            print(intro_manager)

            age_calculator = Agent(name="AGE CALCULATOR AGENT",
                        description="Helper bot calculate users age based on birth year",
                        instructions = "you will get the user's birth year from the Intro Manager, and will calculate the age. Send reply with a message like this: I am the AGE CALCULATOR AGENT, let me know if you need anything later"
                    )
            story_writer = Agent(name="STORY WRITTER AGENT",
                        description="Write story from a given context",
                        instructions = "Write short, adventaruos story with the context that will be given to you. There will be some people or main characters in the story. But always put one main character into the story whose name will be *Dennis*. Always try to make the story about *Dennis* and his experience about the context. IMPORTANT: Write a story within 500 characters, not more than this"
                    )

            agency = Agency([intro_manager,
                            [intro_manager, age_calculator],
                            [intro_manager, story_writer]],shared_instructions="You all are a part of the team who will help me. Create your own environment so that I can have full support")
            agency_arr.append(agency)
        
        b_response = agency_arr[0].get_completion(message, yield_messages=False)
        print(b_response)
        session['messages'].append(b_response)

    return render_template("index.html", messages = session.get('messages'))
    
# @app.route('/get_messages')
# def get_messages():

#     return jsonify({'messages': session["messages"]})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True,port=8000)
