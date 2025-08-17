#!/usr/bin/env python3
"""
Test script to verify the data engineering pipeline components.
Run this after starting the Docker services to test connectivity.
"""

import os
import json
import time
from kafka import KafkaProducer, KafkaConsumer
import psycopg2
from faker import Faker

def test_kafka_connection():
    """Test Kafka connectivity and topic creation."""
    print("🔍 Testing Kafka connection...")
    
    try:
        # Test producer
        producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        # Test consumer
        consumer = KafkaConsumer(
            'test_topic',
            bootstrap_servers=['localhost:9092'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id='test_group'
        )
        
        # Send test message
        test_message = {'test': 'data', 'timestamp': time.time()}
        producer.send('test_topic', test_message)
        producer.flush()
        
        # Consume test message
        messages = consumer.poll(timeout_ms=5000)
        consumer.close()
        producer.close()
        
        print("✅ Kafka connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Kafka connection failed: {e}")
        return False

def test_postgres_connection():
    """Test PostgreSQL connectivity."""
    print("🔍 Testing PostgreSQL connection...")
    
    try:
        conn = psycopg2.connect(
            host='localhost',
            port=5432,
            database='fake_data_db',
            user='postgres',
            password='postgres'
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"✅ PostgreSQL connection successful - Version: {version[0]}")
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL connection failed: {e}")
        return False

def test_faker_data_generation():
    """Test Faker data generation."""
    print("🔍 Testing Faker data generation...")
    
    try:
        fake = Faker()
        
        # Generate sample data
        sample_data = {
            'id': fake.uuid4(),
            'name': fake.name(),
            'email': fake.email(),
            'company': fake.company(),
            'job_title': fake.job()
        }
        
        print("✅ Faker data generation successful")
        print(f"   Sample data: {sample_data}")
        return True
        
    except Exception as e:
        print(f"❌ Faker data generation failed: {e}")
        return False

def test_dagster_import():
    """Test Dagster import."""
    print("🔍 Testing Dagster import...")
    
    try:
        from dagster import asset, AssetExecutionContext
        print("✅ Dagster import successful")
        return True
        
    except Exception as e:
        print(f"❌ Dagster import failed: {e}")
        return False

def test_pyflink_import():
    """Test PyFlink import."""
    print("🔍 Testing PyFlink import...")
    
    try:
        from pyflink.datastream import StreamExecutionEnvironment
        print("✅ PyFlink import successful")
        return True
        
    except Exception as e:
        print(f"❌ PyFlink import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Running Data Engineering Pipeline Tests")
    print("=" * 50)
    
    tests = [
        test_kafka_connection,
        test_postgres_connection,
        test_faker_data_generation,
        test_dagster_import,
        test_pyflink_import
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
        print()
    
    # Summary
    print("📊 Test Results Summary")
    print("=" * 30)
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! Your pipeline is ready to run.")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("💡 Make sure all Docker services are running:")
        print("   docker-compose ps")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
