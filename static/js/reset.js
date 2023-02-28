const form = document.querySelector("form");
const emailInput = document.querySelector("#email");
const messageBox = document.querySelector("#message-box");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = emailInput.value;

    // Send request to server to reset password
    const response = await fetch("/api/auth/reset_password_email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        // include email in request body as email field of JSON object
        body: JSON.stringify({ email }),
    });

    if (response.ok) {
        const data = await response.json();
        console.log(data);
        // Display success message to user
        const messageBox = document.getElementById("message-box");
        const successMessage = document.createElement("div");
        successMessage.classList.add(
            "bg-green-500",
            "text-white",
            "p-4",
            "rounded-lg",
            "mb-4"
        );
        successMessage.textContent =
            "Check your email for instructions to reset your password.";
        messageBox.appendChild(successMessage);
    } else {
        // Display error message to user
        showError("Failed to reset password. Please try again.");
    }
});
