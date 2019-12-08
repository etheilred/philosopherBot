import telebot
import random
from google_images_download import google_images_download
import sys
from gtts import gTTS
import jgen


# Переводит текст в аудио сообщение
def get_audio(s):
    global i
    language = 'ru'
    myobj = gTTS(text=s, lang=language, slow=False)
    myobj.save('message' + str(i) + '.mp3')


# Получает картику по запросу kw
def get_pic(kw):
    orig_stdout = sys.stdout
    f = open('URLS.txt', 'w')
    sys.stdout = f

    response = google_images_download.googleimagesdownload()

    arguments = {"keywords": kw,
                 "limit": 3,
                 "print_urls": True,
                 "size": ">2MP",
                 }
    paths = response.download(arguments)

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
    uid = msg.chat.id
    keybd = telebot.types.ReplyKeyboardMarkup(True)
    btn1 = telebot.types.KeyboardButton(text=advice)
    btn4 = telebot.types.KeyboardButton(text="не генерировать аудио" if gen_audio else "генерировать аудио")
    btn5 = telebot.types.KeyboardButton(text="не генерировать картинку" if gen_picts else "генерировать картинку")
    btn3 = telebot.types.KeyboardButton(text=what_is_good)
    btn2 = telebot.types.KeyboardButton(text=what_is_bad)
    keybd.add(btn1)
    keybd.add(btn2)
    keybd.add(btn3)
    keybd.add(btn4)
    keybd.add(btn5)
    bot.send_message(uid, "Привет! Я хочу поделиться с тобой своей мудростью!", reply_markup=keybd)


# Обработчик ввода пользователя
@bot.message_handler(content_types=['text'])
def random_citation(msg):
    global i
    global gen_audio
    global gen_picts
    if msg.text == "генерировать аудио":  # Пользователь хочет получать аудиосообщения
        gen_audio = True
    elif msg.text == "не генерировать аудио":
        gen_audio = False
    elif msg.text == "генерировать картинку":
        gen_picts = True
    elif msg.text == "не генерировать картинку":
        gen_picts = False

    if msg.text in [advice, what_is_bad, what_is_good]:  # Отпрвка цитаты
        gen_word = ""
        if msg.text == advice:
            gen_word = 'разум'
        if msg.text == what_is_bad:
            gen_word = 'плохо'
        if msg.text == what_is_good:
            gen_word = 'хорошо'
        joke = ""
        while len(joke.split()) < 5:
            joke = jgen.get_joke(gen_word)
        print(joke)

        if gen_picts:
            kw = jgen.photo_search(joke)
            print(kw)
            picts = get_pic(kw)
            if len(picts) != 0:
                bot.send_photo(msg.chat.id, picts[random.randint(0, len(picts) - 1)])
            print(picts)
        if gen_audio:
            get_audio(joke)
            vc = open("message" + str(i) + ".mp3", 'rb')
            bot.send_voice(msg.chat.id, voice=vc)
            vc.close()
            i += 1
        bot.send_message(msg.chat.id, joke)
    else:
        keybd = telebot.types.ReplyKeyboardMarkup(True)
        btn1 = telebot.types.KeyboardButton(text=advice)
        btn4 = telebot.types.KeyboardButton(text="не генерировать аудио" if gen_audio else "генерировать аудио")
        btn5 = telebot.types.KeyboardButton(text="не генерировать картинку" if gen_picts else "генерировать картинку")
        btn3 = telebot.types.KeyboardButton(text=what_is_good)
        btn2 = telebot.types.KeyboardButton(text=what_is_bad)
        keybd.add(btn1)
        keybd.add(btn2)
        keybd.add(btn3)
        keybd.add(btn4)
        keybd.add(btn5)
        bot.send_message(msg.chat.id, "Как прикажешь!", reply_markup=keybd)


i = 0
gen_audio = False
gen_picts = False

bot.polling()
