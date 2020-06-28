from django.shortcuts import render, redirect
import json
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.shortcuts import render
from .models import User, Contact, Message, Chat

def index(request):
    return render(request, 'chat/index.html')

def get_user_contact(phone):
    try:
        user = User.objects.get(phone = phone)
    except User.DoesNotExist:
        user = None
    try:
        contact = Contact.objects.get(user = user)
    except Contact.DoesNotExist:
        contact = None

    return contact

def get_user_chats(request):
    phone = request.session.get('user', None)
    contact = get_user_contact(phone)
    if contact:
        return contact.chats.all()
    else:
        return None

def last_30_messages(chatID):
    try:
        chat = Chat.objects.get(id = chatID)
        return chat.messages.order_by('-timestamp').all()[:30]
    except Chat.DoesNotExist:
        return None
    


def room(request, room_name):
      
    if request.POST.get('user_submit'):
        if User.objects.filter(phone = request.POST.get('user_phone'), name = request.POST['user_name']).exists():
            user = User.objects.get(phone = request.POST.get('user_phone'), name = request.POST['user_name'])
            user_contact = Contact.objects.get(user = user)
            messages.success(request, 'User Logged in successfully!')
        else:
            user = User.objects.create(phone = request.POST.get('user_phone'), name = request.POST['user_name'])
            user_contact = Contact.objects.create(user = user)
            messages.success(request, 'User Created successfully!')
        
        request.session['user'] = user.phone

    try:
        user = User.objects.get(phone = request.session.get('user', None))
        user_contact = Contact.objects.get(user = user)
    except User.DoesNotExist:
        user = None
        return render(request, 'chat/all_conv.html', {
            'username': mark_safe(json.dumps(request.session.get('user', None))),
            'user_obj': user,
        })

    chat = Chat.objects.get(id = room_name) 
    chat_participants = list(chat.participants.all())
    chat_participants.remove(user_contact)
    chat_edited = {
        'chat': chat,
        'other_user': chat_participants[0]
    }

        
    print(request.session.items())
    return render(request, 'chat/chat_inner.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username': mark_safe(json.dumps(request.session.get('user', None))),
        'user_obj': user,
        'is_recent_active':'active',
        'chat':chat_edited,
    })

def all_conv(request):
      
    if request.POST.get('user_submit'):
        if User.objects.filter(phone = request.POST.get('user_phone'), name = request.POST['user_name']).exists():
            user = User.objects.get(phone = request.POST.get('user_phone'), name = request.POST['user_name'])
            user_contact = Contact.objects.get(user = user)
            messages.success(request, 'User Logged in successfully!')
        else:
            user = User.objects.create(phone = request.POST.get('user_phone'), name = request.POST['user_name'])
            user_contact = Contact.objects.create(user = user)
            messages.success(request, 'User Created successfully!')
        
        request.session['user'] = user.phone

    try:
        user = User.objects.get(phone = request.session.get('user', None))
        user_contact = Contact.objects.get(user = user)
    except User.DoesNotExist:
        user = None
        return render(request, 'chat/all_conv.html', {
            'username': mark_safe(json.dumps(request.session.get('user', None))),
            'user_obj': user,
        })
    
    print(request.session.items())

    chats = get_user_chats(request)
    chats_edited = []
    for chat in chats:
        chat_participants = list(chat.participants.all())
        chat_participants.remove(user_contact)
        chats_edited.append({
            'chat': chat,
            'other_user': chat_participants[0]
        })
    
    return render(request, 'chat/all_conv.html', {
        'username': mark_safe(json.dumps(request.session.get('user', None))),
        'user_obj': user,
        'is_all_active': 'active',
        'user_chats': chats_edited,
    })

def logout(request):
    request.session.pop('user', None)
    print(request.session.items())
    return redirect('chat:all_conv')