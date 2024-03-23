from django.shortcuts import render
from .models import UserModels
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from .serializers import UserSerializer

class users_db_operations(APIView):
    
    # create new user from signup form
    def post(self,request):
        try:
            data = json.loads(request.body)
           
            username = data['username']
            user_id = data['user_id']
            email_id = data['email_id']
            password = data['password']
            birthday = data['birthday']
            new_user = UserModels(username=username, user_id=user_id, email_id=email_id, password=password, birthday=birthday)
        
            new_user.save()
            
            return JsonResponse({"success":True,"message":"New user created successfully","record": data}, status=201)
        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
        
    # fetch user data to display on the frontend
    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            username = request.GET.get('username')
            if user_id:
                user = UserModels.objects.get(user_id=user_id)
                user_data = [{'username':user.username,"user_id":user.user_id,"email_id":user.email_id,"password":user.password,"birthday":user.birthday}]
                return JsonResponse({"success":True,"message":"user data fetched successfully","data":user_data}, status=200)
            
            elif username:
                user = UserModels.objects.get(username=username)
                user_data = [{'username':user.username,"user_id":user.user_id,"email_id":user.email_id,"password":user.password,"birthday":user.birthday}]
                return JsonResponse({"success":True,"message":"user data fetched successfully","data":user_data}, status=200)
            else:
                users = UserModels.objects.all()
                print(users)
                user_data = [{'username':user.username,"user_id":user.user_id,"email_id":user.email_id,"password":user.password,"birthday":user.birthday}for user in users]

                return JsonResponse({"success":True,"message":"users data fetched successfully","data":user_data}, status=200)
        except Exception as e:
            return JsonResponse({"success":False, "error": str(e)}, status=500)    
        
    # update user details by admin
    def put(self, request):
        try:
            data = json.loads(request.body)
            user_id = data['user_id']

            user = UserModels.objects.get(user_id=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"success": True, "message": "User details updated successfully", "data": serializer.data}, status=200)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

        except UserModels.DoesNotExist:
            return JsonResponse({"success": False, "error": "User does not exist"}, status=404)

        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
    
    # delete user details by admin
    def delete(self, request):
        try:
            data = json.loads(request.body)
            user_id = data['user_id']
            deleted_user = UserModels.objects.get(user_id=user_id)
            deleted_user.delete()
            return JsonResponse({"success":True,"message": "User deleted successfully", "user_id": user_id})
        
        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
    