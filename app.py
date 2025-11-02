from flask import Flask, request, jsonify
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logging.error('No file part')
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        logging.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400
    if file.content_length > 5 * 1024 * 1024:  # Limit to 5MB
        logging.error('File size exceeds the limit of 5MB')
        return jsonify({'error': 'File size exceeds the limit of 5MB.'}), 400
    try:
        # Only handle CSV files for now, can extend for Excel
        if file.filename.lower().endswith('.csv'):
            df = pd.read_csv(file)
            return jsonify({'message': 'File uploaded successfully', 'data': df.head().to_dict()}), 200
        else:
            logging.error('Invalid file type. Requested: %s', file.filename)
            return jsonify({'error': 'Invalid file type. Please upload a valid CSV file (.csv).'}) , 400
    except pd.errors.EmptyDataError:
        logging.error('No data in the file')
        return jsonify({'error': 'No data in the file'}), 400
    except pd.errors.ParserError:
        logging.error('Error parsing the file')
        return jsonify({'error': 'Error parsing the file. Please check the file format.'}), 400
    except Exception as e:
        logging.error('An error occurred: %s', str(e))
        return jsonify({'error': f'An error occurred while processing the file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)