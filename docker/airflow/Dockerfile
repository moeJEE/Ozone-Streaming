FROM apache/airflow:2.7.3

USER root

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python dependencies
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy DAGs
COPY dags/ /opt/airflow/dags/

# Set environment variables
ENV AIRFLOW__CORE__EXECUTOR=LocalExecutor
ENV AIRFLOW__CORE__SQL_ALCHEMY_CONN=postgresql://streaming_user:streaming_pass@postgres:5432/streaming_db
ENV AIRFLOW__CORE__DAGS_FOLDER=/opt/airflow/dags

