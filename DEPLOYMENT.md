# Deployment Guide: GitHub → Render

## Prerequisites

- GitHub account
- Render account (free tier works)
- Git installed locally
- VS Code installed

## Step-by-Step Deployment

### Part 1: Local Setup and Testing

1. **Open VS Code**
   ```bash
   cd /path/to/household-spending-app
   code .
   ```

2. **Test locally first**
   
   On Mac/Linux:
   ```bash
   ./start.sh
   ```
   
   On Windows:
   ```batch
   start.bat
   ```
   
   Visit `http://localhost:5000` to verify the app works.

3. **Stop the server** (Ctrl+C)

### Part 2: Push to GitHub

1. **Create a new repository on GitHub**
   - Go to github.com
   - Click "+" → "New repository"
   - Name: `household-spending-estimates`
   - Description: "Monthly household grocery spending estimates from ABS data"
   - Public or Private (your choice)
   - DO NOT initialize with README (we already have one)
   - Click "Create repository"

2. **Initialize Git locally** (if not already done)
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Flask app with ABS MHSI integration"
   ```

3. **Add GitHub remote and push**
   
   Replace `YOUR-USERNAME` with your GitHub username:
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/household-spending-estimates.git
   git push -u origin main
   ```

4. **Verify on GitHub**
   - Refresh your GitHub repository page
   - You should see all files uploaded

### Part 3: Deploy to Render

#### Option A: Using Blueprint (Recommended - Easiest)

1. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com/
   - Sign up/Login (can use GitHub account)

2. **New Blueprint**
   - Click "New +" → "Blueprint"
   - Click "Connect account" to link your GitHub
   - Select your `household-spending-estimates` repository
   - Click "Connect"

3. **Review Configuration**
   - Render will detect `render.yaml`
   - Service name: `household-spending-estimates`
   - Environment: Docker
   - Branch: main
   - Click "Apply"

4. **Wait for Deployment**
   - Render will:
     - Clone your repository
     - Build the Docker image
     - Deploy the container
   - This takes 3-5 minutes
   - Watch the logs for progress

5. **Access Your App**
   - Once deployed, you'll get a URL like:
     `https://household-spending-estimates.onrender.com`
   - Click the URL to open your app
   - ✅ Done!

#### Option B: Manual Web Service (Alternative)

1. **New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Click "Connect"

2. **Configure Service**
   - Name: `household-spending-estimates`
   - Region: Choose closest to Sydney (e.g., Oregon or Singapore)
   - Branch: `main`
   - Root Directory: (leave empty)
   - Environment: `Docker`
   - Plan: `Free`

3. **Advanced Settings** (scroll down)
   - Health Check Path: `/`
   - Leave everything else as default

4. **Create Web Service**
   - Click "Create Web Service"
   - Wait for deployment (3-5 minutes)

5. **Get Your URL**
   - Once deployed, find your URL at the top
   - Format: `https://your-service-name.onrender.com`

### Part 4: Share with Colleagues

1. **Share the URL**
   - Copy the Render URL
   - Share with your NDIA team
   - Bookmark it for easy access

2. **Create shortcuts**
   - Methodology page: `https://your-app.onrender.com/methodology`
   - Data table: `https://your-app.onrender.com/data`

### Part 5: Monthly Updates

When new ABS data is released:

1. **Update the data**
   ```bash
   # Edit data_fetcher.py
   code data_fetcher.py
   
   # Add new month to MANUAL_DATA
   # Example:
   'month': [..., '2025-12'],
   'food_aud_m_sa': [..., 12345.6]
   ```

2. **Commit and push**
   ```bash
   git add data_fetcher.py
   git commit -m "Update: December 2025 data"
   git push
   ```

3. **Automatic redeploy**
   - Render detects the push
   - Automatically rebuilds and redeploys
   - Takes ~3 minutes
   - No action needed!

## Troubleshooting

### Issue: Git push fails with authentication error

**Solution:**
```bash
# Use GitHub Personal Access Token
# 1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
# 2. Generate new token (classic)
# 3. Select scopes: repo (all)
# 4. Copy the token
# 5. Use token as password when pushing
```

### Issue: Render build fails

**Check:**
1. Verify all files are pushed to GitHub
2. Check Render logs for specific error
3. Ensure Dockerfile is present
4. Verify requirements.txt is correct

**Common fixes:**
```bash
# Rebuild locally first
docker build -t test-app .

# If that works, the issue is with Git/GitHub
git status  # Check what's not committed
git add .
git commit -m "Fix: Add missing files"
git push
```

### Issue: App works locally but not on Render

**Check:**
1. Environment variables (PORT should be 10000)
2. Render logs for Python errors
3. Try "Manual Deploy" button in Render dashboard

### Issue: Render app is slow to start (cold start)

**This is normal for free tier:**
- Free tier apps sleep after 15 minutes of inactivity
- First request after sleep takes 30-60 seconds
- Subsequent requests are fast
- **Solution**: Upgrade to paid tier ($7/month) for always-on

### Issue: API connection fails on Render

**This is expected:**
- ABS API may be blocked or slow
- App automatically falls back to manual data
- Update manual data regularly in `data_fetcher.py`

## VS Code Tips

### Recommended Extensions
- Python (Microsoft)
- Docker (Microsoft)
- GitLens (for better Git integration)
- GitHub Pull Requests (for GitHub integration)

### Useful Commands in VS Code

Open terminal: `Ctrl+` ` (backtick) or `Cmd+` ` on Mac

```bash
# Test locally
python app.py

# Check git status
git status

# View differences
git diff

# Commit with VS Code UI
# Use Source Control panel (Ctrl+Shift+G)
```

## Security Notes

- Never commit API keys or secrets
- Use environment variables for sensitive data
- The free Render tier is suitable for internal tools
- For production apps, consider paid tier with custom domain

## Cost Estimate

- **GitHub**: Free for public/private repos
- **Render Free Tier**: 
  - ✅ 750 hours/month (enough for one app)
  - ✅ Automatic HTTPS
  - ⚠️ Apps sleep after 15 min inactivity
  - ⚠️ 512 MB RAM limit

- **Render Paid Tier** ($7/month):
  - ✅ Always-on (no cold starts)
  - ✅ More RAM and CPU
  - ✅ Better for team usage

## Support

For issues:
1. Check Render logs first
2. Review this guide
3. Check GitHub repository Issues
4. Contact NDIA AT Markets team

## Next Steps

After deployment:
1. ✅ Test all pages (Dashboard, Methodology, Data)
2. ✅ Share URL with team
3. ✅ Set up monthly data update process
4. ✅ Bookmark for easy access
5. ✅ Document any team-specific customizations

**Congratulations! Your app is now live! 🎉**
