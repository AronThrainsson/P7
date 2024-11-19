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