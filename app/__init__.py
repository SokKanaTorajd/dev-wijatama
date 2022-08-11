from flask import Flask, render_template, request, \
    redirect, url_for, session, flash
from flask_paginate import Pagination, get_page_args
from werkzeug.utils import secure_filename

from app.cloud_storage.gcp_storage import upload_blob_from_filename, \
    download_blob_as_bytes, list_blobs
from app.config import SECRET_KEY, IG_POSTS_COLL
from app.tasks.clustering import start_clustering
from app.tasks.instagram import mongo, get_insights
from app.tasks.notification import db
from app.utils.set_pagination import set_offset

import pandas as pd
import datetime


app = Flask(__name__)
app.secret_key = SECRET_KEY

ig_post_coll = IG_POSTS_COLL

## FIXME
def notif():
	tanggal = datetime.datetime.today()
	tanggal = tanggal.strftime("%Y-%m-%d")
	notifikasi=db.get_notif(tanggal)
	session['notifikasi'] = notifikasi[0]


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        try:
            login_data = db.login(username, password)
            
            if username==login_data[1] and password==login_data[2]:
                session['id'] = login_data[0]
                session['username'] = login_data[1]
                session['nama_lengkap'] = login_data[3]
                return redirect(url_for('dashboard_view'))
            
        except TypeError:
            error = 'Invalid username or password! Please try again.'
            return render_template('index.html', error=error)

    if request.method == 'GET':
        return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        nama_lengkap = request.form['nama_lengkap']
        email = request.form['email']
        user_data = (username, password, nama_lengkap, email)
        db.add_user(user_data)
        return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard_view():
    return render_template('dashboard.html')

@app.route('/data-posting-produk')
def instagram_post_data():
    query = {
            'permalink': 1, 'id': 1, 
            'produk_1': 1, 'produk_2': 1, 
            'produk_3': 1, 'produk_4': 1
        }
    links = mongo.getAllDocument(ig_post_coll, query)
    data = []
    for item in links:
        id = item['id']
        permalink = item['permalink']
        try:
            produk_1 = item['produk_1']
        except KeyError:
            produk_1 = ''
        try:
            produk_2 = item['produk_2']
        except KeyError:
            produk_2 = ''
        try:
            produk_3 = item['produk_3']
        except KeyError:
            produk_3 = ''
        try:
            produk_4 = item['produk_4']
        except KeyError:
            produk_4 = ''
        elements = (id, permalink, produk_1, produk_2, produk_3, produk_4)
        data.append(elements)
    
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(data)
    pagination_data = set_offset(data, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('data-posting-produk.html', data=pagination_data,
                            pagination=pagination, page=page, per_page=per_page,)

@app.route('/update-data-posting/<id>', methods=['GET', 'POST'])
def update_instagram_post(id):
    if request.method == 'GET':
        query = {
            'permalink': 1, 'id': 1, 
            'produk_1': 1, 'produk_2': 1, 
            'produk_3': 1, 'produk_4': 1
        }
        data = mongo.getByOne(ig_post_coll, query)
        id = data['id']
        permalink = data['permalink']
        try:
            produk_1 = data['produk_1']
        except KeyError:
            produk_1 = ''
        try:
            produk_2 = data['produk_2']
        except KeyError:
            produk_2 = ''
        try:
            produk_3 = data['produk_3']
        except KeyError:
            produk_3 = ''
        try:
            produk_4 = data['produk_4']
        except KeyError:
            produk_4 = ''
        return render_template('update-data-posting-produk.html', id=id, 
                                permalink=permalink, produk_1=produk_1, 
                                produk_2=produk_2, produk_3=produk_3,
                                produk_4=produk_4)
    
    if request.method=='POST':
        query = {
            'id': request.form['id'],
            'permalink': request.form['permalink']
        }
        new_values = {
            "$set":
            {
                'produk_1': request.form['produk_1'],
                'produk_2': request.form['produk_2'],
                'produk_3': request.form['produk_3'],
                'produk_4': request.form['produk_4'],
            }}
        mongo.updateByOne(ig_post_coll, query, new_values)
        flash('Data berhasil diupdate')
        return redirect(url_for('instagram_post_data'))

@app.route('/delete-data-posting/<id>', methods=['GET', 'POST'])
def delete_post_data(id):
    mongo.deleteByOne(ig_post_coll, 'id', id)
    flash('Data berhasil dihapus')
    return redirect(url_for('instagram_post_data'))

@app.route('/unggah-data')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(filename)
        destination_folder = 'sales-data/'
        upload_blob_from_filename(filename, destination_folder)
        flash('File berhasil diunggah')
        return redirect(url_for('upload'))

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
        get_insights.delay(session['id'], token['user_access_token'])
        return render_template('collect-data.html')

@app.route('/start-process', methods=['GET'])
def start_process():
    if request.method == 'GET':
        start_clustering.delay(session['id'])
        flash('Proses sedang dilakukan. Silahkan tunggu')
        return redirect(url_for('dashboard_view'))

@app.route('/hasil-rekomendasi')
def output_clustering():
    dest_folder = 'clustering-results/'
    files = list_blobs(dest_folder)
    latest = None
    for i, file in enumerate(files):
        try:
            # get files timestamp
            ts_prev = files[i][1].timestamp()
            ts_after = files[i+1][1].timestamp()
            if ts_prev < ts_after:
                latest = files[i+1]
        except IndexError:
            latest = files[i]
    filename = latest[0]
    print(filename)
    contents = download_blob_as_bytes(filename, dest_folder)
    result = pd.read_excel(contents)

    return render_template('results.html', tables=[result.to_html(classes='data', header="true")])

@app.route('/notifikasi')
def notify():
    return render_template('notification.html')

@app.route('/profil/<id>', methods=['GET', 'POST'])
def user_profil(id):
    if request.method == 'GET':
        user_data = db.get_user_by_id(id)
        return render_template('profil.html', id=user_data[0], username=user_data[1], 
                                password=user_data[2], nama_lengkap=user_data[3],
                                email=user_data[4])

    if request.method == 'POST':
        user_id = request.form['id']
        username = request.form['username']
        password = request.form['password']
        nama_lengkap = request.form['nama_lengkap']
        email = request.form['email']
        data = (username, password, nama_lengkap, email)
        db.update_user(data)
        flash('Data berhasil diupdate')
        return redirect(url_for("user_profil", id=user_id))

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')

@app.route('/tos')
def tos():
    return render_template('privacy.html')
