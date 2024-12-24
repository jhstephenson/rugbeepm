// Main JavaScript file
document.addEventListener('DOMContentLoaded', function() {
   // CSRF token setup for AJAX requests
   function getCookie(name) {
       let cookieValue = null;
       if (document.cookie && document.cookie !== '') {
           const cookies = document.cookie.split(';');
           for (let i = 0; i < cookies.length; i++) {
               const cookie = cookies[i].trim();
               if (cookie.substring(0, name.length + 1) === (name + '=')) {
                   cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                   break;
               }
           }
       }
       return cookieValue;
   }

   const csrftoken = getCookie('csrftoken');

   $.ajaxSetup({
       beforeSend: function(xhr, settings) {
           if (!this.crossDomain) {
               xhr.setRequestHeader("X-CSRFToken", csrftoken);
           }
       }
   });
});