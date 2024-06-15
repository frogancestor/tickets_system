from django.shortcuts import render
from django.http import HttpResponse
from .models import Credentials
from .models import Categories
from .models import Status
from .models import Priority
from .models import Ticket
from .models import Users
from .models import SupportEmployers
from .models import CategorySupportAssociation
from .models import CustomAttributeType
from .models import CustomAttribute
from .models import CategoryCustomAttribute
from .models import StrAttributeData
from .models import TextAttributeData
from .models import ListAttributeDataReference
from .models import ListAttributeData
from .models import AutorizatedPeople
from .models import Attachments
from .models import SupportAdmin
from .models import Chat
from .models import Message
import json
import uuid
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from django.core.files.storage import default_storage
from support.settings import MEDIA_ROOT, MEDIA_URL
from datetime import timedelta
# Create your views here.


def autorisation_view(request):
    return render(request, "index.html")


def chose_role_page_view(request):
    return render(request, "chooserole.html")


def post_authorisation(request):
    login = request.POST.get("login", "Undefined")
    password = request.POST.get("password", "1")
    data = {"alert": "", 'auth_token': ''}
    template_name = "index.html"
    sup_user = Credentials.objects.all().filter(login=login)
    # проверка на существование пользователя
    if sup_user:
        if sup_user[0].password == password:
            user_id = sup_user[0].user
            next_page = redirectPerson(checkUserInTables(user_id))
            newAutorization = AutorizatedPeople(token=uuid.uuid4().__str__(), person=sup_user[0].user)
            newAutorization.save()
            data['auth_token'] = newAutorization.token
            data['next_page'] = next_page
            template_name = 'redir.html'
        else:
            data = {"alert": "Неправильный пароль"}
            template_name = "index.html"
    else:
        data = {"alert": "Такого пользователя не существует"}
        template_name = "index.html"
    return render(request, template_name, context=data)


def tickets_view(request):
    selected_elements = {"categories": {}, "statuses": {}, "priorities": {}, 'user': getUserFullName(request.COOKIES.get('auth_token'))}
    categories = Categories.objects.all()
    statuses = Status.objects.all()
    priorities = Priority.objects.all()

    for element in categories:
        selected_elements["categories"][element.id] = element.category

    for element in statuses:
        selected_elements["statuses"][element.id] = element.status

    for element in priorities:
        selected_elements["priorities"][element.id] = element.priority

    return render(request, "tickets_page.html", context=selected_elements)


def tickets_list_view(request):
    authorised_person = AutorizatedPeople.objects.get(token=request.COOKIES.get('auth_token')).person
    authorised_support = SupportEmployers.objects.all().filter(person=authorised_person)
    if len(authorised_support) == 1:
        authorised_support = authorised_support[0]
        authorised_support = CategorySupportAssociation.objects.get(support_employee=authorised_support)
        ticket_id = request.GET.get("id", "")
        if ticket_id == "":
            authorised_admin = SupportAdmin.objects.all().filter(person=authorised_person)
            if len(authorised_admin) == 1:
                tickets = Ticket.objects.all().filter(**filterTicketsList(request))
            else:
                tickets = Ticket.objects.all().filter(support_employee=authorised_support, **filterTicketsList(request))
        else:
            tickets = Ticket.objects.all().filter(id=ticket_id)
        ticket_objects = collectTicketsData(tickets)
    else:
        print("Ошибка с количеством User в функции tickets_list_view")
    return HttpResponse(json.dumps(ticket_objects, ensure_ascii=False))


def user_create_ticket_page(request):
    selected_elements = {"categories": {}, "priorities": {}, 'user': getUserFullName(request.COOKIES.get('auth_token'))}
    categories = Categories.objects.all()
    priorities = Priority.objects.all()
    for element in categories:
        selected_elements["categories"][element.id] = element.__str__()

    for element in priorities:
        selected_elements["priorities"][element.id] = element.__str__()

    for key, value in selected_elements["categories"].items():
        print(key, value)
    for key, value in selected_elements["priorities"].items():
        print(key, value)

    print(selected_elements) # проверка
    return render(request, "usercreateapp.html", context=selected_elements)


def get_category_custom_attribute(request):
    result = {
        "custom_atr": []
    }
    id_category = request.GET.get('category', '')
    print(id_category)
    if id_category != "":
        cat = Categories.objects.get(id=id_category)
        print(cat)
        categoryCustomAtr = CategoryCustomAttribute.objects.all().filter(category=cat)
        for attribute in categoryCustomAtr:
            atr_type = attribute.custom_attribute.typeOfAttribute.name
            custom_atr_data = {
                'id': attribute.custom_attribute.id,
                'name': attribute.custom_attribute.name,
                'type': atr_type,
            }
            if atr_type == 'list':
                listOptions = []
                list_data = ListAttributeDataReference.objects.all().filter(attribute=attribute.custom_attribute)
                for data in list_data:
                    listOptions.append({
                        'id': data.id,
                        'name': data.data,
                    })
                custom_atr_data['list_options'] = listOptions
                    
            result['custom_atr'].append(custom_atr_data)

    print(result)
    return HttpResponse(json.dumps(result, ensure_ascii=False))


