document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("fraudForm");
    const resultDiv = document.getElementById("result");

    form.addEventListener("submit", (event) => {
        event.preventDefault(); // Prevent page reload

        // Collect form data
        const clientName = document.getElementById("clientName").value.trim();
        const claimAmount = document.getElementById("amount").value.trim();
        const claimReason = document.getElementById("claim").value.trim();
        const cardDetails = document.getElementById("cardDetails").value.trim();

        // Send POST request to Flask API
        fetch("http://127.0.0.1:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                client_name: clientName,
                claim_amount: parseInt(claimAmount),
                claim_reason: claimReason,
                card_details: cardDetails
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.fraud) {
                resultDiv.innerHTML = `<p>Fraud Detected 🚨 for ${clientName}</p>`;
            } else {
                resultDiv.innerHTML = `<p>No Fraud Detected ✅ for ${clientName}</p>`;
            }
        })
        .catch(error => {
            resultDiv.innerHTML = `<p>Error: ${error}</p>`;
        });
    });
});