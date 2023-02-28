const messageBox = document.querySelector("#message-box");
const resetBtn = document.querySelector("#reset-btn");
const passwordInput = document.querySelector("#new-password");
const confirmPasswordInput = document.querySelector("#confirm-password");

resetBtn.addEventListener("click", async (event) => {
    event.preventDefault();

    const password = passwordInput.value;
    const confirmPassword = confirmPasswordInput.value;

    if (password !== confirmPassword) {
        showError("Passwords do not match");
        return;
    }

    const email = document.getElementById("email").value;

    // Use the userId variable in your JavaScript code
    console.log(`User Email: ${email}`);

    const response = await fetch("/api/auth/set_new_password", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
        showSuccess("Password reset successful");
    } else {
        const data = await response.json();
        const message = data.message || "Password reset failed";
        showError(message);
    }
});
