from flask import Flask, request, jsonify, url_for, render_template, make_response, redirect, current_app
import helper_functions, database_functions

app = Flask(__name__)

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

@app.route('/image/upload', methods=['GET', 'POST', 'OPTIONS'])
def route_image_upload():
    return

@app.route('/image/edit', methods=['GET', 'POST', 'OPTIONS'])
def route_image_edit():
    return

@app.route('/image/remove', methods=['GET', 'POST', 'OPTIONS'])
def route_image_remove():
    return

@app.route('/image/like', methods=['GET', 'POST', 'OPTIONS'])
def route_image_like():
    return





app.run(debug=True, host='0.0.0.0', port=7004)