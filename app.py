from flask import Flask, request, jsonify
import google.generativeai as genai
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Configure the Gemini API
GOOGLE_API_KEY = 'AIzaSyBxb1ughJXCz6M9hb7bxlal7ZnfWrNdzAk'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/api/generate', methods=['POST'])
def generate_content():
    data = request.json
    prompt = data.get('prompt')
    path = data.get('path')  # Extract path from request data

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    if not path:
        return jsonify({'error': 'No path provided'}), 400

    # Modify the prompt using the provided path
    prompt = f"Create a {path} using these keywords: {prompt}. (no headings)"

    try:
        response = model.generate_content(prompt)
        generated_text = response.text
        return jsonify({'generated': generated_text})

    except Exception as e:
        return jsonify({'error': f'Failed to generate content: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)