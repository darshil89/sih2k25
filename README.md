# UFDR AI Assistant

A comprehensive AI-powered chat interface for UFDR (Unified Flight Data Recorder) reports with intelligent analysis capabilities.

## 📋 Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Git

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd sih2k25
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Start Database Services
```bash
docker-compose up -d
```

This will start:
- **Neo4j** (Graph Database) on port 7474 (Web UI) and 7687 (Bolt)
- **ChromaDB** (Vector Database) on port 8000

## 🚀 Running the Application

### Option 1: Run Everything Separately

#### 1. Start the Backend API Server
```bash
python main.py
```
The FastAPI server will be available at: `http://localhost:8080`

#### 2. Start the Frontend (Streamlit)
```bash
streamlit run app.py
```
The Streamlit app will be available at: `http://localhost:8501`

### Option 2: Run with Docker (Recommended for Production)

Create a `Dockerfile` for the application:
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080 8501

CMD ["sh", "-c", "python main.py & streamlit run app.py --server.port=8501 --server.address=0.0.0.0"]
```

## 🗄️ Database Configuration

### Neo4j Database
- **Web Interface**: http://localhost:7474
- **Username**: neo4j
- **Password**: password
- **Bolt Connection**: bolt://localhost:7687

### ChromaDB
- **API Endpoint**: http://localhost:8000
- **Data Persistence**: `./chroma_data` directory

## 📁 Project Structure

```
sih2k25/
├── app.py                 # Streamlit frontend application
├── main.py               # FastAPI backend server
├── requirements.txt      # Python dependencies
├── docker-compose.yml    # Database services
├── app/
│   └── types/
│       └── response.py   # Pydantic models
├── reports/              # Uploaded UFDR reports (created automatically)
├── chroma_data/          # ChromaDB data (created by Docker)
└── data/                 # Neo4j data (created by Docker)
```

## 🔧 API Endpoints

### Backend API (FastAPI)
- `GET /` - Health check
- `POST /api/chat/{report_id}` - Chat with UFDR reports

### Example API Usage
```bash
curl -X POST "http://localhost:8080/api/chat/my-report" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Analyze this flight data",
    "report_id": "my-report",
    "image_data": null
  }'
```

## 🎯 Usage Guide

### 1. Upload Reports
1. Open the Streamlit app at `http://localhost:8501`
2. Go to the "📁 Upload Reports" tab
3. Enter a Report ID
4. Upload your UFDR report files
5. Click "Upload" to save the files

### 2. Chat with Reports
1. Go to the "💬 Chat Interface" tab
2. Enter the Report ID you want to chat with
3. Type your message in the chat input
4. Optionally upload an image for visual analysis
5. Send your message to get AI-powered responses

## 🐳 Docker Services

### Start All Services
```bash
docker-compose up -d
```

### Stop All Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

### Reset Databases
```bash
docker-compose down -v
docker-compose up -d
```

## 🔍 Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Ensure ports 8080, 8501, 7474, 7687, and 8000 are available
   - Check if other services are using these ports

2. **Database Connection Issues**
   - Verify Docker is running
   - Check if containers are healthy: `docker-compose ps`
   - Restart services: `docker-compose restart`

3. **Backend Connection Error**
   - Ensure the FastAPI server is running on port 8080
   - Check the backend status in the Streamlit app footer

4. **File Upload Issues**
   - Ensure the `reports/` directory has write permissions
   - Check available disk space

### Health Checks

- **Backend**: http://localhost:8080/
- **Frontend**: http://localhost:8501
- **Neo4j**: http://localhost:7474
- **ChromaDB**: http://localhost:8000

## 🚀 Development

### Development Mode
```bash
# Terminal 1: Start databases
docker-compose up -d

# Terminal 2: Start backend with auto-reload
python main.py

# Terminal 3: Start frontend with auto-reload
streamlit run app.py
```

### Adding New Features
1. Update the FastAPI backend in `main.py`
2. Modify the Streamlit frontend in `app.py`
3. Update API models in `app/types/response.py`
4. Test with the development setup

## 📝 Environment Variables

Create a `.env` file for configuration:
```env
# Backend
BACKEND_PORT=8080
BACKEND_HOST=localhost

# Frontend
FRONTEND_PORT=8501
FRONTEND_HOST=localhost

# Neo4j
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password

# ChromaDB
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the logs: `docker-compose logs`
3. Create an issue in the repository

---

**Happy analyzing! 🚀**
