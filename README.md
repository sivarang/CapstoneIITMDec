📡 NetAssist
Overview
NetAssist is an AI-powered router troubleshooting assistant that helps users diagnose and resolve common WiFi and router issues through an interactive conversational interface.
The application combines LangGraph, FastAPI, Retrieval-Augmented Generation (RAG), and Pinecone Vector Database to provide troubleshooting guidance based on router manuals before escalating unresolved issues to Tier-2 support.
________________________________________
Features
•	🤖 AI-powered conversational troubleshooting
•	📚 RAG-based retrieval from router manuals
•	🌲 LangGraph multi-agent workflow
•	🔍 Automatic router model identification
•	📖 Router manual semantic search using Pinecone
•	💬 Streamlit chat interface
•	📝 Automatic escalation summary generation
•	💾 Session-based conversations
•	📊 LangSmith tracing support
________________________________________
Supported Routers
•	TP-Link Archer C5
•	Netgear D7000
Additional router manuals can be added by ingesting new documentation into Pinecone.
________________________________________
System Architecture
                    Streamlit UI
                          │
                          ▼
                    FastAPI Backend
                          │
                    LangGraph Workflow
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
  Supervisor         RAG Agent      Troubleshooter
        │                 │
        │                 ▼
        │          Pinecone Vector DB
        │                 │
        └────────────► OpenAI GPT-4.1
                          │
                          ▼
                  Escalation Agent
________________________________________
Project Structure
router-support-agent/
│
├── app/
│   ├── agents/
│   │   ├── supervisor.py
│   │   ├── rag_agent.py
│   │   ├── troubleshooter.py
│   │   └── escalation.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── graph/
│   │   ├── workflow.py
│   │   └── state.py
│   │
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── retriever.py
│   │   └── vectorstore.py
│   │
│   ├── prompts/
│   └── utils/
│
├── data/
│   └── manuals/
│
├── streamlit_app.py
├── run.py
├── requirements.txt
└── README.md
________________________________________
LangGraph Workflow
START
  │
  ▼
Supervisor
  │
  ├────────► ASK
  │
  ├────────► Detect Router
  │
  ▼
RAG Agent
  │
  ▼
Troubleshooter
  │
  ├────────► Continue Troubleshooting
  │
  ├────────► Issue Resolved
  │
  ▼
Escalation Agent
  │
  ▼
END
________________________________________
Technology Stack
Component	Technology
Frontend	Streamlit
Backend	FastAPI
Agent Framework	LangGraph
LLM	OpenAI GPT-4.1
Embeddings	OpenAI Embeddings
Vector Database	Pinecone
Prompt Framework	LangChain
Tracing	LangSmith
________________________________________
Installation
Clone the Repository
git clone <repository-url>

cd router-support-agent
________________________________________
Install Dependencies
pip install -r requirements.txt
________________________________________
Configure Environment Variables
Create a .env file.
OPENAI_API_KEY=your_openai_key

PINECONE_API_KEY=your_pinecone_key

PINECONE_INDEX_NAME=router-support

LANGSMITH_API_KEY=your_langsmith_key

LANGSMITH_PROJECT=router-support

LANGSMITH_TRACING=true
________________________________________
Ingest Router Manuals
Place router manuals inside:
data/manuals/
Run:
python -m app.rag.ingest
This process:
•	Loads router manuals
•	Splits documents into chunks
•	Generates embeddings
•	Uploads vectors into Pinecone
________________________________________
Running the Backend
python run.py
FastAPI will start at:
http://127.0.0.1:8000
________________________________________
Running the Frontend
In a separate terminal:
streamlit run streamlit_app.py
The Streamlit interface will open automatically in your browser.
________________________________________
Conversation Flow
1.	User opens NetAssist.
2.	Welcome message is displayed.
3.	User describes the issue.
4.	Router model is identified.
5.	Relevant manual sections are retrieved from Pinecone.
6.	The troubleshooter asks guided diagnostic questions.
7.	If the issue is resolved, the conversation ends.
8.	Otherwise, an escalation summary is generated for Tier-2 support.
________________________________________
Example Conversation
🤖 Welcome to NetAssist.

👤 WiFi is down

🤖 Which router are you using?

👤 TP-Link Archer C5

🤖 Is the Wireless LED lit?

👤 Yes

🤖 Can you see your WiFi network name?

👤 No

🤖 Please check whether the Wireless button is enabled.
________________________________________
Future Enhancements
•	Support additional router models
•	Image-based LED diagnostics
•	Firmware version detection
•	Automatic router configuration validation
•	Streaming responses
•	User authentication
•	Chat transcript export
•	Multi-language support
________________________________________
License
This project was developed as part of an Agentic AI Capstone Project for educational purposes.
