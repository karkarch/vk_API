# 🦊 VK  API

Утилита для получения информации о пользователях ВКонтакте через официальное API.


## 📦 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/karkarch/vk_API.git
cd vk_API
```
2. Уствновите зависимости
```bash
pip install -r requirements.txt
```
2. Создайте файл с токеном
```bash
echo "ВАШ_ТОКЕН" > vk_token.txt
echo "ВАШ_ID" > vk_token.txt
```

## 🚀 Использование
```bash
python vk_info.py [опции]
```
### Доступные опции

| Флаг         | Описание                          | Пример использования           |
|--------------|-----------------------------------|---------------------------------|
| `--info`     | Основная информация о пользователе | `python vk_info.py --info`      |
| `--friends`  | Список друзей                     | `python vk_info.py -f`          |
| `--albums`   | Фотоальбомы пользователя          | `python vk_info.py -a`          |
| `--all`      | Вся доступная информация          | `python vk_info.py --all`       |
| `-h`, `--help` | Справка по использованию          | `python vk_info.py -h`          |