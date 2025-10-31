require('dotenv').config();
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const cors = require('cors');
const bodyParser = require('body-parser');

const app = express();
const PORT = process.env.PORT || 3001;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;

// Middleware
app.use(cors());
app.use(bodyParser.json());

// SQLite DB setup
const db = new sqlite3.Database('./contacts.db', (err) => {
  if (err) throw err;
  db.run(`CREATE TABLE IF NOT EXISTS contacts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    firstName TEXT,
    lastName TEXT,
    email TEXT,
    phone TEXT,
    message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
  )`);
});

// POST /api/contact — Save a submission
app.post('/api/contact', (req, res) => {
  const { firstName, lastName, email, phone, message } = req.body;
  if (!firstName || !lastName || !email || !phone || !message) {
    return res.status(400).json({ error: 'All fields required.' });
  }
  db.run(
    `INSERT INTO contacts (firstName, lastName, email, phone, message) VALUES (?, ?, ?, ?, ?)`,
    [firstName, lastName, email, phone, message],
    function (err) {
      if (err) return res.status(500).json({ error: 'DB error.' });
      res.json({ success: true, id: this.lastID });
    }
  );
});

// GET /api/contacts — Admin only
app.get('/api/contacts', (req, res) => {
  const { admin_password } = req.query;
  if (!ADMIN_PASSWORD || admin_password !== ADMIN_PASSWORD) {
    return res.status(401).json({ error: 'Unauthorized' });
  }
  db.all('SELECT * FROM contacts ORDER BY created_at DESC', [], (err, rows) => {
    if (err) return res.status(500).json({ error: 'DB error.' });
    res.json(rows);
  });
});

app.listen(PORT, () => {
  console.log(`AskAling backend running on http://localhost:${PORT}`);
});
