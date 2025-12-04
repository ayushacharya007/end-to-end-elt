# 🚀 End-to-End ELT Pipeline

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.121.1-009688.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791.svg)
![dbt](https://img.shields.io/badge/dbt-1.9-FF694B.svg)
![Data Warehouse](https://img.shields.io/badge/Data%20Warehouse-Athena-orange.svg)
![Railway](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E.svg)

> A production-ready ELT (Extract, Load, Transform) data pipeline that generates synthetic subscription service data with normalized schema, loads it into PostgreSQL via DLT, exposes it through a paginated REST API, transforms it using dbt, and stores it in AWS Athena (Data Warehouse).

## 📋 Table of Contents

- [Overview](#-overview)
- [Architecture](#️-architecture)
- [Technology Stack](#️-technology-stack)
- [Data Generation](#-data-generation)
- [API Documentation](#-api-documentation)
- [Data Schema](#️-data-schema)
- [dbt Transformations](#-dbt-transformations)
- [Development](#️-development)

## 🎯 Overview

This project demonstrates a complete modern data engineering workflow:

1. **Extract**: Generate realistic synthetic subscription data using Faker with normalized schema
2. **Load**: Bulk load data into PostgreSQL using DLT (Data Load Tool)
3. **Transform**: Apply dimensional modeling using dbt for analytics-ready data
4. **Consume**: Query and expose data through FastAPI with pagination support
5. **Deploy**: Production deployment on Railway with PostgreSQL backend

**Live Demo**: `https://app-production-82bb.up.railway.app/`

## 🏗️ Architecture

```
┌───────────────────────────────────────────────────────────┐
│              Data Generation (Faker)                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                 │
│  │ Lookup   │  │  Entity  │  │  Usage   │                 │
│  │ Tables   │  │  Tables  │  │  Tables  │                 │
│  └─────┬────┘  └────┬─────┘  └────┬─────┘                 │
└────────┼────────────┼─────────────┼───────────────────────┘
         │            │             │
         ▼            ▼             ▼
┌───────────────────────────────────────────────────────────┐
│              DLT ETL Pipeline                             │
│  • Modular data generation scripts                        │
│  • Dependency-based loading order                         │
│  • SCD2 tracking for transactional data                   │
└────────┬──────────────────────────────────────────────────┘
         │
         ▼
┌───────────────────────────────────────────────────────────┐
│         PostgreSQL Database (test_dlt_dataset)            │
│  ┌──────────────────┐  ┌────────────────┐                 │
│  │ Lookup Tables    │  │ Transaction    │                 │
│  │ - regions        │  │ - users        │                 │
│  │ - referral       │  │ - subs         │                 │
│  │ - payment_methods│  │ - usage        │                 │
│  │ - plan_features  │  │                │                 │
│  │ - plans          │  │                │                 │
│  └──────────────────┘  └────────────────┘                 │
└────────┬──────────────────────────┬───────────────────────┘
         │                          │
         ▼                          ▼
┌──────────────────────┐  ┌────────────────────────────────┐
│ dbt Transform        │  │  FastAPI + SQLAlchemy          │
│ • Staging models     │  │  • Paginated endpoints         │
│ • Dimension models   │  │  • Lookup table endpoints      │
│                      │  │  • Query param auth            │
└──────────────────────┘  └────────┬───────────────────────┘
                                   │
                                   ▼
                          ┌──────────────────┐
                          │  Railway Cloud   │
                          │  Production      │
                          └──────────────────┘
```

## 🛠️ Technology Stack

| Component           | Technology           | Purpose                                      |
| ------------------- | -------------------- | -------------------------------------------- |
| **Data Generation** | Faker 38.0.0         | Create realistic synthetic data              |
| **ETL Pipeline**    | DLT 1.18.2           | Efficient data loading with schema evolution |
| **Database**        | PostgreSQL 15        | Production data storage                      |
| **Transformations** | dbt-core             | Dimensional modeling and analytics prep      |
| **API Framework**   | FastAPI 0.121.1      | High-performance REST API                    |
| **ORM**             | SQLAlchemy 2.0.44    | Database abstraction layer                   |
| **Pagination**      | fastapi-pagination   | Efficient paginated API responses            |
| **Validation**      | Pydantic 2.12.4      | Data validation and serialization            |
| **Deployment**      | Railway              | Cloud hosting with CI/CD                     |
| **Authentication**  | Query Parameter Auth | Simple & secure API access                   |

## 🎲 Data Generation

The project features a sophisticated data generation system with realistic patterns:

### Features

- **Normalized Schema**: Lookup tables for regions, referral sources, payment methods, and plan features
- **Multi-Renewal Support**: Users can renew subscriptions multiple times with configurable limits
- **Realistic Usage Patterns**:
  - User engagement levels (low/medium/high)
  - Temporal variations (weekday vs weekend usage)
  - Growth patterns over time
- **Quota Enforcement**: Plan-specific resource limits (API calls, storage)
- **Exhaustion Scenarios**: Simulates users hitting quota limits

### Modular Generation Scripts

Each table has its dedicated generation script in `fake data/data_generation/`:

- `generate_regions.py` - Geographic regions
- `generate_referral_sources.py` - Marketing channels
- `generate_payment_methods.py` - Payment types
- `generate_plans.py` - Subscription plans
- `generate_plan_features.py` - Plan capabilities
- `generate_users.py` - User accounts
- `generate_subscriptions.py` - Multi-renewal subscriptions
- `generate_usage.py` - Usage metrics with quota tracking

The `etl_pipeline.py` orchestrates the generation and loading in dependency order.

## 📚 API Documentation

### Base URL

- **Local**: `http://localhost:8000`
- **Production**: `https://app-production-82bb.up.railway.app/`

### Authentication

All endpoints (except `/check-tables`) require query parameter authentication:

```bash
?username=admin&password=admin
```

### Endpoints

#### Lookup Table Endpoints

| Endpoint            | Method | Description              | Pagination | Auth Required   |
| ------------------- | ------ | ------------------------ | ---------- | --------------- |
| `/regions`          | GET    | Get all regions          | ❌         | ✅ Query Params |
| `/referral-sources` | GET    | Get all referral sources | ❌         | ✅ Query Params |
| `/payment-methods`  | GET    | Get all payment methods  | ❌         | ✅ Query Params |
| `/plan-features`    | GET    | Get all plan features    | ❌         | ✅ Query Params |
| `/plans`            | GET    | Get all plans            | ❌         | ✅ Query Params |

#### Transactional Data Endpoints

| Endpoint         | Method | Description           | Pagination | Auth Required   |
| ---------------- | ------ | --------------------- | ---------- | --------------- |
| `/`              | GET    | Welcome message       | ❌         | ✅ Basic Auth   |
| `/check-tables`  | GET    | List all tables       | ❌         | ❌              |
| `/users`         | GET    | Get all users         | ✅         | ✅ Query Params |
| `/subscriptions` | GET    | Get all subscriptions | ✅         | ✅ Query Params |
| `/usages`        | GET    | Get all usage records | ✅         | ✅ Query Params |

#### Documentation Endpoints

| Endpoint         | Method | Description           | Auth Required   |
| ---------------- | ------ | --------------------- | --------------- |
| `/docs`          | GET    | Swagger UI            | ❌              |
| `/redoc`         | GET    | ReDoc                 | ❌              |

### Pagination

Paginated endpoints support the following query parameters:

- `page` - Page number (default: 1)
- `size` - Items per page (default: 50, max: 100)

**Example Request:**

```bash
GET /users?username=admin&password=admin&page=1&size=20
```

### Response Format

**Success Response (Non-Paginated):**

```json
{
  "items": [
    {
      "region_id": 1,
      "region_name": "North America"
    }
  ]
}
```

**Success Response (Paginated):**

```json
{
  "items": [
    {
      "user_id": "1f3294c1",
      "first_name": "Shane",
      "last_name": "Wyatt",
      "email": "shane@example.com",
      "signup_date": "2025-10-23",
      "plan_id": 3,
      "region_id": 1,
      "referral_source_id": 2
    }
  ],
  "total": 1000,
  "page": 1,
  "size": 50,
  "pages": 20
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
┌──────────────┐      ┌──────────────┐      ┌──────────────┐
│    Region    │      │   Referral   │      │   Payment    │
│              │      │              │      │    Method    │
├──────────────┤      ├──────────────┤      ├──────────────┤
│region_id (PK)│      │referral_id   │      │payment_id    │
│region_name   │      │source_name   │      │method_name   │
└──────┬───────┘      └──────┬───────┘      └──────┬───────┘
       │                     │                     │
       │  ┌──────────────┐   │       ┌─────────────┘
       │  │  PlanFeature │   │       │
       │  ├──────────────┤   │       │
       │  │feature_id(PK)│   │       │
       │  │feature_name  │   │       │
       │  │plan_id (FK)  │   │       │
       │  └──────┬───────┘   │       │
       │         │           │       │
       └────┐    │    ┌──────┘       │
            │    │    │              │
┌───────────▼────▼────▼──────────────▼─────┐
│                 User                     │
├──────────────────────────────────────────┤
│ user_id (PK)                             │
│ first_name, last_name, email             │
│ signup_date                              │
│ plan_id (FK) ───────────┐                │
│ region_id (FK)          │                │
│ referral_source_id (FK) │                │
└────────┬────────────────┼────────────────┘
         │                │
         │   ┌────────────▼────────┐
         │   │        Plan         │
         │   ├─────────────────────┤
         │   │ plan_id (PK)        │
         │   │ plan_name           │
         │   │ monthly_fee         │
         │   │ max_storage_mb      │
         │   │ max_api_calls       │
         │   └────────┬────────────┘
         │            │
         ▼            ▼
┌────────────────────────────┐
│      Subscription          │
├────────────────────────────┤
│ subscription_id (PK)       │
│ user_id (FK)               │
│ plan_id (FK)               │
│ start_date, end_date       │
│ payment_method_id (FK)     │
│ status, renewal_count      │
└────────┬───────────────────┘
         │
         ▼
┌────────────────────────────┐
│         Usage              │
├────────────────────────────┤
│ usage_id (PK)              │
│ user_id (FK)               │
│ plan_id (FK)               │
│ subscription_id (FK)       │
│ usage_date                 │
│ actions_performed          │
│ storage_used_mb            │
│ api_calls                  │
│ active_minutes             │
└────────────────────────────┘
```

### Tables

#### 📍 **regions** (Lookup Table)

| Column        | Type         | Description       |
| ------------- | ------------ | ----------------- |
| `region_id`   | Integer (PK) | Unique region ID  |
| `region_name` | String       | Geographic region |

#### 🔗 **referral** (Lookup Table)

| Column               | Type         | Description        |
| -------------------- | ------------ | ------------------ |
| `referral_source_id` | Integer (PK) | Unique referral ID |
| `source_name`        | String       | Marketing channel  |

#### 💳 **payment_methods** (Lookup Table)

| Column              | Type         | Description         |
| ------------------- | ------------ | ------------------- |
| `payment_method_id` | Integer (PK) | Unique payment ID   |
| `method_name`       | String       | Payment method type |

#### 💼 **plans** (Reference Table)

| Column           | Type         | Description               |
| ---------------- | ------------ | ------------------------- |
| `plan_id`        | Integer (PK) | Unique plan identifier    |
| `plan_name`      | String       | Plan name (Free, Pro...)  |
| `monthly_fee`    | Float        | Monthly subscription cost |
| `max_storage_mb` | Integer      | Storage quota (MB)        |
| `max_api_calls`  | Integer      | API call quota            |

#### ⭐ **features** (Lookup Table)

| Column         | Type         | Description         |
| -------------- | ------------ | ------------------- |
| `feature_id`   | Integer (PK) | Unique feature ID   |
| `plan_id`      | Integer (FK) | Reference to plan   |
| `feature_name` | String       | Feature description |

#### 👥 **users** (Transactional - SCD2)

| Column               | Type         | Description                  |
| -------------------- | ------------ | ---------------------------- |
| `user_id`            | String (PK)  | Unique user identifier       |
| `first_name`         | String       | User's first name            |
| `last_name`          | String       | User's last name             |
| `email`              | String       | User's email address         |
| `signup_date`        | Date         | Account creation date        |
| `plan_id`            | Integer (FK) | Reference to plan            |
| `region_id`          | Integer (FK) | Reference to region          |
| `referral_source_id` | Integer (FK) | Reference to referral source |

#### 📝 **subscriptions** (Transactional - SCD2)

| Column              | Type         | Description                 |
| ------------------- | ------------ | --------------------------- |
| `subscription_id`   | String (PK)  | Unique subscription ID      |
| `user_id`           | String (FK)  | Reference to user           |
| `plan_id`           | Integer (FK) | Reference to plan           |
| `start_date`        | Date         | Subscription start          |
| `end_date`          | Date         | Subscription end            |
| `payment_method_id` | Integer (FK) | Reference to payment method |
| `status`            | String       | Active/Cancelled/Expired    |
| `renewal_count`     | Integer      | Number of times renewed     |

#### 📈 **usage** (Transactional)

| Column              | Type         | Description               |
| ------------------- | ------------ | ------------------------- |
| `usage_id`          | String (PK)  | Unique usage record ID    |
| `user_id`           | String (FK)  | Reference to user         |
| `plan_id`           | Integer (FK) | Reference to plan         |
| `subscription_id`   | String (FK)  | Reference to subscription |
| `usage_date`        | Date         | Date of usage             |
| `actions_performed` | Integer      | Number of actions         |
| `storage_used_mb`   | Float        | Storage consumed (MB)     |
| `api_calls`         | Integer      | API requests made         |
| `active_minutes`    | Integer      | Time spent active         |

### DLT Metadata Columns

DLT automatically adds these columns for tracking:

| Column         | Type      | Purpose                                 |
| -------------- | --------- | --------------------------------------- |
| `_dlt_load_id` | String    | Load batch identifier                   |
| `_dlt_id`      | String    | Record hash for deduplication           |
| `valid_from`   | Timestamp | When version became active (SCD2 only)  |
| `valid_to`     | Timestamp | When version was superseded (SCD2 only) |

## 🔄 dbt Transformations

The project includes dbt models for dimensional modeling and analytics preparation.

### Model Structure

```
dbt_modelling/
├── models/
│   ├── staging/           # Staging layer (raw data cleanup)
│   │   ├── stg_users.sql
│   │   ├── stg_plans.sql
│   │   ├── stg_subscriptions.sql
│   │   └── stg_usages.sql
│   └── dimension/         # Dimensional layer
│       ├── dim_users.sql
│       ├── dim_plans.sql
│       ├── dim_subscriptions.sql
│       └── dim_usages.sql
└── dbt_project.yml
```

## 🛠️ Development

### Project Structure

```
end-to-end-elt/
│
├── fastapi/                          # API application
│   ├── main.py                       # FastAPI app & endpoints
│   ├── model/
│   │   ├── model.py                  # SQLAlchemy models
│   │   └── schema.py                 # Pydantic schemas
│   ├── config/
│   │   └── config.py                 # Database configuration
│   ├── requirements.txt              # FastAPI dependencies
│   ├── railway.json                  # Railway config
│   └── Procfile                      # Process configuration
│
├── fake data/                        # Data generation
│   ├── data_generation/              # Modular generation scripts
│   │   ├── generate_regions.py
│   │   ├── generate_referral_sources.py
│   │   ├── generate_payment_methods.py
│   │   ├── generate_plans.py
│   │   ├── generate_plan_features.py
│   │   ├── generate_users.py
│   │   ├── generate_subscriptions.py
│   │   └── generate_usage.py
│   ├── models/                       # Data models
│   └── pipeline/
│       └── etl_pipeline.py           # DLT ETL orchestration
│
├── pipeline/                         # Additional pipelines
│   ├── rest_athena_pipeline.py       # REST API to Athena
│   └── config.py                     # Pipeline configuration
│
├── dbt_modelling/                    # dbt transformations
│   ├── models/
│   │   ├── staging/                  # Staging models
│   │   │   ├── stg_users.sql
│   │   │   ├── stg_plans.sql
│   │   │   ├── stg_subscriptions.sql
│   │   │   └── stg_usages.sql
│   │   └── dimension/                # Dimensional models
│   │       ├── dim_users.sql
│   │       ├── dim_plans.sql
│   │       ├── dim_subscriptions.sql
│   │       └── dim_usages.sql
│   └── dbt_project.yml               # dbt configuration
│
├── .env                              # Environment variables (gitignored)
├── .env.example                      # Environment template
├── .gitignore                        # Git exclusions
├── pyproject.toml                    # Project metadata
├── requirements.txt                  # Root dependencies
└── README.md                         # This file
```

## 📧 Contact

**Ayush Acharya**

- Email: ayushach007@gmail.com

---
