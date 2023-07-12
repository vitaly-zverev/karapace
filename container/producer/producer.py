####
# pip install confluent-kafka[avro] --upgrade 
####
import confluent_kafka 
from confluent_kafka import avro 
from confluent_kafka.avro import AvroProducer
from confluent_kafka.schema_registry.avro import AvroSerializer
from confluent_kafka.admin import AdminClient, NewTopic
import os

print (f"Confluent_kafka (python package) version: {confluent_kafka.__version__} ")

# Настройка параметров Kafka и реестра схем
kafka_bootstrap_servers = 'kafka:9092'
schema_registry_url = 'http://karapace-registry:8081'
topic = 'my_sample_topic3'

# Создание топика в Kafka
admin_client = AdminClient({'bootstrap.servers': kafka_bootstrap_servers})
topic_config = {'cleanup.policy': 'delete', 'retention.ms': '86400000'}
new_topic = NewTopic(topic, num_partitions=1, replication_factor=1, config=topic_config)
admin_client.create_topics([new_topic])


# Создание объекта AvroProducer с настройками
## DeprecationWarning: AvroProducer has been deprecated. Use AvroSerializer instead.
## https://docs.confluent.io/platform/current/clients/confluent-kafka-python/html/_modules/confluent_kafka/schema_registry/avro.html#AvroSerializer
avro_producer = AvroProducer(config={
    'bootstrap.servers': kafka_bootstrap_servers,
    'schema.registry.url': schema_registry_url
}, default_value_schema=avro.load( os.path.join(os.getcwd(),'./container/producer/path_to_avro_schema_for_value_validation.avsc'))
 , default_key_schema  =avro.load( os.path.join(os.getcwd(),'./container/producer/path_to_avro_schema_for_key_validation.avsc'))
)

#avro_producer = AvroSerializer(config={
#    'bootstrap.servers': kafka_bootstrap_servers,
#    'schema.registry.url': schema_registry_url}, 
#    schema_str=avro.load( os.path.join(os.getcwd(),'./path_to_avro_schema_for_value_validation.avsc'))
#)



# Получение объекта производителя Kafka
# kafka_producer = avro_producer.get_producer()

# Определение сообщения в формате Avro
avro_message = {
    'field1': 'value1',
    'field2': 'value2',
    'field3': 123
}

# Отправка сообщения в Kafka с автоматической регистрацией схемы
# avro_producer.produce(topic=topic, value=avro_message, value_schema=avro_producer._value_schema, key=None)
# avro_producer.produce(topic=topic, value=avro_message, value_schema=avro_producer._value_schema, key=None)
# avro_producer.produce(topic=topic, value=avro_message, value_schema=avro_producer._value_schema, key=None)

# Отправка сообщения в Kafka с автоматической регистрацией схем (и для ключа и для значения)
# и так тоже работает
avro_producer.produce(topic=topic, value=avro_message, key= {"key1":1})
avro_producer.produce(topic=topic, value=avro_message, key= {"key1":2})
avro_producer.produce(topic=topic, value=avro_message, key= {"key1":3})


## Для успешной авторегистрации схемы флаш не требуется
# но мы сообщения тоже доставить хотим, потому:
avro_producer.flush()

