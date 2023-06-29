from app.vk_api.vk_auth import get_user_session, get_group_session

def search_people(age_from, age_to, city_id, sex, status, count=1000):
    """
    Ищет пользователей, соответствующих заданным критериям.
    Возвращает список пользователей.
    """
    session = get_user_session()
    users = session.method("users.search", {"age_from": age_from, 
                                            "age_to": age_to, 
                                            "city": city_id, 
                                            "sex": sex, 
                                            "status": status, 
                                            "count": count})
    return users['items']

def get_top_photos(user_id, count=3):
    """
    Получает топ-3 популярных фотографии профиля пользователя.
    Возвращает список URL фотографий.
    """
    session = get_user_session()
    photos = session.method("photos.get", {"owner_id": user_id, 
                                           "album_id": "profile", 
                                           "extended": 1, 
                                           "count": 200})
    top_photos = sorted(photos['items'], key=lambda x: x['likes']['count'] + x['comments']['count'], reverse=True)[:count]
    top_photos_urls = [photo['sizes'][-1]['url'] for photo in top_photos]
    return top_photos_urls
