/*
This function redirects the user when they hit ENTER on the navbar search bar.
*/

function redirect_to_search_page(e) {
  // Redirect when user hits ENTER
  console.log(JSON.stringify(e));
  if (e.keyCode == 13) {
    search_term = document.querySelector('input[name="nav-search"]').value;
    if (e.shiftKey) window.location = '/search?e=s&t=' + search_term;
    else window.location = '/search?e=cs&t=' + search_term;
  }
}