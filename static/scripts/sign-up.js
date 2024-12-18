const emailField = document.getElementById('login_form_email')
const passwordField = document.getElementById('login_form_password')
const loginBtn = document.getElementById('login_form_btn')

loginBtn.addEventListener('click', (e) => {
    emailField.parentElement.childNodes[2].textContent = ''
    passwordField.parentElement.childNodes[2].textContent = ''
    fetch('/api/private/user', {
        method: 'POST',
        body: JSON.stringify({
            email: emailField.value,
            password: passwordField.value
        }),
        headers: {
            'Content-type': 'application/json; charset=UTF-8',
        },
    })
    .then(async (response) => {
        if (response.status === 200) {
            document.location.href = '/sign-in'
            return
        }
        response_json = await response.json()
        Object.keys(response_json).forEach(key => {
            let error_p = document.createElement("p")
            error_p.classList.add("error-p")
            if (key === 'email') {
                error_p.innerText = response_json[key][0]['message']
                emailField.parentElement.appendChild(error_p)
            } else if (key === 'password') {
                error_p.innerText = response_json[key][0]['message']
                passwordField.parentElement.appendChild(error_p)
            }
        })
    })
})
