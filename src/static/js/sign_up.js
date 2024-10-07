const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{8,20}$/;
const upperRegex = /[A-Z]/;
const digitRegex = /(?=.*\d)/;
const lowerRegex = /[a-z]/;
const specialRegex = /[\W]/; 

// (               # Start of group
//     (?=.*\d)    # must contains one digit from 0-9
//     (?=.*[a-z]) # must contains one lowercase characters
//     (?=.*[\W])  # must contains at least one special character
//     .           # match anything with previous condition checking
//     {8,20}      # length at least 8 characters and maximum of 20
//   )             # End of group

//----------------------------------------------------------------------------//
// REGEX CHECKER
function checkAllRegex(password) {
  if (passwordRegex.test(password)) {
    console.log("Password is valid");
    return true;
  } else {
    console.log("Password is invalid.");
    return false;
  }
}

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

//----------------------------------------------------------------------------//
// HANDLES PASSWORD INPUT FOCUS

$('input[name="password"]').on("focus", function() {
  $('.password-req-container').addClass("active");
});

$('input[name="password"]').on("blur", function() {
  $('.password-req-container').removeClass("active");
});

$('input[name="password"]').on("keyup", function() {
  checkRegex(lowerRegex, "lower")
  checkRegex(upperRegex, "upper")
  checkRegex(digitRegex, "digit")
  checkRegex(specialRegex, "special")
  checkLength(8, "length")
});

$('input[type="submit"]').on("click", function(e) {
  e.preventDefault();
  const email = $('input[name=email]').val()
  const confirmEmail = $('input[name=confirm_email]').val()
  const password = $('input[name=password]').val()
  const checkstate = $('input[name=policyagree]').prop("checked")

  console.log("Email: ", email);
  console.log("Confirm Email: ", confirmEmail);
  console.log("Password: ", password);

  if (email.length === 0 || confirmEmail.length === 0 || password.length === 0) {
    alert("Invalid Length");
    return;
  }
  if (email !== confirmEmail) {
    alert("Emails do not match!");
    return;
  }
  if (!checkAllRegex(password)) {
    alert("Password is invalid");
    return;
  }
  if (!checkstate) {
    alert("You must agree to the terms")
    return;
  }
});