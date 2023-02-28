// function to check user's billing status, returns true if user is active or trialing
function checkBillingStatus() {
    // access user billing status stored in local storage
    const userDict = JSON.parse(localStorage.getItem("user"));
    // get billing status
    const billingStatus = userDict["billing_status"];
    if (billingStatus === "active" || billingStatus === "trialing") {
        return true;
    }
    return false;
}
