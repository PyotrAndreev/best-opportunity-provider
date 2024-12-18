const submitBtn = document.getElementById('submit_btn')
const uploadButton = document.getElementById('cv-upload')
const logoutButton = document.getElementById('logout')

function updateCVList() {
    const cvs_container = document.getElementById('cvs-container')
    cvs_container.innerText = ""
    fetch("/api/user/cvs", {
        method: "GET"
    })
    .then(async (response) => {
        if (response.status === 200) {
            response_json = await response.json()
            for (var cv_id in response_json) {
                cvs_container.appendChild(createCV(cv_id, response_json[cv_id]))
            }
            return
        }
        cvs_container.textContent = 'Some error occured, refresh page to see your CVs'
    })
}

document.addEventListener('DOMContentLoaded', () => {
    updateCVList()
    const avatarUploadButton = document.getElementById("avatar-upload")
    // const avatarField = document.getElementById("avatar-field")
    const avatarImg = document.getElementById("avatar-img")
    const avatarField = document.getElementById("avatar-upload")
    avatarField.onchange = (e) => {
        if (avatarField.files.length === 0) {
            avatarField.parentElement.children[1].textContent = 'Select a file to upload'
            return
        }
        let formData = new FormData()
        formData.append('avatar', avatarField.files[0])
        fetch("/api/user/avatar", {
            method: "POST",
            body: formData
        })
        .then(async (response) => {
            if (response.status === 200) {
                temp = avatarImg.src
                avatarImg.src = ''
                avatarImg.src = temp + "&" + new Date().getTime();
                return
            }
            response_json = await response.json()
            console.log(response_json)
            Object.keys(response_json).forEach(key => {
                // no errors here yet
            })
        })
    }
})

const nameField = document.getElementById('namefield')
const surnameField = document.getElementById('surnamefield')
const birthdayField = document.getElementById('datefield')

submitBtn.addEventListener('click', (e) => {
    let name = null
    if (nameField.value.length > 0)
        name = nameField.value
    let surname = null
    if (surnameField.value.length > 0)
        surname = surnameField.value
    let birthday = null
    if (birthdayField.value.length > 0) {
        let [year, month, day] = birthdayField.value.split('-')
        birthday = {
            day: parseInt(day),
            month: parseInt(month),
            year: parseInt(year)
        }
    }
    fetch("/api/user/info", {
        method: "PATCH",
        body: JSON.stringify({
            name: name,
            surname: surname,
            birthday: birthday
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
    .then(async (response) => {
        if (response.status === 200) {
            alert('Successfully updated user info')
            return
        }
        response_json = await response.json()
        Object.keys(response_json).forEach(key => {
            if (key === 'name') {
                nameField.parentElement.childNodes[2].textContent = response_json[key][0]['message']
            } else if (key === 'surname') {
                surnameField.parentElement.childNodes[2].textContent = response_json[key][0]['message']
            } else if (key === 'birthday') {
                // you are doing something wrong, if you are here
                // birthdayField.parentElement.childNodes[2].textContent = response_json[key]['message']
            }
        })
    })
})

const CVField = document.getElementById('cv-filefield')

uploadButton.addEventListener('click', (e) => {
    if (CVField.files.length === 0) {
        CVField.parentElement.childNodes[2].textContent = 'Select a file to upload'
        return
    }
    let formData = new FormData()
    formData.append('cv', CVField.files[0])
    fetch("/api/cv", {
        method: "POST",
        body: formData
    })
    .then(async (response) => {
        if (response.status === 200) {
            updateCVList()
            return
        }
        response_json = await response.json()
        Object.keys(response_json).forEach(key => {
            // no errors here yet
        })
    })
})

deleteButtons = document.getElementsByClassName('cv-delete')

logoutButton.addEventListener('click', (e) => {
    fetch("/api/logout", {
        method: "POST"
    })
    .then((response) => {
        document.location.href = '/'
        return
    })
})
