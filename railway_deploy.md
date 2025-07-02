# 🚄 RAILWAY DEPLOYMENT - 5 MINUTES

## Step 1: MongoDB Atlas Setup (2 minutes)
1. **Go to**: https://www.mongodb.com/atlas
2. **Sign up** for free account
3. **Create cluster** → Choose FREE tier (M0)
4. **Database Access** → Add user (username/password)
5. **Network Access** → Add IP → Allow access from anywhere (0.0.0.0/0)
6. **Connect** → Connect your application → Copy connection string

**Example connection string:**
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/webhook_db
```

---

## Step 2: Deploy to Railway (3 minutes)
1. **Go to**: https://railway.app
2. **Sign in** with GitHub account
3. **New Project** → **Deploy from GitHub repo**
4. **Select** your `webhook_pro` repository
5. **Deploy** - Railway auto-detects Flask app!

---

## Step 3: Environment Variables
In Railway dashboard → **Variables** tab, add:

```
MONGO_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/webhook_db
GITHUB_WEBHOOK_SECRET=my-webhook-secret-123
SECRET_KEY=flask-secret-key-generate-random
FLASK_DEBUG=False
PORT=5000
```

---

## Step 4: Get Your Live URL
- Railway provides URL like: `https://webhook-pro-production.up.railway.app`
- Your webhook endpoint: `https://your-app.railway.app/webhook`

---

## Step 5: Configure GitHub Webhook
1. Go to your `action-repo` on GitHub
2. **Settings** → **Webhooks** → **Add webhook**
3. **Payload URL**: `https://your-app.railway.app/webhook`
4. **Content type**: `application/json`
5. **Secret**: Same as `GITHUB_WEBHOOK_SECRET` above
6. **Events**: ✅ Pushes, ✅ Pull requests
7. **Active**: ✅ Checked

---

## ✅ DONE!
Your webhook monitor is now live! Test by:
1. Opening your live URL in browser
2. Pushing to action-repo
3. Creating pull requests
4. Watching events appear in real-time!

**Total time: ~5 minutes** 🚀 