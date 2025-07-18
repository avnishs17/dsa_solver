# DSA Solver

An intelligent Data Structures and Algorithms learning assistant powered by **LangChain**, **LangGraph**, and **Streamlit**. This Socratic mentor guides students through problem-solving using AI-powered tools for code analysis, hints, and interactive learning.

## ✨ Features

- 🤖 **Socratic AI Mentor**: Guides learning through questions and hints rather than direct solutions
- 🔧 **Intelligent Tools**: Automatic code execution, complexity analysis, test case generation, and hint system
- 📊 **Real-time Analysis**: Instant time/space complexity analysis with visual formatting
- 💡 **Smart Hints**: Context-aware hints that don't spoil the solution
- 🧪 **Auto Test Cases**: Automatically generates and runs comprehensive test cases
- 📝 **Code Templates**: Built-in templates for common DSA patterns (Two Sum, Binary Search, DFS, BFS, DP)
- 🎯 **Interactive UI**: Clean, modern Streamlit interface with syntax highlighting
- 🔍 **Bug Detection**: Analyzes code for logical issues and provides subtle guidance

## 🛠️ Tech Stack

- **LangChain** + **LangGraph**: AI workflow orchestration
- **Google Gemini 2.5 Flash**: LLM for intelligent responses
- **Streamlit**: Interactive web interface
- **LangSmith**: Tracing and observability
- **Python**: Core execution environment

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
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── .env                  # Environment configuration
├── config/               # Application settings
├── models/               # LLM integration
├── graph/                # LangGraph workflow
├── tools/                # AI tools (hints, analysis, etc.)
├── ui/                   # Streamlit UI components
├── notebook/             # Development notebooks
└── tests/                # Test suite
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
- Check the troubleshooting section in the docs
- Review the example notebooks in `/notebook/`
