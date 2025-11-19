# How to Use Your Deployed Website

## 🎉 Your Website is Live!

Your website is successfully deployed on Railway at:
**https://insta-fbvideodownloader-production.up.railway.app**

## Option 1: Use Railway Only (Recommended - Already Working!)

You **don't need Vercel**! Your Railway deployment serves both:
- ✅ Frontend (React app)
- ✅ Backend API (Flask)

### How to Access:
1. Open your Railway URL: `https://insta-fbvideodownloader-production.up.railway.app`
2. That's it! Everything works from one URL.

### How to Use:
1. Paste an Instagram or Facebook URL
2. Click "Download"
3. Wait for the media to load
4. Click the download button to save

---

## Option 2: Separate Frontend on Vercel (Optional)

If you want to deploy frontend separately on Vercel:

### Step 1: Update Railway CORS
In Railway, add your Vercel domain to environment variables:
```
ALLOWED_ORIGINS=https://your-vercel-app.vercel.app,https://your-custom-domain.com
```

### Step 2: Deploy to Vercel
1. Go to [Vercel](https://vercel.com)
2. Import your GitHub repository
3. Set root directory to `frontend`
4. Add environment variable:
   ```
   REACT_APP_API_URL=https://insta-fbvideodownloader-production.up.railway.app
   ```
5. Deploy!

### Step 3: Fix 404 Errors
The `vercel.json` file is already created to handle React Router routing.

---

## 🚀 Quick Start Guide

### For Railway (Current Setup):
1. Visit: `https://insta-fbvideodownloader-production.up.railway.app`
2. Start downloading!

### For Vercel (If you want separate):
1. Set `REACT_APP_API_URL` in Vercel to your Railway URL
2. Update `ALLOWED_ORIGINS` in Railway to include Vercel domain
3. Deploy!

---

## 🔧 Troubleshooting

### 404 Errors on Vercel:
- ✅ `vercel.json` is already created - this fixes routing
- Make sure `REACT_APP_API_URL` is set correctly
- Check Railway CORS settings

### CORS Errors:
- Update `ALLOWED_ORIGINS` in Railway to include your Vercel domain
- Format: `https://domain1.com,https://domain2.com`

### API Not Working:
- Check Railway logs
- Verify environment variables are set
- Test API directly: `https://your-railway-url.com/api/health`

---

## 📝 Environment Variables

### Railway (Backend):
```
FLASK_ENV=production
FLASK_DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=*
PORT=5000
```

### Vercel (Frontend - if using):
```
REACT_APP_API_URL=https://insta-fbvideodownloader-production.up.railway.app
```

---

## ✅ Recommendation

**Use Railway only** - it's simpler, cheaper, and already working! You don't need Vercel unless you have a specific reason (like custom domain requirements or CDN needs).

