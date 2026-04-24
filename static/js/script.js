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
    // legacy function kept for compatibility
    let check_otp = document.getElementById('otp').value;
    if(check_otp == otp){
        window.location.href = "/dashboard";
    } else {
        alert("Invalid OTP. Please try again");
    }
}

// new server-based verification
async function verify2(){
    const check_otp = document.getElementById('otp').value;
    try {
        const resp = await fetch('/verify-otp', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ otp: check_otp })
        });
        if (resp.ok) {
            window.location.href = "/dashboard";
        } else {
            alert("Invalid OTP. Please try again");
        }
    } catch (err) {
        console.error(err);
        alert("Verification failed");
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

// attach form handlers only if forms exist on this page
window.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('lostForm')) {
        handleForm("lostForm", "lost");
    }
    if (document.getElementById('foundForm')) {
        handleForm("foundForm", "found");
    }
});
