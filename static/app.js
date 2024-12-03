// Populate the search box with scanned text when on the home page
document.addEventListener('DOMContentLoaded', () => {
    const scannedText = localStorage.getItem('scannedText');
    if (scannedText) {
      const searchBox = document.getElementById('keyword');
      if (searchBox) {
        searchBox.value = scannedText; // Set the scanned text in the search box
        localStorage.removeItem('scannedText'); // Clear the stored text
      }
    }
  });