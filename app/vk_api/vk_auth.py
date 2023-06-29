import vk_api
from app.config import TOKEN_USER, TOKEN_GROUP

def get_user_session():
    """
    Создает сессию для пользователя через API VK.
    Возвращает объект сессии.
    """
    session = vk_api.VkApi(token=TOKEN_USER)
    return session

def get_group_session():
    """
    Создает сессию для группы через API VK.
    Возвращает объект сессии.
    """
    session = vk_api.VkApi(token=TOKEN_GROUP)
    return session
