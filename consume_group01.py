import os
import json
import sys
from confluent_kafka import DeserializingConsumer
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from confluent_kafka.serialization import StringDeserializer
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the credentials
bootstrap_servers = os.getenv("BOOTSTRAP_SERVERS")
schema_registry_url = os.getenv("SCHEMA_REGISTRY_URL")
cassandra_node = os.getenv("CASSANDRA_NODES")
cassandra_port = os.getenv("CASSANDRA_PORT")
cassandra_username = os.getenv("CASSANDRA_USERNAME")
cassandra_password = os.getenv("CASSANDRA_PASSWORD")


# Define Kafka configuration
kafka_config = {
    'bootstrap.servers': bootstrap_servers,       # Adjust to your Kafka broker
    'group.id': 'productConsumerGroup01',         # Adjust to your consumer group id
    'auto.offset.reset': 'latest'                 # Adjust to your desired offset reset policy
}

# Create a Schema Registry client
schema_registry_client = SchemaRegistryClient({
    'url': schema_registry_url                    # Adjust to your Schema Registry URL
})

# Fetch the latest Avro schema for the value
subject_name = 'products_stream-value'
schema_str = schema_registry_client.get_latest_version(subject_name).schema.schema_str

# Define Avro Deserializer for the value
key_deserializer = StringDeserializer('utf_8')
avro_deserializer = AvroDeserializer(schema_registry_client, schema_str)

# Define the DeserializingConsumer
consumer = DeserializingConsumer({
    'bootstrap.servers': kafka_config['bootstrap.servers'],
    'key.deserializer': key_deserializer,
    'value.deserializer': avro_deserializer,
    'group.id': kafka_config['group.id'],
    'auto.offset.reset': kafka_config['auto.offset.reset']
})


def cassandra_connection():
    # Configuration
    CASSANDRA_NODES = [cassandra_node]         # Adjust if your Cassandra is hosted elsewhere or in a cluster
    CASSANDRA_PORT = cassandra_port            # Default Cassandra port, adjust if needed
    KEYSPACE = 'product_store'
    
    # Connection setup (without authentication)
    cluster = Cluster(contact_points=CASSANDRA_NODES, port=CASSANDRA_PORT)
    
    # Uncomment below lines and adjust USERNAME and PASSWORD if your Cassandra setup requires authentication.
    USERNAME = cassandra_username
    PASSWORD = cassandra_password
    auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
    cluster = Cluster(contact_points=CASSANDRA_NODES, port=CASSANDRA_PORT, auth_provider=auth_provider)
    
    session = cluster.connect(KEYSPACE)

    return cluster, session

# Subscribe to the 'products_stream' topic
consumer.subscribe(['products_stream'])

# Setup Cassandra connection
cluster, session = cassandra_connection()

# Prepare the Cassandra insertion statement
insert_stmt = session.prepare("INSERT INTO product_store.products_fact (id, name, category, price, last_updated) VALUES (?, ?, ?, ?, ?)")

def msg_poll(consumer_num):
    
    #Continually read messages from Kafka
    try:
        while True:
            msg = consumer.poll(1.0) # How many seconds to wait for message

            if msg is None:
                continue
            
            if msg.error():
                print('Consumer error: {}'.format(msg.error()))
                continue

            print(f'Successfully consumed record with key {msg.key()} and value {msg.value()}!')
            json_data = msg.value()
            
            ## just to define the consumer number
            _ = f"consumer_{consumer_num}.json"
            
            # Prepare data for Cassandra insertion
            cassandra_data = (
                json_data.get("id"),
                json_data.get("name"),
                json_data.get("category"),
                json_data.get("price"),
                json_data.get("last_updated")
            )
            
            # Insert data into Cassandra
            session.execute(insert_stmt, cassandra_data)
            print("Data inserted in cassandra!!")

    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <consumer_num>")
        sys.exit(1)
    
    consumer_num = sys.argv[1]
    msg_poll(consumer_num)