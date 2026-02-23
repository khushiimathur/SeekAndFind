let otp = 0;
let userInput;
async function sendData() {
    console.log("Send OTP clicked");
    userInput = document.getElementById('email').value;
    
    if (userInput.endsWith("@igdtuw.ac.in")){
        const response = await fetch('/process', {
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
    
    let check_otp = document.getElementById('otp').value ;    //= result.result;
    if(check_otp == otp) {
        //redirect to dashboard 
        window.location.href = "/dashboard"; 
        
    }else {
        alert("Invalid OTP. Please try again");
}


}

async function handleForm(formId, type) {
    const form = document.getElementById(formId);

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);
        formData.append("type", type);

        try {
            const res = await fetch("/submit", {
                method: "POST",
                body: formData
            });

            const data = await res.json();

            if (res.ok) {
                alert("Submitted successfully!");
                form.reset();
            } else {
                alert(data.error || "Error occurred");
            }

        } catch (err) {
            console.error(err);
            alert("Server error");
        }
    });
}

handleForm("lostForm", "lost");
handleForm("foundForm", "found");