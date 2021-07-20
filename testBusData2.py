# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 15:15:17 2021

@author: DHRUV
"""


# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 03:21:37 2021

@author: DHRUV
"""

from pykafka import KafkaClient
import json
from datetime import datetime
import uuid
import time


client= KafkaClient(hosts='localhost:9092')

print(client.topics)

topic = client.topics['geodata_final']

producer = topic.get_sync_producer()

    

input_file = open('./data/bus2.json')
json_array = json.load(input_file)
coordinates = json_array['features'][0]['geometry']['coordinates']

#generating unique Ids
def generate_uuid():
    return uuid.uuid4()


def generate_checkpoint(coordinates):
    
    i = 0
    while i<len(coordinates):
        
            
        data = {}
        data['busline'] = '0002'
        data['key'] = data['busline'] + '_' + str(generate_uuid())
        data['timestamp'] = str(datetime.utcnow())
        data['latitude'] = coordinates[i][1]
        data['longitude'] = coordinates[i][0]
        message = json.dumps(data)
        print(message)
        producer.produce(message.encode('ascii'))
        time.sleep(1)
        
        #if bus reaches the end pint, let's start from the beginning
        if i == len(coordinates)-1:
            i =0
        else:
            i+=1
        
generate_checkpoint(coordinates)


   
"""
KAFKA PRODUCER

from pykafka import KafkaClient

client= KafkaClient(hosts='localhost:9092')

print(client.topics)

topic = client.topics['testBusdata']

producer = topic.get_sync_producer()


message = "Hello friend #"
count = 0
while count<6:
    message_f = message+str(count) 
    producer.produce(message_f.encode('ascii'))
    count +=1
    
"""