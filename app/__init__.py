from flask import Flask, render_template, request
from app.tasks.instagram import get_insights


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login-fb')
def login_fb():
    return render_template('login-fb.html')

@app.route('/collect-data', methods=['GET','POST'])
def collect_data():
    tokens = []
    if request.method == 'POST':
        auth_response = request.get_json()
        tokens.append(auth_response['authResponse']['accessToken'])
        return {'message': 'data received'}

    if request.method == 'GET':
        print('initializig to collect data')
        get_insights.delay(tokens[0])
        return 'processing data'

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/tos')
def tos():
    return render_template('privacy.html')
