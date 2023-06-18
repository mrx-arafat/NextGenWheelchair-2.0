const https = require("https");
const fs = require("fs");
const express = require("express");
const app = express();
const path = require("path");

const serverIP = "192.168.0.102"; // Replace with your server's IP address

app.use(express.static(path.join(__dirname, "/")));
app.get("/control-head_test.html", (req, res) => {
  res.sendFile(path.join(__dirname, "control-head_test.html"));
});

const port = 3000; // Choose any available port number

https
  .createServer(
    {
      key: fs.readFileSync("server.key"), // path to your key file
      cert: fs.readFileSync("server.cert"), // path to your cert file
    },
    app
  )
  .listen(port, serverIP, () => {
    console.log(`Web server running at https://${serverIP}:${port}`);
  });
