import base64
import json
from io import BytesIO

AUTH_CREDENTIALS = base64.b64encode(b"user1:password1").decode('utf-8')

def upload_file(client):
    data = {
        'file': (BytesIO(b'this is test file content'), 'temp.txt')
    }
    response = client.post('/upload', data=data, headers={'Authorization': f'Basic {AUTH_CREDENTIALS}'})
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert 'hash' in response_data
    return response_data['hash']

def test_upload_file(client):
    file_hash = upload_file(client)
    assert file_hash is not None

def test_download_file(client):
    file_hash = upload_file(client)
    response = client.get(f'/download/{file_hash}')
    assert response.status_code == 200
    assert response.data == b'this is test file content'
    assert response.headers['Content-Disposition'] == f'attachment; filename={file_hash}'

def test_delete_file(client):
    file_hash = upload_file(client)
    response = client.post('/delete', data=json.dumps({'hash': file_hash}), headers={'Content-Type': 'application/json', 'Authorization': f'Basic {AUTH_CREDENTIALS}'})
    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data['message'] == 'File deleted'

    # Verify file is deleted
    response = client.get(f'/download/{file_hash}')
    assert response.status_code == 404

