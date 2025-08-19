"""
Sample Airflow DAG using datatoolkit operators
"""
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator

# Import your custom operators
from datatoolkit.airflow.operators.data_quality_operator import DataQualityOperator

# Default arguments
default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'sample_data_quality_pipeline',
    default_args=default_args,
    description='Sample data quality pipeline using datatoolkit',
    schedule_interval=timedelta(days=1),
    catchup=False,
    tags=['data-quality', 'datatoolkit']
)

# Start task
start_task = DummyOperator(
    task_id='start',
    dag=dag
)

# Data quality checks for users table
users_quality_check = DataQualityOperator(
    task_id='check_users_quality',
    table_name='users',
    postgres_conn_id='postgres_default',
    checks=[
        {
            'name': 'users_row_count',
            'type': 'row_count',
            'min_count': 1000,
            'max_count': 1000000
        },
        {
            'name': 'email_not_null',
            'type': 'null_count',
            'column': 'email',
            'max_null_percentage': 0.0
        },
        {
            'name': 'user_id_unique',
            'type': 'unique_count',
            'column': 'user_id',
            'should_be_unique': True
        },
        {
            'name': 'age_range',
            'type': 'value_range',
            'column': 'age',
            'min_value': 13,
            'max_value': 120
        }
    ],
    custom_sql_checks=[
        {
            'name': 'active_users_ratio',
            'sql': "SELECT COUNT(*) FROM users WHERE is_active = true",
            'expected_result': None  # Just log the result
        }
    ],
    fail_on_error=True,
    dag=dag
)

# Data quality checks for orders table
orders_quality_check = DataQualityOperator(
    task_id='check_orders_quality',
    table_name='orders',
    postgres_conn_id='postgres_default',
    checks=[
        {
            'name': 'orders_row_count',
            'type': 'row_count',
            'min_count': 500
        },
        {
            'name': 'order_amount_range',
            'type': 'value_range',
            'column': 'amount',
            'min_value': 0.01,
            'max_value': 100000
        }
    ],
    fail_on_error=False,  # Don't fail the pipeline, just log warnings
    dag=dag
)

# End task
end_task = DummyOperator(
    task_id='end',
    dag=dag
)

# Define task dependencies
start_task >> [users_quality_check, orders_quality_check] >> end_task