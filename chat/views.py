# chat/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Message, ChatSession
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from openai import OpenAI

client = OpenAI(api_key='')
import json 

def ask_model(message):
    response    = client.chat.completions.create(
        model   ='gpt-3.5-turbo',
        messages= [
            {
                'role': 'assistant',
                'content': """
                            You are a comedian, your respond by jokes. 

                           """
            },
            {
                'role': 'user',
                'content': message
            },
        ] 
    ) 
    answer = response.choices[0].message.content.strip()
    return answer

# @csrf_exempt
# @api_view(['POST'])
# def send_message(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user = data['user']
#         content = data['content']

#         print(request.data)

#         # Find or create chat session
#         session, created = ChatSession.objects.get_or_create(user=user)

#         if not session.is_human:
#             # Use AI to generate response
            
#             ai_response = ask_model(content)

#             # Save AI message
#             Message.objects.create(sender='AI', content=ai_response)
#             return JsonResponse({'sender': 'AI', 'content': ai_response})

#         else:
#             # Save human message
#             Message.objects.create(sender='Human', content=content)
#             return JsonResponse({'sender': 'Human', 'content': content})



# def takeover(request, user):
#     session = ChatSession.objects.get(user=user)
#     session.is_human = True
#     session.save()
#     return JsonResponse({'status': 'success'})



# chat/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Message, ChatSession
from django.views.decorators.csrf import csrf_exempt
import openai
import json

openai.api_key = 'your_openai_api_key'

@csrf_exempt
@api_view(['POST'])
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']
        content = data['content']
        sender = data.get('sender', 'customer')  # Default sender is the customer

        # Find or create chat session
        session, created = ChatSession.objects.get_or_create(user=user)

        if not session.is_human:
            # Use AI to generate response
            
            ai_response = ask_model(content)
            
            # Save AI message
            Message.objects.create(sender='AI', content=ai_response, session=session)
            return JsonResponse({'sender': 'AI', 'content': ai_response})

        else:
            # Save human (business owner) message
            Message.objects.create(sender=sender, content=content, session=session)
            return JsonResponse({'sender': sender, 'content': content})



@csrf_exempt
@api_view(['POST'])
def takeover(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']
        business_owner = data['business_owner']
        
        session = ChatSession.objects.get(user=user)
        session.is_human = True
        session.business_owner = business_owner
        session.save()
        
        return JsonResponse({'status': 'success'})


@csrf_exempt
@api_view(['POST'])
def handover_to_ai(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = data['user']
        
        session = ChatSession.objects.get(user=user)
        session.is_human = False
        session.business_owner = None  # Clear the business owner once handed over
        session.save()
        
        # Send a message to notify that AI has taken over
        Message.objects.create(sender='AI', content='The business owner has handed the chat back to the AI assistant.', session=session)
        
        return JsonResponse({'status': 'success'})



# Add this to handle retrieval of messages (optional for frontend display)
def get_messages(request, user):
    session = ChatSession.objects.get(user=user)
    messages = session.messages.all().order_by('timestamp')
    return JsonResponse({'messages': [{'sender': msg.sender, 'content': msg.content, 'timestamp': msg.timestamp} for msg in messages]})
