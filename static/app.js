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

// FUNCTION TO PERFORM SEARCH NEW
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('search-form');
  const resultsDiv = document.getElementById('results');

  // Function to perform the search
  function performSearch(query) {
      fetch(`/search?query=${encodeURIComponent(query)}`)
          .then(response => {
              if (!response.ok) {
                  throw new Error("Search failed");
              }
              return response.json();
          })
          .then(data => {
              resultsDiv.innerHTML = ''; // Clear previous results

              if (data.error) {
                  resultsDiv.textContent = data.error;
              } else if (data.length === 0) {
                  resultsDiv.textContent = "No results found.";
              } else {
                  data.forEach(movie => {
                      const div = document.createElement('div');
                      div.textContent = `Title: ${movie.title}, Director: ${movie.director}, Year: ${movie.year}`;
                      resultsDiv.appendChild(div);
                  });
              }
          })
          .catch(error => {
              console.error('Error:', error);
              resultsDiv.textContent = "An error occurred. Please try again.";
          });
  }

  // Handle form submission
  form.addEventListener('submit', (event) => {
      event.preventDefault(); // Prevent the default form submission
      const query = form.querySelector('.search-box').value;
      performSearch(query);
  });
});