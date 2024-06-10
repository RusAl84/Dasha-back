# -*- coding: utf-8 -*-
import os
import json
import nltk
import pymorphy2


def data_proc(filename, save_filename, threshold=0):
    # with open("./uploads/"+filename+".json", "r", encoding="UTF8") as file:
    with open(filename, "r", encoding="UTF8") as file:
        content = file.read()
    messages = json.loads(content)
    text = ""
    count_messages = len(messages)
    print(count_messages)
    num = 0
    proc_messages = []  
    for m in messages:
        text = m["text"]
        print(f"{num / count_messages * 100}     {count_messages-num}     {num} / {count_messages}")
        num += 1
        if len(text) < threshold:
            continue
        line = {}
        line['text'] = text.strip()
        line['remove_all'] = remove_all(text).strip()
        line['normal_form'] = get_normal_form(remove_all(text).strip())
        line["date"] = m["date"]
        line["message_id"] = m["message_id"]
        line["user_id"] = m["user_id"]
        line["reply_message_id"] = m["reply_message_id"]
        proc_messages.append(line)
    jsonstring = json.dumps(proc_messages, ensure_ascii=False)
    with open(save_filename, "w", encoding="UTF8") as file:
        file.write(jsonstring)

def get_sig(text):
    return get_normal_form(remove_all(text).strip())

def find_data(save_filename, find_text, save_score_filename="./dasha_find_data_proc.json", threshold=0, fuzz=1):
    with open(save_filename, "r", encoding="UTF8") as file:
        content = file.read()
    messages = json.loads(content)
    text = ""
    count_messages = len(messages)
    print(count_messages)
    num = 0
    proc_messages = []  
    find_text=get_normal_form(remove_all(find_text).strip())
    scores = set()
    for m in messages:
        print(f"{num / count_messages * 100}     {count_messages-num}     {num} / {count_messages}")
        num += 1
        if len(text) < threshold:
            continue
        line = {}
        line['text'] = m['text']
        line['remove_all'] = m['remove_all']
        line['normal_form'] = m['normal_form']
        line["date"] = m["date"]
        line["message_id"] = m["message_id"]
        line["user_id"] = m["user_id"]
        line["reply_message_id"] = m["reply_message_id"]
        line["score"] = calc_intersection_text(line['normal_form'], find_text)
        scores.add(line["score"])
        if line["score"] < 1:
            continue
        proc_messages.append(line)
    proc_messages = sorted(proc_messages, key=lambda d: d['score'])
    s_scores=sorted(scores)
    s_scores=list(s_scores)
    if fuzz>len(s_scores):
        fuzz=len(s_scores)
    s_scores=s_scores[-fuzz:]
    
    print(find_text)
    print("==================================")
    print()
    final_messages=[]
    for m in proc_messages:
        if m["score"] in s_scores:
            final_messages.append(m)
    jsonstring = json.dumps(final_messages, ensure_ascii=False)
    with open(save_score_filename, "w", encoding="UTF8") as file:
        file.write(jsonstring)
    return jsonstring


def remove_digit(data):
    str2 = ''
    for c in data:
        if c not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '«', '»', '–', "\""):
            str2 = str2 + c
    data = str2
    return data


def remove_punctuation(data):
    str2 = ''
    import string
    pattern = string.punctuation
    for c in data:
        if c not in pattern:
            str2 = str2 + c
        else:
            str2 = str2 + ""
    data = str2
    return data


def remove_stopwords(data):
    str2 = ''
    from nltk.corpus import stopwords
    russian_stopwords = stopwords.words("russian")
    for word in data.split():
        if word not in (russian_stopwords):
            str2 = str2 + " " + word
    data = str2
    return data


def remove_short_words(data, length=1):
    str2 = ''
    for line in data.split("\n"):
        str3 = ""
        for word in line.split():
            if len(word) > length:
                str3 += " " + word
        str2 = str2 + "\n" + str3
    data = str2
    return data


def remove_paragraf_to_lower(data):
    data = data.lower()
    data = data.replace('\n', ' ')
    return data


def remove_all(data):
    data = remove_digit(data)
    data = remove_punctuation(data)
    data = remove_stopwords(data)
    data = remove_short_words(data, length=3)
    data = remove_paragraf_to_lower(data)
    return data


def get_normal_form_mas(words):
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    result = []
    for word in words.split():
        p = morph.parse(word)[0]
        result.append(p.normal_form)
    return result


