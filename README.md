## Real-Time-Data-Processing-with-Confluent-Kafka-MySQL-AVRO-Cassandra

This project is designed to demonstrate real-time data processing capabilities through the integration of various technologies. It involves the following key components:

1. Upstream Data Source
Description: This component focuses on generating mock data to simulate microservice-generated updates, which are crucial for testing and validating real-time data processing pipelines.

Implementation Details:

* Mock Data Generator Script: A Python script is developed to generate realistic product data, including attributes such as product name, category, price, and last updated timestamp.
* MySQL Database Interaction: The generated data is stored in a MySQL database, providing a reliable and structured data source for subsequent processing stages.
Usage:

The `ingest_data_to_mysql_db.py` script can be executed with the desired number of records to generate and insert into the MySQL database.

2. Kafka Producer
* Description: This component is responsible for publishing data from the MySQL database to a Kafka topic, enabling real-time data streaming and processing.

Implementation Details:

Kafka Producer Script: A Python script is developed to connect to the MySQL database, fetch data updates, and publish them to a designated Kafka topic.
Serialization: Avro serialization is utilized to ensure efficient and schema-aware data serialization before publishing to Kafka.
Usage:

The `avro_data_producer.py` script can be configured with the appropriate Kafka broker details and executed to start publishing data to the Kafka topic.

3. Kafka Consumers
Consumer Group 1
* Description: This consumer group is responsible for consuming data from the Kafka topic and storing it in a Cassandra database for further analysis and processing.

Implementation Details:

* Consumer Script: A Python script is developed to consume data from the Kafka topic and insert it into a Cassandra table.
* Cassandra Integration: The script establishes a connection to the Cassandra cluster and executes CQL (Cassandra Query Language) statements to insert data into the appropriate table.

Usage:

* The `consumer_group01.py` script can be executed with the desired consumer group identifier to start consuming and storing data in Cassandra.

Consumer Group 2
* Description: This consumer group performs similar functionality to Consumer Group 1 but connects to a cloud-hosted Cassandra instance using secure connection credentials.

Implementation Details:

* Consumer Script: Similar to Consumer Group 1, a Python script is developed to consume data from the Kafka topic and insert it into a Cassandra table.
* Secure Connection: This consumer group uses secure connection credentials (client ID, secret, token) to establish a connection with the cloud-hosted Cassandra instance.

Usage:

* The `consumer_group02.py` script can be executed with the desired consumer group identifier to start consuming and storing data in the cloud-hosted Cassandra instance.