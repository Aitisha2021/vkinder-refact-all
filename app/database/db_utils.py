from app.database.db_operations import add_user, user_exists, create_connection

def add_user_if_not_exists(user):
    """
    Добавляет пользователя в базу данных, если он еще не существует.
    Возвращает True, если пользователь был добавлен, и False, если он уже существует.
    """
    conn = create_connection()
    if not user_exists(conn, user['id']):
        user_data = (user['id'], user['first_name'], user['last_name'], f"https://vk.com/id{user['id']}", ','.join(user['photos']))
        add_user(conn, user_data)
        return True
    else:
        return False

def get_all_users():
    """
    Извлекает всех пользователей из базы данных.
    Возвращает список словарей, каждый из которых представляет пользователя.
    """
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Users")
    
    users = []
    rows = cur.fetchall()
    for row in rows:
        users.append({
            "id": row[0],
            "first_name": row[1],
            "last_name": row[2],
            "profile_link": row[3],
            "photos": row[4].split(',')
        })

    return users