def get_user_ticket(request):
    id_category = request.POST.get("categories")
    # print(id_category)
    title = request.POST.get("title")
    description = request.POST.get("description")
    id_priority = request.POST.get("priority-choice")
    priority = Priority.objects.all().filter(id=id_priority)[0]
    person = AutorizatedPeople.objects.get(token=request.COOKIES.get('auth_token')).person
    user = Users.objects.all().filter(person=person)
    if len(user) == 1:
        user = user[0]
        category = Categories.objects.all().filter(id=id_category)[0]
        status = Status.objects.all()[0]
        ticket = Ticket(title=title, description=description, user=user, priority=priority, status=status, category=category)
        ticket.save()
        chat = Chat(ticket=ticket)
        chat.save()

        for file in request.FILES.getlist('files'):
            file_name = default_storage.save(os.path.join(MEDIA_ROOT, file.name), file)
            extension = file_name.split('.')[-1]
            file_name = file_name.split('.')[0]
            newAttach = Attachments(file_name=os.path.join(MEDIA_URL, file_name), file_extension=extension, ticket=ticket)
            newAttach.save()

        cat = Categories.objects.get(id=id_category)
        categoryCustomAtr = CategoryCustomAttribute.objects.all().filter(category=cat)
        for custom_atr in categoryCustomAtr:
            custom_atr_id = custom_atr.custom_attribute.id
            custom_atr_data = request.POST.get(str(custom_atr_id))
            custom_atr_type = custom_atr.custom_attribute.typeOfAttribute.name
            if custom_atr_type == "str":
                newStrAtrData = StrAttributeData(data=custom_atr_data, attribute=custom_atr.custom_attribute, ticket=ticket)
                newStrAtrData.save()
            elif custom_atr_type == "text":
                newTextAtrData = TextAttributeData(data=custom_atr_data, attribute=custom_atr.custom_attribute, ticket=ticket)
                newTextAtrData.save()
            elif custom_atr_type == "list":
                list_data = ListAttributeDataReference.objects.get(id=custom_atr_data)
                newListAtrData = ListAttributeData(data=list_data, attribute=custom_atr.custom_attribute, ticket=ticket)
                newListAtrData.save()
            else:
                print("NO SUCH TYPE")

        data = {"alert": "Заявка добавлена"}
    else:
        print("Ошибка с количеством User в функции get_user_ticket")
        data = {"alert": "Не получилось создать заявку"}
    # print(title, description, priority, user, category)
    return render(request, "usercreateapp.html", context=data)


def user_tickets(request):    
    data = {'user': getUserFullName(request.COOKIES.get('auth_token'))}
    return render(request, "userapp.html", context=data)


def get_user_tickets_list(request):
    authorised_person_token = request.COOKIES.get('auth_token')
    authorised_person = AutorizatedPeople.objects.get(token=authorised_person_token).person
    authorised_user = Users.objects.all().filter(person=authorised_person)
    if len(authorised_user) == 1:
        authorised_user = authorised_user[0]
        all_user_tickets = {'statuses': [], 'tickets': {}}
        statuses = Status.objects.all()
        for status in statuses:
            tickets = Ticket.objects.all().filter(user=authorised_user, status=status)
            status_data = {
                "id": status.id,
                "name": status.status,
            }
            all_user_tickets["statuses"].append(status_data)
            all_user_tickets["tickets"][status.id] = []
            for ticket in tickets:
                support = ""
                if ticket.support_employee is not None:
                    support = ticket.support_employee.support_employee.__str__()
                ticket_data = {
                    "id": ticket.id,
                    "title": ticket.title,
                    "description": ticket.description,
                    "support": support,
                    "priority": ticket.priority.__str__(),
                    "category": ticket.category.__str__(),
                }
                all_user_tickets["tickets"][status.id].append(ticket_data)
        
        print(statuses[0], statuses[1], statuses[2], statuses[3])
        print(all_user_tickets)
    else:
        print("Ошибка с количеством User в функции get_user_tickets_list")
    
    return HttpResponse(json.dumps(all_user_tickets, ensure_ascii=False))


