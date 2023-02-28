const loadKeys = async () => {
    const response = await sendAuthenticatedRequest("GET", "/api/key/list");
    if (response.ok) {
        const data = await response.json();
        const keysContainer = document.querySelector("#keys-container");
        keysContainer.innerHTML = ""; // clear existing keys

        const apiKeys = data.api_keys;

        // sort the apiKeys by date created in descending order
        apiKeys.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

        console.log("API keys loaded successfully", apiKeys);
        apiKeys.forEach((key) => {
            console.log("key: ", key);
            const row = document.createElement("tr");
            const keyTd = document.createElement("td");
            keyTd.classList.add("border", "px-4", "py-2", "align-middle");
            const keyInput = document.createElement("input");
            keyInput.setAttribute("type", "text");
            keyInput.setAttribute("value", key.secret);
            keyInput.classList.add(
                "w-full",
                "bg-gray-100",
                "px-3",
                "py-2",
                "rounded-lg",
                "border",
                "border-gray-400",
                "focus:outline-none",
                "focus:border-blue-500",
                "select-all"
            );
            keyTd.appendChild(keyInput);
            const createdTd = document.createElement("td");
            createdTd.classList.add("border", "px-4", "py-2", "align-middle");
            createdTd.textContent = key.created_at;
            const lastUsedTd = document.createElement("td");
            lastUsedTd.classList.add("border", "px-4", "py-2", "align-middle");
            if (key.last_used_at !== null) {
                lastUsedTd.textContent = key.last_used_at;
            } else {
                lastUsedTd.textContent = "Never";
            }
            const deleteButtonTd = document.createElement("td");
            deleteButtonTd.classList.add(
                "border",
                "px-4",
                "py-2",
                "align-middle"
            );
            const deleteButton = document.createElement("button");
            deleteButton.classList.add(
                "bg-red-500",
                "hover:bg-red-700",
                "text-white",
                "font-bold",
                "py-1",
                "px-2",
                "rounded-lg",
                "focus:outline-none",
                "focus:shadow-outline"
            );
            deleteButton.textContent = "Delete";
            deleteButton.addEventListener("click", async () => {
                const deleteEndpoint = "/api/key/delete";
                const requestOptions = {
                    method: "DELETE",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${localStorage.getItem(
                            "jwtToken"
                        )}`,
                    },
                    body: JSON.stringify({ api_secret: key.secret }),
                };
                try {
                    const response = await fetch(
                        deleteEndpoint,
                        requestOptions
                    );
                    if (response.ok) {
                        console.log("API key deleted successfully");
                        // Refresh the keys list after deleting
                        loadKeys();
                    } else {
                        console.error("Failed to delete key: ", key.secret);
                    }
                } catch (err) {
                    console.error("Failed to delete key: ", err);
                }
            });

            deleteButtonTd.appendChild(deleteButton);
            row.appendChild(keyTd);
            row.appendChild(createdTd);
            row.appendChild(lastUsedTd);
            row.appendChild(deleteButtonTd);
            keysContainer.appendChild(row);
        });
    } else {
        console.error("Failed to load keys.");
    }
};

loadKeys();

const createApiKey = async () => {
    const response = await sendAuthenticatedRequest("POST", "/api/key/create");
    if (response.ok) {
        const data = await response.json();
        console.log("API key created successfully", data);
        // console log new key from data.api_secret
        console.log("New API key: ", data.api_secret);

        // Refresh the keys list after creating a new key
        loadKeys();
    } else {
        console.error("Failed to create API key.");
    }
};

document
    .querySelector("#create-api-key-btn")
    .addEventListener("click", createApiKey);
