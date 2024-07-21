from config import KAFKA_HOST, KAFKA_PORT
from confluent_kafka import Producer
import json

config = {
    'bootstrap.servers': f'{KAFKA_HOST}:{KAFKA_PORT}'
}

producer = Producer(**config)

def delivery_report(error, message):
    if error is not None:
        print(f'ERROR:  Error in delivering message: {error}')
    else:
        print(f'INFO:     Message delivered to {message.topic()} [{message.partition()}]')

def send_message(topic, message):
    try:
        producer.produce(topic, json.dumps(message).encode('utf-8'), callback=delivery_report)
        producer.flush()
    except Exception as e:
        print(f'Kafka exception: {e}')