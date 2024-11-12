// app/static/js/scripts.js

/* =====================================================
   Custom JavaScript for BookExchange
   ===================================================== */

/* 
 * Automatically close flash messages after a specified time (e.g., 5 seconds)
 */
document.addEventListener('DOMContentLoaded', function () {
    // Select all flash messages
    var flashMessages = document.querySelectorAll('.alert');

    flashMessages.forEach(function (alert) {
        // Set a timeout to remove the alert after 5 seconds (5000 milliseconds)
        setTimeout(function () {
            // Use Bootstrap's alert dismissal method
            $(alert).alert('close');
        }, 5000);
    });
});


document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        var target = document.querySelector(this.getAttribute('href'));
        if(target) {
            window.scrollTo({
                top: target.offsetTop - 70, // Adjust offset for fixed navbar
                behavior: 'smooth'
            });
        }
    });
});


/* 
 * Additional Custom JavaScript Functions
 * Add any other JavaScript functionalities as needed
 */

/* 
 * Example: Toggle Password Visibility (if you have password fields)
 * Ensure that you have an element with class 'toggle-password' and data-target attribute
 */
/*
document.querySelectorAll('.toggle-password').forEach(function(element) {
    element.addEventListener('click', function (e) {
        e.preventDefault();
        var target = this.getAttribute('data-target');
        var passwordField = document.querySelector(target);
        if(passwordField) {
            if(passwordField.type === 'password') {
                passwordField.type = 'text';
                this.innerHTML = '<i class="fas fa-eye-slash"></i>';
            } else {
                passwordField.type = 'password';
                this.innerHTML = '<i class="fas fa-eye"></i>';
            }
        }
    });
});
*/
