// Get the video element
const videoElement = document.getElementById("videoElement");

// Check if the browser supports the necessary APIs
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  // Access the camera
  navigator.mediaDevices
    .getUserMedia({ video: true })
    .then((stream) => {
      // Set the camera stream as the source of the video element
      videoElement.srcObject = stream;
    })
    .catch((error) => {
      console.error("Error accessing camera:", error);
    });
} else {
  console.error("Camera access not supported by the browser.");
}
