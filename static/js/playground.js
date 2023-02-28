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
    hideMessageBox();

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

    // check billing status, configure endpointURL and headers object accordingly
    let endpointURL = "/api/demo/generate_email";
    let headersObj = {
        "Content-Type": "application/json",
    };

    isPaid = checkBillingStatus();
    if (isPaid) {
        endpointURL = "/api/v1/generate_email";
        // get apiSecret from local storage and add it to headers object
        let apiSecret = localStorage.getItem("api_secret");
        if (apiSecret === null) {
            apiSecret = await getAPIKey();
        }
        headersObj = {
            "Content-Type": "application/json",
            Authorization: `Bearer ${apiSecret}`,
        };
    }

    const response = await fetch(endpointURL, {
        method: "POST",
        headers: headersObj,
        body: JSON.stringify(requestBody),
    });

    const responseBody = await response.text();
    console.log(responseBody);
    const outputElement = document.querySelector("#output");
    if (response.ok) {
        mixpanel.track("Generated Email", {
            url,
            sender_info: senderInfo,
            recipient_info: recipientInfo,
            prompt,
            word_count: wordCount,
            responseBody: responseBody,
        });
        showOutputText(responseBody);
    } else {
        // outputElement.textContent = "Error: " + responseBody;
        console.log("Error: " + responseBody);
        // get pricing page url
        const pricingPageURL = window.location.origin + "/pricing";
        // format error string to include the pricingURL
        const errorString = `You do not have enough credits to generate an email. Visit <a href='${pricingPageURL}'>${pricingPageURL}</a> to upgrade your plan.`;
        showError(errorString);
    }
    generateBtn.disabled = false;
    generateBtnText.textContent = "Generate Email";

    function showOutputText(text) {
        var timeInterval = 120;
        // checks billing status is paid or not
        if (checkBillingStatus()) {
            timeInterval = 60;
        }

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
        }, timeInterval);

        if (!isPaid) {
            // if not paid, then schedule redirect to pricing page 3 seconds after animation finishes
            // redirect to pricing page after the animation is done
            // calculate how long it will take to print all words
            const timeToPrint = words.length * timeInterval;
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
