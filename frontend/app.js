const express = require('express');
const axios = require('axios');
const path = require('path');
const app = express();

// Fix: Use environment variable with fallback
const API_URL = process.env.API_URL || 'http://localhost:8000';
const PORT = process.env.PORT || 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

// Fix: Add health check endpoint
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'healthy' });
});

app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`);
    res.json(response.data);
  } catch (err) {
    console.error('Submit error:', err.message);
    res.status(500).json({ error: "API unavailable" });
  }
});

app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`);
    res.json(response.data);
  } catch (err) {
    console.error('Status error:', err.message);
    res.status(500).json({ error: "API unavailable" });
  }
});

app.listen(PORT, () => {
  console.log(`Frontend running on port ${PORT}`);
  console.log(`API URL configured as: ${API_URL}`);
});