const passwordRegex = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[\W]).{6,20}$/;

// (           # Start of group
//     (?=.*\d)      #   must contains one digit from 0-9
//     (?=.*[a-z])       #   must contains one lowercase characters
//     (?=.*[\W])        #   must contains at least one special character
//                 .     #     match anything with previous condition checking
//                   {8,20}  #        length at least 8 characters and maximum of 20 
//   )           # End of group

let check = false;
let emailCheck = false;
let passwordCheck = false;

function regexCheck(password) {
    if(passwordRegex.test(password)){
        console.log("Password is valid");
        return true;
    } else {
        console.log("Password is invalid.");
        return false;
    }
}

document.getElementById('continue_button').addEventListener('click', function(){
    //get the values
    const email = document.getElementById('email').value;
    const confirmEmail = document.getElementById('confirm_email').value;
    const password = document.getElementById('enter_password').value;

    console.log('Email: ', email);
    console.log('Confirm Email: ', confirmEmail);
    console.log('Password: ', password);

    // check emails if empty
    
    if (email !== confirmEmail){
        alert("Emails do not match!");
        
    }else{
        alert("matched");
        emailCheck = true;
    }
    if (regexCheck(password)) {
        alert("Password is valid!")
        passwordCheck = true;
    } else {
        alert("invalid password")
    }
    
});

//document.getElementById("check").addEventListener')