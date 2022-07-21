from django.shortcuts import render
from flask import Flask, render_template
# from app.tasks.instagram_scraper import ig_profile, ig_user_post, ig_hashtag_post
# from app.tasks.facebook_scraper import fb_profile, fb_page_post, fb_group_post
# from flask_cors import CORS

app = Flask(__name__)
# CORS(app)

# index
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login-fb')
def login_fb():
    return render_template('login-fb.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/tos')
def tos():
    return render_template('privacy.html')
# # # get instagram profile
# @app.route('/instagram/profile/<username>',methods=['GET'])
# def profileIG(username):
#     if request.method == 'GET':
#         ig_profile.delay(username)
#         return 'scraping instagram profile {} is in progress'.format(username)


# # get instagram profile post
# @app.route('/instagram/post/<username>', methods=['GET'])
# def profilePostIG(username):
#     if request.method == 'GET':
#         ig_user_post.delay(username)
#         return 'scraping instagram posts of {} is in progress.'.format(username)


# # get instagram hashtag post
# @app.route('/instagram/post/hashtag/<hashtag_name>', methods=['GET'])
# def hashtagPostIG(hashtag_name):
#     if request.method == 'GET':
#         ig_hashtag_post.delay(hashtag_name)
#         return 'scraping instagram posts of hashtag {} is in progress.'.format(hashtag_name)

