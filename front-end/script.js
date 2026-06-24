const BASE_URL = 'http://localhost:8000'

// MISTAKE: user_email and user_password were defined inside the login onclick
// so the task submit button couldn't access them — moved to top level
var user_email = ''
var user_password = ''

// login / register button
document.getElementById("submit").onclick = async function(){
    user_email = document.getElementById("email").value
    user_password = document.getElementById("password").value
    var log_cond = document.querySelector('input[name="log_opt"]:checked').value
    try {
        if (log_cond == "sign_log"){
            await new_user(user_email, user_password)
        } else {
            await log_in(user_email, user_password)
            // MISTAKE: getTodos result was not used — now we pass it to display
            var todos = await getTodos(user_email, user_password)
            displayTodos(todos)
        }
        document.querySelector('main').style.display = 'flex'
    } catch (error) {
        document.getElementById('error').style.display = 'flex'
    }
}

// MISTAKE: second onclick was also using "submit" id — overwrote the login one
// changed to "task_sub" which is the correct button id
document.getElementById("task_sub").onclick = async function(){
    var user_task = document.getElementById("task_name").value
    var act_cond = document.querySelector('input[name="task_opt"]:checked').value
    try {
        if (act_cond == "add_task"){
            // MISTAKE: created head1 but then styled div which didn't exist
            // fixed: create div, put h1 inside it, style the div
            var div = document.createElement('div')
            var head1 = document.createElement('h1')

            head1.textContent = user_task

            div.style.backgroundColor = 'rgb(255, 204, 204)'
            div.style.padding = '20px'
            div.style.borderRadius = '8px'
            div.style.marginBottom = '8px'
            div.style.color = '#1A1A1A'
            div.className = 'todo-item'

            div.appendChild(head1)
            document.getElementById('tasks').appendChild(div)

            await new_task(user_task, user_email, user_password)
        } else {
            await delete_task(user_email, user_password, user_task)
            // remove from screen after deleting
            document.getElementById('tasks').innerHTML = ''
            var todos = await getTodos(user_email, user_password)
            displayTodos(todos)
        }
    } catch(error) {
        document.getElementById('error').style.display = 'flex'
    }
}

// displays todos on the page
function displayTodos(todos) {
    document.getElementById('tasks').innerHTML = ''
    todos.forEach(function(todo) {
        var div = document.createElement('div')
        var h1 = document.createElement('h1')
        h1.textContent = todo.title
        div.style.backgroundColor = todo.done ? '#DDEB9D' : 'rgb(255, 204, 204)'
        div.style.padding = '20px'
        div.style.borderRadius = '8px'
        div.style.marginBottom = '8px'
        div.className = 'todo-item'
        div.appendChild(h1)
        document.getElementById('tasks').appendChild(div)
    })
}

// MISTAKE: URL was BASE_URL + '/users' — should be '/todos'
async function delete_task(email_arg, password_arg, id_arg) {
    try {
        var res = await fetch(BASE_URL + '/todos', {
            method: 'DELETE',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email_arg, password: password_arg, todo_id: id_arg})
        })
        if (!res.ok) throw new Error(res.status)
        return await res.json()
    } catch (error) {
        document.getElementById('error').style.display = 'flex'
    }
}

async function new_user(email_arg, password_arg) {
    try {
        var res = await fetch(BASE_URL + '/users', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email_arg, password: password_arg})
        })
        return await res.json()
    } catch (error) {
        document.getElementById('error').style.display = 'flex'
    }
}

async function log_in(email_arg, password_arg) {
    try {
        var res = await fetch(BASE_URL + '/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({email: email_arg, password: password_arg})
        })
        if (!res.ok) throw new Error(res.status)
        return await res.json()
    } catch(error) {
        document.getElementById('error').style.display = 'flex'
    }
}

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

async function new_task(title_task, email_arg, password_arg) {
    try {
        var res = await fetch(BASE_URL + '/todos', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({title: title_task, email: email_arg, password: password_arg})
        })
        return await res.json()
    } catch (error) {
        document.getElementById('error').style.display = 'flex'
    }
}