def open_ticket_support(request, id):
    data = {'statuses': {}, 'priorities': {}, 'person': getUserFullName(request.COOKIES.get('auth_token'))}
    ticket = Ticket.objects.get(id=id)
    chat = ''
    try:
        chat = Chat.objects.all().filter(ticket=ticket)[0].chat_name
    except:
        pass
    data["title"] = ticket.title
    data["description"] = ticket.description
    data["user"] = ticket.user.__str__()
    data["support_employee"] = ticket.support_employee.__str__()
    data["priority"] = ticket.priority.__str__()
    data["status"] = ticket.status.__str__()
    data["category"] = ticket.category.__str__()
    data['files'] = []
    data['chat_id'] = chat
    data['ticket_id'] = ticket.id
    files = Attachments.objects.all().filter(ticket=ticket)
    for file in files:
        data['files'].append({
            'name': file.file_name.split('/')[-1],
            'full_name': file.file_name,
            'ext': file.file_extension
        })
    statuses = Status.objects.all()
    priorities = Priority.objects.all()
    for element in statuses:
        data["statuses"][element.id] = element.__str__()

    for element in priorities:
        data["priorities"][element.id] = element.__str__()

    return render(request, "open_ticket_support.html", context=data)


def open_ticket_user(request, id):
    data = {'statuses': {}, 'priorities': {}, 'person': getUserFullName(request.COOKIES.get('auth_token'))}
    ticket = Ticket.objects.get(id=id)
    data["title"] = ticket.title
    data["description"] = ticket.description
    data["user"] = ticket.user.__str__()
    data["support_employee"] = ticket.support_employee.__str__()
    data["priority"] = ticket.priority.__str__()
    data["status"] = ticket.status.__str__()
    data["category"] = ticket.category.__str__()
    data['files'] = []
    files = Attachments.objects.all().filter(ticket=ticket)
    for file in files:
        data['files'].append({
            'name': file.file_name.split('/')[-1],
            'full_name': file.file_name,
            'ext': file.file_extension
        })
    statuses = Status.objects.all()
    priorities = Priority.objects.all()
    for element in statuses:
        data["statuses"][element.id] = element.__str__()

    for element in priorities:
        data["priorities"][element.id] = element.__str__()

    return render(request, "open_ticket_user.html", context=data)


def chat_page_view(request, id, chat_uuid):
    data = {'person': getUserFullName(request.COOKIES.get('auth_token'))}
    return render(request, "chat_page.html", context=data)


def get_chat_history_view(request):
    chat_uuid = request.GET.get('chat', '')
    result = {'messages':[]}
    if chat_uuid != '':
        chat = Chat.objects.all().filter(chat_name=chat_uuid)
        if len(chat) == 1:
            messages = Message.objects.all().filter(chat=chat[0])
            for element in messages:
                result["messages"].append({
                    'sender': f'{element.sender.name} {element.sender.surname}',
                    'datetime': str(element.date_time + timedelta(hours=3)),
                    'message': element.message
                })

    return HttpResponse(json.dumps(result, ensure_ascii=False))


def send_message(request):
    post_data = json.loads(request.body.decode('utf-8'))
    authorised_person_token = request.COOKIES.get('auth_token')
    authorised_person = AutorizatedPeople.objects.get(token=authorised_person_token).person
    chat_uuid = post_data.get('chat', '')
    message_text = post_data.get('message', '')
    print(f'chat: {chat_uuid}')
    print(f'message: {message_text}')
    if chat_uuid != '' and message_text != '':
        chat = Chat.objects.all().filter(chat_name=chat_uuid)
        if len(chat) == 1:
            message = Message(chat=chat[0], sender=authorised_person, message=message_text)
            message.save()

    return HttpResponse(json.dumps({'status': 'ok'}))


def change_ticket(request):
    post_data = json.loads(request.body.decode('utf-8'))
    id_priority = post_data.get("priority")
    priority = Priority.objects.all().filter(id=id_priority)[0]
    id_status = post_data.get("status")
    status = Status.objects.all().filter(id=id_status)[0]
    id_ticket = post_data.get("ticket")
    ticket = Ticket.objects.filter(id=id_ticket)
    user_email = ticket[0].user.person.email
    print(user_email)
    if id_priority != 0 and id_status != 0:
        ticket.update(priority=priority, status=status)
        send_email(user_email, 'Смена статуса заявки', f'Статус заявки {id_ticket} изменён на {status.status}')
    elif id_priority != 0:
        ticket.update(priority=priority)
    elif id_status != 0:
        ticket.update(status=status)
    else:
        print('в функции change_ticket что-то пошло не так')
    return HttpResponse(json.dumps({'status': 'ok'}))


def add_custom_atr_view(request):
    data = {'person': getUserFullName(request.COOKIES.get('auth_token')), 'categories': {}, 'custom_atr_types': {}}
    categories = Categories.objects.all()
    custom_atr_types = CustomAttributeType.objects.all()
    for element in categories:
        data["categories"][element.id] = element.__str__()
    for element in custom_atr_types:
        data["custom_atr_types"][element.id] = element.__str__()

    return render(request, "create_custom_atr.html", context=data)


