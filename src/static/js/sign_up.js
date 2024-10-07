const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{6,20}$/;

// (           # Start of group
//     (?=.*\d)      #   must contains one digit from 0-9
//     (?=.*[a-z])       #   must contains one lowercase characters
//     (?=.*[\W])        #   must contains at least one special character
//                 .     #     match anything with previous condition checking
//                   {8,20}  #        length at least 8 characters and maximum of 20 
//   )           # End of group

var getInput = document.getElementById("enter_password");
var checkDigit = document.getElementById("number");
var checkLower = document.getElementById("letter");
var checkUpper = document.getElementById("capital");
var checkMin = document.getElementById("length");
var checkSpecial = document.getElementById("special");
var continueButton = document.getElementById('continue_button');

var regexBlock = document.getElementById("message");
let emailCheck = false;
let passwordCheck = false;

let origin = window.location.origin;

//----------------------------------------------------------------------------//
// REGEX CHECKER
function regexCheck(password) {
    if(passwordRegex.test(password)){
        console.log("Password is valid");
        return true;
    } else {
        console.log("Password is invalid.");
        return false;
    }
}


//----------------------------------------------------------------------------//
// HANDLES PASSWORD INPUT FOCUS

// when user clicks this pops up
getInput.onfocus = function () {
    regexBlock.style.display = "block";
}
// when user clicks off the password input, the block disappears
getInput.onblur = function () {
    regexBlock.style.display = "none";
}
getInput.onkeyup = function () {
    var myInput = document.getElementById("enter_password");
    var checkUpper = document.getElementById("capital");
    var checkDigit = document.getElementById("number");
    // we are gonna check

  var upperCaseLetters = /[A-Z]/g;
  if(myInput.value.match(upperCaseLetters)) {
    checkUpper.classList.remove("invalid");
    checkUpper.classList.add("valid");
  } else {
    checkUpper.classList.remove("valid");
    checkUpper.classList.add("invalid");
  }

  var digitPattern = /(?=.*\d)/;
  if(myInput.value.match(digitPattern)) {
    checkDigit.classList.remove("invalid");
    checkDigit.classList.add("valid");
  } else {
    checkDigit.classList.remove("valid");
    checkDigit.classList.add("invalid");
  }

  var lowerCaseLetters = /[a-z]/g;
  if(myInput.value.match(lowerCaseLetters)){
    checkLower.classList.remove("invalid");
    checkLower.classList.add("valid");
  } else {
    checkLower.classList.remove("valid");
    checkLower.classList.add("invalid");
  }
  
  if(myInput.value.length >= 8) {
    checkMin.classList.remove("invalid");
    checkMin.classList.add("valid");
  } else {
    checkMin.classList.remove("valid");
    checkMin.classList.add("invalid");
  }

  var specialPattern = /[\W]/;
  if(myInput.value.match(specialPattern)) {
    checkSpecial.classList.remove("invalid");
    checkSpecial.classList.add("valid");
  } else {
    checkSpecial.classList.remove("valid");
    checkSpecial.classList.add("invalid");
  }
}
    
//----------------------------------------------------------------------------//
// CONTINUE BUTTON
document.getElementById('continue_button').addEventListener('click', function(){
    //get the values
    const email = document.getElementById('email').value;
    const confirmEmail = document.getElementById('confirm_email').value;
    const password = document.getElementById('enter_password').value;
    let checkstate = document.getElementById("check").value;

    console.log('Email: ', email);
    console.log('Confirm Email: ', confirmEmail);
    console.log('Password: ', password);

    // check emails if empty
    if(email.length === 0 || confirmEmail.length === 0 || password.length === 0){
        alert("Invalid")
    }
    if (email !== confirmEmail){
        alert("Emails do not match!");
    }else{
        emailCheck = true;
    }
    if (regexCheck(password)) {
        alert("Password is valid!")
        passwordCheck = true;
    } else {
        alert("invalid password")
    }
    

  
    // check if the email,confirm, and password is acceptable
    

    // if it is we send the user to the signin page. 

});