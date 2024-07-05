let popupPort;

chrome.runtime.onConnect.addListener(function (port) {
    popupPort = port;
    port.onMessage.addListener(function (msg) {
        if (msg.action === 'summarizeText') {
            fetch('http://localhost:5000/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: msg.text,
                }),
            })
            .then(response => response.json())
            .then(data => {
                // Send a message to the popup.js to update the output div with the summarized text
                popupPort.postMessage({ action: 'updateOutput', summary: data.summary });
            })
            .catch(error => {
                console.error('Error:', error);
            });
        }
    });
});
