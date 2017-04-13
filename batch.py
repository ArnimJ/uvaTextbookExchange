from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json

es = Elasticsearch(['es'])

while(True):
    try:
        #tries connecting to kafka again and again until it works
        consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
        #creates the index so that a search will not return an error even if nothing has been indexed
        #es.indices.create(index='listing_index', body={"settings" : {"number_of_shards": 1, "number_of_replicas": 1}})
        break
    except:
        pass

for message in consumer:
    listing = json.loads((message.value).decode('utf-8'))
    es.index(index='listing_index', doc_type='listing', id=listing['id'], body=listing)
    es.indices.refresh(index='listing_index')


