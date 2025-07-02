# 🌐 HEROKU DEPLOYMENT GUIDE

## Prerequisites
1. **Heroku CLI**: Download from https://devcenter.heroku.com/articles/heroku-cli
2. **MongoDB Atlas**: Setup (same as Railway guide)

---

## Step 1: Login to Heroku
```bash
heroku login
```

---

## Step 2: Create Heroku App
```bash
heroku create your-webhook-app-name
```

---

## Step 3: Set Environment Variables
```bash
heroku config:set MONGO_URI="mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/webhook_db"
heroku config:set GITHUB_WEBHOOK_SECRET="my-webhook-secret-123" 
heroku config:set SECRET_KEY="flask-secret-key-generate-random"
heroku config:set FLASK_DEBUG="False"
```

---

## Step 4: Deploy
```bash
git push heroku main
```

---

## Step 5: Open App
```bash
heroku open
```

Your app will be available at: `https://your-webhook-app-name.herokuapp.com`

---

## Step 6: Configure GitHub Webhook
Use the Heroku URL: `https://your-webhook-app-name.herokuapp.com/webhook`

---

## Troubleshooting
```bash
# View logs
heroku logs --tail

# Check app status
heroku ps

# Restart app
heroku restart
``` 