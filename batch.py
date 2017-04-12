from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['es'])

while(True):
    try:
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        break
    except:
        pass
    
for message in consumer:
    listing = json.loads((message.value).decode('utf-8'))
    es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
    es.indices.refresh(index='listing_index')


