import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
# from main import process_data
# from utils import some_utility_function

UPLOAD_FOLDER = './data/CSB/sessions/LN05'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route('/api/process', methods=['POST'])
# def process():
#     data = request.json['data']
#     processed_data = process_data(data)
#     return jsonify({'result': processed_data})
#
#
# @app.route('/api/utility', methods=['GET'])
# def utility():
#     result = some_utility_function()
#     return jsonify({'result': result})


@app.route('/api/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({'message': 'File uploaded successfully'})

    return jsonify({'error': 'Invalid file'})


if __name__ == '__main__':
    app.run(debug=True)