def get_normal_form(words):
    import pymorphy2
    morph = pymorphy2.MorphAnalyzer()
    p = morph.parse(words)[0]
    return p.normal_form


def load_data(filename='data.txt'):
    with open(filename, "r", encoding='utf-8') as file:
        data = file.read()
    return data

def remove_from_patterns(text, pattern):
    str2 = ''
    for c in text:
        if c not in pattern:
            str2 = str2 + c
    return str2

def display(text):
    print(text) 
    print("--------------------------------")

def remove_paragraf_and_toLower(text):
    text = text.lower()
    text = text.replace('\n', ' ')
    text = ' '.join([k for k in text.split(" ") if k])
    return text


def nltk_download():
    nltk.download('stopwords')
    nltk.download('punkt')
    

def calc_intersection_list(list1, list2):
    count = 0
    for item1 in list1:
        for item2 in list2:
            count += calc_intersection_text(item1, item2)
    return count

def calc_intersection_text(text1, text2):
    count = 0
    text1 = str(text1)
    text2 = str(text2)
    for item1 in text1.split():
        for item2 in text2.split():
            if item1 == item2:
                count += 1
    return count


def convertMs2String(milliseconds):
    import datetime
    dt = datetime.datetime.fromtimestamp(milliseconds)
    return dt


def convertJsonMessages2text(filename):
    with open(filename, "r", encoding="UTF8") as file:
        content = file.read()
    messages = json.loads(content)
    text = ""
    for m in messages:
        text += f"{convertMs2String(m['date'])} {m['message_id']}  {m['user_id']} {m['reply_message_id']}  {m['text']}  <br>\n"
    return text


def get_fuzzScore(text1, messages,treshold=80):
    from fuzzywuzzy import fuzz #https://habr.com/ru/articles/491448/
    score=0
    for m in messages:
        text2 = m["text"]
        if (fuzz.WRatio(text1, text2) > treshold):
            score += 1
    # print(score)
    return score

def get_lemScore(text1, messages):
    res = 0
    text1 = remove_all(text1)
    text1 = get_normal_form_mas(text1)
    for m in messages:
        text2 = m["text"]
        text2 = remove_all(text2)
        text2 = get_normal_form_mas(text2)
        res += calc_intersection_list(text1,text2)
    return res  

if __name__ == '__main__':
    # nltk_download()
    find_text = """
    Любые упаковочные коробки из картона для вашего бизнеса! О цене договоримся
    """    
    find_text = """
    Вы летите на самолете в командировку, либо по семейным делам
    и тут вдруг Даша и Алина и кошка не съели кошку
    """    
    find_text = """
        Кошка заходит в кафе согласен
        Любые упаковочные коробки
        Привет Извините
    """
    filename="d:/ml/chat/andromedica1.json"   
    filename="d:/ml/chat/tvchat.json"   
    save_filename="./dasha_data_proc.json" 
    save_score_filename  ="./dasha_find_data_proc.json"
    #data_proc(filename, save_filename, 32)
    s=find_data(save_filename, find_text, save_score_filename="./dasha_find_data_proc.json", threshold=0, fuzz=3)
    print(s)
    # s1 = """
    # Кошка заходит в кафе, заказывает кофе и пирожное. Официант стоит с открытым ртом. Кошка:\n— Что?\n— Эээ... вы кошка!\n— Да.\n— Вы разговариваете!\n— Какая новость. Вы принесете мой заказ или нет?\n— Ооо, простите, пожалуйста, конечно, принесу. Я просто никогда раньше не видел...\n— А я тут раньше и не бывала. Я ищу работу, была на собеседовании, решила вот выпить кофе.\nОфициант возвращается с заказом, видит кошку, строчащую что-то на клавиатуре ноутбука.\n\n— Ваш кофе. Эээ... я тут подумал... Вы ведь ищете работу, да? Просто мой дядя — директор цирка, и он с удовольствием взял бы вас на отличную зарплату!\n\n— Цирк? — говорит кошка. — Это где арена, купол, оркестр?\n\n— Да!\n\n— Клоуны, акробаты, слоны?\n\n— Да!\n\n— Сахарная вата, попкорн, леденцы на палочке?\n\n— Да-да-да!\n\n— Звучит заманчиво! А на хрена им программист?
    # """
    # find_text=get_normal_form(remove_all(find_text).strip())
    # s1=get_normal_form(remove_all(s1).strip())
    # print(calc_intersection_text(s1, find_text))