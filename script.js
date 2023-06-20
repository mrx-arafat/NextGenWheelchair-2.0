const ws = new WebSocket("ws://192.168.1.201:81");
console.log("Connected to WebSocket server");

ws.onopen = function() {
  console.log("WebSocket connection established");
};

ws.onmessage = function(event) {
  console.log("Received: " + event.data);
};

const video = document.getElementById('video')

Promise.all([
  faceapi.nets.tinyFaceDetector.loadFromUri('/models'),
  faceapi.nets.faceLandmark68Net.loadFromUri('/models'),
  faceapi.nets.faceRecognitionNet.loadFromUri('/models'),
  faceapi.nets.faceExpressionNet.loadFromUri('/models')
]).then(startVideo)

function startVideo() {
  navigator.mediaDevices.getUserMedia(
    { video: {} }
  ).then(stream => {
    video.srcObject = stream;
  }).catch(err => {
    console.error(err);
  });
}

const MOVEMENT_THRESHOLD = 50;
let initialNosePositionX = null;
let initialNosePositionY = null;

video.addEventListener('play', () => {
  const canvas = faceapi.createCanvasFromMedia(video)
  document.body.append(canvas)
  const displaySize = { width: video.width, height: video.height }
  faceapi.matchDimensions(canvas, displaySize)
  
  setInterval(async () => {
    const detections = await faceapi.detectAllFaces(video, new faceapi.TinyFaceDetectorOptions()).withFaceLandmarks().withFaceExpressions()
    const resizedDetections = faceapi.resizeResults(detections, displaySize)
    canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height)
    faceapi.draw.drawDetections(canvas, resizedDetections)
    faceapi.draw.drawFaceLandmarks(canvas, resizedDetections)
    faceapi.draw.drawFaceExpressions(canvas, resizedDetections)
    
    if (detections.length > 0) {
      const nosePositionX = detections[0].landmarks.getNose()[0].x;
      const nosePositionY = detections[0].landmarks.getNose()[0].y;
      
      if (initialNosePositionX === null && initialNosePositionY === null) {
        initialNosePositionX = nosePositionX;
        initialNosePositionY = nosePositionY;
      }
      
      const horizontalMovement = nosePositionX - initialNosePositionX;
      const verticalMovement = nosePositionY - initialNosePositionY;
      // console.log(horizontalMovement + " " + verticalMovement);
      let data = {
        direction: 'hello',
        angle: 'world'
      };
      if(Math.abs(horizontalMovement) > Math.abs(verticalMovement)) {
        // horizontalMovement
        if (Math.abs(horizontalMovement) > MOVEMENT_THRESHOLD) {
          if (horizontalMovement > 0) {
            console.log('right');
            data.direction = 'right';
          } else {
            console.log('left');
            data.direction = 'left';
          }
        } else {
          console.log('neutral');
          data.direction = 'neutral';
        }
      }
      else {
        // verticalMovement
        if (Math.abs(verticalMovement) > MOVEMENT_THRESHOLD) {
          if (verticalMovement > 0) {
            console.log('down');
            data.direction = 'down';
          } else {
            console.log('up');
            data.direction = 'up';
          }
        } else {
          console.log('neutral');
          data.direction = 'neutral';
        }
      }
      
      ws.send(JSON.stringify(data));
    }
    
  }, 100)
})
