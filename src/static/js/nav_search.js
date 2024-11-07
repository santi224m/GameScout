/*
This function redirects the user when they hit ENTER on the navbar search bar.
*/

function redirect_to_search_page(e, button) {
  // Redirect when user hits ENTER
  if (e.keyCode == 13 || button) {
    search_term = document.querySelector('input[name="nav-search"]').value;
    if (e.shiftKey) window.location = '/search?e=cs&t=' + search_term;
    else window.location = '/search?e=s&t=' + search_term;
  }
}

let active = false;

function toggleDropdown() {
  if (active) {
    active = false;
    $(".nav-account").removeClass("active");
    $(".dropdown").removeClass("active");
  } else {
    active = true;
    $(".nav-account").addClass("active");
    $(".dropdown").addClass("active");
  }
};


$(".nav-account").on("click", function() {
  toggleDropdown()
});


$(".nav-account").on("blur", function(e) {
  if (active && (e.relatedTarget == null || e.relatedTarget.tagName != "A")) toggleDropdown()
});
