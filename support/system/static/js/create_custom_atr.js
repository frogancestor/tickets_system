let category = document.querySelector(".categories_list");
category.onchange = function() {
    let category_value = category.value;
    if (category_value != "") {
        getCustomAttributes(category_value)
        console.log(category_value)
    }
    else {
        console.log("nothing")
    }

}

let listElementsWrapper = document.querySelector('.list-elements__wrapper');

let icon_plus = document.querySelector('.icon-plus');
icon_plus.onclick = function () {
    let list_element = document.createElement('div');
    list_element.classList.add('list-attribute');
    list_element.innerHTML = `<input type="text" placeholder="Введите новый элемент списка" class="input-atr-name">
                                <div onclick="iconMinusAction(this)" class="icon-minus"></div>`
    listElementsWrapper.append(list_element);
}

function iconMinusAction(act) {
    act.parentElement.remove();
}

let listCustomType = document.querySelector(".custom_list");
listCustomType.onchange = function() {
    let type_value = listCustomType.value;
    if (type_value != "") {
        const option = listCustomType.selectedOptions[0].text;
        if (option == 'list') {
            icon_plus.classList.add('active');
        }
        else {
            icon_plus.classList.remove('active');
            listElementsWrapper.innerHTML = '';
        }
    }
    else {
        console.log("nothing")
    }
}

function getCustomAtrData() {
    let inputAtrName = document.querySelector('.input-atr-name');
    let customType = document.querySelector('.custom_list');
    let category = document.querySelector('.categories_list');
    let list_elements = []
    const option = listCustomType.selectedOptions[0].text;
        if (option == 'list') {
            for (let i = 0; i < listElementsWrapper.childNodes.length; i++){
                list_elements.push(listElementsWrapper.children[i].firstChild.value)
            }
        }
    return {name: inputAtrName.value, customType: customType.value, category: category.value, list: list_elements}
}

function clearFields() {
    let inputAtrName = document.querySelector('.input-atr-name');
    let customType = document.querySelector('.custom_list');
    let category = document.querySelector('.categories_list');
    inputAtrName.value = '';
    customType.value = '';
    listElementsWrapper.innerHTML = '';
    // category.value = '';
}

async function sendData(json) {
    console.log(JSON.stringify(json))
    let response = await fetch(`http://127.0.0.1:8000/create-custom-atr`, {
        method: 'POST',
        body: JSON.stringify(json),
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (response.ok) { // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа
        let json = await response.json();
        console.log(json);
        let category_id = category.value;
        getCustomAttributes(category_id);
        clearFields();
    }
    else {
        console.log("Ошибка HTTP: " + response.status);
    }
}

const saveBtn = document.querySelector('.save-btn');
saveBtn.onclick = function() {
    let data = getCustomAtrData();
    sendData(data);
}

async function getCustomAttributes(category_id) {
    let response = await fetch(`http://127.0.0.1:8000/get-category-custom-attribute?category=${category_id}`);

    if (response.ok) { // если HTTP-статус в диапазоне 200-299
    // получаем тело ответа
        let json = await response.json();
        if (json['custom_atr'].length == 0) {
            noAttributesInJSON();
        }
        else {
            addCustomAttributes(json);
        }
        console.log(json);
    }
    else {
        console.log("Ошибка HTTP: " + response.status);
    }
}

function noAttributesInJSON() {
    let lastAttribute = document.querySelector('.custom_atr');
    lastAttribute.classList.remove('hidden');
    let createAtrTable = document.querySelector('.custom-atr-table');
    createAtrTable.classList.add('hidden');
}

function addCustomAttributes(attributes_json) {
    let lastAttribute = document.querySelector('.custom_atr');
    lastAttribute.classList.add('hidden');
    let createAtrTable = document.querySelector('.custom-atr-table');
    createAtrTable.classList.remove('hidden');
    let tbodyCustomAtr = createAtrTable.querySelector('tbody');
    tbodyCustomAtr.innerHTML = '';
    attributes_json["custom_atr"].forEach(customAttribute => {
        let newTableRow = document.createElement('tr');
        let newTdName = document.createElement('td');
        let newTdType = document.createElement('td');
        newTdName.innerHTML = `${customAttribute.name}`;
        newTdType.innerHTML = `${customAttribute.type}`
        newTableRow.append(newTdName);
        newTableRow.append(newTdType);
        if (customAttribute.type == "str") {
            newTdType.innerHTML = `Строка`
        }
        else if (customAttribute.type == "text") {
            newTdType.innerHTML = `Текстовое поле`
        }
        else if (customAttribute.type == "list") {
            newTdType.innerHTML = `Список`
        }
        else {
            console.log("PANIC ERROR NO SUCH TYPE")
        }
        tbodyCustomAtr.append(newTableRow)
    })
}


function logout() {
    cookieStore.delete('auth_token')
    console.log(document.cookie)
}