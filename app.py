from flask import Flask, request, jsonify
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return log_and_respond('No file part', 400)
    file = request.files['file']
    if file.filename == '':
        return log_and_respond('No selected file', 400)
    if file.content_length > 10 * 1024 * 1024:  # Limit to 10MB
        return log_and_respond('File size exceeds the limit of 10MB', 400)
    try:
        if file.filename.lower().endswith('.csv'):
            df = pd.read_csv(file)
            return jsonify({'message': 'File uploaded successfully', 'data': df.head().to_dict()}), 200
        else:
            return log_and_respond('Invalid file type. Please upload a valid CSV file (.csv).', 400)
    except pd.errors.EmptyDataError:
        return log_and_respond('No data in the file', 400)
    except pd.errors.ParserError:
        return log_and_respond('Error parsing the file. Please check the file format.', 400)
    except Exception as e:
        return log_and_respond(f'An error occurred while processing the file: {str(e)}', 500)


def log_and_respond(message, status_code):
    logging.error(message)
    return jsonify({'error': message}), status_code

if __name__ == '__main__':
    app.run(debug=True)