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

def find_data(save_filename, find_text, save_score_filename="./dasha_find_data_proc.json", threshold=32):
    with open(save_filename, "r", encoding="UTF8") as file:
        content = file.read()
    messages = json.loads(content)
    text = ""
    count_messages = len(messages)
    print(count_messages)
    num = 0
    proc_messages = []  
    find_text=get_normal_form(remove_all(find_text).strip())
    # print(find_text)
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
        line["score"] = calc_intersection_text(line['text'], find_text)
        proc_messages.append(line)
    jsonstring = json.dumps(proc_messages, ensure_ascii=False)
    with open(save_score_filename, "w", encoding="UTF8") as file:
        file.write(jsonstring)
    
def load_data_proc(filename):
    with open(filename, "r", encoding="UTF8") as file:
        content = file.read()
    messages = json.loads(content)
    return messages


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
    filename="d:/ml/chat/andromedica1.json"   
    filename="d:/ml/chat/tvchat.json"   
    save_filename="./dasha_data_proc.json"   
    #data_proc(filename, save_filename, 32)
    find_data(save_filename, find_text)
    