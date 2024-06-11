let selected_elements = {
    "categories" : [],
    "statuses" : [],
    "priorities" : []
}

let ticketsJson = {}

// search
const input = document.querySelector('.mysearch');
const cross = document.querySelector('.icon_cross');
const searchBut = document.querySelector('.icon_search')

// filter
const category = document.querySelector('.filter-category');
const statusAtr = document.querySelector('.filter-status');
const priority = document.querySelector('.filter-priority');

const categories = document.querySelector('.categories');
const statuses = document.querySelector('.statuses');
const priorities = document.querySelector('.priorities');

searchBut.onclick = function() {
    filterRecords(input.value)
}

// search functions
input.addEventListener("input", function (event) {
    cross.classList.add('active');
})

function filterRecords(searchStr){
    filteredData = {'tickets': []}
    ticketsJson.tickets.forEach(ticket => {
        if (ticket.title.toLowerCase().includes(searchStr.toLowerCase()) || ticket.description.toLowerCase().includes(searchStr.toLowerCase()) || ticket.user.toLowerCase().includes(searchStr.toLowerCase())) {
            filteredData.tickets.push(ticket)
        }
    })
    generateTicketsCards(filteredData)
}

cross.onclick = function() {
    document.querySelector('.mysearch').value = '';
    cross.classList.remove('active');
    getTickets('');
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
}

const filter_button = document.querySelector('.filter-button');
filter_button.onclick = function () {
    let query = getSearchString(selected_elements);
    getTickets(query);
}


function getSearchString(selected_elements) {
    let result = `?categories=${selected_elements['categories'].join('_')}&statuses=${selected_elements['statuses'].join('_')}&priorities=${selected_elements['priorities'].join('_')}`;
    return result;
}

async function getTickets(query) {
    let response = await fetch(`http://127.0.0.1:8000/tickets-list${query}`);

    if (response.ok) { // если HTTP-статус в диапазоне 200-299
    // получаем тело ответа
        let json = await response.json();
        ticketsJson = json;
        generateTicketsCards(json);
    }
    else {
        console.log("Ошибка HTTP: " + response.status);
    }
}

getTickets("");

function generateTicketsCards(tickets_json) {
    let allTicketsWrapper = document.querySelector('.all-tickets__wrapper');
    allTicketsWrapper.innerHTML = ''
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
        // ticket['custom_atr'].forEach(custAtr => {
        //     ticketAtr = document.createElement('div')
        //     ticketAtr.className = 'ticket-attribute'
        //     ticketAtr.innerHTML = `<div class="ticket-title">${custAtr.name}:</div>
        //                            <p class="ticket-content">${custAtr.data}</p>`
        //     ticketWrapper.append(ticketAtr)
        // })
        allTicketsWrapper.append(ticketWrapper);
    })
}


function logout() {
    cookieStore.delete('auth_token')
}