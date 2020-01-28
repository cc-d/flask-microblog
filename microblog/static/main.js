var highestId = 0;
function showUploadPreview(ethis) {
    document.getElementById('image-preview-' + highestId).src = window.URL.createObjectURL(ethis.files[0])
    //document.getElementById('image-preview-0').src = window.URL.createObjectURL(ethis.files[0]);
    //$('#image-preview-' + inputId) = window.URL.createObjectURL($('#upload-input-' + inputId).files[inputId);
    
}
