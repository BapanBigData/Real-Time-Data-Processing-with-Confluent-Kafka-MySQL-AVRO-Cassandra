Docker command to start cassandra
----------------------------------

docker compose -f docker-compose-cassandra.yml up -d

* Once cassandra container started, open the terminal of docker container
* type cqlsh on terminal
* cqlsh shell will be opened and now cassandra related commands can be executed

Cassandra table Creation
-------------------------------

CREATE KEYSPACE IF NOT EXISTS product_store WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 };

CREATE TABLE product_store.products_fact (
    id BIGINT,
    name TEXT,
    category TEXT,
    price FLOAT,
    last_updated BIGINT,
    PRIMARY KEY (category, last_updated)
);