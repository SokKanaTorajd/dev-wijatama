from app.models.clustering import process_instagram_data, \
    process_sales_data, merge_instagram_and_sales, \
    process_clustering, load_model_cluster
from app.cloud_storage.gcp_storage import upload_blob_from_string
from app.tasks import worker
from app.tasks.notification import send_notif

import datetime, io
from pandas import ExcelWriter


@worker.task(name='clustering.start_clustering')
def start_clustering(user_session):
    # data processing
    ig_posts = process_instagram_data()
    sales_data = process_sales_data()
    product_sales_insights = merge_instagram_and_sales(ig_posts, sales_data)

    # load model and predicting
    model = load_model_cluster()
    result = process_clustering(model, product_sales_insights)

    # convert dataframe into bytes
    output = io.BytesIO()
    writer = ExcelWriter(output)
    result.to_excel(writer)
    writer.save()
    xlsx_data = writer.getvalue()
    now = datetime.datetime.now()
    default_filename = 'Hasil_Rekomendasi_'
    t = now.strftime("%d-%m-%Y-%H:%M:%S")
    file_ext = '.xlsx'
    file_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    dest_folder = f'clustering-results/{default_filename}{t}{file_ext}'
    
    # upload result
    upload_blob_from_string(xlsx_data, dest_folder, file_type)

    # send notification
    time_now = datetime.datetime.now()
    messages = 'media insights was succesfully collected.'
    notif_data = (user_session, messages, time_now)
    
    return send_notif.delay(notif_data)
