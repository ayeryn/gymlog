document.addEventListener('DOMContentLoaded', function () {
    var modeIcon = document.getElementById('modeIcon');
    modeIcon.onclick = function () {
        document.body.classList.toggle("light-theme")
    };

    // Add a click event listener to the element
    modeIcon.addEventListener('click', function () {
        // Toggle the class on the <i> element
        modeIcon.querySelector('i').classList.toggle('fa-sun');
        modeIcon.querySelector('i').classList.toggle('fa-moon');
    });
});