import datetime
import os
import sys
import random
import time

from time import sleep


def type_me(element, text):
    """
    Type like a human
    """
    for letter in text:
        element.send_keys(letter)
        sleep(random.uniform(.1, .3))


def get_correct_path():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
        return application_path
    elif __file__:
        application_path = os.path.dirname(__file__)
        return application_path


def proper_round(num, dec=0):
    num = str(num)[:str(num).index('.') + dec + 2]
    if num[-1] >= '5':
        a = num[:-2 - (not dec)]  # integer part
        b = int(num[-2 - (not dec)]) + 1  # decimal part
        return float(a) + b ** (-dec + 1) if a and b == 10 else float(a + str(b))
    return float(num[:-1])


def read_keyword_file(home_path):
    path = '{}/resources/keywords.txt'.format(home_path)
    with open(path, 'r') as fs:
        keywords_list = []

        for line in fs:
            keywords_list.append(line)

    time.sleep(0.5)
    fs.close()
    return keywords_list


def write_to_file(line_list, home_path):
    today = datetime.datetime.now()
    rnd_num = random.randint(1, 999)
    file_name = f'user_list_{rnd_num}_{today.strftime("%Y-%m-%d")}'
    path = '{}/output/{}'.format(home_path, file_name)
    with open(path, "w") as fp:
        for line in line_list:
            fp.write(line + "\n")
    time.sleep(0.5)
    fp.close()