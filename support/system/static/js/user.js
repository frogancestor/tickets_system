// get user tickets json
async function getTickets() {
    let response = await fetch("http://127.0.0.1:8000/get-user-tickets-list");

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

getTickets();

function generateTicketsCards(tickets_json) {
    let allTicketsWrapper = document.querySelector('.all-user-tickets__wrapper');
    tickets_json["statuses"].forEach(statusOfTicket => {
        let ticketTitle = document.createElement('div');
        ticketTitle.className = "ticket__title";
        ticketTitle.innerHTML = `${statusOfTicket.name}`
        allTicketsWrapper.append(ticketTitle);
        
        let ticketStatusWrap = document.createElement('div');
        ticketStatusWrap.className = "ticket-status__wrapper";
        allTicketsWrapper.append(ticketStatusWrap);

        tickets_json["tickets"][statusOfTicket.id].forEach(ticket => {
            let ticketWrapper = document.createElement('div');
            ticketWrapper.className = "user-ticket";
            ticketWrapper.innerHTML = `<div class="tickets">
                <div class="user-ticket-attribute">
                    <div class="user-ticket-title">${ticket.title}</div>
                </div>
                <div class="user-ticket-attribute">
                    <div class="user-ticket-title">Описание:</div>
                    <p class="user-ticket-content">${ticket.description}</p>
                </div>
                <div class="user-ticket-attribute">
                    <div class="user-ticket-title">Приоритет:</div>
                    <p class="user-ticket-content">${ticket.priority}</p>
                </div>
                <div class="user-ticket-attribute">
                    <div class="user-ticket-title">Категория:</div>
                    <p class="user-ticket-content">${ticket.category}</p>
                </div>
                <div class="user-ticket-attribute">
                    <a class="link-to-user-ticket" target="_blank" href="http://127.0.0.1:8000/open-ticket-user/${ticket.id}">Открыть</a>
                </div>
            </div>`
            ticketStatusWrap.append(ticketWrapper);
            console.log(ticket)
        })
    })
}

function logout() {
    cookieStore.delete('auth_token')
    console.log(document.cookie)
}