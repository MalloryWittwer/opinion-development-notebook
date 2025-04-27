// Check if the form is dirty (i.e., has unsaved changes)
function isFormDirty() {
    var fields = document.querySelectorAll('form textarea');
    for (var i = 0; i < fields.length; i++) {
        if (fields[i].value.trim() !== '') return true;
    }

    var topicSectionInputs = document.querySelectorAll('#topic-section input');
    for (var i = 0; i < topicSectionInputs.length; i++) {
        if (topicSectionInputs[i].value.trim() !== '') return true;
    }

    return false;
}

// Warn the user about unsaved changes before leaving the page
window.addEventListener('beforeunload', function (e) {
    if (isFormDirty()) {
        e.preventDefault();
        e.returnValue = '';
    }
});

// Save the draft as a JSON file
function saveDraft() {
    if (!isFormDirty()) {
        alert('Nothing to save: your notebook is empty.');
        return;
    }
    var form = document.querySelector('form');
    var data = {};
    new FormData(form).forEach(function (value, key) {
        data[key] = value;
    });

    const topic = document.getElementById("topic").value;
    const author = document.getElementById("author").value;
    const imageUrl = document.getElementById("image_url").value;

    data.topic = topic;
    data.author = author;
    data.image_url = imageUrl;

    var blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = (data.topic || 'draft') + '_draft.json';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Load a draft from a JSON file
function loadDraft() {
    document.getElementById('draft-file-input').click();
}

document.getElementById('draft-file-input').addEventListener('change', function (e) {
    var file = e.target.files[0];
    if (!file) return;
    var reader = new FileReader();
    reader.onload = function (evt) {
        try {
            var draft = JSON.parse(evt.target.result);
            var form = document.querySelector('form');
            for (var key in draft) {
                if (form.elements[key]) {
                    form.elements[key].value = draft[key];
                }
            }
            updatePreview();
        } catch (err) {
            alert('Failed to load draft: invalid file format.');
        }
    };
    reader.readAsText(file);
});

function updatePreview() {
    // Get the values from the form fields
    const topic = document.getElementById("topic").value;
    const author = document.getElementById("author").value;
    const imageUrl = document.getElementById("image_url").value;
    console.log(imageUrl)

    // Update the preview elements
    const previewTopic = document.getElementById("preview-topic");
    const previewAuthor = document.getElementById("preview-author");
    const previewImage = document.getElementById("preview-image");

    // Update the topic and author text
    previewTopic.textContent = topic || "Untitled Topic"; // Default text if empty
    previewAuthor.textContent = author || "Anonymous"; // Default text if empty

    // Update the image preview
    if (imageUrl) {
        previewImage.src = imageUrl;
        previewImage.style.display = "inline"; // Ensure the image is visible
    } else {
        previewImage.style.display = "none"; // Hide the image if no URL is provided
    }
}