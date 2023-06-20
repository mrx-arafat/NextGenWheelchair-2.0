// Get the video, canvas, and button elements
const videoElement = document.getElementById("videoElement");
const canvas = document.createElement("canvas");
const button = document.getElementById("webcamButton");

// Set up the socket.io client
const socket = io();

// Keep track of whether the webcam is currently on or off
let webcamOn = false;

// Keep track of the interval that sends frames to the server
let frameInterval = null;

button.addEventListener("click", () => {
  if (webcamOn) {
    // If the webcam is on, stop the stream
    videoElement.srcObject.getTracks().forEach((track) => track.stop());
    clearInterval(frameInterval);
    button.textContent = "Start Webcam";
  } else {
    // If the webcam is off, start the stream
    startWebcam();
    button.textContent = "Stop Webcam";
  }

  webcamOn = !webcamOn;
});

// Function to start the webcam and send frames to the server
function startWebcam() {
  // Check if the browser supports the necessary APIs
  if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Access the camera
    navigator.mediaDevices
      .getUserMedia({ video: { width: 640, height: 480 } }) // Specify resolution
      .then((stream) => {
        // Set the camera stream as the source of the video element
        videoElement.srcObject = stream;

        // Play the videoElement to start showing the stream
        videoElement.play();

        // Set the videoElement's height and width to match the stream
        videoElement.width = stream.getTracks()[0].getSettings().width;
        videoElement.height = stream.getTracks()[0].getSettings().height;

        // Start a loop that sends frames to the server
        frameInterval = setInterval(() => {
          canvas
            .getContext("2d")
            .drawImage(
              videoElement,
              0,
              0,
              videoElement.width,
              videoElement.height
            );
          const dataUrl = canvas.toDataURL("image/jpeg", 0.8);
          socket.emit("stream", dataUrl);
        }, 1000 / 30); // Send 30 frames per second
      })
      .catch((error) => {
        console.error("Error accessing camera:", error);
      });
  } else {
    console.error("Camera access not supported by the browser.");
  }
}
