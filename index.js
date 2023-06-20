const https = require("https");
const fs = require("fs");
const express = require("express");
const app = express();
const path = require("path");
const socketIo = require("socket.io");

const serverIP = "10.103.129.60"; // Replace with your server's IP address

app.use(express.static(path.join(__dirname, "/")));
app.get("/camt.html", (req, res) => {
  res.sendFile(path.join(__dirname, "camt.html"));
});

const port = 3000; // Choose any available port number

const server = https.createServer(
  {
    key: fs.readFileSync("server.key"), // path to your key file
    cert: fs.readFileSync("server.cert"), // path to your cert file
  },
  app
);

const io = socketIo(server);

io.on("connection", (socket) => {
  console.log("A user connected");

  // When a message with the 'stream' event is received, broadcast it to all other clients
  socket.on("stream", (image) => {
    socket.broadcast.emit("stream", image);
  });
});

server.listen(port, serverIP, () => {
  console.log(`Web server running at https://${serverIP}:${port}`);
});
