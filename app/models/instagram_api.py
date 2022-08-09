from time import sleep
import requests, json


class MetaAPI(object):
    def __init__(self):
        self.base_url = 'https://graph.facebook.com/'
        self.api_version = 'v14.0'
        self.user_access_token = None
        self.fb_id = None
        self.page_id = None
        self.ig_id = None

    def get_fbID(self):
        params = {
            'fields': 'id,name',
            'access_token': self.user_access_token,
        }
        url = f'{self.base_url}{self.api_version}/me'
        response = requests.get(url, params=params)
        response = response.json()
        self.fb_id = response['id']
        return response

    def get_fbPages(self, fb_id=None):
        if fb_id is not None:
            self.fb_id = fb_id
        params = {
            'access_token': self.user_access_token,
        }
        url = f'{self.base_url}{self.api_version}/{self.fb_id}/accounts'
        response = requests.get(url, params=params)
        response = response.json()
        if len(response['data']) == 1:
            self.page_id = response['data'][0]['id']

        return response

    def get_igID(self, page_id=None):
        if page_id is not None:
            self.page_id = page_id
        params = {
            'fields': 'instagram_business_account',
            'access_token': self.user_access_token,
        }
        url = f'{self.base_url}{self.api_version}/{self.page_id}/'
        response = requests.get(url, params=params)
        response = response.json()
        self.ig_id = response['instagram_business_account']['id']
        return response
    
    def get_igProfile(self, ig_id=None):
        if ig_id is not None:
            self.ig_id = ig_id
        params = {
            'fields': 'id,username,name,profile_picture_url, \
                biography,media_count,follows_count,followers_count',
            'access_token': self.user_access_token,
        }
        url = f'{self.base_url}{self.api_version}/{self.ig_id}'
        response = requests.get(url, params=params)
        response = response.json()
        return response

    def get_igMedias(self, ig_id=None):
        if ig_id is not None:
            self.ig_id = ig_id
        params = {
            'fields': 'id,caption,media_type,media_url, \
                permalink, thumbnail_url,timestamp,username, \
                like_count,comments_count',
            'access_token': self.user_access_token,
        }
        url = f'{self.base_url}{self.api_version}/{self.ig_id}/media'
        response = requests.get(url, params=params)
        response = response.json()

        try:
            all_medias = [media for media in response['data']]
            while 'next' in response['paging'].keys():
                try:
                    if len(response['data']) > 0:
                        params['after'] = response['paging']['cursors']['after']
                        response = requests.get(url, params=params)
                        response = response.json()
                        for data in response['data']:
                            all_medias.append(data)
                        sleep(5)
                    if len(response['data']) == 0:
                        break
                        
                except KeyError:
                    break

            return all_medias

        except KeyError:
            return response

    def get_mediaInsights(self, post_id, media_type=None, permalink=None):
        if media_type == 'CAROUSEL_ALBUM':
            params = {
                'metric': 'carousel_album_engagement,carousel_album_impressions,carousel_album_reach,carousel_album_saved,carousel_album_video_views',
                'period': 'lifetime',
                'access_token': self.user_access_token,
            }

        if 'reel' in permalink:
            params = {
                'metric': 'comments,likes,plays,reach,saved,shares,total_interactions',
                'period': 'lifetime',
                'access_token': self.user_access_token,
            }

        else:
            params = {
                'metric': 'engagement,impressions,reach,saved',
                'period': 'lifetime',
                'access_token': self.user_access_token,
            }

        url = f'{self.base_url}{self.api_version}/{post_id}/insights'
        response = requests.get(url, params=params)
        return response.json()

    def get_accountInsights(self, ig_id):
        """
        Not available for IG account with fewer than 100 followers
        """
        pass
