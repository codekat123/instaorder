from rest_framework.decorators import api_view
from rest_framework.response import Response 
from messaging.services import handle_message

@api_view(["POST"])
def meta_webhook(request):
    message = request.data.get("message", "")
    sender_id = request.data.get("sender_id", "123")  

    reply = handle_message(message, sender_id)

    return Response({"reply": reply})