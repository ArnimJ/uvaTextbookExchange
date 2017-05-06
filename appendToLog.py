from kafka import KafkaConsumer
import logging
import json
from pathlib import Path

while(True):
    try:
        consumer = KafkaConsumer('new-page-view', group_id='view-indexer', bootstrap_servers=['kafka:9092'])
    except:
        pass

for message in consumer:
    view = json.loads((message.value).decode('utf-8'))
    print(json.loads((message.value).decode('utf-8')))

    #append username item_id to end of log file here
    f = open("pageView.txt", "a")
    f.write(view['username'] + " " + view['item_id'])


    # my_file = Path("/uvaTextbookExchange/pageView.txt")
    # if my_file.is_file():
    #     #append kafka message to log file
    #     with open("pageView.txt", "a") as myfile:
    #         myfile.write(view['username'] + " " + view['item_id'])