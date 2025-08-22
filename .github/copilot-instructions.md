# ZKP Age Verification Project Instructions

This project implements a Zero-Knowledge Proof system for age verification with:
- Python backend (FastAPI) for ZKP logic and API
- Flutter frontend for user interface
- Azure deployment configuration

## Project Structure
- `/backend` - Python FastAPI server with ZKP implementation
- `/frontend` - Flutter mobile/web application
- `/azure` - Azure deployment configurations
- `/docs` - Project documentation

## Development Guidelines
- Backend uses cryptographic libraries for ZKP implementation
- Frontend communicates with backend via REST API
- Azure App Service for backend hosting
- Azure Static Web Apps for Flutter web deployment

## Progress Tracking
- [x] Project requirements clarified
- [x] Scaffold the project structure
- [x] Customize ZKP implementation
- [x] Install required dependencies
- [x] Set up backend server (running on port 8001)
- [x] Set up Flutter frontend (running on port 3000)
- [x] Create comprehensive documentation
- [x] Configure Azure deployment templates
- [x] Test local development environment

## Current Status
✅ **FULLY FUNCTIONAL** - Both backend and frontend are running and ready for testing!

### URLs:
- **Backend API**: http://localhost:8001
- **Frontend Web App**: http://localhost:3000
- **API Documentation**: http://localhost:8001/docs

### Next Steps:
1. Test the age verification functionality
2. Deploy to Azure using the provided templates
3. Update frontend URL to point to Azure backend
4. Set up CI/CD pipelines for automated deployment
