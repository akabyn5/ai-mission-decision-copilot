

### 🚀 **AI Mission Decision Copilot**

**An AI-powered mission control assistant** that analyzes spacecraft telemetry and generates structured, explainable decisions in real time using **Google Gemini**.

---

### 📌 **Overview**

The **AI Mission Decision Copilot** is a lightweight decision-support system designed to simulate real-time mission control operations.

It takes structured telemetry data as input and produces:

- 🔍 **Anomaly classification**
- ⚠️ **Severity level**
- 🛠 **Recommended action**
- 🧠 **Reasoning**

The system prioritizes:
- Clarity over complexity
- Deterministic outputs
- Fast and reliable demo execution

---

### 🧠 **How It Works**

1. The user selects a predefined scenario in the frontend  
2. The frontend sends telemetry data to the backend (`/analyze`)  
3. The backend:
   - Validates the input
   - Sends the prompt + telemetry to the Gemini API
   - Extracts a structured JSON response
4. The UI displays the results clearly for quick evaluation

---

### 🏗 **System Architecture**

```
Frontend (HTML + JS)
        ↓
Flask Backend (/analyze)
        ↓
Gemini API (AI reasoning)
        ↓
Structured JSON response
        ↓
UI Rendering
```

---

### 📁 **Repository Structure**

```
AI-MISSION-DECISION-COPILOT/
├── backend/
│   ├── venv/
│   ├── .env
│   └── app.py
├── docs/
│   ├── input_schema.json
│   ├── output_schema.json
│   └── prompt.txt
├── frontend/
│   ├── index.html
│   └── script.js
├── .gitignore
└── README.md
```

---

### ⚙️ **Setup Instructions**

1. Clone the repository

```bash
git clone https://github.com/akabyn5/ai-mission-decision-copilot.git
cd ai-mission-decision-copilot/backend
```

2. Create and activate the virtual environment

```bash
python -m venv venv
venv\Scripts\activate     # Windows
```

3. Install dependencies

```bash
pip install flask python-dotenv google-genai flask-cors
```

4. Configure environment variables  
Create a `.env` file inside `/backend`:

```env
GEMINI_API_KEY=your_api_key_here
```

5. Run the backend server

```bash
python app.py
```

The server will run at: `http://127.0.0.1:5000`

6. Open the frontend  
Open in your browser: `http://127.0.0.1:5000`

---

### 🎮 **Demo Flow**

1. Select a scenario:
   - 🌡 Thermal Anomaly
   - 🔋 Energy Anomaly
   - 📡 Communication Loss

2. Click **Analyze**

3. View the AI-generated output:
   - Classification
   - Severity
   - Recommended Action
   - Reasoning

---

### 📊 **Input Schema**

```json
{
  "subsystem": "thermal",
  "metric": "temperature_core",
  "value": 85,
  "mission_phase": "nominal",
  "timestamp": "2026-04-17T12:30:00Z"
}
```

### 📤 **Output Schema**

```json
{
  "classification": "thermal degradation",
  "severity": "high",
  "recommended_action": "reduce load and activate cooling",
  "reasoning": "Temperature exceeds nominal threshold while efficiency is decreasing"
}
```

---

### 🤖 **AI Integration (Gemini)**

- **Model:** `gemini-2.5-flash`
- Strict prompt engineering ensures:
  - JSON-only responses
  - No extra text
  - Consistent structure

---

### 🛡 **Reliability Features**

- Input validation
- Secure JSON extraction
- Schema validation
- Fallback response if AI fails
- UI error handling
- CORS enabled

---

### ⚠️ **Limitations**

- No real-time telemetry stream
- No historical data storage
- No confidence scoring
- Limited scenario set

---

### 🔮 **Future Improvements**

- Real telemetry integration
- Historical analysis (RAG / vector DB)
- Confidence scoring
- Multi-agent decision systems
- UI enhancements

---

### 🧪 **Tested Scenarios**

- 🌡 Thermal anomaly (overheating)
- 🔋 Energy degradation (battery issues)
- 📡 Communication loss

---

### 🎯 **Key Design Principle**

**Clarity in under 30 seconds.**  
This system is designed so that any user (or judge) can understand the output instantly without technical knowledge.

---

### 📄 **License**
MIT License

---

### 💡 **Final Note**

This project focuses on:
- Simplicity
- Reliability
- Demonstrability

\
