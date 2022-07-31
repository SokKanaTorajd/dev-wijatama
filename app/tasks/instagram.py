from app import config
from app.models import MetaAPI, MongoDBModel
from app.tasks import worker
from time import sleep

mongo = MongoDBModel(config.DB_NAME, config.MONGODB_URI)
api = MetaAPI()

@worker.task(name='instagram.get_insights')
def get_insights(access_token):
    api.user_access_token = access_token
    # get fb_id
    fb_profile = api.get_fbID()
    sleep(5)

    # get page_id
    pages_info = api.get_fbPages()
    sleep(5)

    # get ig_id
    ig_info = api.get_igID()
    sleep(5)

    # get media_id(s)
    ig_posts = api.get_igMedias()
    sleep(5)

    # get media_insight(s)
    medias = [(elem['id'], elem['media_type'], elem['permalink']) for elem in ig_posts['data']]
    media_insights = []
    for field in medias:
        insight = api.get_mediaInsights(field[0], media_type=field[1], permalink=field[2])
        insight['id'] = field[0]
        media_insights.append(insight)
        sleep(3)

    sleep(5)
    
    # get account_insight

    # input to db
    data = {
        'facebook_profile': fb_profile,
        'facebook_pages': pages_info,
        'instagram_profile': ig_info,
        'instagram_posts': ig_posts,
        'media_insights': media_insights
    }
    mongo.insertByOne('instagram', data)
    return 'All data successfully acquired.'
