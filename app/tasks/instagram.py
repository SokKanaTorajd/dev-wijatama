from app import config
from app.models import MetaAPI, MongoDBModel
from app.tasks import worker
from app.tasks.notification import send_notif
from time import sleep
import datetime

mongo = MongoDBModel(config.DB_NAME, config.MONGODB_URI)
api = MetaAPI()

@worker.task(name='instagram.get_insights')
def get_insights(user_session, access_token):
    api.user_access_token = access_token
    print('user_access_token is received')
    # get fb_id
    fb_profile = api.get_fbID()
    print('fb id was succesfully collected')
    print(fb_profile)
    sleep(5)

    # get page_id
    pages_info = api.get_fbPages()
    print('fb page(s) was succesfully collected')
    print(pages_info)
    sleep(5)

    # get ig_id
    ig_info = api.get_igID()
    print('ig id was succesfully collected')
    print(ig_info)
    sleep(5)

    # get profile instagram
    ig_profile = api.get_igProfile()
    print(ig_profile)
    sleep(5)

    # input to db
    data = {
        'facebook_profile': fb_profile,
        'facebook_pages': pages_info,
        'instagram_profile': ig_profile,
        'instagram_id': ig_info,
    }
    mongo.insertByOne('instagram', data)

    # get media_id(s)
    ig_posts = api.get_igMedias()
    print('ig post was succesfully collected')
    posts_data = {
        'posts': ig_posts
    }
    mongo.insertByOne('ig-posts', posts_data)
    sleep(5)

    # get media_insight(s)
    medias = [(elem['id'], elem['media_type'], elem['permalink']) for elem in ig_posts]
    media_insights = []
    counter = 0
    for field in medias:
        insight = api.get_mediaInsights(field[0], media_type=field[1], permalink=field[2])
        insight['id'] = field[0]
        media_insights.append(insight)
        mongo.insertByOne('media-insights', insight)
        counter += 1
        print(counter)
        sleep(3)
    print('media insights was succesfully collected')
    sleep(5)

    time_now = datetime.datetime.now()
    messages = 'media insights was succesfully collected.'
    notif_data = (user_session, messages, time_now)
    
    return send_notif.delay(notif_data)
