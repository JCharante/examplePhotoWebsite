import os
from flask import Flask, request, jsonify, url_for, render_template, make_response, redirect, current_app, send_from_directory
from werkzeug.utils import secure_filename
import helper_functions, database_functions
import config

#UPLOAD_FOLDER = '/images'
#UPLOAD_FOLDER = '/home/jcharante/Projects/ePW/images'
UPLOAD_FOLDER = config.image_storage_path()
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# App routes


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/admin/panel')
def admin_panel():
    return


@app.route('/account/create', methods=['GET', 'POST', 'OPTIONS'])
def route_account_create():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        data = request.json
        response = {
            'success': False
        }
        if data is not None:
            username = data.get('username', None)
            password = data.get('password', None)
            if username is not None and password is not None:
                uc = database_functions.create_user(username, password)
                if uc[0] is True:
                    response['success'] = True
                    response['uid'] = uc[1]
        return jsonify(**response)
    else:
        return


@app.route('/account/login', methods=['GET', 'POST', 'OPTIONS'])
def route_account_login():
    if request.method == 'GET':
        return render_template("login.html");
    elif request.method == 'POST':
        data = request.json
        response = {
            'success': False
        }
        if data is not None:
            username = data.get('username', None)
            password = data.get('password', None)
            if username is not None and password is not None:
                attempt = database_functions.login(username, password)
                if attempt[0] is True:
                    response['success'] = True
                    response['uid'] = attempt[1]
        return jsonify(**response)
    else:
        return


@app.route('/image/claim', methods=['POST', 'OPTIONS'])
def route_image_claim():
    response = {
        'success': False
    }
    if request.method == 'POST':
        data = request.json
        if data is not None:
            uid = data.get('uid', None)
            title = data.get('title', None)
            image_id = data.get('image_id', None)
            if uid is not None and title is not None and image_id is not None:
                database_functions.claim_image(title, uid, image_id)
                response['success'] = True
            else:
                response['error_message'] = 'no uid, title, or image id sent'
        else:
            response['error_message'] = 'No data sent'
    return jsonify(**response)


@app.route('/image/upload', methods=['GET', 'POST', 'OPTIONS'])
def route_image_upload():
    response = {
        'success': False
    }
    if request.method == 'GET':
        return render_template("image_upload.html")
    elif request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(**response)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return jsonify(**response)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            image_iid = helper_functions.generate_uid()
            filename = image_iid + '.' + filename.split('.')[len(filename.split('.')) - 1]
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            si = database_functions.new_image("untitled", "unclaimed", filename, iid=image_iid)
            if si[0]:
                response['image_id'] = si[1]
                response['success'] = True
        return jsonify(**response)
    else:
        return


@app.route('/image/<int:image_id>/edit', methods=['GET', 'POST', 'OPTIONS'])
def route_image_edit(image_id):
    return


@app.route('/image/<int:image_id>/remove', methods=['GET', 'POST', 'OPTIONS'])
def route_image_remove(image_id):
    return


@app.route('/image/<image_id>/view')
def route_image_view(image_id):
    filename = database_functions.get_file_name_for_image(image_id)[1]
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/image/<int:image_id>/like', methods=['GET', 'POST', 'OPTIONS'])
def route_image_like(image_id):
    return


app.run(debug=True, host='0.0.0.0', port=7004)