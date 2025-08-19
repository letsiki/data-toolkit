"""
Sample Spark job using datatoolkit utilities
"""
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

# Import your custom utilities
from datatoolkit.spark.transformations.data_quality import create_data_quality_checker
from datatoolkit.common.logging.logger import get_logger


def main():
    """Main function to run the data quality job."""
    logger = get_logger(__name__)
    
    # Initialize Spark session
    spark = SparkSession.builder \
        .appName("DataQualityJob") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()
    
    try:
        logger.info("Starting data quality job")
        
        # Load your data (replace with actual data source)
        df = spark.read.option("header", "true").csv("s3://your-bucket/data/users.csv")
        
        # Create and run data quality checks
        checker = create_data_quality_checker(df)
        
        # Run comprehensive checks
        checker \
            .check_schema(
                expected_columns=['user_id', 'email', 'age', 'registration_date'],
                strict=True
            ) \
            .check_null_values(
                columns=['user_id', 'email'],
                max_null_percentage=0.0
            ) \
            .check_null_values(
                columns=['age'],
                max_null_percentage=5.0
            ) \
            .check_duplicates(
                subset=['user_id'],
                max_duplicate_percentage=0.0
            ) \
            .check_value_ranges({
                'age': {'min': 13, 'max': 120}
            }) \
            .check_uniqueness(['user_id'])
        
        # Generate profile
        profile = checker.generate_profile()
        logger.info(f"Data profile: {profile}")
        
        # Validate and get report
        checker.validate_and_raise(fail_on_issues=False)
        report = checker.get_report()
        
        # Log summary
        logger.info(f"Checks performed: {report['checks_performed']}")
        if report['issues_found']:
            logger.warning(f"Issues found: {report['issues_found']}")
        else:
            logger.info("All data quality checks passed!")
        
        # Example of data transformation after quality checks
        if not report['issues_found']:
            logger.info("Proceeding with data transformation")
            
            # Clean and transform data
            cleaned_df = df.filter(col('age').isNotNull()) \
                          .filter(col('age').between(13, 120))
            
            # Add some derived columns
            final_df = cleaned_df.withColumn(
                'age_group',
                when(col('age') < 25, 'Young')
                .when(col('age') < 45, 'Middle')
                .otherwise('Senior')
            )
            
            # Save results (replace with actual destination)
            final_df.write \
                .mode('overwrite') \
                .option("header", "true") \
                .csv("s3://your-bucket/processed/users_cleaned")
            
            logger.info("Data transformation completed successfully")
        else:
            logger.error("Data quality issues found. Skipping transformation.")
        
    except Exception as e:
        logger.error(f"Job failed with error: {str(e)}")
        raise
    finally:
        spark.stop()


if __name__ == "__main__":
    main()