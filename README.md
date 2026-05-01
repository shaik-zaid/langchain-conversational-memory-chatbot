# 🤖 Memory-Enabled Conversational AI Chatbot

A production-style conversational AI chatbot built using **LangChain (LCEL) + Groq**, designed to maintain conversation memory, manage long chat histories using token-aware trimming, and support multilingual interactions.

This project demonstrates how modern LLM systems go beyond simple prompting by incorporating **state (memory), control (token management), and structured pipelines (LCEL)**.

---

## 🚀 Features

### 🧠 Conversational Memory
- Maintains full conversation history per session
- Recalls user-provided information accurately
- Enables context-aware follow-up responses

---

### ✂️ Token-Aware Message Trimming
- Automatically trims older messages when token limits are reached
- Prevents context overflow in long conversations
- Uses `trim_messages` from LangChain

---

### 🌍 Multilingual Support
- Dynamic language switching from UI
- Supports:
  - English
  - Hindi
  - Spanish
  - French

---

### 🔄 Session-Based Chat System
- Multiple independent chat sessions
- Switch between sessions dynamically
- Each session maintains its own memory

---

### 🎛️ Interactive UI (Streamlit)
- Clean chat interface
- Token limit slider
- Toggle trimming ON/OFF
- Real-time conversation display
- Session management panel

---

### ⚡ Error Handling
- Graceful error handling for API issues
- Prevents app crashes during runtime

---

## 🧠 Tech Stack

| Component | Technology |
|----------|-----------|
| LLM | Groq (LLaMA / Gemma models) |
| Framework | LangChain (LCEL) |
| UI | Streamlit |
| Language | Python |

---

## 🧱 System Architecture

```
User Input
   ↓
Session Memory (ChatMessageHistory)
   ↓
Message Trimmer (Token Control)
   ↓
Prompt Template (System + Messages)
   ↓
LLM (Groq)
   ↓
Response
```

---

## 📁 Project Structure

```
├── app/
│   └── app.py                         # Main Streamlit application
├── notebooks/
│   └── conversational-memory-chatbot.ipynb  # Learning + experiments
├── .env                               # API keys (not committed)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Setup Instructions

```bash
# 1. Clone the repository
git clone https://github.com/shaik-zaid/langchain-conversational-memory-chatbot
cd langchain-conversational-memory-chatbot

# 2. Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (Linux / Mac)
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add environment variable
# Create a .env file in root and add:
GROQ_API_KEY=your_api_key_here

# 5. Run the application
streamlit run app/app.py
```

---

## 💬 Example Conversations

### 🧠 Memory Demonstration

```
You: My name is Zaid and I am an AI engineer  
Bot: Nice to meet you, Zaid!

You: What is my name?  
Bot: Your name is Zaid.

You: What do I do?  
Bot: You are an AI engineer.
```

---

### 🌍 Multilingual Example

```
(Language switched to Hindi)

You: What did I tell you about myself?  
Bot: आपने बताया कि आपका नाम Zaid है और आप एक AI engineer हैं।
```

---

### 🧠 Context Awareness

```
You: I am learning machine learning  
Bot: That's great!

You: What should I learn next?  
Bot: Since you're learning machine learning, you can explore deep learning or NLP.
```

---

## 🧪 Key Concepts Demonstrated

- **RunnableWithMessageHistory** → session-based memory  
- **trim_messages** → token-aware context management  
- **LCEL (LangChain Expression Language)** → structured pipelines  
- **Prompt engineering with dynamic variables**  
- **Stateful AI system design**  

---

---

## 🚀 Future Improvements

- 🔍 Add Retrieval-Augmented Generation (RAG)
- 💾 Persistent memory using database (Redis / MongoDB)
- ⚡ Streaming responses
- 🌐 Deploy on Streamlit Cloud / Render
- 📊 Add analytics & usage tracking

---

## 📌 Author

**Shaik Zaid**

---

## ⭐ Support

If you found this project useful:

- ⭐ Star the repository  
- 🔗 Share it on LinkedIn  
- 💬 Give feedback  

---

## 🧠 Final Thought

> A good chatbot doesn’t just answer —  
> it remembers, adapts, and responds with context.