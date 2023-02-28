function copyToClipboard() {
    var outputElement = document.getElementById("output");
    outputElement.select();
    document.execCommand("copy");
}

const form = document.querySelector("form");
form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const url = document.querySelector("#website-url").value;
    const senderInfo = document.querySelector("#sender-info").value;
    const recipientInfo = document.querySelector("#recipient-info").value;
    const prompt = document.querySelector("#prompt").value;
    const wordCount = document.querySelector("#word-count").value;
    const generateBtn = document.getElementById("generate-email-btn");
    const generateBtnText = document.getElementById("generate-email-btn-text");
    generateBtn.disabled = true;
    generateBtnText.textContent = "Generating...";

    const requestBody = {
        url,
        sender_info: senderInfo,
        recipient_info: recipientInfo,
        prompt,
        word_count: wordCount,
    };

    // // get API secret from local storage, if undefined then call getAPIKey to get it
    // let apiSecret = localStorage.getItem("api_secret");
    // if (apiSecret === null) {
    //     apiSecret = await getAPIKey();
    // }

    const response = await fetch("/api/demo/generate_email", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            // Authorization: `Bearer ${apiSecret}`,
        },
        body: JSON.stringify(requestBody),
    });

    const responseBody = await response.text();
    console.log(responseBody);
    const outputElement = document.querySelector("#output");
    if (response.ok) {
        showOutputText(responseBody);
    } else {
        // outputElement.textContent = "Error: " + responseBody;
        console.log("Error: " + responseBody);
        showError(responseBody);
    }
    generateBtn.disabled = false;
    generateBtnText.textContent = "Generate Email";

    function showOutputText(text) {
        const outputElement = document.getElementById("output");
        outputElement.value = "";
        const words = text.split(" ");
        let i = 0;
        const intervalId = setInterval(() => {
            if (i >= words.length) {
                clearInterval(intervalId);
                return;
            }
            outputElement.value += words[i] + " ";
            i++;
        }, 80);

        // access user billing status stored in local storage
        const userDict = JSON.parse(localStorage.getItem("user"));

        // only redirect if user billing status is not active and not trialing
        if (
            userDict["billing_status"] !== "active" &&
            userDict["billing_status"] !== "trialing"
        ) {
            // redirect to pricing page after the animation is done
            // calculate how long it will take to print all words
            const timeToPrint = words.length * 80;
            setTimeout(() => {
                window.location.href = "/pricing";
            }, timeToPrint + 3000);
        }
    }
});

function fillPrompt() {
    var promptTextarea = document.getElementById("prompt");
    promptTextarea.value = promptTextarea.placeholder;
}
