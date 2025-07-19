# DSA Solver

An intelligent Data Structures and Algorithms learning assistant powered by **LangChain**, **LangGraph**, and **Streamlit**. This Socratic mentor guides students through problem-solving using AI-powered tools for code analysis, hints, and interactive learning.

## ✨ Features

- 🤖 **Socratic AI Mentor**: Guides learning through questions and hints rather than direct solutions
- 🔧 **Intelligent Tools**: Automatic code execution, complexity analysis, test case generation, and hint system
- 📊 **Real-time Analysis**: Instant time/space complexity analysis with visual formatting
- 💡 **Smart Hints**: Context-aware hints that don't spoil the solution
- 🧪 **Auto Test Cases**: Automatically generates and runs comprehensive test cases
- 📝 **Code Templates**: Built-in templates for common DSA patterns (Two Sum, Binary Search, DFS, BFS, DP)
- 🎯 **Interactive UI**: Clean, modern Streamlit interface with dual-pane layout (code editor + chat)
- 🔍 **Bug Detection**: Analyzes code for logical issues and provides subtle guidance
- ☁️ **Cloud Ready**: Docker containerization with Kubernetes deployment configuration
- 🚀 **CI/CD Pipeline**: Automated deployment to Google Cloud via GitHub Actions

## 🛠️ Tech Stack

**Core Application:**

- **LangChain** + **LangGraph**: AI workflow orchestration
- **Google Gemini 2.5 Flash**: LLM for intelligent responses
- **Streamlit**: Interactive web interface with dual-pane layout
- **LangSmith**: Tracing and observability
- **Python**: Core execution environment

**Infrastructure & Deployment:**

- **Docker**: Application containerization
- **Kubernetes**: Container orchestration
- **Google Cloud Platform**: Cloud infrastructure
- **GCP Artifact Registry**: Container image storage
- **Google Kubernetes Engine**: Managed Kubernetes
- **GitHub Actions**: CI/CD pipeline automation

## 🚀 Quick Start

### 1. **Clone and Setup Environment**

```bash
git clone https://github.com/avnishs17/dsa_solver.git
cd dsa_solver
python -m venv .venv
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # macOS/Linux
```

### 2. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 3. **Configure Environment Variables**

Create a `.env` file in the root directory:

```env
# Required: Google API Key for Gemini
GOOGLE_API_KEY=your_google_api_key_here

# Optional: LangSmith for tracing (recommended)
LANGSMITH_API_KEY=your_langsmith_api_key_here
LANGSMITH_TRACING=true

# Application Configuration
MODEL_NAME=gemini-2.5-flash
APP_TITLE=DSA Solver
```

### 4. **Run the Application**

```bash
streamlit run app.py
```

### 5. **Open in Browser**

Navigate to: `http://localhost:8501`

## 🚀 Deployment

The application features automated cloud deployment via GitHub Actions to Google Kubernetes Engine.

### Prerequisites

- Google Cloud Platform account with billing enabled
- GitHub repository with this code
- GKE cluster named `dsa-helper` in `us-central1` region
- Google Artifact Registry repository named `dsa-solver` in `us-central1` region

### GCP Setup (Web Interface)

#### 1. Create GKE Cluster

**Go to GKE Console:**

- Visit: <https://console.cloud.google.com/kubernetes/list>
- Select your project

**Create Cluster:**

- Click "CREATE" button
- Choose "GKE Standard"

**Configure Cluster:**

- Name: `dsa-helper`
- Location type: Zonal
- Zone: `us-central1-a` (or any zone in us-central1)

**Networking:**

- Enable DNS option
- Create the cluster (takes 5-10 minutes)

#### 2. Create Artifact Registry Repository

**Go to Artifact Registry Console:**

- Visit: <https://console.cloud.google.com/artifacts>
- Select your project

**Create Repository:**

- Click "CREATE REPOSITORY"
- Name: `dsa-solver`
- Format: Docker
- Mode: Standard
- Region: `us-central1`
- Description: DSA Solver Docker images
- Click "CREATE"

#### 3. Create Service Account for GitHub Actions

**Go to IAM & Admin Console:**

- Visit: <https://console.cloud.google.com/iam-admin/serviceaccounts>
- Select your project

**Create Service Account:**

- Click "CREATE SERVICE ACCOUNT"
- Service account name: `github-actions-sa`
- Display name: GitHub Actions SA
- Description: Service account for GitHub Actions
- Click "CREATE AND CONTINUE"

**Grant Roles (add these roles one by one):**

- Kubernetes Engine Developer
- Artifact Registry Writer
- Kubernetes Engine Cluster Admin
- Artifact Registry Administrator
- Click "CONTINUE" then "DONE"

**Create Key:**

- In the service accounts list, click on `github-actions-sa`
- Go to "KEYS" tab
- Click "ADD KEY" → "Create new key"
- Choose JSON format
- Click "CREATE" (downloads the JSON file)
- Save this JSON file content as `GCP_SA_KEY` GitHub secret

### GitHub Secrets Configuration

#### Finding Your Project ID

- Go to GCP Console Dashboard
- Your Project ID is shown in the project selector dropdown (top navigation)

#### Adding Secrets to GitHub

