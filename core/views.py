from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
# from .models import User_Models
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView, View
import json
from .serializers import UserSerializer, ProductSerializer
from .models import UserDetails, Product


class users_db_operations(View):
    @method_decorator(csrf_exempt)
    # create new user from signup form
    def post(self,request):
        try:
            data = json.loads(request.body)
           
            username = data['username']
            email = data['email_id']
            password = data['password']
            # birthday = data['birthday']
            new_user = User.objects.create_user(username=username, email=email, password=password)
            # UserDetails.objects.create(user=new_user, birthday=birthday)
            
            # new_user.save()
            
            return JsonResponse({"success":True,"message":"New user created successfully","record": data}, status=201)
        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
        
    # fetch user data to display on the frontend
    def get(self, request):
        try:
            user_id = request.GET.get('user_id')
            username = request.GET.get('username')
            # if user_id:
            #     user = User.objects.get(user_id=user_id)
            #     user_data = [{'username':user.username,"user_id":user.user_id,"email_id":user.email_id,"password":user.password,"birthday":user.birthday}]
            #     return JsonResponse({"success":True,"message":"user data fetched successfully","data":user_data}, status=200)
            
            if username:
                user = User.objects.get(username=username)
                user_data = [{'username':user.username,"email":user.email,"password":user.password}]
                return JsonResponse({"success":True,"message":"user data fetched successfully","data":user_data}, status=200)
            else:
                users = User.objects.all()
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

            user = User.objects.get(user_id=user_id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"success": True, "message": "User details updated successfully", "data": serializer.data}, status=200)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "User does not exist"}, status=404)

        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
    
    # delete user details by admin
    def delete(self, request):
        try:
            data = json.loads(request.body)
            user_id = data['user_id']
            deleted_user = User.objects.get(user_id=user_id)
            deleted_user.delete()
            return JsonResponse({"success":True,"message": "User deleted successfully", "user_id": user_id})
        
        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)

class productView(APIView):

    # create new product entry in the db
    def post(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            product_name = serializer.validated_data['product_name']
            description = serializer.validated_data['description']
            image_path = serializer.validated_data['image_path']

            new_product = Product(product_name=product_name, description=description, image_path=image_path)
            new_product.save()

            return Response({"success":True, "message":"Product inserted successfully", "details":request.data},status=201)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    # fetch product details by id and name
    def get(self, request):
        try:
            product_id = request.GET.get('product_id')
            product_name = request.GET.get('product_name')
            print(product_id)

            if product_id:
                product = Product.objects.get(product_id=product_id)
                product_data = [{'product_name': product.product_name, "description": product.description}]
                return Response({"success": True, "message": "Product data fetched successfully", "data": product_data}, status=200)
            
            elif product_name:
                try:
                    product = Product.objects.get(product_name=product_name)
                    print(product)
                    product_data = [{'product_name': product.product_name, "description": product.description}]
                    print(product_data)
                    return Response({"success": True, "message": "Product data fetched successfully", "data": product_data}, status=200)
                except Product.DoesNotExist:
                    return Response({"success": False, "message": "Product with the given name does not exist"}, status=404)
            
            else:
                products = Product.objects.all()
                product_data = [{'product_name': prod.product_name, "description": prod.description} for prod in products]
                return Response({"success": True, "message": "Products data fetched successfully", "data": product_data}, status=200)
        
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)

    # update product details by id
    def put(self, request):
        try:
            data = json.loads(request.body)
            product_id = data['product_id']

            product = Product.objects.get(product_id=product_id)

            serializer = ProductSerializer(product, data = request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"success": True, "message": "Product details updated successfully", "data": serializer.data}, status=200)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

        except Product.DoesNotExist:
            return JsonResponse({"success": False, "error": "Product does not exist"}, status=404)

        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)

    # delete product
    def delete(self, request):
        try:
            data = json.loads(request.body)
            product_id = data['product_id']
            deleted_product = Product.objects.get(product_id=product_id)
            deleted_product.delete()
            return JsonResponse({"success":True,"message": "Product deleted successfully", "prduct_id": product_id})
        
        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)


