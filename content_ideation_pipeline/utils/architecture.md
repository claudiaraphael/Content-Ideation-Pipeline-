
ig_video_api/
├── app.py                 # Flask entry point & Webhook/Cron trigger
├── .env                   # API Keys (Groq, ClickUp, Instagram Cookies)
├── services/
│   ├── email_parser.py    # IMAP logic to fetch/parse emails
│   ├── download_service.py # yt_dlp logic for Instagram
│   ├── transcript_service.py # Groq Whisper API calls
│   ├── marketing_analysis.py # LLM logic (GPT-4/Claude/Groq)
│   └── clickup_service.py # ClickUp API wrapper
├── schemas/               # Data classes/Pydantic models for validation
└── downloads/             # Temporary storage for .mp3 files