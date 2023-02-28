const form = document.querySelector("form");
const email = document.getElementById("email");
const password = document.getElementById("password");
const button = document.getElementById("create-account-btn");
const emailError = document.getElementById("email-error");
const passwordError = document.getElementById("password-error");

form.addEventListener("submit", (event) => {
    event.preventDefault();

    // Validate email and password
    if (email.value.trim() === "") {
        emailError.textContent = "Email is required";
    } else {
        emailError.textContent = "";
    }

    if (password.value.trim() === "") {
        passwordError.textContent = "Password is required";
    } else {
        passwordError.textContent = "";
    }

    // If there are no errors, submit the form
    if (emailError.textContent === "" && passwordError.textContent === "") {
        button.disabled = true;
        button.textContent = "Creating account...";
        const data = {
            email: email.value,
            password: password.value,
        };
        fetch("/api/auth/register", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
            .then((response) => {
                if (response.ok) {
                    // Handle successful sign up
                    response.json().then((data) => {
                        console.log("User signed up successfully", data);
                        const token = data.token;
                        // Store the token in local storage
                        localStorage.setItem("jwtToken", token);

                        // generate an api key
                        generateAPIKey();

                        // Redirect to the home page
                        window.location.href = "/home";
                    });
                } else {
                    // Handle error
                    console.log("Error signing up user");
                    showError("Invalid username or password");
                }
            })
            .catch((error) => {
                // Handle network error
                console.log("Network error:", error);
                showError("Network error");
            })
            .finally(() => {
                button.disabled = false;
                button.textContent = "Create Account";
            });
    }
});

async function generateAPIKey() {
    const response = await sendAuthenticatedRequest("POST", "/api/key/create");
    // parse the request body for api_secret key and store it in localstorage
    response.json().then((data) => {
        console.log("API key generated successfully", data);
        const api_secret = data.api_secret;
        // Store the token in local storage
        localStorage.setItem("api_secret", api_secret);
    });
}
