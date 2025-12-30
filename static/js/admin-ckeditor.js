document.addEventListener('DOMContentLoaded', function() {
    // Wait for CKEditor to initialize
    setTimeout(function() {
        const editors = document.querySelectorAll('.django-ckeditor-5 .ck-editor__editable');
        editors.forEach(editor => {
            editor.style.backgroundColor = 'gray';
            editor.style.color = 'black';
        });
    }, 1000);
});
