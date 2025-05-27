import argparse
from typing import List, Dict

import requests

with open("vk_token.txt") as file:
    ACCESS_TOKEN = file.readline().strip()
    USER_ID =file.readline().strip()



def get_user_info(user_id):
    """Получить основную информацию о пользователе"""
    url = "https://api.vk.com/method/users.get"
    params = {
        "user_ids": user_id,
        "access_token": ACCESS_TOKEN,
        "v": "5.131",
        "fields": "first_name,last_name,sex,bdate,city,country,photo_max_orig,domain"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print(f"Ошибка: {data['error']['error_msg']}")
            return None

        return data["response"][0]  # Возвращаем данные первого пользователя

    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return None


def format_user_info(user_data):
    """Преобразовать данные в читаемый формат"""
    if not user_data:
        return "Данные не получены."

    info = [
        f"Имя: {user_data.get('first_name', 'Не указано')}",
        f"Фамилия: {user_data.get('last_name', 'Не указана')}",
        f"Страница: https://vk.com/{user_data.get('domain', '')}"
    ]

    if "bdate" in user_data:
        info.append(f"Дата рождения: {user_data['bdate']}")

    sex = {1: "Женский", 2: "Мужской"}.get(user_data.get("sex"), "Не указан")
    info.append(f"Пол: {sex}")

    if "city" in user_data:
        info.append(f"Город: {user_data['city']['title']} (ID: {user_data['city']['id']})")
    if "country" in user_data:
        info.append(f"Страна: {user_data['country']['title']} (ID: {user_data['country']['id']})")

    if "photo_max_orig" in user_data:
        info.append(f"Фото профиля: {user_data['photo_max_orig']}")

    return "\n".join(info)


def get_friends_list():
    """Получить список друзей пользователя"""
    url = "https://api.vk.com/method/friends.get"
    params = {
        "user_id": USER_ID,
        "access_token": ACCESS_TOKEN,
        "v": "5.131",
        "fields": "first_name,last_name"
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print(f"Ошибка: {data['error']['error_msg']}")
            return []

        friends = data["response"]["items"]
        return friends

    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []


def get_photo_albums():
    """Получить список фотоальбомов пользователя"""
    url = "https://api.vk.com/method/photos.getAlbums"
    params = {
        "owner_id": USER_ID,
        "access_token": ACCESS_TOKEN,
        "v": "5.131",
        "need_system": 1  # Включить системные альбомы
    }

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "error" in data:
            print(f"Ошибка: {data['error']['error_msg']}")
            return []

        albums = data["response"]["items"]
        return albums

    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []


def main():
    user_data = get_user_info(USER_ID)

    if user_data:
        print("\nОсновная информация:")
        print(format_user_info(user_data))
    else:
        print("Не удалось получить данные.")
    friends = get_friends_list()
    if friends:
        print("\nСписок друзей:")
        for friend in friends:
            print(f"{friend['first_name']} {friend['last_name']} (ID: {friend['id']})")
    else:
        print("Друзей не найдено или ошибка запроса.")

    albums = get_photo_albums()
    if albums:
        print("\nФотоальбомы:")
        for album in albums:
            print(f"{album['title']} (Кол-во фото: {album['size']})")
    else:
        print("Альбомов не найдено или ошибка запроса.")


def print_banner() -> None:
    print("""
    🚀 VK API 🚀
    """)


def pretty_print(title: str, items: List[str], emoji: str) -> None:
    print(f"\n{emoji} {title}")
    print("─" * 50)
    for item in items:
        print(f"  • {item}")


def format_friends(friends: List[Dict]) -> List[str]:
    return [f"{friend['first_name']} {friend['last_name']} 👤 ID: {friend['id']}" for friend in friends]


def format_albums(albums: List[Dict]) -> List[str]:
    return [f"{album['title']} 📸 ({album['size']} фото)" for album in albums]


def main():
    parser = argparse.ArgumentParser(description="🦊 Получить информацию о пользователе ВКонтакте")
    parser.add_argument('-i', '--info', action='store_true', help="📋 Основная информация о пользователе")
    parser.add_argument('-f', '--friends', action='store_true', help="👥 Список друзей")
    parser.add_argument('-a', '--albums', action='store_true', help="📷 Фотоальбомы")
    parser.add_argument('--all', action='store_true', help="🌈 Вся доступная информация")

    args = parser.parse_args()
    print_banner()

    try:
        if args.all or not any(vars(args).values()):
            args.info = args.friends = args.albums = True

        if args.info:
            user_data = get_user_info(USER_ID)
            if user_data:
                info_lines = format_user_info(user_data).split('\n')
                pretty_print("Основная информация", info_lines, "📋")
            else:
                print("\n❌ Не удалось получить основную информацию")

        if args.friends:
            friends = get_friends_list()
            if friends:
                pretty_print("Друзья", format_friends(friends), "👥")
            else:
                print("\n😔 Друзей не найдено")

        if args.albums:
            albums = get_photo_albums()
            if albums:
                pretty_print("Фотоальбомы", format_albums(albums), "📷")
            else:
                print("\n📭 Альбомов не найдено")


    except Exception as e:
        print(f"\n🔥 Ошибка: {str(e)}")
        print("🚑 Проверьте соединение с интернетом и правильность токена")



if __name__ == "__main__":
    main()
