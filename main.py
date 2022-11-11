from pprint import pprint
import json
from vkapi import VK
from ya_disk import YaUploader
from progress.bar import IncrementalBar
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
vk_token = config['Tokens']['vk_token']
ya_token = config['Tokens']['ya_token']
user_id_config = config['Tokens']['user_id']


class Transfer:

    def copying(self, qty_photos, name_folder):
        vk_agent = VK(vk_token, qty_photos, user_id)
        photos_info = vk_agent.photos_info()
        ya_agent = YaUploader(ya_token, name_folder)
        bar = IncrementalBar('Процесс загрузки: ', max=qty_photos)
        count = 0
        photos_info_json = []
        for photo in photos_info:
            ya_agent.upload_vk_photo(name_folder, file_name=photo['file_name'], link=photo['link'])
            bar.next()
            photos_info_dict = {'file_name': photo['file_name'], 'size': photo['size']}
            photos_info_json.append(photos_info_dict)
            count += 1
        print(f'\nПеренос файлов завершен. Сохранено {count} фотографий.')

        self.write_json(photos_info_json)

    @staticmethod
    def write_json(photos_json):
        name_file_json = 'file.json'
        with open(name_file_json, 'w') as f:
            json.dump(photos_json, f)
        print('\nЗагрузка файла завершена.')


if __name__ == '__main__':

    user_id = input(
        'Введите id-пользователя или screen_name.\n'
        'Для пользователя выбранного по умолчанию нажмите Enter: '
    )
    if user_id == '':
        user_id = user_id_config
    qty_photo = int(input('\nВведите количество фотографий: '))
    folder = input('\nВведите название папки для сохранения на Яндекс диске: ')
    enter_datas = Transfer()
    enter_datas.copying(qty_photo, folder)
