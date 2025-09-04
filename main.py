import yt_dlp
import os

def progress_hook(d):
    if d['status'] == 'downloading':
        print(f"\rСкачивается: {d['_percent_str']} завершено, скорость: {d['_speed_str']}, осталось: {d['_eta_str']}", end='')
    elif d['status'] == 'finished':
        print("\nЗагрузка завершена!")

def merge_audio_video(base_name):
    """
    Функция для объединения видео и аудио файлов формата .webm, находящихся в текущей директории,
    с использованием ffmpeg. Ожидается, что видео и аудио файлы будут иметь имена
    base_name.webm и base_name.webm соответственно.
    """
    video_path = f"{base_name}.f244.webm"  # Файл видео
    audio_path = f"{base_name}.webm"  # Файл аудио
    output_path = f"{base_name}_merged.mp4"  # Имя выходного файла

    if not os.path.exists(video_path):
        print(f"Видео файл не найден: {video_path}")
        return

    if not os.path.exists(audio_path):
        print(f"Аудио файл не найден: {audio_path}")
        return

    # Команда для объединения видео и аудио
    command = f'ffmpeg -i "{video_path}" -i "{audio_path}" -c copy "{output_path}"'
    os.system(command)
    print(f"Объединение завершено! Файл сохранён как: {output_path}")

def download(link, choice, name='%(title)s'):
    # Определяем формат для скачивания в зависимости от выбора пользователя
    format_map = {
        '1': 'bestvideo+bestaudio/best',  # Максимальное качество
        '2': 'bestaudio/best',  # Только аудио
        '3': 'bestvideo[height<=720]+bestaudio/best',  # Видео с разрешением до 720p
        '4': 'bestvideo[height<=480]+bestaudio/best',  # Видео с разрешением до 480p
    }

    # Настройки yt-dlp с добавлением возможности возобновления
    ydl_opts = {
        'format': format_map.get(choice, 'bestvideo+bestaudio/best'),  # Выбор формата
        'outtmpl': '{}.%(ext)s'.format(name),  # Имя файла
        'progress_hooks': [progress_hook],  # Отслеживание прогресса
        'retries': 10,  # Количество попыток в случае обрыва соединения
        'noprogress': False,  # Отображение прогресса
        'continuedl': True,  # Возобновление загрузки
    }

    # Скачивание видео или аудио
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(link, download=True)
            downloaded_file_path = ydl.prepare_filename(info_dict)
        except Exception as e:
            print(f"Произошла ошибка при загрузке: {e}")
            return None

    print(f"Файл {downloaded_file_path} успешно загружен!")
    return downloaded_file_path

if __name__ == "__main__":
    # Создаём папку для загрузок, если её нет
    os.makedirs("downloads", exist_ok=True)

    print("Выберите действие:")
    print("1. Скачивание видео и аудио")
    print("2. Скачивание только аудио")
    print("3. Видео в 720p")
    print("4. Видео в 480p")
    print("5. Объединить скачанное аудио и видео из текущей директории")

    choice = input("Введите ваш выбор (1, 2, 3, 4 или 5): ")

    if choice == "5":
        # Объединение аудио и видео
        base_name = input("Введите базовое имя файла (без расширения): ")
        merge_audio_video(base_name)

    else:
        # Скачивание одного или нескольких видео
        urls = input(
            "Введите ссылку на видео YouTube, либо введите несколько ссылок через запятую: "
        )
        urls = [
            u.strip() for u in urls.split(",") if u.strip()
        ]  # убираем пробелы и пустые строки

        for i, url in enumerate(urls, start=1):
            print(f"\n=== Загружается {i}-е видео из {len(urls)} ===")
            download(url, choice, name="downloads/%(title)s [%(id)s]")
