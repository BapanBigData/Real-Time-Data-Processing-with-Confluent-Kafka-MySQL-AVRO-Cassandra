# Real-Time-Data-Processing-with-Confluent-Kafka-MySQL-AVRO-Cassandra

This project focuses on real-time data processing by mimicking a microservice application's data updates into a MySQL database. The project is divided into several key components:

1. Upstream Data Source
A Python script is developed to generate mock data simulating microservice-generated updates. This script utilizes Python programming to generate random product data (e.g., name, category, price) and stores it into a MySQL database. The script ensures realistic data updates mimicking user shopping activities.

2. Kafka Producer
The data from the MySQL database is published to a Kafka topic using a Kafka producer. This component facilitates the seamless transfer of data from the MySQL database to the Kafka topic, enabling real-time data streaming and processing.

3. Kafka Consumers
Two Kafka consumer groups consume the data from the Kafka topic. Each consumer group performs distinct tasks:

* Consumer Group 1: This consumer group dumps the received data into a Cassandra table, providing fault-tolerant and scalable data storage for high-volume and high-velocity data streams.

* Consumer Group 2: This consumer group also dumps the received data into another Cassandra table. However, it connects to a cloud-hosted Cassandra instance using secure connection credentials, ensuring secure and reliable data storage.
