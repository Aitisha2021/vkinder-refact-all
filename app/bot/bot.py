import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from app.vk_api.vk_auth import get_group_session
from app.bot.bot_commands import start, search

def parse_parameters(parameters):
    params_dict = {}
    for param in parameters:
        if ':' not in param:
            continue
        key, value = param.split(':')
        value = value.strip()  # Удаляем лишние пробелы
        if key == 'пол':
            params_dict['sex'] = 1 if value == 'мужской' else 2
        elif key == 'возраст':
            try:
                age_range = [int(age) for age in value.split('-') if age.isdigit()]
                if len(age_range) == 2:
                    params_dict['age'] = tuple(age_range)
            except ValueError:
                pass
        elif key == 'город':
            if value.isdigit():
                params_dict['city_id'] = int(value)
        elif key == 'статус':
            if value.isdigit():
                params_dict['status'] = int(value)
    return params_dict


def main():
    vk_session = get_group_session()
    longpoll = VkBotLongPoll(vk_session, 220440878)
    states = {}
    
    for event in longpoll.listen():
        if event.type == VkBotEventType.MESSAGE_NEW:
            msg = event.obj.message['text'].lower()
            msg_parts = msg.split()
            command = msg_parts[0]
            parameters = msg_parts[1:]
            peer_id = event.obj.message['peer_id']

            if command == '/start':
                start(event, vk_session)
            elif command == '/search' or (command == 'далее' and peer_id in states):
                if command == '/search' or command == 'далее':
                    states.pop(peer_id, None)  # Удаляем предыдущее состояние поиска, если есть
                    search_params = parse_parameters(parameters)
                    search(event, vk_session, states, search_params)
            elif peer_id in states:  # Обработка выбора параметров поиска
                state = states[peer_id]
                index = state['index']
                search_results = state['search_results']

                if index < len(search_results):
                    params = parse_parameters(msg_parts[1:])
                    if 'sex' in params:
                        search_results = filter_results(search_results, 'sex', params['sex'])
                    if 'age' in params:
                        search_results = filter_results(search_results, 'age', params['age'])
                    if 'city_id' in params:
                        search_results = filter_results(search_results, 'city_id', params['city_id'])
                    if 'status' in params:
                        search_results = filter_results(search_results, 'status', params['status'])

                    if search_results:
                        state['search_results'] = search_results
                        state['index'] = 0
                        states[peer_id] = state
                        search(event, vk_session, states)
                    else:
                        vk_session.method('messages.send', {'peer_id': peer_id, 'message': 'Нет результатов по выбранным параметрам.', 'random_id': 0})
                else:
                    vk_session.method('messages.send', {'peer_id': peer_id, 'message': 'Поиск завершен. Для нового поиска напишите /search.', 'random_id': 0})
            else:
                vk_session.method('messages.send', {'peer_id': peer_id, 'message': 'Я не понимаю эту команду.', 'random_id': 0})


main()



def filter_results(search_results, key, value):
    """
    Фильтрует результаты поиска по указанному ключу и значению.
    Возвращает отфильтрованный список результатов.
    """
    filtered_results = []
    for result in search_results:
        if result.get(key) == value:
            filtered_results.append(result)
    return filtered_results

def extract_age_range(msg):
    """
    Извлекает диапазон возраста из сообщения.
    Возвращает кортеж (age_from, age_to) или (None, None), если диапазон не указан.
    """
    age_from = None
    age_to = None

    # Находим числа в сообщении
    numbers = [int(s) for s in msg.split() if s.isdigit()]

    if len(numbers) == 2:
        age_from, age_to = numbers
    elif len(numbers) == 1:
        age_from = numbers[0]

    return age_from, age_to

def extract_city_id(msg):
    """
    Извлекает идентификатор города из сообщения.
    Возвращает идентификатор города или None, если не найден.
    """
    city_id = None
    numbers = [int(s) for s in msg.split() if s.isdigit()]

    if numbers:
        city_id = numbers[0]

    return city_id


def extract_status(msg):
    """
    Извлекает статус из сообщения.
    Возвращает статус или None, если не найден.
    """
    status = None

    # Список возможных статусов
    statuses = ['свободен', 'занят', 'всё сложно']

    # Проверяем наличие статусов в сообщении
    for s in statuses:
        if s in msg:
            status = s
            break

    return status
