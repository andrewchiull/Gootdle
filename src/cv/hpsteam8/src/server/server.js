const express = require("express");
const cors = require("cors");

const app = express();

app.use(cors()); // Enable CORS for all routes
app.use(express.json()); // Parse JSON request body

app.get("/", (req, res) => {
  res.send("Hello from Express!");
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
