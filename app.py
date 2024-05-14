import hashlib
from flask import Flask, request, send_file, jsonify
from auth import auth
from flask_sqlalchemy import SQLAlchemy
from storage import save_file, delete_file, get_file
import io
import logging

logging.basicConfig(level=logging.INFO, filename='app.log', filemode='a', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# app configs
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Создание объекта SQLAlchemy
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hash = db.Column(db.String(64), unique=True, nullable=False)
    data = db.Column(db.LargeBinary, nullable=False)

    def __repr__(self):
        return f'<File {self.hash}>'

# Инициализация базы данных
def init_db():
    with app.app_context():
        db.create_all()

@app.route('/upload', methods=['POST'])
@auth.login_required
def upload_file():
    if 'file' not in request.files:
        logger.error('No file part in the request')
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    file_data = file.read()
    file_hash = hashlib.sha256(file_data).hexdigest()

    # Сохранение файла в базе данных
    new_file = File(hash=file_hash, data=file_data)
    db.session.add(new_file)
    db.session.commit()

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

    # Удаление файла из базы данных
    file = File.query.filter_by(hash=file_hash).first()
    if file:
        db.session.delete(file)
        db.session.commit()
        logger.info(f'File with hash: {file_hash} deleted by user: {auth.current_user()}')
        return jsonify({'message': 'File deleted'})
    
    logger.error(f'File with hash: {file_hash} not found for deletion by user: {auth.current_user()}')
    return jsonify({'error': 'File not found'}), 404

@app.route('/download/<file_hash>', methods=['GET'])
def download_file(file_hash):
    # Получение файла из базы данных
    file = File.query.filter_by(hash=file_hash).first()
    if file:
        logger.info(f'File with hash: {file_hash} downloaded')
        return send_file(
            io.BytesIO(file.data),
            mimetype='application/octet-stream',
            as_attachment=True,
            download_name=file_hash
        )
    
    logger.error(f'File with hash: {file_hash} not found for download')
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
