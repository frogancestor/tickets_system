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