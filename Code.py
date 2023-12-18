import os
import random
import shutil

import speech_recognition
import pyttsx3

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5
engine = pyttsx3.init()

commands_dict = {
    'commands': {
        'greeting': ['привет', 'приветствую'],
        'create_task': ['добавить задачу', 'создать задачу', 'заметка', 'заметки'],
        'play_music': ['включить музыку', 'дискотека', 'включи музыку', 'включай музыку', 'музыка'],
        'create_folder': ['создать папку', 'создай папку'],
        'delete_folder': ['удалить папку', 'удали папку'],
        'delete_file': ['удалить файл', 'удали файл'],
        'create_file': ['создать файл', 'создай файл'],
        'read_file': ['прочитать файл', 'прочитай файл'],
    }
}


def listen_command():
    try:
        with speech_recognition.Microphone() as mic:
            sr.adjust_for_ambient_noise(source=mic, duration=0.5)
            audio = sr.listen(source=mic)
            query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

        return query
    except speech_recognition.UnknownValueError:
        return 'Не понял что ты сказал'


def greeting():
    return 'Здарова!'

def create_task():
    print('Что добавим в список дел?')
    engine.say('Что добавим в список дел?')  # Проговариваем вопрос голосом
    engine.runAndWait()  # Ожидаем завершения произношения голосом
    query = listen_command()

    with open(os.path.join(os.path.expanduser('~'), 'Desktop', 'todo-list.txt'), 'a') as file:
        file.write(f'{query}\n')

    return f'Задача "{query}" добавлена в список дел!'


def play_music():
    music_folder = os.path.expanduser('~/Desktop/Music')  # Путь к папке с музыкой на рабочем столе
    files = os.listdir(music_folder)
    random_file = random.choice(files)
    music_file = os.path.join(music_folder, random_file)
    os.startfile(music_file)  # Открытие файла с помощью os.startfile

    return f'Танцуем под {random_file} 🎶🔊'


def create_folder():
    print('Какую папку создать?')
    engine.say('Какую папку создать?')  # Проговариваем вопрос голосом
    engine.runAndWait()  # Ожидаем завершения произношения голосом
    folder_name = listen_command()
    os.makedirs(os.path.join(os.path.expanduser('~'), 'Desktop', folder_name))

    return f'Папка "{folder_name}" создана на рабочем столе!'


def create_file():
    print('Какое имя у файла?')
    engine.say('Какое имя у файла?')  # Проговариваем вопрос голосом
    engine.runAndWait()  # Ожидаем завершения произношения голосом
    file_name = listen_command()
    print('В какой папке он будет находиться?')
    engine.say('В какой папке он будет находиться?')  # Проговариваем вопрос голосом
    engine.runAndWait()  # Ожидаем завершения произношения голосом
    folder_name = listen_command()

    if folder_name == 'рабочий стол':
        folder_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    else:
        folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', folder_name)

    if not os.path.exists(folder_path):
        return f'Извините, указанная папка "{folder_name}" для файла не найдена.'

    print('Говорите текст для записи в файл:')
    content = listen_command()

    file_path = os.path.join(folder_path, file_name + '.txt')

    with open(file_path, 'w') as file:
        file.write(content)

    return f'Файл "{file_name}.txt" создан в папке "{folder_name}" на рабочем столе!'


def read_file():
    print('В какой папке находится файл?')
    engine.say('В какой папке находится файл?')
    engine.runAndWait()
    folder_name = listen_command()

    desktop_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    if folder_name == 'рабочий стол':
        folder_path = desktop_path
    else:
        folder_path = os.path.join(desktop_path, folder_name)

    if os.path.exists(folder_path):
        print('Какой файл нужно прочитать?')
        engine.say('Какой файл нужно прочитать?')
        engine.runAndWait()
        file_name = listen_command()

        file_path = os.path.join(folder_path, file_name + '.txt')

        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                content = file.read()

            if content:
                print(f'--- Заголовок: {file_name} ---')
                engine.say(f'Заголовок: {file_name}')
                engine.runAndWait()

                print(content)
                engine.say(content)
                engine.runAndWait()
            else:
                print(f'Файл "{file_name}.txt" пуст!')
                engine.say(f'Файл "{file_name}.txt" пуст!')
                engine.runAndWait()
        else:
            print(f'Извините, файл "{file_name}" не найден.')
            engine.say(f'Извините, файл "{file_name}" не найден.')
            engine.runAndWait()
    else:
        print(f'Извините, папка "{folder_name}" не найдена.')
        engine.say(f'Извините, папка "{folder_name}" не найдена.')
        engine.runAndWait()
    return ''


