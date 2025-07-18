# DSA Solver

An interactive Data Structures and Algorithms learning assistant powered by LangChain and Streamlit.

## How to Run

1. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   MODEL_NAME=gpt-3.5-turbo
   TEMPERATURE=0.7
   MAX_TOKENS=1000
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser to:** `http://localhost:8501`

## Run Tests

```bash
pytest tests/ -v
```
