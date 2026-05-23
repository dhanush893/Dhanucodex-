const express = require('express');
const mongoose = require('mongoose');
const cors = require('cors');
const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));
require('dotenv').config();

const app = express();
app.use(cors());
app.use(express.json());

// ── MongoDB Connection ──
mongoose.connect(process.env.MONGO_URI)
  .then(() => console.log('✅ MongoDB connected'))
  .catch(err => console.error('❌ MongoDB error:', err));

// ── Message Schema ──
const messageSchema = new mongoose.Schema({
  message: { type: String, required: true, maxlength: 300 },
  sentAt:  { type: Date, default: Date.now },
  ip:      { type: String },
});
const Message = mongoose.model('Message', messageSchema);

// ── Telegram Helper ──
async function sendToTelegram(text) {
  const TOKEN   = process.env.TELEGRAM_BOT_TOKEN;
  const CHAT_ID = process.env.TELEGRAM_CHAT_ID;
  const url = `https://api.telegram.org/bot${TOKEN}/sendMessage`;
  const body = {
    chat_id:    CHAT_ID,
    text:       `💌 *New Anonymous Message*\n\n${text}`,
    parse_mode: 'Markdown',
  };
  const res = await fetch(url, {
    method:  'POST',
    headers: { 'Content-Type': 'application/json' },
    body:    JSON.stringify(body),
  });
  return res.json();
}

// ── POST /api/message ──
app.post('/api/message', async (req, res) => {
  try {
    const { message } = req.body;

    if (!message || message.trim().length === 0)
      return res.status(400).json({ error: 'Message cannot be empty.' });

    if (message.length > 300)
      return res.status(400).json({ error: 'Message too long (max 300 chars).' });

    // Save to MongoDB
    const doc = await Message.create({
      message: message.trim(),
      ip: req.headers['x-forwarded-for'] || req.socket.remoteAddress,
    });

    // Forward to Telegram
    const tgResult = await sendToTelegram(message.trim());
    if (!tgResult.ok) {
      console.error('Telegram error:', tgResult);
    }

    return res.status(200).json({ success: true, id: doc._id });
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: 'Something went wrong. Try again.' });
  }
});

// ── GET /api/messages (optional admin view) ──
app.get('/api/messages', async (req, res) => {
  const secret = req.query.secret;
  if (secret !== process.env.ADMIN_SECRET)
    return res.status(401).json({ error: 'Unauthorized' });

  const messages = await Message.find().sort({ sentAt: -1 }).limit(100);
  res.json(messages);
});

// ── Health check ──
app.get('/', (req, res) => res.send('🚀 AskMe backend is running!'));

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));

