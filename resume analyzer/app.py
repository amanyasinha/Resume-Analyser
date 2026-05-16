from flask import Flask, render_template, request
import PyPDF2
import openai
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

openai.api_key = "YOUR_API_KEY"

def extract_text(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text()
    return text

def analyze_resume(text):
    prompt = f"""
    Analyze this resume and provide:
    1. Strengths
    2. Missing skills
    3. Suggestions for improvement

    Resume:
    {text}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response['choices'][0]['message']['content']

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None

    if request.method == 'POST':
        file = request.files['resume']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)

        text = extract_text(path)
        result = analyze_resume(text)

    return render_template('index.html', result=result)

if __name__ == "__main__":
    app.run(debug=True)