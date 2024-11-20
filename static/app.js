const menu = document.querySelector('#mobile-menu');
const menuLinks = document.querySelector('.navbar_menu');

menu.addEventListener('click', function() {
  menu.classList.toggle('is-active');
  menuLinks.classList.toggle('active');
});

function openInNewWindow() {
  window.open('https://www.unicef.org/parenting/food-nutrition/feeding-your-baby-6-12-months', '_blank');
}

//Function to open the link in a new tab
document.addEventListener('DOMContentLoaded', () => {
  // Select all buttons with the "open-link" class
  const buttons = document.querySelectorAll('.open-link');

  // Loop through each button and add a click event listener
  buttons.forEach(button => {
      button.addEventListener('click', () => {
          const url = button.getAttribute('data-url'); // Retrieve the URL from the data attribute
          window.open(url, '_blank'); // Open the link in a new window or tab
      });
  });
});

// Function to handle "Most searched" button clicks
function search(query) {
  const form = document.getElementById('search-form');
  const searchBox = form.querySelector('.search-box');
  searchBox.value = query; // Set the query value
  form.submit(); // Submit the form
}

// Automatically handle Enter key in the search box
document.querySelector('.search-box').addEventListener('keypress', function (event) {
  if (event.key === 'Enter') {
      event.preventDefault(); // Prevent default behavior
      document.getElementById('search-form').submit(); // Submit the form
  }
});

// Add event listeners to "Most searched" buttons
document.querySelectorAll('.search-button').forEach(button => {
  button.addEventListener('click', function () {
      const query = this.getAttribute('data-query');
      search(query);
  });
});