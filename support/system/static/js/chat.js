const currentUrl = window.location.href;
const chat_uuid = currentUrl.split('/').slice(-1);

async function getChatHistory(chat_uuid) {
    let response = await fetch(`http://127.0.0.1:8000/get-chat-history?chat=${chat_uuid}`);

    if (response.ok) { // если HTTP-статус в диапазоне 200-299
    // получаем тело ответа
        let json = await response.json();
        addMessages(json);
    }
    else {
        console.log("Ошибка HTTP: " + response.status);
    }
}

function addMessages(messages_json) {
    let chatWrapper = document.querySelector('.chat__wrapper');
    chatWrapper.innerHTML = '';
    messages_json["messages"].forEach(message => {
        let messageWrapper = document.createElement('div');
        messageWrapper.className = "message__wrapper";
        messageWrapper.innerHTML = `<div class="person_name">${message.sender}</div>
        <div class="message">${message.message}</div>
        <div class="datetime">${message.datetime.split('.')[0]}</div>`
        console.log(message.datetime)
        chatWrapper.append(messageWrapper);
    })
}

async function sendMessage(chat_uuid, message) {
    console.log(JSON.stringify({'chat': chat_uuid, 'message': message}))
    let response = await fetch(`http://127.0.0.1:8000/send-message`, {
        method: 'POST',
        body: JSON.stringify({'chat': chat_uuid[0], 'message': message}),
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken': csrftoken
        }
    })
    if (response.ok) { // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа
        let json = await response.json();
        console.log(json);
        getChatHistory(chat_uuid)
    }
    else {
        console.log("Ошибка HTTP: " + response.status);
    }
}

const button_submit = document.querySelector('.message-button');
button_submit.onclick = function() {
    let message_text = document.querySelector('.message-textarea');
    sendMessage(chat_uuid, message_text.value);
    message_text.value = "";
}

setInterval(getChatHistory, 1000, chat_uuid);