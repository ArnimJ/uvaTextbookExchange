from kafka import KafkaConsumer
import json

while(True):
    try:
        consumer = KafkaConsumer('new-page-view', group_id='view-indexer', bootstrap_servers=['kafka:9092'])
    except:
        pass

for message in consumer:
    listing = json.loads((message.value).decode('utf-8'))
    #append username item_id to end of log file here