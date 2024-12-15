function createGeotag(id, name) {
    let tag_container = document.createElement("div")
    tag_container.className += "geotag-container"
    tag_container.setAttribute("geo_tag_id", id)
    tag_container.style = "cursor:pointer"
    let tag_text = document.createElement("p")
    tag_text.innerText = name
    tag_container.appendChild(tag_text)
    return tag_container
}
