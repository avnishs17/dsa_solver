# DSA Mentor

AI-powered DSA mentoring assistant with Flask frontend and FastAPI backend.

## Setup

### Backend
```bash
# Install uv package manager
pip install uv

# Create virtual environment
uv venv -p python3.11

# Activate virtual environment
.venv/Scripts/activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install backend dependencies
uv pip install -r requirements.txt

# Copy .env.example to .env and add your API keys
# Start backend server
python -m app.main
```

### Frontend
```bash
streamlit run streamlit_app.py
```

## Usage

1. Backend runs on http://localhost:8000
2. Frontend runs on http://localhost:8501