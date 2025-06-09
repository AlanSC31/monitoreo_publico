const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());
const port = 3000;

// Conexión a MySQL
const db = mysql.createConnection({
  host: 'sql5.freesqldatabase.com',
  user: 'sql5782791',
  password: 'rWhInNN5gt',
  database: 'sql5782791'
});

// Ruta para obtener el conteo por zona
app.get('/api/conteo', (req, res) => {
  db.query('SELECT * FROM conteo_zona ORDER BY timestamp DESC LIMIT 50', (err, results) => {
    if (err) return res.status(500).json({ error: err });
    res.json(results);
  });
});

// Ruta para alertas de congestión
app.get('/api/alertas', (req, res) => {
  db.query('SELECT * FROM alertas_congestion ORDER BY timestamp DESC LIMIT 10', (err, results) => {
    if (err) return res.status(500).json({ error: err });
    res.json(results);
  });
});

// Ruta para tiempo promedio por zona
app.get('/api/tiempo', (req, res) => {
  db.query(`
    SELECT fila, columna,
       AVG(tiempo_segundos) AS tiempo_promedio,
       COUNT(DISTINCT persona_id) AS cantidad_personas
FROM tiempo_en_zona
GROUP BY fila, columna
  `, (err, results) => {
    if (err) return res.status(500).json({ error: err });
    res.json(results);
  });
});

// Ruta para detecciones por hora
app.get('/api/hora-pico', (req, res) => {
  db.query(`
    SELECT DATE_FORMAT(timestamp, '%H:%i') AS hora_minuto, COUNT(*) AS cantidad
    FROM conteo_zona
    GROUP BY hora_minuto
    ORDER BY hora_minuto
  `, (err, results) => {
    if (err) return res.status(500).json({ error: err });
    res.json(results);
  });
});



app.listen(port, () => {
  console.log(`Servidor corriendo en http://localhost:${port}`);
});
const path = require('path');
app.use(express.static(path.join(__dirname, 'public')));
