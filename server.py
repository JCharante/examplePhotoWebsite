from flask import Flask, request, jsonify, url_for, render_template, make_response, redirect, current_app

app = Flask(__name__)


@app.route('/admin/panel')
def admin_panel():

    return str(5)

app.run(debug=True, host='0.0.0.0', port=7004)