document.getElementById("submit").onclick = function(){
    var user_email = document.getElementById("email").value
    var user_password = document.getElementById("password").value
    var log_cond = document.querySelector('input[name="log_opt"]:checked').value
}
try {
    if (log_cond == "sign_log"){
    new_user(user_email, user_password)
    } else {
    log_in(user_email, user_password)
    getTodos(user_email, user_password)
    }
    document.querySelector('main').style.display = 'flex'
} catch (error) {
    document.getElementById('error').style.display = 'flex'    
}

const BASE_URL = 'http://localhost:8000'

//Sign In
async function new_user(email_arg, password_arg) {
    try {
        var res = await fetch(BASE_URL + '/users',{
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email_arg, password: password_arg})
        })
    } catch (error) {
        document.getElementById('error').style.display = 'flex'
    }
    
}


//Get To Do Tasks
async function getTodos(email_arg, password_arg) {
    try {
        var res = await fetch(BASE_URL + '/todos/get', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email_arg, password: password_arg })
        })
        if (!res.ok) throw new Error(res.status)
        return await res.json()
    } catch (error) {
        document.getElementById('error').style.display = 'flex'
    }
}


//Log In
async function log_in(email_arg, password_arg) {
    try{
        var res = await fetch(BASE_URL + '/login',{
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email_arg, password: password_arg})
        })
        if (!res.ok) throw new Error(res.status)
        return await res.json()
    } catch(error){
        document.getElementById('error').style.display = 'flex'
    }
}

//create todo



