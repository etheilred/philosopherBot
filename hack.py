import telebot
import random
from google_images_download import google_images_download
import sys
from gtts import gTTS
import jgen
import os
import shutil


# Переводит текст в аудио сообщение
def get_audio(s, path):
    language = 'ru'
    myobj = gTTS(text=s, lang=language, slow=False)
    myobj.save(path)


# Получает картику по запросу kw
def get_pic(kw):
    orig_stdout = sys.stdout
    f = open('URLS.txt', 'w')
    sys.stdout = f

    response = google_images_download.googleimagesdownload()

    arguments = {"keywords": kw,
                 "limit": 3,
                 "print_urls": True,
                 "size": ">2MP"
                 }
    paths = response.download(arguments)
    dirPath = os.path.abspath(__file__)
    ind = dirPath.index('\\', len(dirPath) - 10, len(dirPath))
    dirPath = dirPath[0:ind + 1] + "downloads"
    shutil.rmtree(dirPath)
    # os.remove(dirPath)

    sys.stdout = orig_stdout
    f.close()

    with open('URLS.txt') as f:
        content = f.readlines()
    f.close()

    urls = []
    for j in range(len(content)):
        if content[j][:9] == 'Completed':
            urls.append(content[j - 1][11:-1])
    return urls


# токен бота
token = "855028663:AAGQgv_AG6x73oZGfYSvyx9dTxG_nOnh6_k"

# подключаемся к телеграму
bot = telebot.TeleBot(token=token)

# Обходим блокировку
telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}

advice = "Дай совет"
what_is_bad = "Что есть плохо?"
what_is_good = "Что есть хорошо?"


# Обработчик начала общения
@bot.message_handler(commands=['start'])
def start_cmd(msg):

    keybd = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.KeyboardButton(text=advice)
    btn4 = telebot.types.KeyboardButton(text="генерировать аудио")
    btn5 = telebot.types.KeyboardButton(text="генерировать картинку")
    btn3 = telebot.types.KeyboardButton(text=what_is_good)
    btn2 = telebot.types.KeyboardButton(text=what_is_bad)
    keybd.add(btn1)
    keybd.add(btn2)
    keybd.add(btn3)
    keybd.add(btn4)
    keybd.add(btn5)
    personal_settings[msg.chat.id] = [0, False, False]
    bot.send_message(msg.chat.id, "Привет! Я хочу поделиться с тобой своей мудростью!", reply_markup=keybd)


# Обработчик ввода пользователя
@bot.message_handler(content_types=['text'])
def random_citation(msg):
    if msg.chat.id not in personal_settings.keys():
        settings = [0, False, False]
    else:
        settings = personal_settings[msg.chat.id]

    if msg.text == "генерировать аудио":  # Пользователь хочет получать аудиосообщения
        settings[1] = True
    elif msg.text == "не генерировать аудио":
        settings[1] = False
    elif msg.text == "генерировать картинку":
        settings[2] = True
    elif msg.text == "не генерировать картинку":
        settings[2] = False

    if msg.text in [advice, what_is_bad, what_is_good]:  # Отпрвка цитаты
        gen_word = ""
        if msg.text == advice:
            gen_word = 'разум'
        if msg.text == what_is_bad:
            gen_word = 'плохо'
        if msg.text == what_is_good:
            gen_word = 'хорошо'
        joke = ""
        while len(joke.split()) < 4:
            joke = jgen.get_joke(gen_word)
        print(joke)

        if settings[2]:
            kw = jgen.photo_search(joke)
            print(kw)
            pics = get_pic(kw)
            if len(pics) != 0:
                bot.send_photo(msg.chat.id, pics[random.randint(0, len(pics) - 1)])
            print(pics)
        if settings[1]:
            path = "voice-msg" + str(msg.chat.id) + str(settings[0]) + ".mp3"
            get_audio(joke, path)
            vc = open(path, 'rb')
            bot.send_voice(msg.chat.id, voice=vc)
            vc.close()
            os.remove(path)
            settings[0] += 1
        bot.send_message(msg.chat.id, joke)
    elif "генерировать аудио" not in msg.text or "генерировать картинку" not in msg.text:
        keybd = telebot.types.ReplyKeyboardMarkup(True)
        btn1 = telebot.types.KeyboardButton(text=advice)
        btn4 = telebot.types.KeyboardButton(text="не генерировать аудио" if settings[1] else "генерировать аудио")
        btn5 = telebot.types.KeyboardButton(text="не генерировать картинку" if settings[2] else "генерировать картинку")
        btn3 = telebot.types.KeyboardButton(text=what_is_good)
        btn2 = telebot.types.KeyboardButton(text=what_is_bad)
        keybd.add(btn1)
        keybd.add(btn2)
        keybd.add(btn3)
        keybd.add(btn4)
        keybd.add(btn5)
        bot.send_message(msg.chat.id, "Как прикажешь!", reply_markup=keybd)
    else:
        bot.send_message(msg.chat.id, "Моя твоя не понимать. Щёлкай по предложенным кнопкам!")

    personal_settings[msg.chat.id] = settings


# personal_settings[user_id] = (i, gen_audio, gen_pics)
personal_settings = {}

bot.polling()
