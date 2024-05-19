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
import json
import uuid
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

    for element in range(len(categories)):
        selected_elements["categories"][element] = categories[element]

    for element in range(len(statuses)):
        selected_elements["statuses"][element] = statuses[element]

    for element in range(len(priorities)):
        selected_elements["priorities"][element] = priorities[element]

    return render(request, "tickets_page.html", context=selected_elements)


def tickets_list_view(request):
    ticket_id = request.GET.get("id", "")
    if ticket_id == "":
        tickets = Ticket.objects.all()
    else:
        tickets = Ticket.objects.all().filter(id=ticket_id)
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
        print(ticket_objects)
    return HttpResponse(json.dumps(ticket_objects, ensure_ascii=False))


def user_create_ticket_page(request):
    selected_elements = {"categories": {}, "priorities": {}}
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


def user_attribute(request):
    pass


def get_user_ticket(request):
    id_category = request.POST.get("categories")
    # print(id_category)
    title = request.POST.get("title")
    description = request.POST.get("description")
    id_priority = request.POST.get("priority-choice")
    priority = Priority.objects.all().filter(id=id_priority)[0]
    user = Users.objects.all()[0]
    category = Categories.objects.all().filter(id=id_category)[0]
    status = Status.objects.all()[0]
    ticket = Ticket(title=title, description=description, user=user, priority=priority, status=status, category=category)
    ticket.save()
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

    data = {"alert": "получилось"}
    # print(title, description, priority, user, category)
    return render(request, "usercreateapp.html", context=data)


def user_tickets(request):
    data = {'user': getUserFullName(request.COOKIES.get('auth_token'))}
    return render(request, "userapp.html", context=data)


def get_user_tickets_list(request):
    all_user_tickets = {'statuses': [], 'tickets': {}}
    statuses = Status.objects.all()
    for status in statuses:
        tickets = Ticket.objects.all().filter(status=status)
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
                "title": ticket.title,
                "description": ticket.description,
                "support": support,
                "priority": ticket.priority.__str__(),
                "category": ticket.category.__str__(),
            }
            all_user_tickets["tickets"][status.id].append(ticket_data)
    
    print(statuses[0], statuses[1], statuses[2], statuses[3])
    print(all_user_tickets)
    return HttpResponse(json.dumps(all_user_tickets, ensure_ascii=False))


def open_ticket_support(request, id):
    data = {}
    ticket = Ticket.objects.get(id=id)
    data["title"] = ticket.title
    data["description"] = ticket.description
    data["user"] = ticket.user.__str__()
    data["support_employee"] = ticket.support_employee.__str__()
    data["priority"] = ticket.priority.__str__()
    data["status"] = ticket.status.__str__()
    data["category"] = ticket.category.__str__()

    return render(request, "open_ticket_support.html", context=data)


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
