from flask import Flask, request, jsonify

app=Flask(__name__)

import fitz
import requests
import io


@app.route("/")
def home():
    return "Home"



@app.route("/get-pdf",methods=["POST"])
def pdf():
    # URL of the online PDF file
   
    #pdf_url = 'https://media.geeksforgeeks.org/wp-content/uploads/d.pdf'

    url = request.get_json()
    ans=url['link']
    print(ans)

    # if url:
    #     url=url
    # else:
    #     url=pdf_url

    # Download the PDF
    response = requests.get(ans)
    pdf_bytes = response.content

    # Convert bytes to a file-like object
    pdf_file = io.BytesIO(pdf_bytes)

    # Create a PDF document object
    pdf_document = fitz.open(stream=pdf_file, filetype='pdf')

    # Read each page of the PDF
    ans=[]
    for page_num in range(len(pdf_document)):
        page = pdf_document[page_num]
        text = page.get_text()
        ans.append(text)
    return ans

if __name__ == "__main__":
    app.run(debug=True)

