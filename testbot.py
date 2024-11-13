from flask import Flask, request, jsonify, render_template, redirect, url_for, send_from_directory
import openai
from dotenv import load_dotenv
import os
import random

app = Flask(__name__)

# Load API key from environment variables
load_dotenv()
openai.api_key = "your-openai-api-key"


# Sample question database with image solutions
questions_db = {
    "Integration by parts method library": [
        {"question": "int ln (x) (x^-1) dx", "image_solution": ""},
        {"question": "int ln(x) (x^-2) dx", "image_solution": "/static/Intergetions by parts/int ln(x) (x^-2) dx.png"},
        {"question": "int ln (x) (x) dx", "image_solution": "/static/Intergetions by parts/int ln (x) (x) dx.png"},
        {"question": "int ln(x) (x^2) dx", "image_solution": "/static/Intergetions by parts/int ln(x) (x^2) dx.png"},
        {"question": "int ln (x^2) (x^-1) dx", "image_solution": "/static/Intergetions by parts/int ln (x^2) (x^-1) dx.png"},
        {"question": "int ln (x^2) (x^-2) dx", "image_solution": "/static/Intergetions by parts/int ln (x^2) (x^-2) dx.png"},
        {"question": "int ln (x^2) (x) dx", "image_solution": "/static/Intergetions by parts/int ln (x^2) (x) dx.png"},
        {"question": "int ln (x^2)(x^2)dx", "image_solution": "/static/Intergetions by parts/int ln (x^2)(x^2)dx.png"},
        {"question": "int sin^-1 x (x) dx", "image_solution": "/static/Intergetions by parts/int sin^-1 x (x) dx.png"},
        {"question": "int sin^-1 x (x^2) dx", "image_solution": "/static/Intergetions by parts/int sin^-1 x (x^2) dx.png"},
        {"question": "int tan^-1 x (x) dx", "image_solution": "/static/Intergetions by parts/int tan^-1 x (x) dx.png"},
        {"question": "int tan^-1 x (x^2) dx", "image_solution": "/static/Intergetions by parts/int tan^-1 x (x^2) dx.png"}
    ],

    # DI method 1st general library
    "DI method 1st general library": [
        {"question": "int (x)(e^x) dx", "image_solution": "/static/DI method 1st general/int (x) (e^x) dx.png"},
        {"question": "int (x)(e^2x) dx", "image_solution": "/static/DI method 1st general/int (x)( e^2x) dx.png"},
        {"question": "int (x)(e^-x) dx", "image_solution": "/static/DI method 1st general/int (x) (e^-x) dx.png"},
        {"question": "int (x)(e^-2x) dx", "image_solution": "/static/DI method 1st general/int (x)(e^-2x) dx.png"},
        {"question": "int (x^2)(e^x) dx", "image_solution": "/static/DI method 1st general/int (x^2) ( e^x) dx.png"},
        {"question": "int (x^2)(e^2x) dx", "image_solution": "/static/DI method 1st general/int (x^2)( e^2x) dx.png"},
        {"question": "int (x^2)(e^-x) dx", "image_solution": "/static/DI method 1st general/int( x^2) ( e^-x) dx.png"},
        {"question": "int (x^2)(e^-2x) dx", "image_solution": "/static/DI method 1st general/int (x^2) ( e^-2x) dx.png"}
    ],

    # DI method 2nd general library
    "DI method 2nd general library": [
        {"question": "int (x) sin(x) dx", "image_solution": "/static/DI method 2nd general/int (x) sin(x) dx.png"},
        {"question": "int (x) sin(2x) dx", "image_solution": "/static/DI method 2nd general/int (x) sin(2x) dx.png"},
        {"question": "int (x) sin(-x) dx", "image_solution": "/static/DI method 2nd general/int (x) sin(-x) dx.png"},
        {"question": "int (x) sin(-2x) dx", "image_solution": "/static/DI method 2nd general/int (x) sin(-2x) dx.png"},
        {"question": "int (x^2) sin(x) dx", "image_solution": "/static/DI method 2nd general/int (x^2) sin(x) dx.png"},
        {"question": "int (x^2) sin(2x) dx", "image_solution": "/static/DI method 2nd general/int (x^2) sin(2x) dx.png"},
        {"question": "int (x^2) sin(-x) dx", "image_solution": "/static/DI method 2nd general/int (x^2) sin(-x) dx.png"},
        {"question": "int (x^2) sin(-2x) dx", "image_solution": "/static/DI method 2nd general/int (x) sin(x) dx.png"}
    ],

    # DI method 3rd general library
    "DI method 3rd general library": [
        {"question": "int (x) cos(x) dx", "image_solution": "/static/DI method 3rd general/int (x) cos(x) dx.png"},
        {"question": "int (x) cos(2x) dx", "image_solution": "/static/DI method 3rd general/int (x) cos(2x) dx.png"},
        {"question": "int (x) cos(3x) dx", "image_solution": "/static/DI method 3rd general/int (x) cos(3x) dx.png"},
        {"question": "int (x) cos(4x) dx", "image_solution": "/static/DI method 3rd general/int (x) cos(4x) dx.png"},
        {"question": "int (x^2) cos(x) dx", "image_solution": "/static/DI method 3rd general/int (x^2) cos(x) dx.png"},
        {"question": "int (x^2) cos(2x) dx", "image_solution": "/static/DI method 3rd general/int (x^2) cos(2x) dx.png"},
        {"question": "int (x^2) cos(3x) dx", "image_solution": "/static/DI method 3rd general/int (x^2) cos(3x) dx.png"},
        {"question": "int (x^2) cos(-x) dx", "image_solution": "/static/DI method 3rd general/int (x^2) cos(-x) dx.png"}
    ],

    # DD method 1st general library
    "DD method 1st general library": [
        {"question": "int (e^x) cos(x) dx", "image_solution": "/static/DD method 1st general/int (e^x) cos(x) dx.png"},
        {"question": "int (e^x) cos(2x) dx", "image_solution": "/static/DD method 1st general/int (e^x) cos(2x) dx.png"},
        {"question": "int (e^-x) cos(x) dx", "image_solution": "/static/DD method 1st general/int (e^-x) cos(x) dx.png"},
        {"question": "int (e^-x) cos(2x) dx", "image_solution": "/static/DD method 1st general/int (e^-x) cos(2x) dx.png"},
        {"question": "int (e^2x) cos(x) dx", "image_solution": "/static/DD method 1st general/int (e^2x) cos(x) dx.png"},
        {"question": "int (e^2x) cos(2x) dx", "image_solution": "/static/DD method 1st general/int (e^2x) cos(2x) dx.png"},
        {"question": "int (e^-2x) cos(x) dx", "image_solution": "/static/DD method 1st general/int (e^-2x) cos(x) dx.png"},
        {"question": "int (e^-2x) cos(2x) dx", "image_solution": "/static/DD method 1st general/int (e^-2x) cos(2x) dx.png"}
    ],

    # DD method 2nd general library
    "DD method 2nd general library": [
        {"question": "int (e^x) sin(x) dx", "image_solution": "/static/DD method 2nd general/int (e^x) sin(x) dx.png"},
        {"question": "int (e^x) sin(2x) dx", "image_solution": "/static/DD method 2nd general/int (e^x) sin(2x) dx.png"},
        {"question": "int (e^-x) sin(x) dx", "image_solution": "/static/DD method 2nd general/int (e^-x) sin(x) dx.png"},
        {"question": "int (e^-x) sin(2x) dx", "image_solution": "/static/DD method 2nd general/int (e^-x) sin(2x) dx.png"},
        {"question": "int (e^2x) sin(x) dx", "image_solution": "/static/DD method 2nd general/int (e^2x) sin(x) dx.png"},
        {"question": "int (e^2x) sin(2x) dx", "image_solution": "/static/DD method 2nd general/int (e^2x) sin(2x) dx.png"},
        {"question": "int (e^-2x) sin(x) dx", "image_solution": "/static/DD method 2nd general/int (e^-2x) sin(x) dx.png"},
        {"question": "int (e^-2x) sin(2x) dx", "image_solution": "/static/DD method 2nd general/int (e^-2x) sin(2x) dx.png"}
    ]
}

