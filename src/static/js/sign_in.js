// const rmCheck = document.getElementById("rememberMe"),
//     emailInput = document.getElementById("email");

// if (localStorage.checkbox && localStorage.checkbox !== "") {
//   rmCheck.setAttribute("checked", "checked");
//   emailInput.value = localStorage.username;
// } else {
//   rmCheck.removeAttribute("checked");
//   emailInput.value = "";
// }

// function lsRememberMe() {
//   if (rmCheck.checked && emailInput.value !== "") {
//     localStorage.username = emailInput.value;
//     localStorage.checkbox = rmCheck.value;
//   } else {
//     localStorage.username = "";
//     localStorage.checkbox = "";
//   }
// }
let passwordShown = false;

function togglePasswordVis() {
  if (passwordShown) { 
    $('input[name="password"]').attr("type", "password");
    $('.normal').addClass("active");
    $('.slash').removeClass("active");
    passwordShown = false;
  } else {
    $('input[name="password"]').attr("type", "text");
    $('.normal').removeClass("active");
    $('.slash').addClass("active");
    passwordShown = true;
  }
}

$('button').on("click", function(e){
  e.preventDefault();
  togglePasswordVis();
});

