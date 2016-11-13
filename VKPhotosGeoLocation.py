import vk
import time
import webbrowser

print('\nVK Photos geo location\n')

# Авторизуем сессию с помощью access token
session = vk.Session('a9f44c18f8ab67703e49c510ce1e47c44d2e2cd23c5f86816f872f1b28ce731712a9990c0e151d36863ff')

# Создаём объект API
api = vk.API(session)

# Запрашивает список всех друзей
friends = api.friends.get()

# Получаем информацию о всех друзьях
friends_info = api.users.get(user_ids=friends)

# Здесь будут храниттся геоданные
geolocation = []

# Получаем геоданные всех фотографий каждого друга
# Цикл перебирающий всех друзей
for friend in friends_info:
        print('ID: %s Имя: %s %s' % (friend['uid'], friend['last_name'], friend['first_name']))
        id = friend['uid']
        # Получаем все альбомы пользователя, кроме служебных
        albums = api.photos.getAlbums(owner_id=id)
        print('\t...альбомов % s...' % len(albums))
        # Цикл перебирающий все альбомы пользователя
        for album in albums:
            # Обрабатываем исключение для приватных альбомов/фото
            try:
                # Получаем все фотографии из альбома
                photos = api.photos.get(owner_id=id, album_id=album['aid'])
                print('\t\t...обрабатываем фотографии альбома...')
                # Цикл перебирающий все фото в альбоме
                for photo in photos:
                    # Если в фото имеются геоданны, то добавляем их в список geolocation
                    if 'lat' in photo and 'long' in photo:
                        geolocation.append((photo['lat'], photo['long']))
                print('\t\t...найдено %s фото...' % len(photos))
            except:
                pass
            # Задержка между запросами photos.get
            time.sleep(0.5)
        # Задержка между запросами photos.getAlbums
        time.sleep(0.5)

# Здесь будет хранится сгенерированный JavaScript код
js_code = ""

# Проходим по всем геоданным и генерирум JS команду добавления маркера
for loc in geolocation:
    js_code += 'new google.maps.Marker({position: {lat: %s, lng: %s}, map: map }); \n' % (loc[0], loc[1])

# Считываем из файла-шаблона html данные
html = open('map.html').read()

# Заменяем placeholder на сгенерированный код
html = html.replace('/* PLACEHOLDER */ ', js_code)

# Записываем данные в новый файл
f = open('VKPhotosGeoLocation.html', 'w')
f.write(html)
f.close()

# Открываем браузер
print('\nОткрывается браузер...')
webbrowser.open('VKPhotosGeoLocation.html')