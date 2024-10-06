document.getElementById('continue_button').addEventListener('click', function(){
    //get the values
    const email = document.getElementById('email').value;
    const confirmEmail = document.getElementById('confirm_email').value;
    const password = document.getElementById('enter_password').value;

    console.log('Email: ', email);
    console.log('Confirm Email: ', confirmEmail);
    console.log('Password: ', password);

    if (email !== confirmEmail){
        alert("Emails do not match!");
    }else{
        alert("matched");
    }
});