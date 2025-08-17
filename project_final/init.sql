-- Initialize PostgreSQL database for fake data
-- This script runs when the PostgreSQL container starts

-- Create the fake_data table
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

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_fake_data_partition_date ON fake_data(partition_date);
CREATE INDEX IF NOT EXISTS idx_fake_data_processed_at ON fake_data(processed_at);

-- Create a view for recent data
CREATE OR REPLACE VIEW recent_fake_data AS
SELECT * FROM fake_data 
WHERE processed_at >= CURRENT_DATE - INTERVAL '7 days'
ORDER BY processed_at DESC;

-- Grant permissions
GRANT ALL PRIVILEGES ON TABLE fake_data TO postgres;
GRANT ALL PRIVILEGES ON VIEW recent_fake_data TO postgres;

-- Insert a sample record to verify the table works
INSERT INTO fake_data (id, name, email, company, job_title, created_at, partition_date)
VALUES (
    'sample-001',
    'John Doe',
    'john.doe@example.com',
    'Sample Corp',
    'Software Engineer',
    '2024-01-01T00:00:00',
    '2024-01-01'
) ON CONFLICT (id) DO NOTHING;
