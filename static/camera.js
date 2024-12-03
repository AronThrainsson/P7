const cameraFeed = document.getElementById('camera-feed');
const captureButton = document.getElementById('capture-button');
const canvas = document.getElementById('snapshot');

let stream;

// Function to start the camera
navigator.mediaDevices
  .getUserMedia({ video: { facingMode: 'environment' } }) // Use rear camera
  .then((mediaStream) => {
    stream = mediaStream;
    cameraFeed.srcObject = stream;
  })
  .catch((err) => {
    console.error('Error accessing camera:', err);
    alert('Unable to access camera. Please check your permissions.');
  });

// Function to capture the image
captureButton.addEventListener('click', () => {
  const context = canvas.getContext('2d');
  canvas.width = cameraFeed.videoWidth;
  canvas.height = cameraFeed.videoHeight;
  context.drawImage(cameraFeed, 0, 0, canvas.width, canvas.height);

  // Stop the camera
  stream.getTracks().forEach((track) => track.stop());

  // Convert the canvas to a Base64 image
  const imageData = canvas.toDataURL('image/png');

  // Send the image to the backend
  fetch('/scan', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ image: imageData }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        // Store scanned text temporarily and redirect to the home page
        localStorage.setItem('scannedText', data.text);
        window.location.href = '/';
      } else {
        alert('Error scanning the image. Please try again.');
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
});