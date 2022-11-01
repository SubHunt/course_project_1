import requests
import json
from datetime import datetime
from vkapi import VK
from ya_disk import YaUploader
from config import token, access_token, user_id
from progress.bar import IncrementalBar

if __name__ == '__main__':

    qty_photos = int(input('Введите количество фотографий, которое хотите скопировать: '))
    name_folder = input('Введите название папки ня Яндекс диске , в которую хотите сохранить фотографии: ')
    vk = VK(access_token, user_id, qty_photos)
    vk_func = vk.users_info()
    place_find = vk_func['response']['items']
    bar = IncrementalBar('Процесс загрузки: ', max=qty_photos)
    new_list = []  # Если нужно создавать кол-во json файлов = кол-во фото, => данный список нужно сместить в цикл
    uploader = YaUploader(token, name_folder)
    for el, _ in enumerate(place_find):
        bar.next()
        url_photo = place_find[el]['sizes'][-1][
            'url']  # Получаем фото с максимальным разрешением, оно последнее в списке
        size_photo = place_find[el]['sizes'][-1]['type']  # Получаем тип максимального размера, он последний в списке
        date_photo = place_find[el]['date']  # Получаем дату в unixформате
        likes = place_find[el]['likes']['count']  # Получаем кол-во лайков
        new_dict = {'file_name': likes, 'size': size_photo}  # Собираем словарь для json
        new_list.append(new_dict)  # Создаем список со словарями
        # В задании сказано сделать 'json-файл с информацией по файлу', думаю это опечатка и нужно сделать один json по
        # всем файлам, а не для каждого, если я ошибся,
        # следующие строки нужно разкомментировать для создания каждого json для каждого файла с фото
        # name_file_json = 'file' + str(el) + datetime.utcfromtimestamp(date_photo).strftime('%d-%m-%Y')+'.json'
        # with open(name_file_json, 'w') as f:
        #    json.dump(new_list, f)

        # Собираем имя файла из кол-во лайков + дата в человеском восприятии. Если оставить только лайки, то файлы при
        # совпадении лайков будут перезаписываться
        r = requests.get(url_photo)
        name_file_photo = str(likes) + '-' + datetime.utcfromtimestamp(date_photo).strftime('%d-%m-%Y') + '.jpg'
        with open(name_file_photo, 'wb') as f:
            f.write(r.content)

        uploader.upload_link(name_file_photo)

    name_file_json = 'file.json'
    with open(name_file_json, 'w') as f:  # Создаем файл json
        json.dump(new_list, f)
    print('\nЗагрузка файлов завершена.')
