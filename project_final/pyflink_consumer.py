import os
import json
import time
from kafka import KafkaConsumer
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def parse_json_message(message):
    """Parse JSON message from Kafka."""
    try:
        # Handle both string and bytes messages
        if isinstance(message.value, bytes):
            message_str = message.value.decode('utf-8')
        else:
            message_str = str(message.value)
        
        data = json.loads(message_str)
        return (
            data.get('id', ''),
            data.get('name', ''),
            data.get('email', ''),
            data.get('company', ''),
            data.get('job_title', ''),
            data.get('created_at', ''),
            data.get('partition_date', '')
        )
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}, value: {message.value}")
        return None

def create_kafka_consumer():
    """Create Kafka consumer configuration."""
    
    kafka_bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    kafka_topic = os.getenv('KAFKA_TOPIC', 'fake_data_topic')
    kafka_group_id = os.getenv('KAFKA_GROUP_ID', 'kafka_consumer_group')
    
    return KafkaConsumer(
        kafka_topic,
        bootstrap_servers=kafka_bootstrap_servers,
        group_id=kafka_group_id,
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        value_deserializer=lambda x: x.decode('utf-8')
    )

def insert_into_postgres(data, cursor, conn):
    """Insert data into PostgreSQL."""
    
    try:
        cursor.execute("""
            INSERT INTO fake_data (id, name, email, company, job_title, created_at, partition_date) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, data)
        conn.commit()
        return True
    except Exception as e:
        logger.error(f"Error inserting data: {e}")
        conn.rollback()
        return False

def create_postgres_table():
    """Create PostgreSQL table if it doesn't exist."""
    
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    
    postgres_host = os.getenv('POSTGRES_HOST', 'localhost')
    postgres_port = os.getenv('POSTGRES_PORT', '5432')
    postgres_database = os.getenv('POSTGRES_DB', 'fake_data_db')
    postgres_username = os.getenv('POSTGRES_USER', 'postgres')
    postgres_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            host=postgres_host,
            port=postgres_port,
            database=postgres_database,
            user=postgres_username,
            password=postgres_password
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Create table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS fake_data (
            id VARCHAR(255) PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255),
            company VARCHAR(255),
            job_title VARCHAR(255),
            created_at VARCHAR(255),
            partition_date VARCHAR(255),
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        cursor.execute(create_table_sql)
        logger.info("PostgreSQL table 'fake_data' created successfully")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Error creating PostgreSQL table: {e}")

def main():
    """Main function to run the Kafka consumer."""
    
    logger.info("Starting Kafka consumer...")
    
    # Create PostgreSQL table
    create_postgres_table()
    
    # Create Kafka consumer
    consumer = create_kafka_consumer()
    
    # Create PostgreSQL connection
    postgres_host = os.getenv('POSTGRES_HOST', 'localhost')
    postgres_port = os.getenv('POSTGRES_PORT', '5432')
    postgres_database = os.getenv('POSTGRES_DB', 'fake_data_db')
    postgres_username = os.getenv('POSTGRES_USER', 'postgres')
    postgres_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
    
    try:
        conn = psycopg2.connect(
            host=postgres_host,
            port=postgres_port,
            database=postgres_database,
            user=postgres_username,
            password=postgres_password
        )
        cursor = conn.cursor()
        
        logger.info("Connected to PostgreSQL successfully")
        
        # Start consuming messages
        logger.info("Starting to consume messages from Kafka...")
        
        for message in consumer:
            try:
                # Parse the message
                data = parse_json_message(message)
                
                if data:
                    # Insert into PostgreSQL
                    if insert_into_postgres(data, cursor, conn):
                        logger.info(f"Successfully processed message: {data[0]}")  # Log the ID
                    else:
                        logger.error(f"Failed to insert message: {data[0]}")
                else:
                    logger.warning("Skipping invalid message")
                    
            except Exception as e:
                logger.error(f"Error processing message: {e}")
                continue
                
    except Exception as e:
        logger.error(f"Error connecting to PostgreSQL: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        consumer.close()
        logger.info("Consumer stopped")

if __name__ == "__main__":
    main()
