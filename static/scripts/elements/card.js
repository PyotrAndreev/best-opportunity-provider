function createOpportunityCard(card) {
    let card_div = document.createElement("div");
    card_div.classList.add("opportunity-card")
    card_div.onclick = () => {
        document.location.href=`/opportunity/${card.opportunity_id}`
    }
    let card_provider_div = document.createElement("div")
    card_provider_div.classList.add("card-provider-container")
    let provider_img = document.createElement("img")
    provider_img.src = card.provider_logo_url
    let provider_name = document.createElement("p")
    provider_name.innerText = card.provider_name
    card_provider_div.appendChild(provider_img)
    card_provider_div.appendChild(provider_name)

    let card_title_container = document.createElement("div")
    card_title_container.classList.add("card-title-container")
    let card_title = document.createElement("p")
    card_title.innerText = card.card_title
    card_title.classList.add("card-title")
    let card_subtitle = document.createElement("p")
    card_subtitle.innerText = card.card_subtitle
    card_subtitle.classList.add("card-subtitle")
    card_title_container.appendChild(card_title)
    card_title_container.appendChild(card_subtitle)

    let card_tags = document.createElement("div")
    card_tags.classList.add("card-tags")
    let card_tags_container = document.createElement("div")
    card_tags_container.classList.add("card-tags-container")
    let card_geotag_container = document.createElement("div")
    card_geotag_container.classList.add("card-geotag-container")

    for (let [id, name] of Object.entries(card.geotags)) {
        card_geotag_container.appendChild(createGeotag(id, name))
    }

    let card_tag_container = document.createElement("div")
    card_tag_container.classList.add("card-tag-container")

    for (let [id, name] of Object.entries(card.tags)) {
        card_tag_container.appendChild(createTag(id, name))
    }

    card_tags_container.appendChild(card_geotag_container)
    card_tags_container.appendChild(card_tag_container)
    card_tags.appendChild(card_tags_container)

    card_div.appendChild(card_provider_div)
    card_div.appendChild(card_title_container)
    card_div.appendChild(card_tags)
    return card_div
}