def delete_folder():
    print('Какую папку удалить?')
    engine.say('Какую папку удалить?')  # Проговариваем вопрос голосом
    engine.runAndWait()  # Ожидаем завершения произношения голосом
    folder_name = listen_command()
    folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', folder_name)

    if os.path.exists(folder_path):
        if len(os.listdir(folder_path)) > 0:
            print(f'Внимание: папка "{folder_name}" не пустая. Удаление ее приведет '
                  f'к удалению всех файлов внутри. Вы уверены, что хотите продолжить?')
            confirmation = listen_command()
            positive_responses = ['да', 'да, я хочу удалить эту папку', 'все равно удаляй', 'удаляй', 'удали']
            negative_responses = ['нет', 'не надо', 'не удаляй', 'тогда не удаляй']

            if confirmation in positive_responses:
                shutil.rmtree(folder_path)
                return f'Папка "{folder_name}" на рабочем столе успешно удалена вместе с содержимым!'
            elif confirmation in negative_responses:
                return f'Операция удаления папки "{folder_name}" отменена.'
            else:
                return 'Не удалось распознать ваш ответ. Операция удаления папки отменена.'
        else:
            os.rmdir(folder_path)
            return f'Папка "{folder_name}" на рабочем столе успешно удалена!'
    else:
        return f'Извините, папка "{folder_name}" не найдена.'


def delete_file():
    print('В какой папке находится файл?')
    engine.say('В какой папке находится файл?')
    engine.runAndWait()
    folder_name = listen_command()
    print('Какой файл нужно удалить?')
    engine.say('Какой файл нужно удалить?')
    engine.runAndWait()
    file_name = listen_command()

    if folder_name == 'рабочий стол':
        folder_path = os.path.join(os.path.expanduser('~'), 'Desktop')
    else:
        folder_path = os.path.join(os.path.expanduser('~'), 'Desktop', folder_name)
    file_path = os.path.join(folder_path, file_name + '.txt')

    if os.path.exists(file_path):
        os.remove(file_path)
        return f'Файл "{file_name}.txt" удален из папки "{folder_name}" на рабочем столе!'

    else:
        return f'Извините, файл "{file_name}.txt" не найден.'




def main():
    while True:
        query = listen_command()

        for k, v in commands_dict['commands'].items():
            if query in v:
                if k == 'greeting':
                    print(greeting())
                    engine.say(greeting())
                    engine.runAndWait()
                elif k == 'create_task':
                    print(create_task())
                    #engine.say(create_task())
                    #engine.runAndWait()
                elif k == 'play_music':
                    print(play_music())
                    #engine.say(play_music())
                    #engine.runAndWait()
                elif k == 'create_folder':
                    print(create_folder())
                    #engine.say(create_folder())
                    #engine.runAndWait()
                elif k == 'create_file':
                    print(create_file())
                    #engine.say(create_file())
                    #engine.runAndWait()
                elif k == 'delete_folder':
                    print(delete_folder())
                    #engine.say(delete_folder())
                    #engine.runAndWait()
                elif k == 'delete_file':
                    print(delete_file())
                    #engine.say(delete_file())
                    #engine.runAndWait()
                elif k == 'read_file':
                    print(read_file())
                    #engine.say(read_file())
                    #engine.runAndWait()

if __name__ == '__main__':
    main()