def create_custom_atr(request):
    post_data = json.loads(request.body.decode('utf-8'))
    name = post_data.get("name")
    id_customType = post_data.get("customType")
    customType = CustomAttributeType.objects.all().filter(id=id_customType)[0]
    id_category = post_data.get("category")
    category = Categories.objects.all().filter(id=id_category)[0]
    el_list = post_data.get("list")
    newCustomAttribute = CustomAttribute(name=name, typeOfAttribute=customType)
    newCustomAttribute.save()
    newCategoryAttributeAssoc = CategoryCustomAttribute(category=category, custom_attribute=newCustomAttribute)
    newCategoryAttributeAssoc.save()
    if customType.name == 'list':
        for element in el_list:
            newAtrReference = ListAttributeDataReference(data=element, attribute=newCustomAttribute)
            newAtrReference.save()
    print(name, customType, category, el_list)
    return HttpResponse(json.dumps({'status': 'ok'}))


# ======================================================
# служебные функции


def checkUserInTables(user_id):
    usersTable = Users.objects.all().filter(person=user_id)
    suportsTable = SupportEmployers.objects.all().filter(person=user_id)
    flag = 0
    if usersTable and suportsTable:
        flag = 1
    elif usersTable:
        flag = 2
    elif suportsTable:
        flag = 3
    return flag


def redirectPerson(flag):
    redirect = ""
    if flag == 1:
        redirect = "chose-role"
    elif flag == 2:
        redirect = "user-tickets"
    elif flag == 3:
        redirect = "tickets"
    return redirect


def getUserFullName(token):
    result = {'name': 'none', 'second_name': 'none'}
    userToken = AutorizatedPeople.objects.get(token=token)
    result['name'] = userToken.person.name
    result['second_name'] = userToken.person.surname
    return result


def filterTicketsList(request):
    result = {}

    categories = request.GET.get('categories', '')
    priorities = request.GET.get('priorities', '')
    statuses = request.GET.get('statuses', '')
    if categories != '':
        categories = categories.split('_')
        categories = tuple(categories)
        search_categories = Categories.objects.all().filter(id__in=categories)
        result['category__in'] = tuple(search_categories)
    else:
        print("len of categories is 0")
    if priorities != '':
        priorities = priorities.split('_')
        priorities = tuple(priorities)
        search_priorities = Priority.objects.all().filter(id__in=priorities)
        result['priority__in'] = tuple(search_priorities)
    else:
        print("len of priorities is 0")
    if statuses != '':
        statuses = statuses.split('_')
        statuses = tuple(statuses)
        search_statuses = Status.objects.all().filter(id__in=statuses)
        result['status__in'] = tuple(search_statuses)
    else:
        print("len of statuses is 0")
    # print(result)
    return result


def collectTicketsData(tickets):
    ticket_objects = {
        "tickets": []
    }
    for ticket in tickets:
        support = ""
        if ticket.support_employee is not None:
            support = ticket.support_employee.support_employee.__str__()
        ticket_data = {
            "id": ticket.id,
            "title": ticket.title,
            "description": ticket.description,
            "user": ticket.user.person.__str__(),
            "support": support,
            "priority": ticket.priority.__str__(),
            "status": ticket.status.__str__(),
            "category": ticket.category.__str__(),
            "custom_atr": []
        }
        categoryCustomAtr = CategoryCustomAttribute.objects.all().filter(category=ticket.category)
        for attribute in categoryCustomAtr:
            name = attribute.custom_attribute.name
            atr_type = attribute.custom_attribute.typeOfAttribute.name
            atrData = ''
            if atr_type == "str":
                atrData = StrAttributeData.objects.all().filter(attribute=attribute.custom_attribute, ticket=ticket)
            elif atr_type == 'text':
                atrData = TextAttributeData.objects.all().filter(attribute=attribute.custom_attribute, ticket=ticket)
            elif atr_type == 'list':
                atrData = ListAttributeData.objects.all().filter(attribute=attribute.custom_attribute, ticket=ticket)

            if len(atrData) > 0:
                if atr_type == 'list':
                    atrData = atrData[0].data.data
                else:
                    atrData = atrData[0].data
            else:
                atrData = ''
            ticket_data['custom_atr'].append({
                'name': name,
                'type': atr_type,
                'data': atrData
            })
        ticket_objects["tickets"].append(ticket_data)
    return ticket_objects

def send_email(recipient, subject, email_text) -> None:
    gmail_user = 'tickets.sup.sys@gmail.com'
    gmail_password = 'bovp ltzw iqea kcey'

    sent_from = 'tickets_support_system'
    msg = MIMEText(email_text, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = gmail_user
    msg['To'] = recipient

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, [recipient], msg.as_string())
        server.close()
    except Exception as e:
        print(e)