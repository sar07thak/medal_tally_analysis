# 🚀 Deploy Olympics Analysis to Render

## Prerequisites
- Git installed
- GitHub account
- Render account (free)

## Steps to Deploy

### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit for Render deployment"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/olympics-analysis.git
git branch -M main
git push -u origin main
```

### 2. Deploy on Render

1. Go to [render.com](https://render.com) and sign up/login

2. Click **"New +"** → **"Blueprint"**

3. Connect your GitHub account and select your repository

4. Render will auto-detect the `render.yaml` configuration

5. Click **"Apply"** to deploy

### 3. Access Your App

Once deployed, you'll get a URL like:
```
https://olympics-analysis.onrender.com
```

## Important Notes

⚠️ **Data Files**: The `data/` folder contains CSV files (~50MB). If you face issues:
- Use Git LFS: `git lfs install && git lfs track "*.csv"`
- Or upload data separately after deployment

⚠️ **Free Tier Limits**:
- Web services spin down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds to load
- 750 hours/month free (enough for one service running 24/7)

## Troubleshooting

### Check Logs
In Render dashboard: **Logs** tab

### Environment Variables
Already set in `render.yaml`:
- `PYTHON_VERSION=3.11.0`
- `STREAMLIT_SERVER_PORT=8501`
- `STREAMLIT_SERVER_ADDRESS=0.0.0.0`

### Build Issues
If build fails, check:
1. `requirements.txt` has all dependencies
2. Data files are accessible
3. Python version compatibility

## Manual Deployment (Alternative)

If Blueprint doesn't work:

1. Go to Render Dashboard
2. **New +** → **Web Service**
3. Connect your repo
4. Configure:
   - **Name**: olympics-analysis
   - **Region**: Oregon (closest to you)
   - **Branch**: main
   - **Root Directory**: (leave blank)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0`
5. Choose **Free** plan
6. Click **Create Web Service**
