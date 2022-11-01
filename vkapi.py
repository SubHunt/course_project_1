import requests


class VK:

    def __init__(self, access_token, user_id, qty_photo=5, version='5.131'):
        self.token = access_token
        self.id = user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}
        self.qty_photo = qty_photo

    def users_info(self):
        """Функция получает фотографии пользователя"""
        url = 'https://api.vk.com/method/photos.get'
        params = {'user_id': self.id, 'album_id': 'wall', 'photo_sizes': 1, 'extended': 1, 'count': self.qty_photo}
        response = requests.get(url, params={**self.params, **params})

        return response.json()
