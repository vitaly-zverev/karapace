####
# pip install confluent-kafka[avro] --upgrade 
####
from confluent_kafka import avro
from confluent_kafka.avro import AvroProducer
from confluent_kafka.admin import AdminClient, NewTopic
import os

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
avro_producer = AvroProducer({
    'bootstrap.servers': kafka_bootstrap_servers,
    'schema.registry.url': schema_registry_url
}, default_value_schema=avro.load( os.path.join(os.getcwd(),'./path_to_avro_schema.avsc')))

# Получение объекта производителя Kafka
# kafka_producer = avro_producer.get_producer()

# Определение сообщения в формате Avro
avro_message = {
    'field1': 'value1',
    'field2': 'value2',
    'field3': 123
}

# Отправка сообщения в Kafka с автоматической регистрацией схемы
avro_producer.produce(topic=topic, value=avro_message, value_schema=avro_producer._value_schema, key=None)

## Для успешной авторегистрации схемы даже флаш не требуется !!!
#avro_producer.flush()

