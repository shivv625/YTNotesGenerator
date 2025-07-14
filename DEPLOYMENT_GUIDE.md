# 🚀 YouTube Notes Generator - Deployment Guide

This guide will help you deploy your YouTube Notes Generator to **Netlify (Frontend)** and **Render (Backend)** for free.

## 📋 Prerequisites

1. **GitHub Account**: Your code should be in a GitHub repository
2. **OpenRouter API Key**: Get from [https://openrouter.ai/keys](https://openrouter.ai/keys)
3. **Netlify Account**: Sign up at [https://netlify.com](https://netlify.com)
4. **Render Account**: Sign up at [https://render.com](https://render.com)

## 🔧 Code Changes Made

### ✅ Frontend Changes

- Created `.env.production` file for environment variables
- Added `netlify.toml` configuration
- API URL configuration is already production-ready

### ✅ Backend Changes

- Updated `requirements.txt` (removed problematic packages)
- Updated CORS configuration for production
- Created `build.sh` and `run.py` for Render deployment
- Environment variables are properly configured

## 🎯 Step-by-Step Deployment

### Step 1: Deploy Backend to Render

#### 1.1 Prepare Your Repository

1. Push all changes to your GitHub repository
2. Ensure your repository structure looks like this:
   ```
   your-repo/
   ├── backend/
   │   ├── main.py
   │   ├── requirements.txt
   │   ├── build.sh
   │   ├── run.py
   │   ├── config.py
   │   └── .env (create this locally)
   └── frontend/
       ├── src/
       ├── package.json
       ├── netlify.toml
       └── .env.production
   ```

#### 1.2 Deploy to Render

1. **Sign up/Login to Render**: [https://render.com](https://render.com)
2. **Create New Web Service**:

   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repository

3. **Configure the Service**:

   ```
   Name: youtube-notes-backend (or your preferred name)
   Root Directory: backend
   Runtime: Python 3
   Build Command: chmod +x build.sh && ./build.sh
   Start Command: python run.py
   ```

4. **Set Environment Variables**:

   - Click "Environment" tab
   - Add these variables:

   ```
   OPENROUTER_API_KEY=your_actual_api_key_here
   OPENROUTER_MODEL=mistralai/mistral-small-3.2-24b-instruct:free
   ```

5. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Copy your service URL (e.g., `https://your-app.onrender.com`)

### Step 2: Deploy Frontend to Netlify

#### 2.1 Update Frontend Environment

1. **Update `.env.production`** in your frontend directory:
   ```
   VITE_API_URL=https://your-actual-render-backend-url.onrender.com
   ```
   Replace with your actual Render backend URL from Step 1.

#### 2.2 Deploy to Netlify

1. **Sign up/Login to Netlify**: [https://netlify.com](https://netlify.com)
2. **Deploy from Git**:

   - Click "New site from Git"
   - Connect your GitHub repository
   - Select your repository

3. **Configure Build Settings**:

   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: dist
   ```

4. **Set Environment Variables** (Optional):

   - Go to Site settings → Environment variables
   - Add: `VITE_API_URL=https://your-render-backend-url.onrender.com`

5. **Deploy**:
   - Click "Deploy site"
   - Wait for deployment (2-3 minutes)
   - Your site will be available at `https://your-app.netlify.app`

### Step 3: Update CORS Configuration

#### 3.1 Update Backend CORS

1. **Update `backend/config.py`**:

   ```python
   ALLOWED_ORIGINS = [
       "http://localhost:3000",
       "http://localhost:5173",
       "https://your-actual-netlify-app.netlify.app",  # Replace with your Netlify URL
       "https://*.netlify.app"
   ]
   ```

2. **Redeploy Backend**:
   - Go to your Render dashboard
   - Click "Manual Deploy" → "Deploy latest commit"

## 🔧 Environment Variables Summary

### Backend (Render) Environment Variables

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
OPENROUTER_MODEL=mistralai/mistral-small-3.2-24b-instruct:free
```

### Frontend (Netlify) Environment Variables

```
VITE_API_URL=https://your-render-backend-url.onrender.com
```

## 🧪 Testing Your Deployment

### 1. Test Backend API

Visit your Render URL + `/health`:

```
https://your-backend.onrender.com/health
```

### 2. Test Frontend

Visit your Netlify URL and try:

- Enter a YouTube URL
- Generate notes
- Download PDF

### 3. Test API Documentation

Visit your Render URL + `/docs`:

```
https://your-backend.onrender.com/docs
```

## 🚨 Troubleshooting

### Common Issues:

1. **CORS Errors**:

   - Update CORS configuration in `backend/config.py`
   - Redeploy backend

2. **API Key Issues**:

   - Verify your OpenRouter API key is correct
   - Check Render environment variables

3. **Build Failures**:

   - Check Render logs for Python version issues
   - Ensure all dependencies are in `requirements.txt`

4. **Frontend Not Loading**:
   - Check Netlify build logs
   - Verify environment variables are set correctly

### Debug Commands:

**Check Backend Logs**:

- Go to Render dashboard → Your service → Logs

**Check Frontend Logs**:

- Go to Netlify dashboard → Your site → Deploys → Latest deploy → View deploy log

## 📊 Performance Optimization

### Render (Backend):

- **Free Tier**: 750 hours/month
- **Auto-sleep**: After 15 minutes of inactivity
- **Cold start**: ~30 seconds after sleep

### Netlify (Frontend):

- **Free Tier**: Unlimited
- **CDN**: Global distribution
- **Build time**: ~2-3 minutes

## 🔄 Continuous Deployment

Both services will automatically redeploy when you push changes to your GitHub repository.

## 📞 Support

If you encounter issues:

1. Check the logs in Render/Netlify dashboards
2. Verify environment variables are set correctly
3. Test locally first with the same configuration

---

**🎉 Congratulations!** Your YouTube Notes Generator is now live and accessible to users worldwide!
