# from __init__ import app

# if __name__ == '__main__':
# 	app.run(debug=True)	
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt #pip install Flask-Bcrypt = https://pypi.org/project/Flask-Bcrypt/
from flask_cors import CORS, cross_origin #ModuleNotFoundError: No module named 'flask_cors' = pip install Flask-Cors
from models import db, User, Teacher, Student
from werkzeug.utils import secure_filename
import os
 
app = Flask(__name__)
 
app.config['SECRET_KEY'] = 'presence-attendance-app'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'
 
# SQLALCHEMY_TRACK_MODIFICATIONS = False
# SQLALCHEMY_ECHO = True
  
bcrypt = Bcrypt(app) 
CORS(app, supports_credentials=True)
db.init_app(app)
  
# with app.app_context():
#     db.create_all()
 
@app.route("/")
def hello_world():
    return "Hello, World!"
 
@app.route("/signup", methods=["POST"])
def signup():
    print(request.data)
    name = request.json["name"]
    username = request.json["username"]
    email = request.json["email"]
    role = request.json["role"]
    classid = request.json["classid"]
    rollid = request.json["rollid"]
    password = request.json["password"]
    # uploaded_files = request.files.getlist('photos')
    
    # for file in uploaded_files:
    #     file.save("C:\\Users\\athir\\mini-project\\presence\\facer-classroom\\data\\enroll\\" + file.filename)

    # return 'Photos uploaded successfully'
 
    user_exists = User.query.filter_by(email=email).first() is not None
 
    if user_exists:
        return jsonify({"error": "Email already exists"}), 409
     
    hashed_password = bcrypt.generate_password_hash(password)
    new_user = User(name=name, username=username, email=email, role=role, classid=classid, rollid=rollid, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
	 # Check if the user is a teacher
    if role == 'teacher':
        # Create a new teacher entry
        new_teacher = Teacher(teacherid=rollid, teachername=name, tmail=email, classid=classid)
        db.session.add(new_teacher)
        db.session.commit()
        
		 # Check if the user is a student
    if role == 'student':
        # Create a new student entry
        new_student = Student(studentrollno=rollid,  classid=classid, stuname=name, stumail=email)
        db.session.add(new_student)
        db.session.commit()
 
    session["user_id"] = new_user.id
 
    return jsonify({
        "id": new_user.id,
        "email": new_user.email
    })
 
@app.route("/login", methods=["POST"])
def login_user():
    email = request.json["email"]
    password = request.json["password"]
  
    user = User.query.filter_by(email=email).first()
  
    if user is None:
        return jsonify({"error": "Unauthorized Access"}), 401
  
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Unauthorized"}), 401
      
    session["user_id"] = user.id
  
    return jsonify({
        "id": user.id,
        "email": user.email
    })

UPLOAD_FOLDER = './data/sessions/LN05'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# def allowed_file1(filename1):
#     return '.' in filename1 and filename1.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
# def allowed_file2(filename2):
#     return '.' in filename2 and filename2.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

# @app.route('/api/upload1', methods=['POST'])
# def upload1():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})

#     if file and allowed_file1(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return jsonify({'message': 'File uploaded successfully'})

#     return jsonify({'error': 'Invalid file'})

# @app.route('/api/upload2', methods=['POST'])
# def upload2():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part'})

#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'No selected file'})

#     if file and allowed_file2(file.filename):
#         filename = secure_filename(file.filename)
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
#         return jsonify({'message': 'File uploaded successfully'})

#     return jsonify({'error': 'Invalid file'})
# @app.route('/upload-photos', methods=['POST'])
# def upload_photos():
#     uploaded_files = request.files.getlist('selectedPhotos')
    
#     for file in uploaded_files:
#         file.save("C:\\Users\\athir\\mini-project\\presence\\facer-classroom\\data\\enroll\\" + file.filename)

#     return 'Photos uploaded successfully'
 
if __name__ == "__main__":
    app.run(debug=True)