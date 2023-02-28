function getJwtToken() {
    // Read the JWT token from the localStorage
    return localStorage.getItem("jwtToken");
}

window.onload = function () {
    const jwtToken = getJwtToken();
    if (!jwtToken) {
        // Redirect the user to the signup page if there is no JWT token
        window.location.href = "/signup";
        return;
    }
    // // Send a request to the protected endpoint to check if the token is valid
    // sendAuthenticatedRequest("GET", "/playground")
    //     .then((response) => {
    //         if (response.status === 401) {
    //             // Redirect the user to the login page if the token is not valid
    //             window.location.href = "/login";
    //         }
    //     })
    //     .catch((error) => console.error(error));
};
