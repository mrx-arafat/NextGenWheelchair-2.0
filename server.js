const https = require("https");
const fs = require("fs");
const express = require("express");
const app = express();
const serverIP = "192.168.0.101";
const port = 3000;
app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

https
  .createServer(
    {
      key: fs.readFileSync("server.key"),
      cert: fs.readFileSync("server.cert"),
    },
    app
  )
  .listen(port, serverIP, () => {
    console.log(`Web server running at http://${serverIP}:${port}`);
  });
