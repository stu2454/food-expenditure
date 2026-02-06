# 🚀 QUICK START GUIDE

## What You Have

A complete Flask web application for displaying household spending estimates, ready to deploy to Render.com.

## Three Steps to Deploy

### 1️⃣ Test Locally (2 minutes)

```bash
# Navigate to the folder
cd household-spending-app

# Run quick start
./start.sh          # Mac/Linux
# OR
start.bat           # Windows

# Visit: http://localhost:5002
```

✅ **Verify**: All three pages work (Dashboard, Methodology, Data)

### 2️⃣ Push to GitHub (5 minutes)

```bash
# Create repository on GitHub.com first, then:

git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/household-spending-estimates.git
git push -u origin main
```

✅ **Verify**: All files visible on GitHub

### 3️⃣ Deploy to Render (5 minutes)

1. Go to https://dashboard.render.com/
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository
4. Click "Apply"
5. Wait 3-5 minutes for deployment

✅ **Done!** You'll get a URL like: `https://household-spending-estimates.onrender.com`

## File Overview

| File | Purpose |
|------|---------|
| `app.py` | Flask web application |
| `data_fetcher.py` | ABS API integration |
| `templates/*.html` | Web pages |
| `static/css/style.css` | Styling |
| `Dockerfile` | Container config |
| `requirements.txt` | Python packages |
| `render.yaml` | Render config |
| `start.sh` / `start.bat` | Quick start scripts |

## Need Help?

1. **Testing locally fails?**
   - Check you have Python 3.11+ installed: `python --version`
   - Try: `pip install -r requirements.txt` manually

2. **GitHub push fails?**
   - Create Personal Access Token: GitHub.com → Settings → Developer settings
   - Use token as password when pushing

3. **Render deploy fails?**
   - Check all files are on GitHub
   - View logs in Render dashboard
   - Try "Manual Deploy" button

4. **App is slow to start?**
   - Normal on free tier (cold starts)
   - First request takes 30-60 seconds
   - Subsequent requests are fast

## Monthly Updates

When new ABS data is released:

1. Open `data_fetcher.py`
2. Add new month to `MANUAL_DATA`:
   ```python
   'month': [..., '2025-12'],
   'food_aud_m_sa': [..., 12345.6]
   ```
3. Commit and push:
   ```bash
   git add data_fetcher.py
   git commit -m "Update: December 2025 data"
   git push
   ```
4. Render auto-redeploys in ~3 minutes

## Complete Documentation

- **PROJECT_SUMMARY.md** - Full project overview
- **README.md** - Setup and features
- **DEPLOYMENT.md** - Detailed deployment steps

## VS Code Tips

1. Open folder in VS Code: `code household-spending-app`
2. Use integrated terminal: `Ctrl+` `
3. Use Source Control panel for Git: `Ctrl+Shift+G`

## What's Next?

After deployment:
- ✅ Share URL with team
- ✅ Bookmark the site
- ✅ Set monthly reminder for data updates
- ✅ Celebrate! 🎉

---

**Questions?** Check DEPLOYMENT.md for troubleshooting or contact NDIA AT Markets team.
