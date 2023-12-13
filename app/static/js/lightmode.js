let lightMode = localStorage.getItem("lightMode");
const lightModeToggle = document.querySelector("#lightModeToggle");

const enableLightMode = () => {
    // add light-mode to the body
    document.body.classList.add("light-mode");

    // update localStorage
    localStorage.setItem("lightMode", "enabled");
};

const disableLightMode = () => {
    // remove light-mode to the body
    document.body.classList.remove("light-mode");

    // update localStorage
    localStorage.setItem("lightMode", null);
};


if (lightMode === "enabled") {
    /* IMPORTANT!!!
     * Make sure mode persists between page refreshes and redirects
     */
    enableLightMode();
}

lightModeToggle.addEventListener("click", () => {
    //refresh lightMode var every time a click happens
    lightMode = localStorage.getItem("lightMode");
    if (lightMode !== "enabled") {
        enableLightMode();
    } else {
        disableLightMode();
    }
});