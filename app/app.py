from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import uuid

app = Flask(__name__)
CORS(app)  


UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


uploaded_items = []

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        
        if 'file' not in request.files:
            
            text_data = request.form.get('text', '')
            if text_data:
                item_id = str(uuid.uuid4())
                new_item = {
                    'id': item_id,
                    'fileName': text_data,
                    'fileType': 'text',
                    'uploadedAt': str(datetime.now())
                }
                uploaded_items.append(new_item)
                return jsonify(new_item), 201
            return jsonify({'error': 'No file or text provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        
        filename = str(uuid.uuid4()) + '_' + file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

       
        item_id = str(uuid.uuid4())
        new_item = {
            'id': item_id,
            'fileName': filename,
            'fileType': file.content_type,
            'uploadedAt': str(datetime.now())
        }
        uploaded_items.append(new_item)

        return jsonify(new_item), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/uploaded-items', methods=['GET'])
def get_uploaded_items():
    return jsonify(uploaded_items)

@app.route('/api/delete-item/<item_id>', methods=['DELETE'])
def delete_item(item_id):
    global uploaded_items
    original_length = len(uploaded_items)
    uploaded_items = [item for item in uploaded_items if item['id'] != item_id]
    
    if len(uploaded_items) < original_length:
        return jsonify({'message': 'Item deleted successfully'}), 200
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/api/interact', methods=['POST'])
def interact_with_text():
    try:
        text = request.json.get('text', '')
        
        interaction_result = f"Processed text: {text}"
        
        return jsonify({'result': interaction_result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    from datetime import datetime
    app.run(debug=True)