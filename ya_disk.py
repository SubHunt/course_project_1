import requests


class YaUploader:
    URL = 'https://cloud-api.yandex.net/v1/disk'

    def __init__(self, token_yd: str, folder):
        self.token = token_yd
        self.folder = folder
        self.headers = {
            "Accept": "application/json",
            "Authorization": "OAuth " + self.token
        }

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    # def upload_link(self, disk_file_path):
    #     """Функция выгружает загруженные файлы из профиля с VK на Яндекс диск"""
    #     upload_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    #     create_folder_url = 'https://cloud-api.yandex.net/v1/disk/resources'
    #     headers = self._get_headers()
    #     params = {"path": disk_file_path, "overwrite": "true"}
    #     # Creating folder  
    #     requests.put(f'{create_folder_url}?path={self.folder}', headers=headers)
    #     res = requests.get(f'{create_folder_url}/upload?path={self.folder}/{disk_file_path}&overwrite=replace',
    #                        headers=headers).json()
    #     with open(disk_file_path, 'rb') as f:
    #         try:
    #             requests.put(res['href'], files={'file': f})
    #         except KeyError:
    #             print(res)
    #     response = requests.get(upload_url, headers=headers, params=params)
    #     return response.json()

    def upload_vk_photo(self, folder, file_name, link):
        url = self.URL + '/resources'
        params = {
            'path': f'{folder}/{file_name}',
            'url': link,
            'overwrite': 'false'
        }
        headers = self._get_headers()
        requests.put(f'{url}?path={folder}', headers=headers)
        response = requests.post(url=url + '/upload', params=params, headers=headers)
        if response.status_code != 202:
            print('Ошибка на сервере')
