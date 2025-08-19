# Data Toolkit 🛠️

A collection of reusable data engineering utilities for Airflow, Spark, and more. Designed for easy installation and maximum portability across different environments.

## Quick Start

### Install Individual Components

```bash
# Common utilities (recommended for all installations)
pip install git+https://github.com/yourusername/data-toolkit.git#subdirectory=common

# Airflow operators and utilities
pip install git+https://github.com/yourusername/data-toolkit.git#subdirectory=airflow

# Spark transformations and utilities
pip install git+https://github.com/yourusername/data-toolkit.git#subdirectory=spark
```

### Install Common Combinations

```bash
# Airflow + Common utilities
pip install -r https://raw.githubusercontent.com/yourusername/data-toolkit/main/examples/requirements_examples/airflow_requirements.txt

# Spark + Common utilities  
pip install -r https://raw.githubusercontent.com/yourusername/data-toolkit/main/examples/requirements_examples/spark_requirements.txt
```

## What's Included

### 📁 Common (`common/`)
Shared utilities used across all data engineering tools:
- **Logging**: Standardized logging configuration
- **Validation**: Data validation utilities and custom exceptions
- **Configuration**: Common configuration management

### ✈️ Airflow (`airflow/`)
Custom Airflow operators and utilities:
- **DataQualityOperator**: Comprehensive data quality checks for database tables
- **Custom Hooks**: Enhanced database connections
- **DAG Utilities**: Helper functions for DAG creation

### ⚡ Spark (`spark/`)
PySpark transformations and utilities:
- **Data Quality Checker**: Comprehensive DataFrame validation
- **Schema Validation**: Schema compatibility checking
- **Common Transformations**: Reusable data transformation functions

## Usage Examples

### Airflow Data Quality Operator

```python
from datatoolkit.airflow.operators.data_quality_operator import DataQualityOperator

# Use in your DAG
quality_check = DataQualityOperator(
    task_id='check_users_table',
    table_name='users',
    postgres_conn_id='postgres_default',
    checks=[
        {
            'name': 'row_count_check',
            'type': 'row_count',
            'min_count': 1000
        },
        {
            'name': 'email_not_null',
            'type': 'null_count',
            'column': 'email',
            'max_null_percentage': 0.0
        }
    ],
    fail_on_error=True
)
```

### Spark Data Quality Checker

```python
from datatoolkit.spark.transformations.data_quality import create_data_quality_checker

# Create checker for your DataFrame
checker = create_data_quality_checker(df)

# Run quality checks with method chaining
checker \
    .check_schema(['user_id', 'email', 'age']) \
    .check_null_values(max_null_percentage=5.0) \
    .check_duplicates() \
    .check_value_ranges({'age': {'min': 0, 'max': 120}}) \
    .validate_and_raise()

# Get detailed report
report = checker.get_report()
```

## Repository Structure

```
data-toolkit/
├── common/           # Shared utilities
├── airflow/          # Airflow operators and hooks
├── spark/            # Spark transformations
└── examples/         # Usage examples and requirements files
```

## Installation in Different Environments

### Local Development
```bash
pip install git+https://github.com/yourusername/data-toolkit.git#subdirectory=airflow
```

### Docker/Containers
```dockerfile
FROM apache/airflow:2.8.0
RUN pip install git+https://github.com/yourusername/data-toolkit.git#subdirectory=common \
                git+https://github.com/yourusername/data-toolkit.git#subdirectory=airflow
```

### Requirements File
```txt
# requirements.txt
git+https://github.com/yourusername/data-toolkit.git#subdirectory=common
git+https://github.com/yourusername/data-toolkit.git#subdirectory=airflow
apache-airflow>=2.5.0
```

## Features

- **🔧 Modular**: Install only what you need
- **📦 Portable**: Works in any Python environment
- **🚀 Easy to Use**: Simple, memorable installation URLs
- **🔍 Well-Tested**: Comprehensive data quality checks
- **📖 Well-Documented**: Clear examples and documentation
- **🔗 No Dependencies**: Each module can work independently

## Examples

Check out the `examples/` directory for:
- Sample Airflow DAGs using custom operators
- Spark job examples with data quality checks
- Requirements files for common installation patterns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests and documentation
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Versioning

This project uses semantic versioning. Install specific versions using:

```bash
pip install git+https://github.com/yourusername/data-toolkit.git@v1.0.0#subdirectory=airflow
```