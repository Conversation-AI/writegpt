function getJwtToken() {
    // Read the JWT token from the localStorage
    return localStorage.getItem("jwtToken");
}

function sendAuthenticatedRequest(method, url, data) {
    const jwtToken = getJwtToken();
    if (!jwtToken) {
        // Redirect the user to the login page if there is no JWT token
        console.log("No JWT token found");
        return;
    }
    // Set the Authorization header to the JWT token
    const headers = { Authorization: `Bearer ${jwtToken}` };
    // Send the authenticated request
    return fetch(url, {
        method,
        headers,
        body: JSON.stringify(data),
    });
}

async function getAPIKey() {
    const response = await sendAuthenticatedRequest("GET", "/api/key/list");
    if (response.ok) {
        const data = await response.json();
        const secret = data.api_keys[0].secret;
        localStorage.setItem("api_secret", secret);
        console.log("API key found successfully", secret);
        return secret;
    } else {
        console.log("Error getting API key");
        throw new Error("Failed to get API key");
    }
}
