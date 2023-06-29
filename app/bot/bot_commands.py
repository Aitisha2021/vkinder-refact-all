from app.vk_api import get_user_info, search_people
from app.database import add_user_if_not_exists, get_all_users, User
from app.vk_api.vk_auth import get_user_session
from vk_api.exceptions import VkApiError

def validate_user_id(user_id):
    if not isinstance(user_id, int) or user_id < 1:
        raise ValueError("Invalid user_id")

def start(event, vk_api):
    """
    Обработка команды /start.
    Возвращает приветственное сообщение.
    """
    user_id = event.object.message['from_id']
    validate_user_id(user_id)
    message = f"Привет, {user_id}! Я бот VKinder. Я помогу тебе найти людей, которые тебе понравятся."
    vk_api.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})

def search(event, vk_api, states, search_params):
    """
    Обработка команды /search.
    Ищет пользователей, соответствующих критериям поиска, и отправляет их информацию пользователю.
    """
    user_id = event.object.message['from_id']
    validate_user_id(user_id)
    try:
        user_info = get_user_info(user_id)
    except Exception as e:
        print(f"Failed to get user info for user_id: {user_id}. Error: {e}")
        return

    vk_api_user = get_user_session()

    age_from = search_params.get('age', (18, 30))[0]
    age_to = search_params.get('age', (18, 30))[1]
    city_id = search_params.get('city_id', 1)
    sex = search_params.get('sex', 1)
    status = search_params.get('status', 1)

    try:
        search_results = search_people(age_from=age_from, age_to=age_to, city_id=city_id, sex=sex, status=status)
    except Exception as e:
        print(f"Failed to search people. Error: {e}")
        return

    if user_id not in states:
        states[user_id] = {'index': 0, 'search_results': search_results, 'waiting': False}

    state = states[user_id]
    index = state['index']
    search_results = state['search_results']

    if state['waiting'] and 'далее' not in event.object.message['text'].lower():
        return

    if 'далее' in event.object.message['text'].lower():
        state['waiting'] = False

    while index < len(search_results) and not state['waiting']:
        if '/search' in event.object.message['text']:
            state['index'] = 0
            states[user_id] = state

        user = search_results[index]
        user_id = user['id']
        try:
            user_info = vk_api.method('users.get', {'user_ids': user_id, 'fields': 'photo_max_orig'})
        except VkApiError as e:
            print(f"VkApiError occurred while getting user info: {e}")
            return

        if 'is_closed' in user_info[0] and user_info[0]['is_closed']:
            index += 1
            continue

        photos = user_info[0].get('photo_max_orig')

        user_obj = User(user['id'], user['first_name'], user['last_name'], photos)

        if add_user_if_not_exists(user_obj.to_dict()):
            message = str(user_obj)

            try:
                photos_info = vk_api_user.method('photos.get', {'owner_id': user_id, 'album_id': 'profile'})
                photos_data = photos_info['items']
                photos_data.sort(key=lambda p: p.get('likes', {}).get('count', 0) + p.get('comments', {}).get('count', 0), reverse=True)
                for photo in photos_data[:3]:
                    photo_url = photo['sizes'][-1]['url']
                    message += f"\nФото: {photo_url}"

            except VkApiError as e:
                message = "Произошла ошибка при получении информации о фотографиях."

            vk_api.method('messages.send', {'user_id': event.object.message['peer_id'], 'message': message, 'random_id': 0})
            state['waiting'] = True

        state['index'] += 1
        index += 1

    if not state['waiting']:
        del states[user_id]
