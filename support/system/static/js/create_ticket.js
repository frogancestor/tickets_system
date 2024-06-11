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

async function getCustomAttributes(category_id) {
    let response = await fetch(`http://127.0.0.1:8000/get-category-custom-attribute?category=${category_id}`);

    if (response.ok) { // если HTTP-статус в диапазоне 200-299
    // получаем тело ответа
        let json = await response.json();
        console.log(json);
        addCustomAttributes(json);
    }
    else {
        console.log("Ошибка HTTP: " + response.status);
    }
}

function addCustomAttributes(attributes_json) {
    let createAppForm = document.querySelector('.custom_atr_area');
    createAppForm.innerHTML = '';
    attributes_json["custom_atr"].forEach(customAttribute => {
        let newLabel = document.createElement('label');
        newLabel.className = "input-text";
        let newSpan = document.createElement('span');
        newSpan.className = "input-title";
        newSpan.innerHTML = `${customAttribute.name}:`;
        newLabel.append(newSpan);
        if (customAttribute.type == "str") {
            let newInput = document.createElement('input');
            newInput.type = "text";
            newInput.className = "input-textmessage";
            newInput.name = customAttribute.id;
            newLabel.append(newInput);
        }
        else if (customAttribute.type == "text") {
            let newInput = document.createElement('textarea');
            newInput.className = "description-textarea";
            newInput.name = customAttribute.id;
            newLabel.append(newInput);
        }
        else if (customAttribute.type == "list") {
            let newInput = document.createElement('select');
            newInput.id = customAttribute.id;
            newInput.className = "custom_list";
            newInput.name = customAttribute.id;
            let zero_option = document.createElement('option');
            zero_option.value = "";
            zero_option.innerHTML = "-- Выберите опцию --";
            newInput.append(zero_option);
            newLabel.append(newInput);

            customAttribute.list_options.forEach(option => {
                let newOption = document.createElement('option');
                console.log(option)
                console.log(newOption)
                newOption.value = option.id;
                newOption.innerHTML = option.name;
                newInput.append(newOption);
            })
        }
        else {
            console.log("PANIC ERROR NO SUCH TYPE")
        }
        createAppForm.append(newLabel)
    })
}

function logout() {
    cookieStore.delete('auth_token')
    console.log(document.cookie)
}
