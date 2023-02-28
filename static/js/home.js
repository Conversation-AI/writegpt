// Check for JWT token in local storage
const jwtToken = localStorage.getItem("jwtToken");

// If JWT token is not present, redirect user to login page
if (!jwtToken) {
    window.location.href = "/login";
}
