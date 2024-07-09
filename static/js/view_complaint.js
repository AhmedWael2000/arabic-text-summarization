function showEditForm() {
    document.getElementById('edit-form').classList.remove('hidden');
    document.getElementById('edit-button').classList.add('hidden');
}

function saveNewValue() {
    var newText = document.getElementById('new-value').options[document.getElementById('new-value').selectedIndex].text;
    document.getElementById('current-value').innerText = newText;
    document.getElementById('edit-form').classList.add('hidden');
    document.getElementById('edit-button').classList.remove('hidden');
    document.getElementById('update-tfidf-form').submit();
}

function cancelEdit() {
    document.getElementById('edit-form').classList.add('hidden');
    document.getElementById('edit-button').classList.remove('hidden');
}

function summarizeComplaint(complaintId) {
    var complaintText = document.getElementById('complaint-text').innerText;
    var summaryElement = document.getElementById('complaint-summary');
    var loadingIndicator = document.getElementById('loading-indicator');

    loadingIndicator.style.display = 'block';
    summaryElement.innerText = '';

    fetch(`/summarize/${complaintId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ complaint_text: complaintText })
    })
    .then(response => response.json())
    .then(data => {
        loadingIndicator.style.display = 'none';
        summaryElement.innerText = data.summary;
    })
    .catch(error => {
        console.error('Error:', error);
        loadingIndicator.style.display = 'none';
        summaryElement.innerText = 'حدث خطأ أثناء توليد الملخص. يرجى المحاولة مرة أخرى.';
    });
}


function goBack(classifiedvalue) {
    var previous_url = '';
    if (classifiedvalue === 0) {
        previous_url = '/transports';
    } else if (classifiedvalue === 1) {
        previous_url = '/health';
    } else if (classifiedvalue === 2) {
        previous_url = '/waterandelec';
    } else {
        previous_url = '/not_classified';
    }
    window.location.href = previous_url; 
}

