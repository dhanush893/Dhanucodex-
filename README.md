# AskMe - Anonymous Messaging App
## Full Stack: Express + MongoDB + Telegram Bot

---

## 📁 File Structure
```
askme-backend/
├── server.js       ← Backend API
├── index.html      ← Frontend (host this separately)
├── .env            ← Your secrets (NEVER share/commit this)
├── package.json
└── README.md
```

---

## 🚀 Deploy Backend on Render (Free)

1. Go to https://render.com → Sign up (free)
2. Click **New → Web Service**
3. Connect your GitHub repo (or upload files)
4. Set:
   - **Build Command:** `npm install`
   - **Start Command:** `node server.js`
5. Add these **Environment Variables** (in Render dashboard):
   ```
   MONGO_URI=mongodb+srv://dhanushrdhanushr518_db_user:YOUR_NEW_PASSWORD@dhanucodex.fsfzfob.mongodb.net/?appName=Dhanucodex
   TELEGRAM_BOT_TOKEN=YOUR_NEW_BOT_TOKEN
   TELEGRAM_CHAT_ID=-1003590007546
   ADMIN_SECRET=pick_a_secret_password
   PORT=3000
   ```
6. Click **Deploy** → copy the URL (e.g. https://askme-xyz.onrender.com)

---

## 🌐 Deploy Frontend

1. Open `index.html`
2. Replace this line:
   ```js
   const API_URL = 'https://your-backend-url.com/api/message';
   ```
   With your Render URL:
   ```js
   const API_URL = 'https://askme-xyz.onrender.com/api/message';
   ```
3. Host on **Netlify** (drag & drop at netlify.com/drop) or any static host

---

## 📬 How Messages Work

1. User visits your frontend page
2. Types an anonymous message → hits Send
3. Backend saves it to **MongoDB** (Messages collection)
4. Backend forwards it to your **Telegram bot** instantly
5. You see it in Telegram like:

```
💌 New Anonymous Message

Hey, I really admire how you handle things!
```

---

## 🔍 View All Messages (Admin)

GET https://your-backend.onrender.com/api/messages?secret=YOUR_ADMIN_SECRET

---

## ⚠️ IMPORTANT SECURITY STEPS

Since your credentials were shared, do these NOW:

1. **Regenerate Telegram Bot Token:**
   - Open Telegram → search @BotFather
   - Send: /mybots → select your bot → API Token → Revoke
   - Copy new token → update .env

2. **Change MongoDB Password:**
   - Go to https://cloud.mongodb.com
   - Database Access → Edit user → Update password
   - Update connection string in .env

---

## 🛠 Run Locally (for testing)

```bash
npm install
node server.js
# Server runs on http://localhost:3000
```
