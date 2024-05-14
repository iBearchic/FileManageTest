from flask import Flask, request, send_file, jsonify
from auth import auth
from storage import save_file, delete_file, get_file
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    file_data = file.read()
    file_hash = save_file(file_data)
    return jsonify({'hash': file_hash})

@app.route('/delete', methods=['POST'])
@auth.login_required
def delete_file_route():
    data = request.json
    if 'hash' not in data:
        return jsonify({'error': 'No hash provided'}), 400
    file_hash = data['hash']
    if delete_file(file_hash):
        return jsonify({'message': 'File deleted'})
    return jsonify({'error': 'File not found'}), 404

@app.route('/download/<file_hash>', methods=['GET'])
def download_file(file_hash):
    file_data = get_file(file_hash)
    if file_data:
        return send_file(
            io.BytesIO(file_data),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=file_hash
        )
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
