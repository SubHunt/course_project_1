import requests
from datetime import datetime


class VK:
    URL = 'https://api.vk.com/method/'

    def __init__(self, access_token, qty_photo, user_id, version='5.131'):
        self.token = access_token
        self.user_id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.qty_photo = qty_photo

    def user_info(self, user_id):
        user_url = self.URL + 'users.get'
        user_params = {
            'user_ids': user_id
        }
        params = {**self.params, **user_params}
        response = requests.get(user_url, params).json()
        first_name = response['response'][0]['first_name']
        last_name = response['response'][0]['last_name']
        self.user_id = response['response'][0]['id']
        print(f'По введенным данным мы нашли: {first_name} {last_name} id: {self.user_id}')
        return first_name, last_name, self.user_id

    def photos_info(self):
        items = self.photos_get()['response']['items']
        photos_info = []
        likes_count = []
        repeat_likes_count = []

        for like in items:
            likes_count.append(like['likes']['count'])

        for like in likes_count:
            if likes_count.count(like) > 1:
                repeat_likes_count.append(like)

        for item in items:
            like = item['likes']['count']
            date_photo = datetime.utcfromtimestamp(item['date']).strftime('%d-%m-%Y')
            info = {
                'size': item['sizes'][-1]['type'],
                'link': item['sizes'][-1]['url']
            }

            if like in repeat_likes_count:
                info['file_name'] = f'{like}_{date_photo}.jpg'
                photos_info.append(info)
            else:
                info['file_name'] = f'{like}.jpg'
                photos_info.append(info)
        return photos_info

    def photos_get(self):
        self.user_info(self.user_id)
        album = input('Фото забираем со стены или из профиля?\n'
                      ' Введите wall или profile: ').lower()
        photos_url = self.URL + 'photos.get'
        photos_params = {
            'owner_id': self.user_id,
            'album_id': album,
            'rev': 0,
            'extended': 1,
            'count': self.qty_photo
        }

        params = {**self.params, **photos_params}
        response = requests.get(photos_url, params).json()

        return response
