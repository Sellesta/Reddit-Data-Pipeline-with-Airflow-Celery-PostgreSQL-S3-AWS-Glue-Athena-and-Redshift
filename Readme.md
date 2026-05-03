<div align="center">

# Reddit Data Pipeline

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Apache Airflow](https://img.shields.io/badge/Airflow-2.x-017CEE?style=flat-square&logo=apacheairflow&logoColor=white)](https://airflow.apache.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker&logoColor=white)](https://docker.com)
[![AWS](https://img.shields.io/badge/AWS-S3%20·%20Glue%20·%20Athena%20·%20Redshift-FF9900?style=flat-square&logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

A production-grade ETL pipeline that extracts posts from the Reddit API, stages them in S3, transforms them with AWS Glue + Athena, and loads the results into a Redshift data warehouse — all orchestrated by Apache Airflow running in Docker.

</div>

---

## Architecture

```mermaid
flowchart LR
    subgraph Ingest["Ingest"]
        A[Reddit API\nPRAW] --> B[Airflow DAG\n+ Celery]
        B --> C[(PostgreSQL\nMetadata)]
    end

    subgraph Storage["Storage"]
        B --> D[(Amazon S3\nRaw JSON)]
    end

    subgraph Transform["Transform"]
        D --> E[AWS Glue\nCrawler + Job]
        E --> F[Amazon Athena\nSQL views]
    end

    subgraph Serve["Serve"]
        F --> G[(Amazon Redshift\nData Warehouse)]
        G --> H[Analytics /\nBI Tools]
    end

    style Ingest fill:#E6F1FB,stroke:#185FA5,color:#0C447C
    style Storage fill:#FAEEDA,stroke:#854F0B,color:#633806
    style Transform fill:#EAF3DE,stroke:#3B6D11,color:#27500A
    style Serve fill:#EEEDFE,stroke:#534AB7,color:#3C3489
```

| Stage | Tool | Role |
|---|---|---|
| Orchestration | Apache Airflow + Celery | DAG scheduling, task distribution, retries |
| Metadata store | PostgreSQL | Airflow backend, pipeline run history |
| Extraction | PRAW (Reddit API) | Pull posts, comments, metadata |
| Raw storage | Amazon S3 | Immutable data lake landing zone |
| Cataloguing | AWS Glue Crawler | Auto-detect schema, populate Data Catalog |
| Transformation | AWS Glue Jobs + Amazon Athena | Clean, deduplicate, aggregate via SQL |
| Warehousing | Amazon Redshift | Columnar analytics at scale |

---

## Project Structure

```
├── dags/               # Airflow DAG definitions
├── etls/               # Extraction & transformation logic
├── pipelines/          # Pipeline orchestration helpers
├── utils/              # Shared utilities (config, logging)
├── data/               # Local staging for development
├── Dockerfile          # Custom Airflow image
├── docker-compose.yml  # Full stack: Airflow, Celery, PostgreSQL
├── airflow.env         # Environment variables template
└── requirements.txt    # Python dependencies
```

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.9+ |
| Docker + Docker Compose | Latest |
| AWS Account | S3, Glue, Athena, Redshift permissions |
| Reddit API credentials | [Create app here](https://www.reddit.com/prefs/apps) |

---

## Quick Start

```bash
# 1. Clone
git clone https://github.com/Sellesta/Reddit-Data-Pipeline-with-Airflow-Celery-PostgreSQL-S3-AWS-Glue-Athena-and-Redshift.git
cd Reddit-Data-Pipeline-with-Airflow-Celery-PostgreSQL-S3-AWS-Glue-Athena-and-Redshift

# 2. Configure
cp airflow.env .env
# Edit .env — add your Reddit API keys and AWS credentials

# 3. Launch the stack
docker-compose up -d

# 4. Open Airflow UI
open http://localhost:8080
# Default login: airflow / airflow

# 5. Enable the DAG and trigger a run
```

---

## AWS Setup

Before running the pipeline, provision the following:

```
S3:       Create a bucket (e.g. reddit-raw-data-<your-name>)
Glue:     Create a Crawler pointing at the S3 bucket prefix
Athena:   Set a query results location in the same bucket
Redshift: Create a cluster and a target schema/table
IAM:      Attach AmazonS3FullAccess, AWSGlueConsoleFullAccess,
          AmazonAthenaFullAccess, AmazonRedshiftFullAccess to your user/role
```

Update the paths in `utils/config.py` to match your bucket name and Redshift connection string.

---

## How It Works

1. Airflow triggers the DAG on a schedule (configurable — default daily)
2. A Celery worker calls the Reddit API via PRAW and pulls the top N posts from a target subreddit
3. Raw JSON is written to S3 at `s3://<bucket>/raw/YYYY/MM/DD/`
4. AWS Glue Crawler runs and updates the Data Catalog schema
5. A Glue Job + Athena view cleans and aggregates the data
6. The transformed dataset is `COPY`-loaded into Redshift
7. Airflow marks the DAG run complete and logs metadata to PostgreSQL

---

## Configuration

Key settings in `utils/config.py`:

| Variable | Description |
|---|---|
| `REDDIT_CLIENT_ID` | Reddit API app client ID |
| `REDDIT_SECRET` | Reddit API app secret |
| `TARGET_SUBREDDIT` | Subreddit to pull from (default: `r/dataengineering`) |
| `POST_LIMIT` | Number of posts per run |
| `S3_BUCKET` | Your S3 bucket name |
| `REDSHIFT_CONN` | SQLAlchemy connection string |

---

## Author

Built by [Moses Wanjema](https://github.com/Sellesta) · [LinkedIn](https://www.linkedin.com/in/moses-wanjema-a43253133/) · [Portfolio](https://datascienceportfol.io/brilliantpenman)
