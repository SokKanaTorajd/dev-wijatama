from app import config
from app.models import MetaAPI, MongoDBModel
from app.tasks import worker
from time import sleep

mongo = MongoDBModel(config.DB_NAME, config.MONGODB_URI)
api = MetaAPI()

@worker.task(name='instagram.get_insights')
def get_insights(access_token):
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

    # get profile instagram
    ig_profile = api.get_igProfile()
    print(ig_profile)
    sleep(5)

    # get ig_id
    ig_info = api.get_igID()
    print('ig id was succesfully collected')
    print(ig_info)
    sleep(5)

    # get media_id(s)
    ig_posts = api.get_igMedias()
    print('ig post was succesfully collected')
    print(ig_posts)
    sleep(5)

    # get media_insight(s)
    medias = [(elem['id'], elem['media_type'], elem['permalink']) for elem in ig_posts]
    media_insights = []
    for field in medias:
        insight = api.get_mediaInsights(field[0], media_type=field[1], permalink=field[2])
        insight['id'] = field[0]
        media_insights.append(insight)
        sleep(3)
    print('media insights was succesfully collected')
    sleep(5)
    
    # get account_insight

    # input to db
    data = {
        'facebook_profile': fb_profile,
        'facebook_pages': pages_info,
        'instagram_profile': ig_profile,
        'instagram_id': ig_info,
        'instagram_posts': ig_posts,
        'media_insights': media_insights
    }
    mongo.insertByOne('instagram', data)
    return 'All data successfully acquired.'
