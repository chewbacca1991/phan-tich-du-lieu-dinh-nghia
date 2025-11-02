from flask import Flask, request, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        df = pd.read_csv(file)  # Chỉ xử lý CSV ở đây, có thể mở rộng cho Excel
        return jsonify({'message': 'File uploaded successfully', 'data': df.head().to_dict()})

if __name__ == '__main__':
    app.run(debug=True)
