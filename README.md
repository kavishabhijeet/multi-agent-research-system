# 🔬 ResearchMind AI — Multi-Agent Research System

A fully autonomous multi-agent research pipeline built with LangChain, powered by Mistral AI (or Groq/Gemini), and wrapped in a sleek Streamlit UI. Give it any topic and it will search the web, scrape sources, write a structured report, and critique its own output — end to end.

---

## 🚀 Demo

> Enter a topic → 4 agents work in sequence → get a publication-ready research report with critic feedback.

![Pipeline Flow](https://via.placeholder.com/900x200/0a0a0f/9b78e8?text=Search+→+Read+→+Write+→+Critique)

---

## 🧠 How It Works

The system runs four agents/chains in a sequential pipeline:

```
User Topic
    │
    ▼
┌─────────────────────────────────────────────────────┐
│  Agent 1 — Search Agent                             │
│  Uses Tavily to find top 3 web results              │
│  Returns: titles, URLs, snippets                    │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Agent 2 — Reader Agent                             │
│  Picks the most relevant URL and scrapes it         │
│  Returns: clean extracted text content              │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Chain 3 — Writer Chain                             │
│  Combines search + scraped data                     │
│  Writes structured report (Intro, Findings,         │
│  Conclusion, Sources)                               │
└────────────────────┬────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────┐
│  Chain 4 — Critic Chain                             │
│  Reviews the report and scores it X/10              │
│  Returns: strengths, areas to improve, verdict      │
└─────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Multi_Agent_Project/
│
├── app.py           # Streamlit UI — presentation layer only
├── pipeline.py      # Main pipeline orchestrator — runs all 4 agents in sequence
├── agents.py        # Agent & chain definitions (Search, Reader, Writer, Critic)
├── tools.py         # LangChain tools (web_search via Tavily, scrap_url via BeautifulSoup)
├── .env             # API keys (never commit this!)
├── .gitignore       # Excludes venv, .env, __pycache__
├── requirements.txt # Python dependencies
└── README.md        # You are here
```

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Mistral AI (`mistral-small-latest`) / Groq / Gemini |
| Agent Framework | LangChain (`create_react_agent` + `AgentExecutor`) |
| Web Search | Tavily API |
| Web Scraping | BeautifulSoup4 + Requests |
| UI | Streamlit |
| Env Management | python-dotenv |

---

## 🛠️ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/Multi_Agent_Project.git
cd Multi_Agent_Project
```

### 2. Create and activate a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API keys

Create a `.env` file in the project root:

```env
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxxxxxxxxxx
MISTRAL_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxx
```

> **Where to get API keys:**
> - Tavily: [https://app.tavily.com](https://app.tavily.com) — free tier available
> - Mistral: [https://console.mistral.ai](https://console.mistral.ai) — free tier available

---

## ▶️ Running the App

### Streamlit UI (recommended)

```bash
streamlit run app.py
```

Then open your browser at `http://localhost:8501`

### Terminal / CLI

```bash
python pipeline.py
```

---

## 🔑 API Keys Reference

| Key | Service | Get it at |
|---|---|---|
| `TAVILY_API_KEY` | Web search | [app.tavily.com](https://app.tavily.com) |
| `MISTRAL_API_KEY` | LLM | [console.mistral.ai](https://console.mistral.ai) |
| `GROQ_API_KEY` | LLM (alternative) | [console.groq.com](https://console.groq.com) |
| `GOOGLE_API_KEY` | LLM (alternative) | [aistudio.google.com](https://aistudio.google.com) |

---

## 🔄 Switching LLM Providers

If Mistral is unavailable (503 errors), swap the `llm` in `agents.py`:

**Groq (free, fast):**
```python
from langchain_groq import ChatGroq
llm = ChatGroq(model_name="llama-3.1-8b-instant", temperature=0.2, max_retries=3)
```

**Google Gemini (free tier):**
```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
```

---

## 📦 Requirements

Create a `requirements.txt` with:

```
langchain
langchain-mistralai
langchain-community
langchain-core
tavily-python
beautifulsoup4
requests
streamlit
python-dotenv
```

Install all at once:
```bash
pip install -r requirements.txt
```

---

## 🖥️ UI Features

- **4-step pipeline indicator** — shows which agent is currently active
- **3-tab results view:**
  - 📋 Full Report — structured report with download button
  - 🔍 Raw Research — search results + scraped content side by side
  - 🔎 Critic Feedback — score badge + detailed analysis
- **Download report** as `.txt`
- **Error handling** — shows clean error messages in UI
- **Run again** button for new topics

---

## ⚠️ Common Issues

| Error | Cause | Fix |
|---|---|---|
| `TAVILY_API_KEY not found` | `.env` not loading in Streamlit | Use `os.path.dirname(__file__)` in `load_dotenv()` |
| `503 Service Unavailable` | Mistral server down | Switch to Groq or Gemini temporarily |
| `create_react_agent() got unexpected keyword 'model'` | Wrong import (LangGraph vs LangChain) | Use `from langchain.agents import create_react_agent` with `llm=` param |
| `ModuleNotFoundError: streamlit` | Wrong Python environment | Activate venv, then `pip install streamlit` |
| Streamlit underline on `import streamlit` in VS Code | VS Code using wrong interpreter | Press `Ctrl+Shift+P` → Python: Select Interpreter → choose venv |

---

## 🔒 .gitignore

Make sure your `.gitignore` includes:

```
venv/
.env
__pycache__/
*.pyc
.DS_Store
```

**Never commit your `.env` file** — it contains secret API keys.

---

## 🗺️ Roadmap

- [ ] Add memory so agents can reference past research sessions
- [ ] Support PDF export of final report
- [ ] Add source citation links in report
- [ ] Allow user to pick number of search results
- [ ] Add streaming output so report appears word by word

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

## 👤 Author

**Abhijeet**
- GitHub: [@kavishabhijeet](https://github.com/kavishabhijeet)

---

> Built with ❤️ using LangChain + Mistral AI + Streamlit