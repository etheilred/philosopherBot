import random
import sys


# возвращает самое частое слово
def photo_search(joke):
    a = joke.split(' ')
    a = sorted(a, key=len)
    a.reverse()
    return " ".join(a[:2])

def search(text, word):
    for  i in range(len(text)):
        if word == text[i][1]:
            return(word + " " + text[i][2])

def random_start(text):
    num = random.randint(1, len(text))
    for i in range(len(text)):
        if i + 1 == num:
            return text[i][1]


def destr(word,key):
    st = ""
    arr = list(map(str, word.split()))
    st += arr[1]+" "
    st+=key
    return st

# Генерирует цитату по словарю и ключевому слову word
def frequency(dt, word):
    # размер высказавания пока будет равен 10
    arr = list(map(str, word.split()))
    st = arr[0].title() + " "
    for i in range(10):
        own,bill = 0,0
        for el in dt[word]:
            own += dt[word][el]
        num = random.uniform(0, 1)
        for el in dt[word]:
            bill += dt[word][el]
            if bill / own > num:
                st += el + " "
                word = destr(word,el)
                if el == "END":
                    return st
                break
    return st


# Переводит список слов в словарь
def normalize(text):
    dt = {}
    for i in range(len(text)):
        for j in range(1,len(text[i])-2):
            unick = text[i][j] + " " + text[i][j+1]
            if unick not in dt:
                d = {}
                d[text[i][j+2]] = 1
                dt[unick] = d
            else:
                if text[i][j + 2] not in dt[unick]:
                    dt[unick][text[i][j+2]] = 1
                else:
                    dt[unick][text[i][j+2]] += 1

    return dt


# Парсит базу данных
def parse2(words):
    arr = []
    st = ""
    index = 0
    arr.append(["START"])
    for i in range(len(words)):
        for j in range(len(words[i])):
            if "а" <= words[i][j] <= "я":
                st += words[i][j]
            elif words[i][j] == ".":
                arr[index].append(st)
                arr[index].append("END")
                index += 1
                st = ""
                arr.append(["START"])
                break
            elif st != "":
                arr[index].append(st)
                st = ""
        if st != "":
            arr[index].append(st)
            arr[index].append("END")
    return arr


# Получает высказывание, основываясь на ключевом слове word
def get_joke(word):
    text_file = open('Phil.txt', 'r', encoding='utf-8')
    pre_text = text_file.readlines()
    pre_text = parse2(pre_text)[:-1]
    text_file.close()
    dt = normalize(pre_text)
    start = word
    a = False
    for i in range(len(pre_text)):
        if pre_text[i][1] == start:
            a = True
            start = search(pre_text, start)
            break
    if not a:
        start = random_start(pre_text)
    # print(frequency(dt,start))
    st = frequency(dt, start)

    if st[-2] == "D":
        st = st[:-4]
    return st


if __name__ == "__main__":
    print(sys.getdefaultencoding())
    print(get_joke('плохо'))
