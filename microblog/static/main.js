var highestId = 0;

function showUploadPreview(imageThis) {
    imageExts = ['png', 'gif', 'jpg', 'jpeg']
    fileExt = imageThis.files[0].name.split('.').pop().toLowerCase();

    if (imageExts.includes(fileExt)) {
        previewId = document.getElementById('image-preview-' + highestId);
        previewId.src = window.URL.createObjectURL(imageThis.files[0]);
        previewId.src = window.URL.createObjectURL(imageThis.files[0]);
        $(previewId).css('display', 'block');
        $('#text-preview-' + highestId).css('display','none');
    } else {
        previewId = document.getElementById('text-preview-' + highestId);
        $('#ext-preview-txt-' + highestId).text('.' + fileExt);
        $(previewId).css('display', 'block');
        $('#image-preview-' + highestId).css('display','none');
    }

    //document.getElementById('image-preview-0').src = window.URL.createObjectURL(ethis.files[0]);
    //$('#image-preview-' + inputId) = window.URL.createObjectURL($('#upload-input-' + inputId).files[inputId);
    
}
