const sqlite3 = require('sqlite3').verbose();

const db = new sqlite3.Database('path/to/your/database.db', err => {
  if (err) {
    console.error('Error connecting to database:', err);
  } else {
    console.log('Connected to database');
  }
});

module.exports = db;
