# Data Engineering Project: Dagster + Kafka + PyFlink + PostgreSQL

This project demonstrates a complete data engineering pipeline that generates fake data using Dagster, sends it to Kafka, processes it with PyFlink, and stores it in PostgreSQL.

## Architecture Overview

```
Dagster Pipeline (Daily at 10 AM)
         ↓
    Generate Fake Data
         ↓
    Send to Kafka Topic
         ↓
    Kafka Consumer (Python)
         ↓
    PostgreSQL Database
```

## Current Status ✅

**All components are working successfully!**

- ✅ **Dagster**: Generates fake data and sends to Kafka
- ✅ **Kafka**: Receives and stores messages
- ✅ **Kafka Consumer**: Processes messages and inserts into PostgreSQL  
- ✅ **PostgreSQL**: Stores data with proper timestamps
- ✅ **Dagster UI**: Accessible at http://localhost:3000
- ✅ **Kafka UI**: Accessible at http://localhost:8080

**Data Flow Verified**: The pipeline has successfully processed multiple batches of fake data, demonstrating end-to-end functionality.

## Components

- **Dagster**: Orchestrates data generation and scheduling
- **Faker**: Generates realistic fake data
- **Kafka**: Message broker for data streaming
- **Kafka Consumer (Python)**: Stream processing and data ingestion
- **PostgreSQL**: Data warehouse
- **Docker Compose**: Local development environment

## Prerequisites

- Docker and Docker Compose installed on your MacBook
- At least 4GB of available RAM
- Ports 3000, 8080, 9092, 5432 available

## Quick Start

### 1. Clone and Setup

```bash
# Navigate to your project directory
cd project_final

# Make sure all files are in place
ls -la
```

### 2. Start the Infrastructure

```bash
# Start all services
docker-compose up -d

# Check service status
docker-compose ps
```

### 3. Verify Services

Wait for all services to be healthy (this may take 2-3 minutes):

```bash
# Check service health
docker-compose ps

# View logs if needed
docker-compose logs -f
```

## Service Access Points

- **Dagster UI**: http://localhost:3000
- **Kafka UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432
- **Kafka**: localhost:9092

## Running the Pipeline

### Option 1: Manual Execution

```bash
# Run the Dagster pipeline manually
python dagster_pipeline.py
```

### Option 2: Test End-to-End Pipeline

```bash
# Test the complete data flow
python test_end_to_end.py
```

### Option 2: Scheduled Execution

```bash
# Start the scheduler (runs daily at 10 AM)
python dagster_scheduler.py
```

### Option 3: Through Dagster UI

1. Open http://localhost:3000
2. Navigate to Assets
3. Click on "generate_and_send_fake_data"
4. Click "Materialize" to run manually

## Data Flow

1. **Data Generation**: Dagster generates 100 fake records daily with 5 columns:
   - `id`: Unique identifier
   - `name`: Full name
   - `email`: Email address
   - `company`: Company name
   - `job_title`: Job title
   - `created_at`: Timestamp
   - `partition_date`: Date partition

2. **Kafka Streaming**: Data is sent to Kafka topic `fake_data_topic`

3. **Flink Processing**: PyFlink consumer reads from Kafka and processes the data

4. **Database Storage**: Processed data is stored in PostgreSQL table `fake_data`

## Monitoring

### Kafka UI
- Access: http://localhost:8080
- Monitor topics, messages, and consumer groups
- View message content and offsets

### Dagster UI
- Access: http://localhost:3000
- Monitor pipeline runs and asset materializations
- View logs and execution history

### PostgreSQL
```bash
# Connect to database
docker exec -it postgres psql -U postgres -d fake_data_db

# View data
SELECT COUNT(*) FROM fake_data;
SELECT * FROM fake_data ORDER BY processed_at DESC LIMIT 10;
```

## Troubleshooting

### Common Issues

1. **Port Conflicts**
   ```bash
   # Check what's using a port
   lsof -i :3000
   lsof -i :9092
   lsof -i :5432
   ```

2. **Service Not Starting**
   ```bash
   # Check logs
   docker-compose logs [service-name]
   
   # Restart specific service
   docker-compose restart [service-name]
   ```

3. **Memory Issues**
   ```bash
   # Check Docker resource usage
   docker stats
   
   # Increase Docker memory limit in Docker Desktop
   ```

### Reset Everything

```bash
# Stop and remove all containers
docker-compose down -v

# Remove all volumes
docker volume prune

# Start fresh
docker-compose up -d
```

## Development

### Adding New Data Fields

1. Modify `dagster_pipeline.py` to generate new fields
2. Update `pyflink_consumer.py` to handle new fields
3. Modify `init.sql` to add new columns
4. Restart services

### Changing Schedule

Edit `dagster_scheduler.py`:
```python
# Change from 10:00 AM to 2:00 PM
schedule.every().day.at("14:00").do(run_dagster_job)
```

### Scaling

- Increase `FLINK_PARALLELISM` in config.env
- Adjust Kafka partitions in docker-compose.yml
- Modify PostgreSQL connection pooling

## File Structure

```
project_final/
├── dagster_pipeline.py      # Main Dagster pipeline
├── pyflink_consumer.py      # Flink consumer for Kafka
├── dagster_scheduler.py     # Daily scheduler
├── docker-compose.yml       # Infrastructure setup
├── Dockerfile.pyflink       # PyFlink container
├── init.sql                 # Database initialization
├── requirements.txt         # Python dependencies
├── config.env              # Environment variables
└── README.md               # This file
```

## Performance Tuning

- **Kafka**: Adjust `KAFKA_BATCH_SIZE` and `KAFKA_LINGER_MS`
- **Flink**: Modify `FLINK_PARALLELISM` and checkpoint intervals
- **PostgreSQL**: Tune `shared_buffers` and `work_mem`

## Security Notes

- Default credentials are for development only
- Change passwords in production
- Consider SSL/TLS for Kafka and PostgreSQL
- Implement proper authentication for Dagster

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Docker logs: `docker-compose logs -f`
3. Verify service health: `docker-compose ps`
4. Check resource usage: `docker stats`

## Next Steps

- Add data validation and quality checks
- Implement error handling and retry logic
- Add monitoring and alerting
- Set up CI/CD pipeline
- Add unit and integration tests
- Implement data lineage tracking
