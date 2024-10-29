// Variables
const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,20}$/;
const upperRegex = /[A-Z]/;
const digitRegex = /(?=.*\d)/;
const lowerRegex = /[a-z]/;
const specialRegex = /[\W]/; 

const emailRegex = /.+[@].+(?<![.])$/;

let passwordShown = false;
let passwordEntropy = 0;

// (               # Start of group
//     (?=.*\d)    # must contains one digit from 0-9
//     (?=.*[a-z]) # must contains one lowercase characters
//     (?=.*[\W])  # must contains at least one special character
//     .           # match anything with previous condition checking
//     {8,20}      # length at least 8 characters and maximum of 20
//   )             # End of group

// Regex and Length Checks
function checkRegex(regex, name) {
  if ($('input[name="password"]').val().match(regex)) {
    $(`.${name}`).removeClass("invalid")
    $(`.${name}`).addClass("valid")
    $(`.${name} .fa-xmark`).removeClass("active")
    $(`.${name} .fa-check`).addClass("active")
  } else {
    $(`.${name}`).addClass("invalid")
    $(`.${name}`).removeClass("valid")
    $(`.${name} .fa-xmark`).addClass("active")
    $(`.${name} .fa-check`).removeClass("active")
  }
}

function checkLength(length, name) {
  if ($('input[name="password"]').val().length >= length) {
    $(`.${name}`).removeClass("invalid")
    $(`.${name}`).addClass("valid")
    $(`.${name} .fa-xmark`).removeClass("active")
    $(`.${name} .fa-check`).addClass("active")
  } else {
    $(`.${name}`).addClass("invalid")
    $(`.${name}`).removeClass("valid")
    $(`.${name} .fa-xmark`).addClass("active")
    $(`.${name} .fa-check`).removeClass("active")
  }
}

// Calculate password entropy
function calculateEntropy() {
  let password = $('input[name="password"]').val();
  let length = password.length;
  let currentPoolSize = 0;
  if (password.match(upperRegex)) currentPoolSize += 26;
  if (password.match(lowerRegex)) currentPoolSize += 26;
  if (password.match(digitRegex)) currentPoolSize += 10;
  if (password.match(specialRegex)) currentPoolSize += 32;

  passwordEntropy = length * Math.log2(currentPoolSize);

  $('.strength-current').removeClass("great good ok weak veryweak none")

  if (passwordEntropy >= 60) $('.strength-current').addClass("great")
  else if (passwordEntropy >= 40) $('.strength-current').addClass("good")
  else if (passwordEntropy >= 20) $('.strength-current').addClass("ok")
  else if (passwordEntropy >= 10) $('.strength-current').addClass("weak")
  else if (passwordEntropy > 0) $('.strength-current').addClass("veryweak")
  else $('.strength-current').addClass("none")
}

// Toggle password visibility
$('button').on("click", function(e){
  e.preventDefault();
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
});

// Check for valid email (not repeats, handled by db)
$('input[type="email"]').on("blur", function() {
  if (!$(this).val().match(emailRegex)) $(this).parent().parent().addClass("invalid")
});

$('input[type="email"]').on("keyup", function() {
  if ($(this).val().match(emailRegex)) $(this).parent().parent().removeClass("invalid")
});

// Check if there is a valid username (not repeats, handled by db)
$('input[name="username"]').on("blur", function() {
  if ($(this).val().length == 0) $(this).parent().parent().addClass("invalid")
});

$('input[name="username"]').on("keyup", function() {
  if ($(this).val().length != 0) $(this).parent().parent().removeClass("invalid")
});

// Check if there is a password
$('input[name="password"]').on("blur", function() {
  if ($(this).val().length == 0) $(this).parent().parent().parent().addClass("invalid")
});

$('input[name="password"]').on("keyup", function() {
  if ($(this).val().length != 0) $(this).parent().parent().parent().removeClass("invalid")
});

// Regex and Entropy Checking
$('input[name="password"]').on("keyup", function() {
  checkRegex(lowerRegex, "lower")
  checkRegex(upperRegex, "upper")
  checkRegex(digitRegex, "digit")
  checkRegex(specialRegex, "special")
  checkLength(8, "length")

  calculateEntropy()
});