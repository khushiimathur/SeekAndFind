let otp = 0;
let userInput;
async function sendData() {
    userInput = document.getElementById('email').value;
    console.log(userInput);
    if (userInput.endsWith("@igdtuw.ac.in")){
        const response = await fetch('https://seekandfind.onrender.com/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_input: userInput }),
        });
    
        const result = await response.json();
        otp = result['result'];
    }
    else {
        alert("Please enter valid igdtuw Email ID only")
    }
    
};

async function verify(){
    console.log(otp);
    let check_otp = document.getElementById('otp').value ;    //= result.result;
    if(check_otp == otp) {
        //redirect to dashboard 
        window.location.href = "/dashboard"; 
        
    }else {
        alert("Invalid OTP. Please try again");
}


}

