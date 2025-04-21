// Define draft metadata
window.draftMeta = {
    topic: "{{ topic|e }}",
    author: "{{ author|e }}",
    image_url: "{{ image_url|e }}"
};

// Check if the form is dirty (i.e., has unsaved changes)
function isFormDirty() {
    var fields = document.querySelectorAll('form textarea');
    for (var i = 0; i < fields.length; i++) {
        if (fields[i].value.trim() !== '') return true;
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
    data.topic = window.draftMeta.topic;
    data.author = window.draftMeta.author;
    data.image_url = window.draftMeta.image_url;
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
        } catch (err) {
            alert('Failed to load draft: invalid file format.');
        }
    };
    reader.readAsText(file);
});