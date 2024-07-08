from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# Get the API key from the environment variable
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

app = Flask(__name__)

def calculate_bmi(height: float, weight: float) -> float:
    return weight / (height / 100) ** 2

def get_openai_response(prompt: str) -> str:
    try:
        response = client.Completion.create(
            model="gpt-3.5-turbo-1106",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_fitness_advice', methods=['POST'])
def get_fitness_advice():
    data = request.json
    height = float(data.get('height'))
    weight = float(data.get('weight'))
    goal = data.get('goal').lower()
    body_type = data.get('body_type').lower()

    bmi = calculate_bmi(height, weight)

    diet_prompt = f"Provide diet tips for {goal} for someone with a {body_type} body type."
    exercise_prompt = f"Provide an exercise regimen for {goal} for someone with a {body_type} body type."

    diet_tips = get_openai_response(diet_prompt)
    exercise_regimen = get_openai_response(exercise_prompt)

    return jsonify({
        'bmi': bmi,
        'diet_tips': diet_tips,
        'exercise_regimen': exercise_regimen
    })

if __name__ == '__main__':
    app.run(debug=True)
