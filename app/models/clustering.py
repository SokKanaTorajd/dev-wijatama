from app.cloud_storage.gcp_storage import download_blob_as_bytes, list_blobs
from app.tasks.instagram import mongo
from app.utils.data_processing import extract_metrics, \
    aggregate_by_product, casting_int, data_scaling

import pandas as pd
import pickle


def process_instagram_data():
    """
    process instagram post and metrics data.
    output: product_insights in dataframe object
    """
    # get instagram post from mongodb
    post_query = {
        'id': 1, 'media_type': 1,
        'timestamp': 1, 'produk_1': 1,
        'produk_2': 1, 'produk_3': 1, 'produk_4': 1
    }
    ig_posts = mongo.getAllDocument('ig-posts', post_query)

    # get instagram media insights from mongodb
    insight_query = {'data': 1, 'id': 1}
    media_insights = mongo.getAllDocument('media-insights', insight_query)

    # create dataframe
    posts_df = pd.DataFrame(ig_posts, columns=['id', 'media_type', 'timestamp', 'produk_1', 'produk_2', 'produk_3', 'produk_4'])
    metrics_df = pd.DataFrame(media_insights, columns=['data', 'id'])
    post_metrics_df = posts_df.merge(metrics_df, how='left', on='id')

    # type casting column timestamp and filter post based on specific time
    post_metrics_df['timestamp'] = post_metrics_df['timestamp'].astype('datetime64')
    post_metrics_df['year'] = post_metrics_df['timestamp'].dt.year
    post_metrics_df['month'] = post_metrics_df['timestamp'].dt.month
    filtered_metrics = post_metrics_df[(post_metrics_df['year'] == 2022) & (post_metrics_df['month'] < 6)]
    filtered_metrics.reset_index(inplace=True)

    # extract insights from column data
    columns_name = [
        'id', 'engagement', 'impressions', 'reach', 
        'saved', 'plays', 'shares', 'total_interactions'
    ]
    extracted_insights = extract_metrics(filtered_metrics)
    counted_metrics = pd.DataFrame(extracted_insights, columns=columns_name)

    # join and filter data in specific columns
    filtered_metrics = filtered_metrics.merge(counted_metrics, how='left', on='id')
    filtered_metrics.drop(columns='index', inplace=True)
    filtered_metrics = filtered_metrics[
        (filtered_metrics['media_type'] != 'VIDEO') & 
        (filtered_metrics['produk_1'].notna()) & 
        (filtered_metrics['produk_1'] != '-')
    ]
    filtered_metrics.reset_index(inplace=True)

    # aggregate instagram metric data based on product's name
    column_targets= ['engagement', 'impressions', 'reach', 'saved']
    df_1 = aggregate_by_product(filtered_metrics, column_targets, 'produk_1')
    df_2 = aggregate_by_product(filtered_metrics, column_targets, 'produk_2')
    df_3 = aggregate_by_product(filtered_metrics, column_targets, 'produk_3')
    df_4 = aggregate_by_product(filtered_metrics, column_targets, 'produk_4')
    product_insights = pd.concat([df_1, df_2, df_3, df_4], ignore_index=True)
    product_insights = product_insights.groupby('produk')[column_targets].sum()
    return product_insights


def process_sales_data():
    # get sales data from Google Cloud Storage
    dest_folder = 'sales-data/'
    files = list_blobs(dest_folder)
    newest = max(files, key=lambda x: x[1])
    filename = newest[0]
    contents = download_blob_as_bytes(filename, dest_folder)
    sales_df = pd.read_excel(contents)
    sales_df['Produk Dilihat'] = sales_df['Produk Dilihat'].map(casting_int)
    sales_df['Keranjang'] = sales_df['Keranjang'].map(casting_int)
    sales_df['Wishlist'] = sales_df['Wishlist'].map(casting_int)

    # rename columns
    columns_rename = {
        'Nama Produk': 'produk',
        'Produk Terjual': 'produk_terjual', 
        'Produk Dilihat': 'produk_dilihat',
        'Keranjang': 'keranjang',
        'Pesanan': 'pesanan',
        'Wishlist': 'wishlist'
    }
    sales_df = sales_df.rename(columns=columns_rename)

    # aggregate product sales by 'produk'
    targets = ['produk_terjual', 'produk_dilihat', 'keranjang', 'wishlist']
    sales_df = aggregate_by_product(sales_df, targets, 'produk')
    sales_df = sales_df.set_index('produk')
    return sales_df


def merge_instagram_and_sales(ig_df, sales_df):
    # join social media data and sales data
    product_sales_insights = sales_df.join(ig_df)
    # remove NaN value inside entire DataFrame
    if product_sales_insights.isnull().values.any():
        product_sales_insights.dropna(inplace=True)
    df_columns = product_sales_insights.columns
    scaled_df = data_scaling(product_sales_insights, df_columns)
    return scaled_df


def load_model_cluster():
    # get model from Google Cloud Storage
    filename = 'kmeans_model.pickle'
    dest_folder = 'model/'
    downloaded_model = download_blob_as_bytes(filename, dest_folder)
    model = pickle.loads(downloaded_model)
    return model


def process_clustering(model, dataframe):
    copied_df = dataframe.copy()
    copied_df = copied_df[
        [
            'produk_terjual', 'produk_dilihat', 
            'keranjang', 'wishlist', 'engagement', 
            'impressions', 'reach', 'saved'
        ]
    ]
    # re-scale data
    scaled_df = data_scaling(copied_df, copied_df.columns)
    # clustering
    dataframe['cluster'] = model.predict(scaled_df)
    return dataframe
