from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    try:
        # Only handle CSV files for now, can extend for Excel
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
            return jsonify({'message': 'File uploaded successfully', 'data': df.head().to_dict()}), 200
        else:
            return jsonify({'error': 'Invalid file type. Please upload a CSV file.'}), 400
    except pd.errors.EmptyDataError:
        return jsonify({'error': 'No data in the file'}), 400
    except pd.errors.ParserError:
        return jsonify({'error': 'Error parsing the file. Please check the file format.'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred while processing the file: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)