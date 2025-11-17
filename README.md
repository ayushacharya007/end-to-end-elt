# 🚀 End-to-End ELT Pipeline

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121.1-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E.svg)

> A production-ready ELT (Extract, Load, Transform) data pipeline that generates synthetic subscription service data, loads it into PostgreSQL via DLT, and exposes it through an authenticated REST API.

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#-architecture)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [API Documentation](#-api-documentation)
- [Data Schema](#-data-schema)
- [Deployment](#-deployment)
- [Development](#-development)
- [Configuration](#-configuration)

## 🎯 Overview

This project demonstrates a complete data engineering workflow:

1. **Extract**: Generate synthetic subscription data using Faker
2. **Load**: Bulk load data into PostgreSQL using DLT (Data Load Tool)
3. **Transform**: Query and expose data through FastAPI endpoints
4. **Deploy**: Production deployment on Railway with PostgreSQL backend

**Live Demo**: `https://fastapi-production-15f1.up.railway.app`

## 🏗️ Architecture

```
┌─────────────────┐
│  Faker Library  │  Generate synthetic data
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DLT Pipeline   │  Extract & Load to PostgreSQL
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  PostgreSQL DB  │  faker_dlt_dataset schema
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ FastAPI + SQLAlchemy│  REST API Layer
└────────┬────────────┘
         │
         ▼
┌─────────────────┐
│  Railway Cloud  │  Production Deployment
└─────────────────┘
```

### Technology Stack

| Component           | Technology           | Purpose                                      |
| ------------------- | -------------------- | -------------------------------------------- |
| **Data Generation** | Faker 38.0.0         | Create realistic synthetic data              |
| **ETL Pipeline**    | DLT 1.18.2           | Efficient data loading with schema evolution |
| **Database**        | PostgreSQL 15        | Production data storage                      |
| **API Framework**   | FastAPI 0.121.1      | High-performance REST API                    |
| **ORM**             | SQLAlchemy 2.0.44    | Database abstraction layer                   |
| **Deployment**      | Railway              | Cloud hosting with CI/CD                     |
| **Authentication**  | Query Parameter Auth | Simple & secure API access                   |

## 📚 API Documentation

### Base URL

- **Local**: `http://localhost:8000`
- **Production**: `https://fastapi-production-15f1.up.railway.app`

### Authentication

All endpoints (except `/check-tables`) require query parameter authentication:

```bash
?username=admin&password=admin
```

### Endpoints

| Endpoint         | Method | Description           | Auth Required   |
| ---------------- | ------ | --------------------- | --------------- |
| `/`              | GET    | Welcome message       | ✅ Basic Auth   |
| `/check-tables`  | GET    | List all tables       | ❌              |
| `/users`         | GET    | Get all users         | ✅ Query Params |
| `/plans`         | GET    | Get all plans         | ✅ Query Params |
| `/subscriptions` | GET    | Get all subscriptions | ✅ Query Params |
| `/usages`        | GET    | Get all usage records | ✅ Query Params |

### Response Format

**Success Response:**

```json
{
  "users": [
    {
      "user_id": "1f3294c1",
      "first_name": "Shane",
      "last_name": "Wyatt",
      "email": "shane@example.com",
      "signup_date": "2025-10-23",
      "plan_id": 3,
      "region": "North America",
      "referral_source": "social media"
    }
  ]
}
```

**Error Response:**

```json
{
  "error": "Error message",
  "traceback": "Detailed stack trace..."
}
```

## 🗄️ Data Schema

### Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│     User     │       │     Plan     │       │ Subscription │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ user_id (PK) │───┐   │ plan_id (PK) │───┐   │subscription_id│
│ first_name   │   │   │ plan_name    │   │   │ user_id (FK) │
│ last_name    │   │   │ monthly_fee  │   │   │ plan_id (FK) │
│ email        │   │   │ max_users    │   │   │ start_date   │
│ signup_date  │   │   │ features     │   │   │ end_date     │
│ plan_id      │   │   └──────────────┘   │   │ status       │
│ region       │   │                      │   └──────────────┘
│referral_src  │   │   ┌──────────────┐   │
└──────────────┘   │   │    Usage     │   │
                   │   ├──────────────┤   │
                   └──▶│ user_id (FK) │   │
                       │ plan_id (FK) │◀──┘
                       │ usage_date   │
                       │ actions_perf │
                       │ storage_mb   │
                       │ api_calls    │
                       │active_minutes│
                       └──────────────┘
```

### Tables

#### 📊 **user** (1,000 records)

| Column            | Type            | Description                 |
| ----------------- | --------------- | --------------------------- |
| `user_id`         | String (PK)     | Unique user identifier      |
| `first_name`      | String          | User's first name           |
| `last_name`       | String          | User's last name            |
| `email`           | String (Unique) | User's email address        |
| `signup_date`     | String          | Account creation date       |
| `plan_id`         | Integer         | Subscription plan reference |
| `region`          | String          | Geographic region           |
| `referral_source` | String          | How user found service      |

#### 💼 **plan** (5 records)

| Column        | Type         | Description                   |
| ------------- | ------------ | ----------------------------- |
| `plan_id`     | Integer (PK) | Unique plan identifier        |
| `plan_name`   | String       | Plan name (Free, Basic, etc.) |
| `monthly_fee` | Float        | Monthly subscription cost     |
| `max_users`   | String       | User limit                    |
| `features`    | JSON         | Plan features array           |

#### 📝 **subscription** (1,717 records)

| Column            | Type         | Description            |
| ----------------- | ------------ | ---------------------- |
| `subscription_id` | String (PK)  | Unique subscription ID |
| `user_id`         | String (FK)  | Reference to user      |
| `plan_id`         | Integer (FK) | Reference to plan      |
| `start_date`      | String       | Subscription start     |
| `end_date`        | String       | Subscription end       |
| `payment_method`  | String       | Payment type           |
| `status`          | String       | Active/Inactive        |

#### 📈 **usage** (5,000 records)

| Column              | Type         | Description            |
| ------------------- | ------------ | ---------------------- |
| `usage_id`          | String (PK)  | Unique usage record ID |
| `user_id`           | String (FK)  | Reference to user      |
| `plan_id`           | Integer (FK) | Reference to plan      |
| `usage_date`        | String       | Date of usage          |
| `actions_performed` | Integer      | Number of actions      |
| `storage_used_mb`   | Float        | Storage consumed (MB)  |
| `api_calls`         | Integer      | API requests made      |
| `active_minutes`    | Integer      | Time spent active      |

### SCD2 Columns (Historical Tracking)

DLT automatically adds these columns for tracking changes:

| Column         | Type      | Purpose                                      |
| -------------- | --------- | -------------------------------------------- |
| `_dlt_load_id` | String    | Load batch identifier                        |
| `_dlt_id`      | String    | Record hash for deduplication                |
| `valid_from`   | Timestamp | When version became active                   |
| `valid_to`     | Timestamp | When version was superseded (NULL = current) |

## 🛠️ Development

### Project Structure

```
end-to-end-elt/
│
├── fastapi/                    # API application
│   ├── main.py                 # FastAPI app & endpoints
│   ├── model.py                # SQLAlchemy models
│   ├── config.py               # Database configuration
│   ├── migrate_to_railway.py  # Migration script
│   ├── requirements.txt        # Python dependencies
│   ├── railway.json            # Railway config
│   └── Procfile                # Process configuration
│
├── faker data/                 # Data generation
│   ├── test.ipynb              # Jupyter notebook
│   └── .dlt/                   # DLT configuration
│       └── secrets.toml        # DLT secrets (gitignored)
│
├── .env                        # Environment variables (gitignored)
├── .env.example                # Environment template
├── .gitignore                  # Git exclusions
├── pyproject.toml              # Project metadata
├── requirements.txt            # Root dependencies
└── README.md                   # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable               | Description                 | Example                               |
| ---------------------- | --------------------------- | ------------------------------------- |
| `LOCAL_DATABASE_URL`   | Local PostgreSQL connection | `postgresql://user:pass@localhost/db` |
| `RAILWAY_DATABASE_URL` | Production PostgreSQL URL   | Auto-generated by Railway             |
| `BASIC_AUTH_USERNAME`  | API authentication username | `admin`                               |
| `BASIC_AUTH_PASSWORD`  | API authentication password | `secure_password_123`                 |
| `DATASET_NAME`         | DLT dataset schema name     | `faker_dlt_dataset`                   |
| `PIPELINE_NAME`        | DLT pipeline identifier     | `railway_migration_pipeline`          |
| `DESTINATION`          | DLT destination type        | `postgres`                            |

### DLT Write Dispositions

Configure data loading behavior in `migrate_to_railway.py`:

| Mode        | Description               | Use Case      |
| ----------- | ------------------------- | ------------- |
| **replace** | Drop and recreate table   | Full refresh  |
| **append**  | Add without deduplication | Event logs    |
| **merge**   | Upsert (update/insert)    | Current state |
| **scd2**    | Historical tracking       | Audit trail   |

## 📧 Contact

**Ayush Acharya**

- Email: ayushach007@gmail.com

---
