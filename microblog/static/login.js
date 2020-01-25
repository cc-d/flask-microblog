function checkPasswords() {
    pInput = document.getElementById('login-password');
    confirmInput = document.getElementById('login-password2');
    confirmMsg = document.getElementById('confirm-password-msg');

    if (confirmInput.value !== undefined ) {
        if (confirmInput.value.length > 0) {
            if (pInput.value === confirmInput.value) {
                confirmMsg.innerText = 'Passwords Match';
                confirmMsg.className = 'text-success';
                pInput.className = changeBorder(pInput.className, 'success')
                confirmInput.className = changeBorder(confirmInput.className, 'success')
            } else {
                confirmMsg.innerText = 'Passwords Do Not Match';
                confirmMsg.className = 'text-danger';
                pInput.className = changeBorder(pInput.className, 'danger')
                confirmInput.className = changeBorder(confirmInput.className, 'danger')
            }
        }
    }
}

function changeBorder(elemClass, changeTo) {
    if (elemClass.includes('border-' + changeTo)) {
        return elemClass;
    } else {
        if (elemClass.includes('border-')) {
            return elemClass.replace(/border-[a-zA-Z]*/g, 'border-' + changeTo);
        } else {
            return elemClass + (' border-' + changeTo);
        }
    }
}