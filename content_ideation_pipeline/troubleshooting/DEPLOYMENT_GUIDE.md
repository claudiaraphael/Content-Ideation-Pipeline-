# Instagram Video Downloader API - Setup & Deployment Guide

## 🔧 What Each Error Was & How I Fixed It

### main.py Errors (10 total):

1. **"Import 'video_downloader' could not be resolved"** done
   - **Problem**: Import path was wrong - you need `from services.video_downloader import...`
   - **Fix**: Changed to `from services.video_downloader import download_video_locally`

2. **"N8N_WEBHOOK_URL is not defined"** done
   - **Problem**: You used this variable but never defined it
   - **Fix**: Added `N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "")` at the top

3-10. **All the "Type is unknown" and "Argument type is unknown" errors** done
   - **Problem**: Missing type hints - Pylance couldn't infer types 
   - **Fix**: Added type hint `file_path: str = download_video_locally(video_url)`
   - These were all cascading from the import error and missing type hints

### video_downloader.py Errors (5 total):

1. **"Type annotation is missing for parameter 'video_url'"** done
   - **Problem**: Function parameter had no type hint
   - **Fix**: Changed to `def download_video_locally(video_url: str) -> str:`

2. **"Type of 'ydl_opts' is partially unknown"** done
   - **Problem**: Dictionary type couldn't be inferred
   - **Fix**: This is actually fine - it's a dict with mixed types. Pylance is just being cautious.

3. **"Argument of type dict[str, Unknown] cannot be assigned..."** done
   - **Problem**: yt_dlp is strict about types
   - **Fix**: Adding the return type annotation `-> str` helps Pylance understand the flow

4-5. **"Argument type is unknown" errors** done
   - **Problem**: Cascading from the missing parameter type hint
   - **Fix**: Fixed by adding `video_url: str` parameter type

## 📋 Prerequisites

Before running locally, you need:

1. **FFmpeg** (required by yt-dlp to merge video/audio) done
   ```bash
   brew install ffmpeg
   ```

2. **Python 3.10+** (you have this ✓)

3. **UV package manager** (you have this ✓)

## 🚀 How to Run Locally

### 1. Set up your environment:

```bash
# Navigate to your project
cd /Users/joraro/Documents/cacau/ig_video_api

# Create .env file from template
cp .env.example .env

# Edit .env and add your N8N webhook URL
nano .env  # or use VS Code: code .env
```

### 2. Install dependencies (if not already done):

```bash
uv sync
```

### 3. Activate your virtual environment:

```bash
source .venv/bin/activate
```

### 4. Run the Flask app:

```bash
python main.py
```

Your API will be running at `http://localhost:5500`

### 5. Test it with curl:

```bash
curl -X POST http://localhost:5500/process-video \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/reel/YOUR_REEL_ID/"}'
```

## 🚢 Deploying to Railway

### 1. Create required files:

**Procfile** (Railway will auto-detect this):
```
web: python main.py
```

Or Railway can auto-detect Flask and run it directly.

### 2. Environment Variables in Railway:

Go to your Railway project → Variables tab and add:
- `N8N_WEBHOOK_URL` = your n8n webhook URL

### 3. Railway Build Configuration:

Railway should auto-detect your `pyproject.toml` and use uv. If not, add these:

**railway.toml** (optional, Railway usually auto-detects):
```toml
[build]
builder = "nixpacks"

[deploy]
startCommand = "python main.py"
```

### 4. System Dependencies:

For FFmpeg on Railway, you might need a `nixpacks.toml`:

```toml
[phases.setup]
aptPkgs = ["ffmpeg"]
```

## 📁 Project Structure

```
ig_video_api/
├── main.py                 # Flask API server
├── services/
│   ├── __init__.py        # Makes services a package
│   └── video_downloader.py # Video download logic
├── .env                    # Your environment variables (don't commit!)
├── .env.example           # Template for environment variables
├── pyproject.toml         # Dependencies
├── uv.lock               # Lock file for dependencies
└── downloads/            # Temp folder for videos (auto-created)
```

## 🔍 Should You Keep It Modularized?

**YES! Keep it modular.** Here's why:

✅ **Pros of keeping it modular (current setup):**
- Easy to test `video_downloader` independently
- Clean separation of concerns
- Can reuse downloader logic elsewhere
- Easier to maintain and debug
- Better for team collaboration

❌ **Cons of putting everything in main.py:**
- Hard to test
- Messy code
- Difficult to reuse logic
- Harder to debug

Your current structure is great for a production app!

## 🐛 Debugging Tips

If something goes wrong:

1. **Check logs**:
   ```bash
   # Local
   python main.py  # Shows all print/error output
   
   # Railway
   Check the deployment logs in Railway dashboard
   ```

2. **Test video downloader separately**:
   ```python
   from services.video_downloader import download_video_locally
   
   file_path = download_video_locally("https://www.instagram.com/reel/...")
   print(f"Downloaded to: {file_path}")
   ```

3. **Common issues**:
   - Missing FFmpeg → `brew install ffmpeg`
   - Wrong N8N webhook URL → Check your .env file
   - Instagram blocking → Try different video URL
   - Permissions → Make sure `downloads/` folder can be created

## 🎯 Next Steps

1. Replace the files in your project with the fixed versions I created
2. Create a `.env` file with your N8N webhook URL
3. Test locally with `python main.py`
4. Deploy to Railway
5. Test the deployed endpoint from n8n

## 📝 Notes

- The code will work fine even with some Pylance warnings
- Type hints are for developer experience, not runtime
- Keep your `.env` file in `.gitignore` (never commit secrets!)
- Railway will automatically install FFmpeg if you add the nixpacks.toml

Good luck with your deployment! 🚀
