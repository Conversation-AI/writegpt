const form = document.querySelector("form");
const emailInput = document.querySelector("#email");
const passwordInput = document.querySelector("#password");
const button = document.getElementById("login-btn");

form.addEventListener("submit", (event) => {
    event.preventDefault();

    button.disabled = true;
    button.textContent = "Logging in...";

    const email = emailInput.value;
    const password = passwordInput.value;

    const data = {
        email: email,
        password: password,
    };

    fetch("/api/auth/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    })
        .then((response) => {
            if (response.ok) {
                // Handle successful login
                response.json().then((data) => {
                    console.log("User logged in successfully", data);
                    const token = data.token;
                    // Store the token in local storage
                    localStorage.setItem("jwtToken", token);

                    // Redirect to the home page
                    window.location.href = "/home";
                });
            } else {
                // Handle error
                console.log("Error logging in user");
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
            button.textContent = "Log in";
        });
});
