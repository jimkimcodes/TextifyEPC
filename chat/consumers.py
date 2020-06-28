import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, User, Chat, Contact
from .views import last_30_messages

class ChatConsumer(WebsocketConsumer):

    def get_messages(self, data):
        messages = last_30_messages(data['chatID'])
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))

        return result

    def message_to_json(self, message):
        return {
            'id': message.id,
            'author': message.contact.user.phone,
            'content': message.content,
            'timestamp': str(message.timestamp),
        }

    def new_message(self, data):
        author_phone = data['from']
        author_user = User.objects.get(phone=author_phone)
        author_contact = Contact.objects.get(user = author_user)
        message = Message.objects.create(contact = author_contact, content=data['message'])
        current_chat = Chat.objects.get(id = data['chatID'])
        current_chat.messages.add(message)
        current_chat.save()
        print(data)
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }

        return self.send_chat_message(content)

    def to_new_user(self, data):
        to_phone = data['to']
        try:
            to_user = User.objects.get(phone=to_phone)
            to_contact = Contact.objects.get(user = to_user)
        except User.DoesNotExist:
            content = {
                'command': 'New_user_not_found',
            }
            return self.send_chat_message(content)

        author_phone = data['from']
        author_user = User.objects.get(phone=author_phone)
        author_contact = Contact.objects.get(user = author_user)
        message = Message.objects.create(contact = author_contact, content=data['message'])

        chat_found = False
        for chat in Chat.objects.all():
            if author_contact in chat.participants.all() and to_contact in chat.participants.all():
                current_chat = chat
                chat_found = True
                break

        if not chat_found:
            current_chat = Chat.objects.create()
            current_chat.participants.add(author_contact)
            current_chat.participants.add(to_contact)

        current_chat.messages.add(message)
        current_chat.save()

        messages = last_30_messages(current_chat.id)
        content = {
            'command': 'got_chat',
            'chatID': current_chat.id,
            'messages': self.messages_to_json(messages)
        }

        return self.send_chat_message(content)


    commands = {
        'get_messages': get_messages,
        'new_message': new_message,
        'to_new_user': to_new_user,
    }

    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data  = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']
        self.send(text_data=json.dumps(message))