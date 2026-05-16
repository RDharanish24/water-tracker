# 💧 AI-Powered Hydration Tracker

An intelligent, full-stack water tracking application that monitors your daily fluid intake and leverages the power of generative AI to provide real-time, context-aware hydration feedback and health advice.

Built with a decoupled architecture featuring a **FastAPI** backend, **SQLite** database, **LangChain** orchestrator, and a reactive **Streamlit** frontend interface.

---

## 🚀 Features

- **Quick & Custom Logging:** Easily log water intake in milliliters (`ml`) via the interactive UI dashboard or standard API endpoints.
- **Persistent Storage:** Local SQLite database tracks user consumption logs automatically without structural data rot.
- **Smart Progress Tracking:** Dynamic visual indicators and progress bars compute metrics against your daily hydration milestones.
- **AI Hydration Insights:** Integrates with **Gemini 3 Flash Lite** to deliver tailored health cues, behavioral tips, and physiological indicator evaluations based on actual consumption history.
- **Decoupled Architecture:** Clean separation between the engine layer (Backend API) and display layer (Frontend UI).

---

## 🛠️ Architecture & Tech Stack

- **Frontend:** Streamlit
- **Backend Framework:** FastAPI
- **LLM Orchestration:** LangChain (`langchain-google-genai`)
- **AI Model:** Google Gemini 3 Flash Lite (Free Tier compatible)
- **Database:** SQLite3
- **Language:** Python 3.10+

---

## 📂 Project Directory Structure

```text
water-tracker/
├── src/
│   ├── agent.py          # LangChain wrapper & Gemini AI configuration
│   ├── database.py       # SQLite connection layer and schema execution
│   └── logger.py         # Application level operations logging (Optional)
├── app.py                # FastAPI main application server instance
├── frontend.py           # Streamlit UI dashboard client 
├── .env                  # Environment configurations (Protected)
└── README.md             # Project documentation
```
## ⚙️ Setup and Installation
1. Prerequisites
Ensure you have Python 3.10 or higher installed on your system.

2. Clone the Repository & Navigate
Bash
cd "water tracker"
3. Initialize & Activate Virtual Environment
Bash
#### Windows
```
python -m venv venv
.\venv\Scripts\activate
```
#### Mac/Linux
```
python3 -m venv venv
source venv/bin/activate
```
4. Install Project Dependencies
Bash
pip install fastapi uvicorn streamlit langchain-google-genai pydantic python-dotenv requests pandas
5. Configure Environment Variables
Create a file named .env in the root folder of your project and insert your Google AI Studio API key:

Code snippet
```
GEMINI_API_KEY="your_actual_free_tier_gemini_api_key_here"
```
### 🏃‍♂️ Running the Application
Because this app uses a separated frontend and backend client structure, you will need two terminal windows open with your virtual environment activated in both.

Step 1: Fire up the Backend API
In your first terminal, launch the Uvicorn server:

```
uvicorn api:app --reload
```
The API engine will initialize the database schema and host the application endpoint maps at http://127.0.0.1:8000.

Step 2: Launch the Interactive Dashboard
In your second terminal, run the Streamlit client application:
```
streamlit run src/dashboard.py
```
Your web browser will automatically open to http://127.0.0.1:8501 rendering the user interface dashboard.

📡 API Documentation Preview
If you want to bypass the UI layer or interact programmatically, the backend provides access out of the box. You can test these directly inside the Interactive Swagger docs at http://127.0.0.1:8000/docs.

1. Log New Water Intake
Endpoint: POST /log-intake

Payload Structure:
```
JSON
{
  "user_id": "user_1",
  "intake_ml": 500
}

```
### 2. Fetch Aggregated User History
* **Endpoint:** `GET /history/{user_id}`