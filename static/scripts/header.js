const avatar_container = document.getElementById("user-container")
const dropdown = document.getElementById("user-dropdown-menu")

avatar_container.onclick = ((e) => {
    if (dropdown.classList.contains("active-menu")) {
        if (!dropdown.contains(e.target)) {
            dropdown.classList.remove("active-menu")
        }
    } else {
        dropdown.classList.add("active-menu")
    }
})

document.addEventListener('click', function(e) {
    if (e.target !== avatar_container && !avatar_container.contains(e.target)) {
        dropdown.classList.remove("active-menu")
    }
})

document.getElementById("logout-option").onclick = (e) => {
     fetch("/api/logout", {
        method: "POST"
     }).then(async response => {
        location.href = "";
     })
}
