from flask import Flask, request, send_file, jsonify
from auth import auth
from storage import save_file, delete_file, get_file
import io
import logging

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    if 'file' not in request.files:
        logger.error('No file part')
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    file_data = file.read()
    file_hash = save_file(file_data)
    logger.info(f'File uploaded with hash: {file_hash} by user: {auth.current_user()}')
    return jsonify({'hash': file_hash})

@app.route('/delete', methods=['POST'])
@auth.login_required
def delete_file_route():
    data = request.json
    if 'hash' not in data:
        logger.error('No hash provided in the request')
        return jsonify({'error': 'No hash provided'}), 400
    
    file_hash = data['hash']
    if delete_file(file_hash):
        logger.info(f'File with hash: {file_hash} deleted by user: {auth.current_user()}')
        return jsonify({'message': 'File deleted'})
    
    logger.error(f'File with hash: {file_hash} not found for deletion by user: {auth.current_user()}')
    return jsonify({'error': 'File not found'}), 404

@app.route('/download/<file_hash>', methods=['GET'])
def download_file(file_hash):
    file_data = get_file(file_hash)
    if file_data:
        logger.info(f'File with hash: {file_hash} downloaded')
        return send_file(
            io.BytesIO(file_data),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=file_hash
        )
    
    logger.error(f'File with hash: {file_hash} not found for download')
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
