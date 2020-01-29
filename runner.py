from __future__ import print_function
from __future__ import unicode_literals
import csv
from rtmbot.core import Plugin
import numpy as np
import random
import time
from chatbot import bag_of_words
from chatbot import model
from chatbot import labels
from chatbot import words
import json

class FeedsparqPlugin(Plugin):
    def process_message(self, data):
        print("Message data object: {}".format(data))
        if too_old(data):
            print("--- Not processing message - it's too old!")
            return
        global flag
        flag = True
        with open("menu1.csv", encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            if data['text'].lower() == 'menu':
                for row in csv_reader:
                    steak_origin = row[0]
                    steak_type = row[1]
                    steak_size = row[2]
                    steak_price = row[3]
                    self.outputs.append([data['channel'], ' {}---{}---{}---${}'.format(steak_origin, steak_type, steak_size, steak_price)])
                    flag = False
            else:
                for row in csv_reader:
                    steak_origin = row[0]
                    steak_origin_split = steak_origin.split("-")
                    steak_origin = steak_origin_split[0]
                    steak_type = row[1]
                    steak_size = row[2]
                    steak_price = row[3]
                    if data['text'] == steak_origin:
                        self.outputs.append([data['channel'], 'The price for a {} {} {} Steak is ${}'.format(steak_size, steak_type, steak_origin, steak_price)])
                        flag = False

        if flag == True:
            with open('intents.json') as file:
                data1 = json.load(file)
            results = model.predict([bag_of_words(data['text'], words)])[0]
            results_index = np.argmax(results)
            tag = labels[results_index]
            if results[results_index] > 0.7:
                for tg in data1["intents"]:
                    if tg["tag"] == tag:
                        global responses
                        responses = tg["responses"]
                self.outputs.append(
                    [data['channel'], '{}'.format(random.choice(responses))]
                )
            else:
                self.outputs.append([data['channel'], "Sorry I didn't understand that. Please try again"])


def too_old(data):
    TOO_OLD_THRESHHOLD = 10
    now = int(time.time())
    msg_time = int(data['ts'].split('.')[0])
    if (now - msg_time) > TOO_OLD_THRESHHOLD:
        return True

    return False

