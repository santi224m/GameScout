/*
This function changes the system requirements tab on button press
*/

function change_tab(tab) {
  $(".windows, .mac, .linux").removeClass("active")
  $(`.${tab}`).addClass("active")
}