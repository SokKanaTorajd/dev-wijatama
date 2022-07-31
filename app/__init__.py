from flask import Flask, render_template, request
from app.tasks.instagram import mongo, get_insights
import datetime


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login-fb')
def login_fb():
    return render_template('login-fb.html')

@app.route('/collect-data', methods=['GET','POST'])
def collect_data():
    if request.method == 'POST':
        auth_response = request.get_json()
        token = {
            'datetime': datetime.datetime.now(),
            'user_access_token': auth_response['authResponse']['accessToken']
        }
        mongo.insertByOne('tokens', token)
        print('data inserted to mongodb')
        return {'message': 'data received'}

    if request.method == 'GET':
        print('initializing to collect data')
        token = mongo.getToken()
        get_insights.delay(token['user_access_token'])
        return 'processing data'

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/tos')
def tos():
    return render_template('privacy.html')
