/*
This function redirects the user when they hit ENTER on the navbar search bar.
*/

function redirect_to_search_page(e) {
  // Redirect when user hits ENTER
  if (e.keyCode == 13) {
    search_term = document.querySelector('input[name="nav-search"]').value;
    window.location = '/search?title=' + search_term;
  }
}