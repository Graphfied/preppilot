# 🧠 PrepPilot AI - Exam Prep with Agentic AI & MCP

PrepPilot is an AI-powered learning assistant that takes in your syllabus and gives you everything you need to prepare for exams:

- ✅ Structured topics
- ✅ Summarized notes
- ✅ Auto-generated MCQs
- ✅ Mock exam with scoring

All built using a modular **Crew-style agent system**, powered by **Google Gemini** and structured with **Model Context Protocol (MCP)**.

---

## 🚀 How It Works

### ✅ 1. Student Login
- Student enters name and email to start session

### 📥 2. Upload Syllabus
- Upload a **PDF** or paste **syllabus text**

### 🤖 3. Run AI Agents
- Agents extract topics, summarize notes, and generate MCQs
- Results shown in real-time, structured and clean

### 🧪 4. Take Mock Exam
- 5-question random MCQ test
- Instant scoring and result breakdown

### 💾 5. Export & Save
- Results saved in `/results/`
- All test attempts and summaries stored per session

---

## 🧩 Agents Architecture

Each agent has its own logic + prompt loaded dynamically from `context_config.yaml` (MCP file):

- **SyllabusReaderAgent** → extracts chapters + topics
- **TopicSummarizerAgent** → bullet point notes
- **MCQMasterAgent** → MCQs (JSON formatted)
- **MockTesterAgent** → selects questions, scores test

---

## 🔧 MCP (Model Context Protocol)

All prompts, model configs, and behavior are defined in:

```
src/preppilot/mcp/context_config.yaml
```

You can edit it directly **OR** use our UI editor:

```bash
streamlit run web/mcp_editor.py
```

This opens a UI to:
- Select agent
- Edit prompt & model name
- Save and preview config

---

## 🖥️ Frontend: Streamlit UI

Main user-facing app:
```bash
streamlit run web/preppilot_ui.py
```

Built with Streamlit — dynamic step-by-step flow:
- Login form
- PDF/text upload
- Run agent pipeline
- See MCQs, start test
- Get feedback after submission

---

## 📁 Project Structure

```
preppilot/
├── agents/               # All AI agents (syllabus_reader, summarizer, etc)
├── mcp/                  # MCP configuration YAML
├── results/              # Saved sessions and test results
├── web/                  # Streamlit UI files
│   ├── preppilot_ui.py   # Main student flow
│   └── mcp_editor.py     # Admin MCP prompt editor
├── config_loader.py      # YAML loader for tasks/agents
├── protocol.py           # MCP protocol logic
└── context_config.yaml   # MCP prompt + model mapping
```

---

## 📦 Requirements

Install all dependencies:
```bash
pip install -r requirements.txt
```

Set up your `.env`:
```
GEMINI_API_KEY=your_gemini_key_here
MODEL=gemini-1.5-flash
```

---

## ✅ Ready to Use

### Admin Side:
```bash
streamlit run web/mcp_editor.py
```

### Student/User Side:
```bash
streamlit run web/preppilot_ui.py
```

---

Made with ❤️ by Fahad & Team

> Easily editable, fully modular — use it to power your own learning flows or educational AI products.
