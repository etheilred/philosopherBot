import random
import sys


# возвращает самое частое слово
def photo_search(joke):
    a = joke.split(' ')
    a = sorted(a, key=len)
    a.reverse()
    return " ".join(a[:2])


def random_start(text):
    num = random.randint(1, len(text))
    for i in range(len(text)):
        if i + 1 == num:
            return text[i][1]


# Генерирует цитату по словарю и ключевому слову word
def frequency(dict, word):
    # размер высказавания пока будет равен 10
    st = word.title() + " "
    for i in range(10):
        if word == "END":
            return st
        summ = 0
        bill = 0
        for key in dict[word]:
            summ += dict[word][key]
        num = random.uniform(0, 1)
        for key in dict[word]:
            bill += dict[word][key]
            if bill / summ > num:
                st += key + " "
                word = key
                break
    return st


# Переводит список слов в словарь
def normalize(text):
    dt = {}
    for i in range(len(text)):
        for j in range(len(text[i])):
            if text[i][j] != 'END':
                if text[i][j] not in dt:
                    d = {text[i][j + 1]: 1}
                    dt[text[i][j]] = d
                else:
                    if text[i][j + 1] not in dt[text[i][j]]:
                        dt[text[i][j]][text[i][j + 1]] = 1
                    else:
                        dt[text[i][j]][text[i][j + 1]] += 1

        else:
            d = {"None": 1}
            dt[text[i][j]] = d
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
        if start == pre_text[i][1]:
            a = True
    if not a:
        start = random_start(pre_text)
    # print(frequency(dt,start))
    st = frequency(dt, start)

    if st.contains("END"):
        st = st[:-4]
    return st


if __name__ == "__main__":
    print(sys.getdefaultencoding())
    print(get_joke('плохо'))
