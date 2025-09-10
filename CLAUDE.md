# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
This is a full-stack market analysis web application with:
- **Frontend**: React with TypeScript, Material-UI, Redux Toolkit, and Vite
- **Backend**: FastAPI (Python) with Clean Architecture pattern
- **Infrastructure**: Kubernetes (Helm charts), Terraform for AWS EKS, Docker Compose for local development
- **Database**: MySQL with Redis for caching
- **Testing**: Vitest for frontend, pytest for backend

## Development Commands

### Frontend (React/TypeScript)
```bash
cd frontend
npm run dev          # Start development server (port 3000)
npm run build        # Build for production
npm run test         # Run tests once
npm run test:watch   # Run tests in watch mode
npm run coverage     # Generate test coverage
npm run lint         # Run ESLint
npm run preview      # Preview production build
```

### Backend (FastAPI/Python)
```bash
cd backend
# Install dependencies
pip install -r requirements.txt

# Database migrations
python scripts/run_alembic.py upgrade head
python scripts/run_alembic_test.py upgrade head  # For test DB

# Initialize assets data
python scripts/initialize_assets.py
```

### Local Development with Docker
```bash
# Start all services (frontend, backend, database, redis)
docker-compose up -d

# View logs
docker-compose logs -f [service_name]

# Stop services
docker-compose down
```

### Kubernetes/Helm Deployment
```bash
cd k8s

# Deploy individual services
helm install backend ./backend
helm install frontend ./frontend
helm install mysql ./mysql
helm install redis ./redis
helm install cronjob ./cronjob

# Upgrade deployments
helm upgrade [release-name] ./[chart-directory]
```

### Terraform Infrastructure
```bash
cd terraform/composition/market-analysis-infra/ap-northeast-1/prod
terraform init
terraform plan
terraform apply
```

## Architecture

### Backend Clean Architecture
Located in `backend/src/`:
- **Domain Layer**: Core business logic (`entities/`, `value_objects/`, `repositories/`, `services/`)
- **Application Layer**: Use cases and web API (`web/api/routers/`, `background_workers/`)
- **Infrastructure Layer**: External concerns (`infrastructure/`)

Key routers:
- `asset_router`: Asset management endpoints
- `auth_router`: Authentication and authorization  
- `futures_data_router`: Financial futures data
- `trade_date_router`: Trading calendar operations
- `user_router`: User management

### Frontend Architecture
Located in `frontend/src/`:
- **Components**: Reusable UI components (`components/`)
- **Store**: Redux state management (`store/`)
- **ViewModels**: Business logic layer (`viewModels/`)
- **API**: Backend communication (`api/`)
- **Types**: TypeScript type definitions (`types/`)

### Infrastructure
- **K8s**: Helm charts for each service in `k8s/`
- **Terraform**: AWS EKS infrastructure modules in `terraform/`
- **Docker**: Multi-stage builds with development and production Dockerfiles

## Testing Strategy

### Backend Testing
Located in `backend/tests/`:
```bash
cd backend
pytest                    # Run all tests
pytest tests/unit/        # Unit tests only
pytest tests/integration/ # Integration tests only
pytest --cov             # With coverage
```

### Frontend Testing
```bash
cd frontend
npm run test              # Run all tests
npm run test:watch       # Watch mode
npm run coverage         # Coverage report
```

## Database

### Schema Management
- **Alembic**: Database migrations in `backend/alembic/`
- **Test DB**: Separate test database with `alembic_test.ini`

### Scripts
- `initialize_assets.py`: Populate initial asset data
- `run_alembic.py`: Main DB migrations
- `run_alembic_test.py`: Test DB migrations

## Development Environment

### Dev Container
- `.devcontainer/`: VS Code dev container configuration
- Custom entrypoint script for permission management

### Environment Configuration
- `.env`: Main environment variables
- `backend/backend.env`: Backend-specific config
- `frontend/frontend.env`: Frontend-specific config
- `mysql/mysql.env`: Database configuration

### Ports
- Frontend: 3000
- Backend: 8000  
- MySQL: 3306
- Redis: 6379

## Key Dependencies

### Frontend
- React 18 + TypeScript
- Material-UI for components
- Redux Toolkit for state management
- Axios for API calls
- Plotly.js for data visualization
- Vitest for testing

### Backend  
- FastAPI for REST API
- SQLAlchemy for ORM
- Alembic for migrations
- Redis for caching
- Selenium for web scraping
- pytest for testing

## Infrastructure Notes
- AWS EKS cluster managed via Terraform
- Helm charts for Kubernetes deployments
- Development uses Docker Compose
- Production deployment on Kubernetes with multiple environments support