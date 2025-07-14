# 🚀 Deployment Checklist

## ✅ Pre-Deployment Checklist

### Code Changes

- [x] Updated `backend/requirements.txt` (removed whisper packages)
- [x] Updated `backend/config.py` (CORS configuration)
- [x] Updated `backend/main.py` (CORS middleware)
- [x] Created `backend/build.sh` (Render build script)
- [x] Created `backend/run.py` (Render run script)
- [x] Created `frontend/netlify.toml` (Netlify configuration)
- [x] Created `frontend/.env.production` (environment variables)

### Prerequisites

- [ ] Get OpenRouter API key from [https://openrouter.ai/keys](https://openrouter.ai/keys)
- [ ] Create GitHub repository and push all code
- [ ] Sign up for Render: [https://render.com](https://render.com)
- [ ] Sign up for Netlify: [https://netlify.com](https://netlify.com)

## 🎯 Deployment Steps

### Backend (Render)

- [ ] Create new Web Service on Render
- [ ] Connect GitHub repository
- [ ] Set Root Directory: `backend`
- [ ] Set Build Command: `chmod +x build.sh && ./build.sh`
- [ ] Set Start Command: `python run.py`
- [ ] Add Environment Variables:
  - [ ] `OPENROUTER_API_KEY=your_api_key`
  - [ ] `OPENROUTER_MODEL=mistralai/mistral-small-3.2-24b-instruct:free`
- [ ] Deploy and copy the URL

### Frontend (Netlify)

- [ ] Update `frontend/.env.production` with your Render backend URL
- [ ] Create new site on Netlify
- [ ] Connect GitHub repository
- [ ] Set Base directory: `frontend`
- [ ] Set Build command: `npm run build`
- [ ] Set Publish directory: `dist`
- [ ] Deploy and copy the URL

### Final Configuration

- [ ] Update `backend/config.py` with your Netlify URL
- [ ] Redeploy backend on Render
- [ ] Test the complete application

## 🧪 Testing Checklist

- [ ] Backend health check: `https://your-backend.onrender.com/health`
- [ ] API docs: `https://your-backend.onrender.com/docs`
- [ ] Frontend loads: `https://your-app.netlify.app`
- [ ] YouTube URL input works
- [ ] Notes generation works
- [ ] PDF download works

## 🚨 Common Issues to Check

- [ ] CORS errors in browser console
- [ ] API key authentication errors
- [ ] Build failures in deployment logs
- [ ] Environment variables not set correctly

---

**🎉 Once all checkboxes are marked, your app is live!**
