import os
import json
from datetime import datetime
from dagster import (
    asset,
    AssetExecutionContext,
    DailyPartitionsDefinition,
    Definitions,
)
from faker import Faker
from kafka import KafkaProducer
import pandas as pd

# Initialize Faker
fake = Faker()

# Kafka configuration
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'kafka:29092')
KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'fake_data_topic')

# Daily partitions for the asset
daily_partitions = DailyPartitionsDefinition(start_date="2025-08-01")

@asset(
    partitions_def=daily_partitions,
    description="Generate fake dataset with 5 columns and send to Kafka"
)
def generate_and_send_fake_data(context: AssetExecutionContext) -> None:
    """Generate fake data and send to Kafka topic."""
    
    # Get partition date (if available)
    try:
        partition_date = context.partition_key
        context.log.info(f"Processing partition: {partition_date}")
    except:
        partition_date = datetime.now().strftime("%Y-%m-%d")
        context.log.info(f"No partition context, using current date: {partition_date}")
    
    # Generate fake data
    records = []
    num_records = 100  # Generate 100 records per day
    
    for i in range(num_records):
        record = {
            'id': fake.uuid4(),
            'name': fake.name(),
            'email': fake.email(),
            'company': fake.company(),
            'job_title': fake.job(),
            'created_at': fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
            'partition_date': partition_date
        }
        records.append(record)
    
    # Convert to DataFrame for logging
    df = pd.DataFrame(records)
    context.log.info(f"Generated {len(records)} records")
    context.log.info(f"Sample data:\n{df.head()}")
    
    # Send to Kafka
    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode('utf-8'),
        key_serializer=lambda k: k.encode('utf-8') if k else None
    )
    
    try:
        for record in records:
            # Use partition date as key for partitioning
            producer.send(
                topic=KAFKA_TOPIC,
                key=partition_date,
                value=record
            )
        
        producer.flush()
        context.log.info(f"Successfully sent {len(records)} records to Kafka topic: {KAFKA_TOPIC}")
        
    except Exception as e:
        context.log.error(f"Error sending data to Kafka: {str(e)}")
        raise e
    finally:
        producer.close()

# Load assets and create definitions
defs = Definitions(
    assets=[generate_and_send_fake_data]
)

if __name__ == "__main__":
    # This allows running the pipeline directly
    from dagster import materialize
    result = materialize([generate_and_send_fake_data])
    print(f"Asset materialization completed with status: {result.success}")
