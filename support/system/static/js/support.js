let selected_elements = {
    "categories" : [],
    "statuses" : [],
    "priorities" : []
}

// search
const input = document.querySelector('.mysearch');
const cross = document.querySelector('.icon_cross');

// filter
const category = document.querySelector('.filter-category');
const statusAtr = document.querySelector('.filter-status');
const priority = document.querySelector('.filter-priority');

const categories = document.querySelector('.categories');
const statuses = document.querySelector('.statuses');
const priorities = document.querySelector('.priorities');

// search functions
input.addEventListener("input", function (event) {
    cross.classList.add('active');
})

cross.onclick = function() {
    document.querySelector('.mysearch').value = '';
    cross.classList.remove('active');
}
// filter functions
category.onclick = function() {
    categories.classList.toggle('open');
}

statusAtr.onclick = function() {
    statuses.classList.toggle('open');
}

priority.onclick = function() {
    priorities.classList.toggle('open');
}

const checkboxes = document.getElementsByName('attributes');

console.log(checkboxes);

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('click', (e)=>{
        checkedAttributes(e.target);
    })
})

function checkedAttributes(element) {
    key = element.parentNode.parentNode.classList[0];
    if (element.checked) {
        selected_elements[key].push(element.value)
    }
    else {
        index0fElement = selected_elements[key].indexOf(element.value);
        selected_elements[key].splice(index0fElement, 1);
    }
    console.log(element.parentNode.parentNode.classList[0]);
    console.log(selected_elements);
}

// function getSearchString(selected_elements) {

// }

// function placeSearchStrIntoDiv() {

// }

async function getTickets() {
    let response = await fetch("http://127.0.0.1:8000/tickets-list");

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
    let allTicketsWrapper = document.querySelector('.all-tickets__wrapper');
    tickets_json["tickets"].forEach(ticket => {
        let ticketWrapper = document.createElement('div');
        ticketWrapper.className = "ticket__wrapper";
        ticketWrapper.innerHTML = `<div class="ticket-attribute">
        <div class="ticket-title-content">${ticket.title}</div>
    </div>
    <div class="ticket-attribute">
        <div class="ticket-title">Описание:</div>
        <p class="ticket-content">${ticket.description}</p>
    </div>
    <div class="ticket-attribute">
        <div class="ticket-title">Пользователь:</div>
        <p class="ticket-content">${ticket.user}</p>
    </div>
    <div class="ticket-attribute">
        <div class="ticket-title">Саппорт:</div>
        <p class="ticket-content">${ticket.support}</p>
    </div>
    <div class="ticket-attribute">
        <div class="ticket-title">Приоритет:</div>
        <p class="ticket-content">${ticket.priority}</p>
    </div>
    <div class="ticket-attribute">
        <div class="ticket-title">Статус:</div>
        <p class="ticket-content">${ticket.status}</p>
    </div>
    <div class="ticket-attribute">
        <div class="ticket-title">Категория:</div>
        <p class="ticket-content">${ticket.category}</p>
    </div>
    <div class="ticket-attribute">
        <a class="link-to-ticket" target="_blank" href="http://127.0.0.1:8000/watch-ticket/${ticket.id}">Открыть</a>
    </div>`
        ticket['custom_atr'].forEach(custAtr => {
            ticketAtr = document.createElement('div')
            ticketAtr.className = 'ticket-attribute'
            ticketAtr.innerHTML = `<div class="ticket-title">${custAtr.name}:</div>
                                   <p class="ticket-content">${custAtr.data}</p>`
            ticketWrapper.append(ticketAtr)
        })
        allTicketsWrapper.append(ticketWrapper);
    })
}


