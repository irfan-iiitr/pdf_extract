from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

import fitz
import requests
import io

@app.route("/")
def home():
    return "Home"

@app.route("/get-pdf", methods=["PUT"])
def pdf():
    data = request.get_json()
    pdf_url = data.get('link')

    if pdf_url:
        try:
            # Download the PDF
            response = requests.get(pdf_url)
            response.raise_for_status()
            pdf_bytes = response.content

            # Convert bytes to a file-like object
            pdf_file = io.BytesIO(pdf_bytes)

            # Create a PDF document object
            pdf_document = fitz.open(stream=pdf_file, filetype='pdf')

            # Read each page of the PDF
            pdf_text = []
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text = page.get_text()
                pdf_text.append(text)

            return jsonify({'pdf_text': pdf_text})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Missing or invalid "link" parameter in JSON data'}), 400

if __name__ == "__main__":
    app.run(debug=True)
