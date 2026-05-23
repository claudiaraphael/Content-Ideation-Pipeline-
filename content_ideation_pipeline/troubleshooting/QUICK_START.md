# ⚡ Quick Setup Checklist

## 🎯 File Placement

```
ig_video_api/                    ← Your project root
├── main.py                      ← Replace with fixed version
├── Procfile                     ← Put here (root level)
├── nixpacks.toml               ← Put here (root level)
├── .env                         ← Create from .env.example
├── .env.example                ← Reference template
├── .gitignore                  ← Important for security
├── instagram_cookies.txt       ← Export from browser
├── pyproject.toml              ← Your existing file
├── uv.lock                     ← Your existing file
└── services/
    ├── __init__.py             ← Should exist
    └── video_downloader.py     ← Replace with fixed version
```

## ✅ Setup Steps (5 minutes)

### 1. Install FFmpeg
```bash
brew install ffmpeg
```

### 2. Get Instagram Cookies
1. Install "Get cookies.txt LOCALLY" Chrome extension
2. Log into Instagram
3. Click extension → Export
4. Save as `instagram_cookies.txt` in project root

### 3. Configure Environment
```bash
cp .env.example .env
nano .env  # Add your N8N webhook URL
```

### 4. Test Locally
```bash
# Make sure you're in your project directory
cd /Users/joraro/Documents/cacau/ig_video_api

# Run the server
python main.py

# In another terminal, test it:
curl -X POST http://localhost:5500/process-video \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/reel/REAL_REEL_ID/"}'
```

### 5. Deploy to Railway
```bash
# Make sure Procfile and nixpacks.toml are in root
# Add environment variables in Railway dashboard:
# - N8N_WEBHOOK_URL
# - INSTAGRAM_COOKIES (paste entire cookies.txt content)

# Push to git and Railway will auto-deploy
```

## 🚨 Common Issues

### "Import 'video_downloader' could not be resolved"
- ✅ Make sure `services/__init__.py` exists
- ✅ Restart VS Code window (Cmd+Shift+P → Reload Window)

### "Instagram sent an empty media response"
- ✅ Export fresh cookies from browser
- ✅ Make sure `instagram_cookies.txt` is in project root
- ✅ Use a real reel ID (not "YOUR_REEL_ID")

### Railway deployment fails
- ✅ Check `Procfile` is in root (not in services/)
- ✅ Check `nixpacks.toml` is in root
- ✅ Add cookies as `INSTAGRAM_COOKIES` env variable in Railway

### Type errors in VS Code
- ✅ Select correct Python interpreter (Cmd+Shift+P → Python: Select Interpreter)
- ✅ Choose the one with `.venv` in the path

## 🎉 You're Done When...

- [ ] FFmpeg installed (`ffmpeg -version` works)
- [ ] Cookies exported and saved
- [ ] `.env` file configured with N8N webhook URL
- [ ] Test curl command returns success
- [ ] Procfile and nixpacks.toml in project root
- [ ] No errors in VS Code (after reloading window)

## 📚 Read Next

- `INSTAGRAM_AUTH_GUIDE.md` - Detailed cookie setup
- `DEPLOYMENT_GUIDE.md` - Full deployment instructions

## 💡 Pro Tips

- Use a separate Instagram account for automation (not your main account)
- Cookies expire after ~90 days - set a reminder to refresh
- Test with public reels first
- Check Railway logs if deployment fails
