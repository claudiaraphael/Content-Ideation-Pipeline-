# 🎬 AI Video Marketing Analyst

An intelligent automation API and Web App that processes social media videos (Instagram Reels), transcribes the audio, and automatically outputs an AI generated strategic marketing analysis directly into your task manager (Clickup).

> This project accepts video URLs via **Email**.

## 🚀 Features

The automation executes the following sequential pipeline:

* **User sends a video URL through email**
* **The email is being listened to constantly:** to automatically parse video URLs sent by the team.
* **Tracking:** Immediately creates a task in ClickUp for tracking.
* **Extraction:** Downloads video audio (mp3) using `yt-dlp` (supports Instagram -  TikTok and YouTube coming soon).
* **Transcription:** Uses Groq for ultra-high-speed transcription.
* **Refinement:** Agent cleans and punctuates the transcription.
* **Intelligence:** LLM analyzes content to generate a marketing report (Hooks, CTAs, Emotional Triggers).
* **Delivery:** Updates the original task in ClickUp with the report formatted in Markdown.

## 🛠️ Tech Stack

* **Language:** Python 3.9+
* **Web Framework:** Flask (API)
* **Protocols:** IMAP/SMTP (Email Parsing)
* **Tools:** `yt-dlp`, `ffmpeg`
* **Integrations:** ClickUp API

## ⚙️ Configuration and Installation

### 1. Prerequisites

Ensure the following are installed on your system:

* Python 3.10+
* FFmpeg (Essential for audio processing)
- Mac: brew install ffmpeg
- Linux: apt install ffmpeg
- Windows: download from ffmpeg.org

### 2. Installation and Virtual Environment

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install packages
pip install -r requirements.txt

```
**Note:** `requirements.txt` must include: 
`flask`, 
`python-dotenv`, 
`requests`, 
`yt-dlp`, 
`groq`, 
`imap-tools`.

---

## ▶️ Usage Guide

### 🅰️ For Marketing Teams 

1. **Compose:** Write an email to the Pvragon's address (e.g., `your-automation-email@gmail.com`).
2. **Subject:** "Analyze" (or leave blank).
3. **Body:** Paste the video URL (e.g., `https://www.instagram.com/reel/xyz/`).
4. **Send:** The system will pick it up, process it, and notify you in ClickUp.

### 🅱️ For Developers (Backend)

#### Start the API Server (flask)

```bash
python app.py

```

#### Start the Email Listener

(Run this in a separate terminal or as a background service)

```bash
python services/email_listener.py

# python3 services/email_listener.py # mac

```

#### API Endpoint

```bash
curl -X POST http://localhost:5500/process-video \
     -H "Content-Type: application/json" \
     -d '{"url": "https://www.instagram.com/reel/Example/"}'

```  

## 🔒 Security Note

This application handles sensitive session data and API keys. 
* **Environment Variables:** All credentials (API keys, Cookies, Email passwords) must be stored in a `.env` file. Never commit this file to version control.
* **Session Management:** Instagram cookies are handled via environment variables to avoid hardcoding session IDs.
* **Production Safety:** Ensure `FLASK_DEBUG` is set to `False` in production to prevent remote code execution.