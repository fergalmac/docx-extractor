from flask import Flask, request, jsonify
from docx import Document
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/extract-docx', methods=['POST'])
def extract_docx():
    try:
        # Log the incoming request body
        app.logger.info("Received request: %s", request.json)

        # Get file URL from request body
        file_url = request.json.get("fileUrl")
        if not file_url:
            app.logger.error("No fileUrl provided in the request.")
            return jsonify({"error": "fileUrl is required"}), 400

        # Download the DOCX file
        app.logger.info("Downloading file from URL: %s", file_url)
        response = requests.get(file_url)
        response.raise_for_status()  # Raises an error for bad status codes

        # Read the DOCX file content
        app.logger.info("Reading DOCX file content.")
        docx_file = BytesIO(response.content)
        doc = Document(docx_file)
        text_content = '\n'.join([para.text for para in doc.paragraphs if para.text.strip()])

        app.logger.info("Successfully extracted text from DOCX.")
        return jsonify({"extractedText": text_content})

    except requests.exceptions.RequestException as e:
        # Catch any issues with file download
        app.logger.error(f"Failed to download DOCX file: {str(e)}")
        return jsonify({"error": "Failed to download DOCX file", "details": str(e)}), 500

    except Exception as e:
        # Catch all other issues
        app.logger.error(f"An error occurred during processing: {str(e)}")
        return jsonify({"error": "A server error has occurred", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
