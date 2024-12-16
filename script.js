document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("fraudForm");
    const resultDiv = document.getElementById("result");

    // Set the API URL to the live backend URL
    const apiUrl = "https://sbi-web-2.onrender.com/predict";

    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent page reload

        // Collect form data
        const clientName = document.getElementById("clientName").value.trim();
        const claimAmount = document.getElementById("amount").value.trim();
        const claimReason = document.getElementById("claim").value.trim();
        const cardDetails = document.getElementById("cardDetails").value.trim();

        // Validate input
        if (!clientName || !claimAmount || !claimReason || !cardDetails) {
            resultDiv.innerHTML = `<p style="color: red;">All fields are required!</p>`;
            return;
        }

        // Send POST request to Flask API
        fetch(apiUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                client_name: clientName,
                claim_amount: parseInt(claimAmount),
                claim_reason: claimReason,
                card_details: cardDetails
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.fraud) {
                resultDiv.innerHTML = `<p style="color: red;">Fraud Detected 🚨 for ${clientName}</p>`;
            } else {
                resultDiv.innerHTML = `<p style="color: green;">No Fraud Detected ✅ for ${clientName}</p>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
        });
    });
});
