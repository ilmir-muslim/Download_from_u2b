import yt_dlp

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\rСкачивается: {d['_percent_str']} завершено, скорость: {d['_speed_str']}, осталось: {d['_eta_str']}", end='')
    elif d['status'] == 'finished':
        print("\nЗагрузка завершена!")

def download(link, choice, name='%(title)s'):
    # Определяем формат для скачивания в зависимости от выбора пользователя
    format_map = {
        '1': 'bestvideo+bestaudio/best',  # Максимальное качество
        '2': 'bestaudio/best',  # Только аудио
        '3': 'bestvideo[height<=720]+bestaudio/best',  # Видео с разрешением до 720p
        '4': 'bestvideo[height<=480]+bestaudio/best',  # Видео с разрешением до 480p
    }

    # Настройки yt-dlp
    ydl_opts = {
        'format': format_map.get(choice, 'bestvideo+bestaudio/best'),  # Выбор формата
        'outtmpl': '{}.%(ext)s'.format(name),  # Имя файла
        'progress_hooks': [progress_hook],  # Отслеживание прогресса
    }

    # Скачивание видео
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(link, download=True)
        downloaded_file_path = ydl.prepare_filename(info_dict)

    print(f"Видео {downloaded_file_path} успешно загружено!")
    return downloaded_file_path


if __name__ == "__main__":
    # Ввод данных от пользователя
    url = input("Введите ссылку на видео YouTube: ")
    print("Выберите формат для скачивания:")
    print("1. Максимальное качество видео")
    print("2. Только аудио")
    print("3. Видео в 720p")
    print("4. Видео в 480p")
    choice = input("Введите ваш выбор (1, 2, 3 или 4): ")

    name = input("Введите имя файла (оставьте пустым для использования названия видео): ")

    # Скачивание видео
    download(url, choice, name or '%(title)s')