# YouTube tutorial links
tutorial_videos = {
    "Can you show me a tutorial on Integration by Parts?": "https://www.youtube.com/watch?v=bLhxQIdbWW8",
    "Can you show me a tutorial on DI method 1st general?": "https://www.youtube.com/watch?v=2I-_SV8cwsw",
    "Can you show me a tutorial on DI method 2nd general?": "https://www.youtube.com/watch?v=2I-_SV8cwsw",
    "Can you show me a tutorial on DI method 3rd general?": "https://www.youtube.com/watch?v=2I-_SV8cwsw",
    "Can you show me a tutorial on DD method 1st general?": "https://www.youtube.com/watch?v=noWsimJHlK0",
    "Can you show me a tutorial on DD method 2nd general?": "https://www.youtube.com/watch?v=AaosD4OzE_o",
    # Add more topic-video links here
}

#Test_Link
test_page = {"start the test" : "file:///C:/FYP%20Semester%202%20ChatGPT%20Project%202024/chatbot_with%20API-20231227T030416Z-001_1/chatbot_with%20API/Second%20Protoge/Chatbot/Python/templates/front%20page.html" ,#Add your test link here

} 

@app.route('/static/<path:filename>')
def send_file(filename):
    return send_from_directory('static', filename)

@app.route('/')
def index():
    return render_template('index.html')

