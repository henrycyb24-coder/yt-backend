const express = require("express");
const cors = require("cors");
const { exec } = require("child_process");

const app = express();
app.use(cors());
app.use(express.json());

app.post("/download", (req, res) => {
  const url = req.body.url;

  exec(`yt-dlp -f best -g ${url}`, (err, stdout, stderr) => {
    if (err) return res.status(500).send(stderr);
    res.json({ downloadUrl: stdout.trim() });
  });
});

app.listen(10000, () => console.log("Server running"));
