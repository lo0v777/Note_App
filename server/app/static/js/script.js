function openModal() {
    document.getElementById('noteModal').style.display = 'flex';
}
function closeModal() {
    document.getElementById('noteModal').style.display = 'none';
}
window.onclick = function(event) {
    if (event.target == document.getElementById('noteModal')) {
        closeModal();
    }
}