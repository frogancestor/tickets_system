async function getTickets() {
    const currentUrl = window.location.href;
    let id = currentUrl.split("/").at(-1);
    id = Number(id)
    console.log(id)
    if (Number.isFinite(id)) {
        let response = await fetch(`http://127.0.0.1:8000/tickets-list?id=${id}`);
        if (response.ok) { // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа
            let json = await response.json();
            console.log(json);
            generateTicketsCards(json);
        }
        else {
            console.log("Ошибка HTTP: " + response.status);
        }
    }
    else {
        console.log("NOT VALID ID")
    }
    
}

getTickets();

function generateTicketsCards(tickets_json) {
    let allTicketsWrapper = document.querySelector('.create-app');
    tickets_json["tickets"].forEach(ticket => {
        ticket['custom_atr'].forEach(custAtr => {
            ticketAtr = document.createElement('div')
            ticketAtr.className = 'ticket-attribute__wrapper'
            ticketAtr.innerHTML = `<div class="input-title">${custAtr.name}:</div>
                                   <div class="ticket-attribute">${custAtr.data}</div>`
            allTicketsWrapper.append(ticketAtr)
        })
    })
}

let changebtn = document.querySelector('.change-btn');
let priority = document.querySelector('.priority');
let statusOfTicket = document.querySelector('.status');
let savebtn = document.querySelector('.save-btn');
let priorities_list = document.querySelector('.priorities_list');
let statuses_list = document.querySelector('.statuses_list');

function changeStatusOrPriority() {
    changebtn.classList.add('hidden');
    priority.classList.add('hidden');
    statusOfTicket.classList.add('hidden');
    savebtn.classList.remove('hidden');
    priorities_list.classList.remove('hidden');
    statuses_list.classList.remove('hidden');
}

const currentUrl = window.location.href;
const ticket_id = currentUrl.split('/').slice(-1);

function getChangedAttributes() {
    let priority_value = priorities_list.value;
    let status_value = statuses_list.value;
    if (priority_value != "" && status_value != "") {
        saveStatusOrPriority(ticket_id, priority_value, status_value)
        console.log(ticket_id, priority_value, status_value)
    }
    else if (priority_value == "") {
        console.log('priority_value пуст')
    }
    else if (status_value == "") {
        console.log('status_value пуст')
    }
    else{
        console.log('priority_value и status_value пусты')
    }
}


async function saveStatusOrPriority(ticket_id, priority, statusOfTicket) {
    console.log(JSON.stringify({'ticket': ticket_id, 'priority': priority, 'status': statusOfTicket}))
    let response = await fetch(`http://127.0.0.1:8000/change_ticket`, {
        method: 'POST',
        body: JSON.stringify({'ticket': ticket_id[0], 'priority': priority, 'status': statusOfTicket}),
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (response.ok) { // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа
        let json = await response.json();
        console.log(json);
    }
    else {
        console.log("Ошибка HTTP: " + response.status);
    }
    location.reload();
}

changebtn.onclick = changeStatusOrPriority;
savebtn.onclick = getChangedAttributes;

function logout() {
    cookieStore.delete('auth_token')
    console.log(document.cookie)
}