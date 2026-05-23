# Instagram Authentication Setup

Instagram now requires authentication to download videos. Here are 3 methods to fix this:

## 🍪 Method 1: Export Cookies from Your Browser (RECOMMENDED)

This is the easiest and most reliable method.

### Step 1: Install a Cookie Exporter Extension

**For Chrome/Brave:**
1. Install "Get cookies.txt LOCALLY" extension
   - https://chrome.google.com/webstore/detail/get-cookiestxt-locally/cclelndahbckbenkjhflpdbgdldlbecc

**For Firefox:**
1. Install "cookies.txt" extension
   - https://addons.mozilla.org/en-US/firefox/addon/cookies-txt/

**For Safari:**
1. Install "ExportCookies" extension
   - Available in Mac App Store

### Step 2: Export Instagram Cookies

1. **Log into Instagram** in your browser
2. Go to instagram.com
3. Click the cookie extension icon
4. Click "Export" or "Get cookies.txt"
5. Save the file as `instagram_cookies.txt` in your project root

### Step 3: Add to Your Project

```bash
# Your project structure should look like:
ig_video_api/
├── main.py
├── instagram_cookies.txt    ← Put cookies file here
├── services/
└── ...
```

### Step 4: Update .env (optional)

If you want to use a different filename or path:

```bash
COOKIES_FILE=instagram_cookies.txt
```

### Step 5: Test It!

```bash
curl -X POST http://localhost:5500/process-video \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/reel/ACTUAL_REEL_ID/"}'
```

Replace `ACTUAL_REEL_ID` with a real reel ID (like `C8xAbCDeFgH`)

---

## 🔐 Method 2: Use yt-dlp's Browser Cookie Import (Alternative)

Instead of manually exporting, yt-dlp can read cookies directly from your browser.

Update `video_downloader.py`:

```python
ydl_opts = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'outtmpl': output_template,
    'quiet': True,
    'no_warnings': True,
    'cookiesfrombrowser': ('chrome',),  # or 'firefox', 'safari', 'brave'
}
```

**Pros:** No manual cookie export
**Cons:** May not work on Railway (browser not available on server)

---

## 🤖 Method 3: Use Instagram API Alternative (For Production)

For a production deployment on Railway, cookies can expire and need refreshing. Consider these alternatives:

### Option A: Instaloader (Python library)
```bash
uv add instaloader
```

### Option B: Third-party API Services
- RapidAPI Instagram endpoints
- Apify Instagram scrapers
- ScraperAPI

---

## 🚢 For Railway Deployment

### Challenge:
Cookies expire after ~90 days. You'll need to update them periodically.

### Solutions:

**1. Manual Cookie Refresh (Simple)**
- Export cookies monthly
- Upload via Railway file editor or environment variable

**2. Cookie as Environment Variable (Better)**

```bash
# In Railway dashboard, add this environment variable:
INSTAGRAM_COOKIES=<paste entire cookies.txt content>
```

Then update your code to write it to a file:

```python
# In main.py, after load_dotenv()
cookies_content = os.getenv("INSTAGRAM_COOKIES")
if cookies_content:
    with open("instagram_cookies.txt", "w") as f:
        f.write(cookies_content)
```

**3. Automated Cookie Refresh (Advanced)**
- Use Selenium/Playwright to auto-login and refresh cookies
- Store cookies in Railway's persistent volume or database
- Run a cron job to refresh cookies weekly

---

## 🔍 Troubleshooting

### Error: "Instagram sent an empty media response"
- ✅ Make sure you're logged into Instagram in your browser
- ✅ Export fresh cookies
- ✅ Check the cookies file is in the right location
- ✅ Verify the Instagram post is public or accessible to your account

### Error: "HTTP Error 429: Too Many Requests"
- Instagram is rate-limiting you
- Wait 15-30 minutes
- Use fewer requests or spread them out

### Cookies Not Working on Railway
- Check the file exists: Add debug logging
- Verify environment variable is set correctly
- Make sure cookies file is in .gitignore (don't commit to git!)

### "Login required" error
- Your cookies have expired
- Re-export fresh cookies from your browser
- Update them in Railway environment variables

---

## 📝 Security Notes

⚠️ **IMPORTANT:**
- Never commit `instagram_cookies.txt` to git
- Add it to `.gitignore`
- Cookies contain your session data - treat them like passwords
- Rotate cookies if they're exposed
- Use a separate Instagram account for automation (not your personal account)

---

## 🎯 Quick Test

After setting up cookies, test with a public reel:

```bash
# Start your server
python main.py

# Test with a real Instagram reel
curl -X POST http://localhost:5500/process-video \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.instagram.com/reel/C1234567890/"}'
```

If you get a success response, you're all set! 🎉
