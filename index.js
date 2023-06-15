const express = require("express");
const app = express();
const path = require("path");

const serverIP = "192.168.0.101"; // Replace with your server's IP address

app.use(express.static(path.join(__dirname, "")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "control-head_test.html"));
});

const port = 3000; // Choose any available port number
app.listen(port, serverIP, () => {
  console.log(`Web server running at http://${serverIP}:${port}`);
});
