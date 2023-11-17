function closePopup(redirectUrl) {
    document.getElementById('overlay').style.display = 'none';
    if (redirectUrl) {
        window.location.href = redirectUrl;
    }
}