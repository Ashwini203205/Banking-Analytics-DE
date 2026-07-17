# Banking-Analytics-DE"
# 🏦 Banking Analytics Data Engineering Pipeline

> End-to-End Data Engineering Project using PySpark, PostgreSQL, Docker, Apache Airflow, and Power BI

---

# 📌 Project Overview

This project demonstrates a complete **Data Engineering Pipeline** built using industry-standard tools and best practices.

The pipeline ingests raw banking customer data, processes it through the **Medallion Architecture (Bronze, Silver, Gold)**, stores the transformed data in PostgreSQL, automates the workflow using Apache Airflow, containerizes the application with Docker, and visualizes business insights using Power BI.

---

# 🎯 Project Objectives

- Build an end-to-end ETL pipeline
- Implement Medallion Architecture
- Perform data cleaning and transformations
- Create business summary tables
- Store processed data in PostgreSQL
- Automate the pipeline using Apache Airflow
- Containerize the project using Docker
- Build an interactive Power BI dashboard

---

# 🏗️ Project Architecture

```
                        CSV Dataset
                             │
                             ▼
                     PySpark Ingestion
                             │
                             ▼
                     Bronze Layer (Raw)
                             │
                             ▼
                Silver Layer (Cleaned Data)
                             │
                             ▼
               Gold Layer (Business Tables)
                             │
                             ▼
                     PostgreSQL Database
                     /                  \
                    /                    \
                   ▼                      ▼
        Apache Airflow              Power BI Dashboard
          (Automation)           (Business Insights)
                   ▲
                   │
              Docker Container
```

---

# 🛠️ Technology Stack

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| PySpark | Data Processing |
| PostgreSQL | Data Warehouse |
| SQL | Querying |
| Apache Airflow | Workflow Automation |
| Docker | Containerization |
| Power BI | Dashboard & Reporting |
| Git | Version Control |
| GitHub | Source Code Repository |

---

# 📂 Project Structure

```
Banking-Analytics-DE
│
├── airflow/
│   └── DAG files
│
├── data/
│   └── bank.csv
│
├── docker/
│   └── Docker related files
│
├── jars/
│   └── PostgreSQL JDBC Driver
│
├── logs/
│
├── spark/
│   ├── load_bronze.py
│   ├── load_silver.py
│   ├── load_gold.py
│   ├── load_gold_customer.py
│   ├── load_gold_job.py
│   ├── load_gold_month.py
│   ├── load_gold_education.py
│   ├── load_gold_marital.py
│   ├── scd_type2.py
│   └── ...
│
├── dashboard/
│   └── Banking Analytics.pbix
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

# 🔄 ETL Pipeline

## Step 1 – Data Source

- Bank Marketing Dataset (CSV)
- 45,211 customer records

---

## Step 2 – Bronze Layer

Purpose:

- Store raw data
- No modifications
- Preserve original records

Output Table

```
bronze.customer_raw
```

---

## Step 3 – Silver Layer

Data Cleaning Performed

- Remove duplicates
- Handle null values
- Trim spaces
- Standardize text
- Convert data types
- Validate records

Output Table

```
silver.customer_clean
```

---

## Step 4 – Gold Layer

Business transformation tables created:

| Table | Description |
|--------|-------------|
| customer_summary | Overall KPIs |
| deposit_summary | Deposit Subscription Summary |
| job_summary | Customers by Job |
| education_summary | Customers by Education |
| marital_summary | Customers by Marital Status |
| month_summary | Monthly Subscription Analysis |

---

# 🗄️ Data Warehouse

Database

```
PostgreSQL
```

Database Name

```
banking_analytics
```

Schemas

```
bronze
silver
gold
```

---

# 📈 Power BI Dashboard

Dashboard includes:

✅ Total Customers

✅ Subscribed Customers

✅ Average Age

✅ Average Balance

✅ Total Balance

✅ Customers by Job

✅ Customers by Education

✅ Customers by Marital Status

✅ Monthly Subscription Trend

✅ Deposit Subscription Status

✅ Business Insights Panel

---

# 📊 Business Insights

- 45K total customers
- Around 5K customers subscribed to deposits
- Average customer age is approximately 41 years
- Total customer balance exceeds ₹61M
- Majority of customers are married
- Secondary education customers form the largest group
- Customer subscriptions vary significantly across months

---

# ⚙️ Apache Airflow

Airflow is used to automate the ETL workflow.

Pipeline Flow

```
Start

↓

Load Bronze

↓

Load Silver

↓

Load Gold

↓

SCD Type 2

↓

End
```

Benefits

- Workflow scheduling
- Dependency management
- Monitoring
- Retry on failures
- Pipeline automation

---

# 🐳 Docker

Docker is used to containerize the application.

Benefits

- Consistent environment
- Easy deployment
- Portable setup
- Simplified dependency management

---

# 🧩 Slowly Changing Dimension (SCD Type 2)

Implemented for customer history tracking.

Maintains:

- Historical records
- Start Date
- End Date
- Current Flag

Table

```
gold.dim_customer_history
```

---

# 🚀 How to Run the Project

## Clone Repository

```bash
git clone <repository-url>
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

---

## Activate Environment

Windows

```bash
.venv\Scripts\activate
```

---

## Install Requirements

```bash
pip install -r requirements.txt
```

---

## Start PostgreSQL

Ensure PostgreSQL service is running.

---

## Run ETL

```bash
python spark/load_bronze.py

python spark/load_silver.py

python spark/load_gold.py

python spark/scd_type2.py
```

---

## Start Airflow

```bash
docker compose up -d
```

Open

```
http://localhost:8080
```

---

## Open Power BI Dashboard

Refresh the dashboard after ETL execution.

---

# 📷 Screenshots

## Architecture

(Add architecture image)

---

## Airflow DAG

(Add screenshot)

---

## Docker Containers

(Add screenshot)

---

## Power BI Dashboard

(Add dashboard screenshot)

---

# 💼 Skills Demonstrated

- Data Engineering
- ETL Pipeline
- ELT Concepts
- Medallion Architecture
- PySpark
- SQL
- PostgreSQL
- Docker
- Docker Compose
- Apache Airflow
- Power BI
- Data Warehouse
- Data Modeling
- Data Cleaning
- Business Transformation
- SCD Type 2
- Git
- GitHub

---

# 🔮 Future Enhancements

- Incremental Loading
- Kafka Streaming
- Delta Lake
- Azure Data Factory
- Snowflake
- AWS S3
- Databricks
- CI/CD Integration
- Unit Testing
- Data Quality Framework

---

# 👨‍💻 Author

**Ashwini Giri**

Bachelor of Engineering (Information Technology)

Passionate about Data Engineering, Big Data, ETL Pipelines, Cloud Technologies, and Business Intelligence.

GitHub:
(Add GitHub Link)

LinkedIn:
(Add LinkedIn Link)

---

# ⭐ If you found this project helpful, please consider giving it a star!
