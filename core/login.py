from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        print(username, password)

        user = authenticate(request, username=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
            session_id = request.session.session_key
            user = User.objects.get(username=username)
            user_data = [{'username':user.username,"user_id":user.id,"email_id":user.email}]
            return JsonResponse({"success": True, 
                                 "message":"Login successful",
                                 "session_id":session_id,
                                 "username":user_data[0]['username'],
                                 "user_id":user_data[0]['user_id'],
                                 "email_id":user_data[0]["email_id"]},status=200)
        else:
            return JsonResponse({"success": False, "error": "Invalid username or password"}, status=400)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return JsonResponse({"success": True, "message":"Logged out successfully"})