# Handle user queries
@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json.get('query')
    response = process_query(user_input)
    return jsonify(response)


asked_questions = {}

def clean_query(query):
    return query.strip().lower()

def process_query(query):
    if not query:
        return {"response": "Please provide a valid query."}

    #Objective 1 : For generating questions
    if "questions from the topic" in query:
        # Extract the topic and requested number of questions (if provided)
        topic = query.split("topic")[-1].strip()
        num_questions = 6  # Default number of questions

        # Check if user requested a specific number of questions
        if "number" in query:
            try:
                num_questions = int(query.split("number")[-1].strip())
            except ValueError:
                pass  # If conversion fails, keep the default value

        # Retrieve the questions from the database
        questions = questions_db.get(topic, ["No questions available for this topic."])
        question_list = [q["question"] for q in questions]  # Extract question text

        # Limit the number of questions returned to the requested amount
        return {"response": question_list[:num_questions]}

    # Objective 2: For showing solutions with images
    if "solution of" in query:
        problem = query.split("solution of")[-1].strip()
        if not problem:
            return {"response": "Please provide a valid problem."}

        # List of all method libraries
        method_libraries = [
            "Integration by parts method library", 
            "DI method 1st general library", 
            "DI method 2nd general library", 
            "DI method 3rd general library",  
            "DD method 1st general library", 
            "DD method 2nd general library"
        ]

        # Search all libraries for the solution
        for method in method_libraries:
            for question in questions_db.get(method, []):
                if problem in question["question"]:
                    #Dynamically use the image filename stored in the database
                    return {"response": "Here is the solution : ","image_solution": url_for('static',filename='DI method 2nd general/int (x^2) sin(2x) dx.png')}
                    
        return {"response": "Solution not found in the database."}

    # Objective 3: Provide tutorial videos
    elif query in tutorial_videos:
        link = tutorial_videos[query]
        return {"response": f"Here is the tutorial link: {link}"}

    # Objective 4: Link to the Front page (test)
    if query in test_page:
        link = test_page[query]
        return {"response": f"Link here to start the test: {link}"}


    # Default response if no match found
    return {"response": "I'm not sure how to help with that. Could you please ask differently?"}

if __name__ == '__main__':
    app.run(debug=True)