1. Go to your GitHub repository
2. Click Settings → Secrets and variables → Actions
3. Click "New repository secret" for each secret below:

| Secret Name | Description | How to Get Value |
|-------------|-------------|------------------|
| `GCP_PROJECT_ID` | Your Google Cloud Project ID | From GCP Console dashboard |
| `GCP_SA_KEY` | Service Account JSON Key | Copy entire contents of downloaded JSON file |
| `GOOGLE_API_KEY` | Gemini API key | From [Google AI Studio](https://aistudio.google.com/app/apikey) |
| `LANGSMITH_API_KEY` | LangSmith tracing key (optional) | From [LangSmith](https://smith.langchain.com) |

### Automated CI/CD Pipeline

Push to the main branch triggers the complete deployment workflow:

1. **Build**: Creates Docker image from the Dockerfile
2. **Push**: Uploads image to GCP Artifact Registry
3. **Deploy**: Updates Kubernetes deployment on Google Kubernetes Engine
4. **Verify**: Runs health check validation

### Cloud Infrastructure

The Kubernetes deployment includes:

- **Namespace**: Isolated environment for the application
- **ConfigMap**: Non-sensitive configuration values
- **Secret**: API keys and sensitive data (managed via GitHub secrets)
- **Deployment**: Application pods with health checks and resource limits
- **Service**: Internal cluster communication
- **Ingress**: External access with SSL termination

### Required GitHub Secrets

Configure these in your repository settings:

- `GCP_PROJECT_ID`: Your Google Cloud project ID
- `GCP_SA_KEY`: Service account key (JSON format)
- `GOOGLE_API_KEY`: Gemini API key
- `LANGSMITH_API_KEY`: LangSmith tracing key (optional)

## 📋 How to Use

1. **Start a Conversation**: Ask about any DSA problem or paste your code
2. **Get Intelligent Guidance**: The AI mentor will ask probing questions and provide hints
3. **Automatic Analysis**: Code is automatically executed with test cases and complexity analysis
4. **Learn Iteratively**: Work through problems step-by-step with AI guidance

### Example Interactions

- *"Help me solve the Two Sum problem"*
- *"Analyze this binary search implementation"*
- *"I'm stuck on dynamic programming"*
- *Paste any algorithm code for instant analysis*

## 🧰 Available Tools

The AI mentor has access to several specialized tools:

- **🐍 Code Executor**: Runs Python code with comprehensive test cases
- **💡 Hint Generator**: Provides context-aware hints without spoiling solutions  
- **🧪 Test Case Generator**: Creates edge cases and examples automatically
- **📊 Complexity Analyzer**: Analyzes time/space complexity with detailed explanations
- **🔍 Bug Detector**: Identifies logical issues and suggests improvements

## 🎯 Key Features

### Socratic Learning Approach

- Never gives direct solutions - guides through questions
- Encourages critical thinking and problem-solving skills
- Adapts to student's understanding level

### Smart Code Analysis

- Automatically detects missing test cases and adds them
- Provides detailed complexity analysis with visual formatting
- Identifies edge cases and potential optimizations

### Interactive Templates

Choose from built-in algorithm templates:

- Two Sum (Hash Map approach)
- Binary Search variations
- Depth-First Search (DFS)
- Breadth-First Search (BFS)  
- Dynamic Programming patterns

## 🧪 Running Tests

```bash
pytest tests/ -v
```

## 📁 Project Structure

```text
dsa_solver/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Container image definition
├── kubernetes-deployment.yaml # Kubernetes deployment manifests
├── .env                      # Environment configuration (local)
├── .github/
│   └── workflows/
│       └── deploy.yaml       # GitHub Actions CI/CD pipeline
├── config/                   # Application settings
│   ├── __init__.py
│   └── settings.py
├── models/                   # LLM integration
│   ├── __init__.py
│   └── llm.py
├── graph/                    # LangGraph workflow
│   ├── __init__.py
│   └── graph_builder.py
├── tools/                    # AI tools (hints, analysis, etc.)
│   ├── __init__.py
│   ├── complexity_analyzer.py
│   ├── hint_tool.py
│   ├── persistent_python_repl.py
│   ├── test_case_tool.py
│   └── tools_registry.py
├── ui/                       # Streamlit UI components
│   ├── __init__.py
│   ├── chat_display.py
│   ├── chat_input.py
│   ├── code_editor.py
│   └── sidebar.py
├── notebook/                 # Development notebooks
│   ├── clean.ipynb
│   └── code.ipynb
└── tests/                    # Test suite
```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY`: **Required** - Your Google API key for Gemini
- `LANGSMITH_API_KEY`: Optional - For conversation tracing
- `LANGSMITH_TRACING`: Set to `true` to enable tracing
- `MODEL_NAME`: LLM model (default: `gemini-2.5-flash`)
- `APP_TITLE`: Application title (default: `DSA Solver`)

### API Keys Setup

1. **Google API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
2. **LangSmith** (Optional): Sign up at [LangSmith](https://smith.langchain.com)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙋‍♂️ Support

If you encounter any issues or have questions:

- Open an issue on GitHub
- Review the example notebooks in `/notebook/`
