// popup.js
document.addEventListener('DOMContentLoaded', function () {
    var inputText = document.getElementById('inputText');
    var summarizeButton = document.getElementById('summarizeButton');
    
    // Get the output div and the SUMMARY heading
    var outputDiv = document.getElementById('outputDiv');
    var summaryHeading = document.getElementById('summaryHeading');
    

    // Establish a connection to the background script
    const backgroundPort = chrome.runtime.connect({ name: 'popup' });

    summarizeButton.addEventListener('click', function () {
        var textToSummarize = inputText.value;

        // Send a message to the background script to initiate text summarization
        backgroundPort.postMessage({ action: 'summarizeText', text: textToSummarize });
    });

    // Handle messages from the background script
    backgroundPort.onMessage.addListener(function (msg) {
        if (msg.action === 'updateOutput') {
            // Update the heading and the output div with the summarized text
            summaryHeading.style.display = 'block';
            outputDiv.style.display = 'block';
            outputDiv.innerText = msg.summary;
        }
    });
});
