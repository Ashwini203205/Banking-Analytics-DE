FROM apache/airflow:2.9.2

USER root

RUN apt-get update && apt-get install -y default-jdk && apt-get clean

ENV JAVA_HOME=/usr/lib/jvm/default-java

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt