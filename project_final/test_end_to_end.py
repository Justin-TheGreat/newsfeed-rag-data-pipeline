#!/usr/bin/env python3
"""
Test script to demonstrate the end-to-end data pipeline.
This script will:
1. Generate fake data using Dagster
2. Check if data flows to Kafka
3. Verify data is stored in PostgreSQL
"""

import os
import time
import subprocess
import psycopg2
from datetime import datetime

def test_dagster_pipeline():
    """Test the Dagster pipeline by running it manually."""
    print("🧪 Testing Dagster Pipeline...")
    
    try:
        # Run the Dagster pipeline
        result = subprocess.run([
            "docker", "exec", "dagster-webserver", 
            "python", "/opt/dagster/app/dagster_pipeline.py"
        ], capture_output=True, text=True, timeout=60)
        
        if "Successfully sent" in result.stdout:
            print("✅ Dagster pipeline executed successfully")
            return True
        else:
            print("❌ Dagster pipeline failed")
            print(f"Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Dagster pipeline: {e}")
        return False

def test_kafka_consumer():
    """Test if the Kafka consumer is processing messages."""
    print("🧪 Testing Kafka Consumer...")
    
    try:
        # Check consumer logs for recent activity
        result = subprocess.run([
            "docker", "compose", "logs", "kafka-consumer", "--tail", "5"
        ], capture_output=True, text=True, timeout=30)
        
        if "Successfully processed message" in result.stdout:
            print("✅ Kafka consumer is processing messages")
            return True
        else:
            print("❌ Kafka consumer not processing messages")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Kafka consumer: {e}")
        return False

def test_postgresql_data():
    """Test if data is being stored in PostgreSQL."""
    print("🧪 Testing PostgreSQL Data Storage...")
    
    try:
        # Connect to PostgreSQL and check data
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            database="fake_data_db",
            user="postgres",
            password="postgres"
        )
        
        cursor = conn.cursor()
        
        # Check total count
        cursor.execute("SELECT COUNT(*) FROM fake_data")
        total_count = cursor.fetchone()[0]
        
        # Check recent data
        cursor.execute("""
            SELECT COUNT(*) FROM fake_data 
            WHERE processed_at >= NOW() - INTERVAL '5 minutes'
        """)
        recent_count = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        print(f"✅ PostgreSQL has {total_count} total records")
        print(f"✅ {recent_count} records processed in the last 5 minutes")
        
        return total_count > 0
        
    except Exception as e:
        print(f"❌ Error testing PostgreSQL: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing End-to-End Data Pipeline")
    print("=" * 50)
    
    # Wait for services to be ready
    print("⏳ Waiting for services to be ready...")
    time.sleep(10)
    
    # Test each component
    dagster_success = test_dagster_pipeline()
    time.sleep(5)  # Wait for data to flow
    
    kafka_success = test_kafka_consumer()
    time.sleep(5)  # Wait for data to be processed
    
    postgres_success = test_postgresql_data()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    print(f"Dagster Pipeline: {'✅ PASS' if dagster_success else '❌ FAIL'}")
    print(f"Kafka Consumer:  {'✅ PASS' if kafka_success else '❌ FAIL'}")
    print(f"PostgreSQL:      {'✅ PASS' if postgres_success else '❌ FAIL'}")
    
    if all([dagster_success, kafka_success, postgres_success]):
        print("\n🎉 All tests passed! The data pipeline is working correctly.")
        return True
    else:
        print("\n⚠️  Some tests failed. Check the logs for more details.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
