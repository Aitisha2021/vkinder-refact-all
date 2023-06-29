from vk_api import VkTools
from app.vk_api.vk_auth import get_user_session

def get_city_id(city_name):
    """
    Возвращает идентификатор города по его названию.
    """
    session = VkTools(get_user_session())
    cities = session.get_all('database.getCities', 1000, {'country_id': 1, 'q': city_name})
    if cities['items']:
        return cities['items'][0]['id']
    else:
        return None

def get_user_info(user_id):
    """
    Возвращает информацию о пользователе по его идентификатору.
    """
    session = get_user_session()
    user = session.method("users.get", {"user_ids": user_id, "fields": "sex,bdate,city,status"})
    return user[0]

def format_user_info(user_info, photos):
    """
    Форматирует информацию о пользователе для отправки сообщением.
    """
    info = f"ID: {user_info['id']}\n"
    info += f"Имя: {user_info['first_name']} {user_info['last_name']}\n"
    info += f"Дата рождения: {user_info.get('bdate', 'не указана')}\n"
    info += f"Город: {user_info.get('city', {}).get('title', 'не указан')}\n"
    info += f"Статус: {user_info.get('status', 'не указан')}\n"
    info += f"Топ фото: {', '.join(photos)}\n"
    return info
