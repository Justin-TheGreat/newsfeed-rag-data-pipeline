import os
import schedule
import time
from datetime import datetime
from dagster import execute_job
from dagster_pipeline import daily_fake_data_job

def run_dagster_job():
    """Execute the Dagster job."""
    try:
        print(f"[{datetime.now()}] Starting Dagster job execution...")
        
        # Execute the job
        result = execute_job(daily_fake_data_job)
        
        if result.success:
            print(f"[{datetime.now()}] Job completed successfully!")
        else:
            print(f"[{datetime.now()}] Job failed!")
            
    except Exception as e:
        print(f"[{datetime.now()}] Error executing job: {str(e)}")

def main():
    """Main function to run the scheduler."""
    
    print("Starting Dagster Scheduler...")
    print("Job will run daily at 10:00 AM")
    
    # Schedule the job to run at 10:00 AM daily
    schedule.every().day.at("10:00").do(run_dagster_job)
    
    # Run the job immediately for testing (optional)
    # run_dagster_job()
    
    # Keep the scheduler running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main()
