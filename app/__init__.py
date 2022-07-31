from flask import Flask, render_template, request
from app.tasks.instagram import get_insights


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login-fb')
def login_fb():
    return render_template('login-fb.html')

@app.route('/collect-data', methods=['POST'])
def collect_data():
    if request.method == 'POST':
        auth_response = request.get_json()
        access_token = auth_response.authResponse['accessToken']
        get_insights.delay(access_token)
        return render_template('collect-data.html')
    
    return render_template('index.html')

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/tos')
def tos():
    return render_template('privacy.html')
