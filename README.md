# DEFECT-

> **Automated Technical Documentation & Continuous Synchronization**  
> *Synchronized by RepoMind AI & ASDSE Platform*

| Repository Version | Branch | Active Commit | Primary Language | Sync State |
| :--- | :--- | :--- | :--- | :--- |
| **V2** | `main` | [`e6d011b`](https://github.com/PadmaPriya78/DEFECT-.git/commit/e6d011b61b9642b67ff074e8a9d112122713f392) | `Python` | `✓ Grounded & Synchronized` |

> **Commit Identity**: `e6d011b` (e6d011b61b9642b67ff074e8a9d112122713f392)  
> **Author**: RepoMind ASDSE Bot | **Date**: 23/10/2026, 8:56:59 pm  
> **Message**: *docs(asdse): synchronize generated documentation*

> ℹ️ **Version Transition**: Synchronized from baseline **c928e27** → **e6d011b** with 1 changed files (+416 / -39 lines).

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Environment Variables](#environment-variables)
- [Database Management](#database-management)
- [Running the Application](#running-the-application)
- [Build & Development Scripts](#build--development-scripts)
- [Deployment & DevOps](#deployment--devops)
- [API Endpoints](#api-endpoints)
- [Authentication & Security](#authentication--security)
- [Dependencies](#dependencies)
- [Version Changelog](#version-changelog)
- [License](#license)

---

## Project Overview

**DEFECT-** is a software system built using **Python** with **FastAPI** and **React**, utilizing **PostgreSQL** for persistent storage.

This codebase provides a modular architecture designed for maintainability, with defined separation across business logic, routing, persistence, and service execution.

## Key Features

- **Modular Backend Service**: Engineered using FastAPI with structured request controllers and service boundaries.
- **Interactive User Interface**: Implemented with React.
- **Data Persistence Layer**: Grounded PostgreSQL storage managing 3 database entities with schema validation.
- **Structured HTTP API**: 6 documented RESTful endpoints with method routing and contract handlers.
- **Authentication & Access Control**: Enforces security policies via Environment-based Secrets.
- **Containerized Runtime**: Production-ready Docker containerization for portable environment parity.

## Technology Stack

| Category | Technologies Verified in Codebase |
| :--- | :--- |
| **Primary Language** | `Python` (All: `Python`, `JavaScript`, `YAML`, `HTML`, `JSON`, `React JSX`, `CSS`) |
| **Backend Framework** | `FastAPI` |
| **Frontend Framework** | `React` |
| **Database Engine** | `PostgreSQL` |
| **Authentication** | `Environment-based Secrets` |
| **Manifest Files** | `requirements.txt`, `package.json` |

## System Architecture

The repository follows a **Microservice Architecture** pattern.

### System Context Diagram

```mermaid
graph TD
    classDef userClass fill:#1E293B,stroke:#38BDF8,stroke-width:2px,color:#F8FAFC;
    classDef systemClass fill:#0F172A,stroke:#818CF8,stroke-width:2px,color:#F8FAFC;
    classDef externalClass fill:#1E293B,stroke:#94A3B8,stroke-width:2px,color:#CBD5E1;

    User["User / Client Applications"]:::userClass
    System["DEFECT- Platform"]:::systemClass
    ExtServices["External Services / Cloud APIs"]:::externalClass
    Database["Relational Database"]:::externalClass

    User -->|"Interacts via HTTP / REST"| System
    System -->|"Persists & Queries Data"| Database
    System -->|"Delegates to External Integrations"| ExtServices

```

### Container Architecture Diagram

```mermaid
graph TD
    classDef container fill:#1E293B,stroke:#60A5FA,stroke-width:2px,color:#F8FAFC;
    classDef db fill:#0F172A,stroke:#34D399,stroke-width:2px,color:#F8FAFC;

    ClientApp["Frontend Client UI<br/><i>(Client UI Layer)</i>"]:::container
    BackendApp["Application Core Service<br/><i>(Domain & Business Logic Engine)</i>"]:::container
    DatabaseContainer["Persistence Store<br/><i>(Relational Database)</i>"]:::db

    ClientApp -->|"API Calls / HTTP Requests"| BackendApp
    BackendApp -->|"Queries & Transactions"| DatabaseContainer

```

## Repository Structure

| Directory / Path | Module Purpose |
| :--- | :--- |
| `.` | Application module directory |
| `backend` | Application module directory |
| `frontend` | Application module directory |
| `backend/ml_artifacts` | Application module directory |
| `backend/model` | Database entity definitions and data models |
| `frontend/src` | Application module directory |
| `frontend/src/components` | Frontend UI components and templates |

## Prerequisites

Ensure the following tools, runtimes, and external services are configured on your host environment before setup:

### 💻 Runtime Environment & Package Managers

- **Python**: `3.11+` (Core runtime environment)
- **Node.js**: `v18.0.0 or higher` (LTS recommended)
- **Package Manager**: `pip` / `npm`
- **Git**: `v2.30+` for source version control

### 🗄️ Database & Persistence Services

- **PostgreSQL**: 14+ — *Running PostgreSQL server instance or cloud database URL*

### 🔑 External Services & API Keys

- **JSON Web Token (JWT)** (`JWT_SECRET`): Cryptographic 256-bit secret string for issuing and verifying auth session tokens

### 🐳 Container & Deployment Tooling (Optional)

- **Docker & Docker Compose**: Docker Engine v24.0+ & Compose v2.20+ for containerized runtime execution

## Installation & Setup

Follow these step-by-step instructions to set up the repository locally for development:

### 1. Clone the Repository

```bash
git clone https://github.com/PadmaPriya78/DEFECT-.git.git
cd defect-
```

### 2. Switch to Verified Branch / Commit

```bash
git checkout main
```

### 3. Configure Environment Variables

Initialize your local environment file:

```bash
# Create local .env file
touch .env
# Populate with the required variables documented in the Environment Variables section below
```

### 4. Install Dependencies

This repository contains separated modules. Install dependencies for each tier:

**Option A: Backend API Service (`backend/`)**

```bash
cd backend
pip install -r requirements.txt
cd ..
```

**Option B: Frontend Client Application (`frontend/`)**

```bash
cd frontend
npm install
cd ..
```

## Environment Variables

Create a `.env` file in the root directory based on the configuration template below (placeholders are sanitized):

### Configuration Parameters Table

| Variable Name | Required | Default / Safe Placeholder | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | **Yes** | `postgresql://defectguard:defectguard@localhost:5432/defectguard` | Configuration parameter for DATABASE_URL |
| `JWT_SECRET` | **Yes** | `your-jwt-secret-placeholder` | Configuration parameter for JWT_SECRET |
| `JWT_ALGORITHM` | **Yes** | `your-jwt-algorithm-placeholder` | Configuration parameter for JWT_ALGORITHM |
| `JWT_EXPIRE_MINUTES` | **Yes** | `your-jwt-expire-minutes-placeholder` | Configuration parameter for JWT_EXPIRE_MINUTES |
| `GOOGLE_CLIENT_ID` | Optional | `your_google_oauth_client_id` | Configuration parameter for GOOGLE_CLIENT_ID |
| `GOOGLE_CLIENT_SECRET` | **Yes** | `your-google-client-secret-placeholder` | Configuration parameter for GOOGLE_CLIENT_SECRET |
| `FRONTEND_ORIGIN` | Optional | `http://localhost:5173` | Configuration parameter for FRONTEND_ORIGIN |
| `MODEL_DIR` | Optional | `./ml_artifacts` | Configuration parameter for MODEL_DIR |
| `CLONE_DIR` | Optional | `./tmp_repos` | Configuration parameter for CLONE_DIR |
| `PORT` | Optional | `5173` | Application HTTP server listening port |
| `NODE_ENV` | Optional | `development` | Runtime environment (development | production | test) |

### Template Configuration File (`.env`)

```env
# Configuration parameter for DATABASE_URL (Required)
DATABASE_URL=postgresql://defectguard:defectguard@localhost:5432/defectguard

# Configuration parameter for JWT_SECRET (Required)
JWT_SECRET=your-jwt-secret-placeholder

# Configuration parameter for JWT_ALGORITHM (Required)
JWT_ALGORITHM=your-jwt-algorithm-placeholder

# Configuration parameter for JWT_EXPIRE_MINUTES (Required)
JWT_EXPIRE_MINUTES=your-jwt-expire-minutes-placeholder

# Configuration parameter for GOOGLE_CLIENT_ID (Optional)
GOOGLE_CLIENT_ID=your_google_oauth_client_id

# Configuration parameter for GOOGLE_CLIENT_SECRET (Required)
GOOGLE_CLIENT_SECRET=your-google-client-secret-placeholder

# Configuration parameter for FRONTEND_ORIGIN (Optional)
FRONTEND_ORIGIN=http://localhost:5173

# Configuration parameter for MODEL_DIR (Optional)
MODEL_DIR=./ml_artifacts

# Configuration parameter for CLONE_DIR (Optional)
CLONE_DIR=./tmp_repos

# Application HTTP server listening port (Optional)
PORT=5173

# Runtime environment (development | production | test) (Optional)
NODE_ENV=development

```

## Database Management

* **Database Engine**: `PostgreSQL`
* **Registered Entities / Collections**: 3

### Database Initialization & Migration Strategy

Database connections are established dynamically via `PostgreSQL`. Ensure the database service is running prior to starting the application.

### Registered Entities & Data Models

| Entity / Table Name | Purpose | Key Attributes |
| :--- | :--- | :--- |
| `User` | Entity model for User | `id, created_at` |
| `Analysis` | Entity model for Analysis | `id, created_at` |
| `ModuleResult` | Entity model for ModuleResult | `id, created_at` |

### Entity-Relationship Diagram

```mermaid
erDiagram
    USER {
        INTEGER id PK
        TEXT data
    }
    ANALYSIS {
        INTEGER id PK
        TEXT data
    }
    MODULERESULT {
        INTEGER id PK
        TEXT data
    }
    USER ||--o{ ANALYSIS : references

```

## Running the Application

### Development Mode

Launch backend and frontend tiers in separate terminal instances:

**Terminal — Backend API Service (`backend/`):**

```bash
cd backend
uvicorn main:app --reload
```

*Listening at*: `http://localhost:5000`

**Terminal — Frontend Client Application (`frontend/`):**

```bash
cd frontend
npm run dev
```

*Listening at*: `http://localhost:3000`

### Production Build & Execution

```bash
# 2. Start production server
uvicorn main:app --reload --port 5173
```

## Build & Development Scripts

| Command | Script / Execution Target | Description |
| :--- | :--- | :--- |
| `uvicorn main:app --reload --port 5173` | `uvicorn main:app --reload --port 5173` | Starts the Python server process |
| `python -m unittest discover` | `python -m unittest discover` | Executes automated Python test cases |

## Deployment & DevOps

### Docker Containerization

```bash
# Build and launch all services in detached mode
docker-compose up --build -d

# View streaming logs
docker-compose logs -f

# Stop container stack
docker-compose down
```

### Deployment Topology Diagram

```mermaid
graph TB
    classDef node fill:#1E293B,stroke:#F59E0B,stroke-width:2px,color:#F8FAFC;

    subgraph UserDevice["Client Device"]
        Browser["Modern Web Browser"]:::node
    end

    subgraph HostServer["Host Server Environment (Docker Container)"]
        Ingress["HTTP/S Ingress Gateway"]:::node
        AppServer["Application Server Runtime<br/><i>(Application Runtime)</i>"]:::node
        DBInstance["Persistence Node<br/><i>(Relational Database)</i>"]:::node
    end

    Browser -->|"HTTP / HTTPS"| Ingress
    Ingress -->|"Internal Router"| AppServer
    AppServer -->|"Query Connection"| DBInstance

```

## API Endpoints

Total Verified Endpoints: **6**

| HTTP Method | Endpoint Route | Handler / Controller | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | `GET /health` | `Public` |
| `POST` | `/auth/register` | `POST /auth/register` | `Public` |
| `POST` | `/auth/login` | `POST /auth/login` | `Public` |
| `POST` | `/analyze` | `POST /analyze` | `Public` |
| `GET` | `/analyze/{analysis_id}` | `GET /analyze/{analysis_id}` | `Public` |
| `GET` | `/analyses` | `GET /analyses` | `Public` |

### API Execution Sequence

```mermaid
sequenceDiagram
    actor Client as User / Frontend
    participant API as POST /auth/register
    participant Svc as AuthService
    participant DB as Database (User)

    Client->>API: Submit Credentials (email/username, password)
    API->>Svc: validateCredentials(payload)
    Svc->>DB: findOne({ email })
    DB-->>Svc: Return Stored User Record & Hash
    Svc->>Svc: verifyHash(password, storedHash)
    alt Credentials Valid
        Svc->>Svc: generateJwtToken(userPayload)
        Svc-->>API: { token, userProfile }
        API-->>Client: 200 OK (JWT Token + Auth Headers)
    else Credentials Invalid
        Svc-->>API: AuthenticationError
        API-->>Client: 401 Unauthorized
    end
```

## Authentication & Security

* **Authentication Mechanisms**: `Environment-based Secrets`
* **Token & Key Management**: Sensitive tokens must be stored in secure environment variables.

### Authentication Flow

```mermaid
sequenceDiagram
    actor User as User Browser / Client
    participant Server as Application Server
    participant Session as Session & Security Store

    User->>Server: HTTP Request (Method + Headers)
    Server->>Session: Validate Session State & Security Keys
    alt Valid Session / Public Route
        Session-->>Server: proceed(authorized)
        Server->>Server: dispatchToController()
        Server-->>User: 200 OK (Response Payload)
    else Invalid / Unauthenticated
        Server-->>User: 401 Unauthorized / Redirect
    end

```

## Dependencies

The system relies on **21** runtime and development dependencies defined in `requirements.txt`, `package.json`.

### Primary Packages

| Package | Version Range | Category |
| :--- | :--- | :--- |
| `react` | `^18.3.1` | `Runtime` |
| `react-dom` | `^18.3.1` | `Runtime` |
| `recharts` | `^2.12.7` | `Runtime` |
| `axios` | `^1.7.2` | `Runtime` |
| `@vitejs/plugin-react` | `^4.3.1` | `Runtime` |
| `autoprefixer` | `^10.4.19` | `Runtime` |
| `postcss` | `^8.4.38` | `Runtime` |
| `tailwindcss` | `^3.4.4` | `Runtime` |
| `vite` | `^5.3.1` | `Runtime` |
| `fastapi` | `latest` | `Runtime` |
| `uvicorn` | `latest` | `Runtime` |
| `sqlalchemy` | `latest` | `Runtime` |
| `psycopg2-binary` | `latest` | `Runtime` |
| `python-dotenv` | `latest` | `Runtime` |
| `python-jose[cryptography]` | `latest` | `Runtime` |

## Version Changelog

### Version V2 (`e6d011b`)
- **Base Version**: `c928e27`
- **Files Added** (0): None
- **Files Modified** (1): `[object Object]`
- **Files Deleted** (0): None
- **Diff Statistics**: +416 / -39 lines changed

## License

This project is licensed under the **Proprietary / Standard Repository License**.

---
*Generated automatically by [ASDSE RepoMind Intelligence](https://github.com/Spidey390/Neighbor-to-Neighbor) — Continuous Technical Documentation & GitHub Synchronization Pipeline.*
