from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
# from .models import User_Models
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
import json
from .serializers import UserSerializer, ProductSerializer, CartSerializer, OrderSerializer, CustomOrderSerializer
from .models import UserDetails, Product, Cart, Orders, CustomOrders
from rest_framework.parsers import MultiPartParser, FormParser
import datetime
from django.db.models import Sum

class users_db_operations(APIView):
    # @method_decorator(csrf_exempt)
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
            if user_id:
                user = User.objects.get(id=user_id)
                user_data = [{'username':user.username,"user_id":user.id,"email_id":user.email, "password":user.password, "date_joined":user.date_joined, "last_login":user.last_login}]
                return JsonResponse({"success":True,"message":"user data fetched successfully","data":user_data}, status=200)
            
            elif username:
                user = User.objects.get(username=username)
                user_data = [{'username':user.username,"email":user.email,"password":user.password,"date_joined":user.date_joined, "last_login":user.last_login}]
                return JsonResponse({"success":True,"message":"user data fetched successfully","data":user_data}, status=200)
            else:
                users = User.objects.all()
                print(users)
                user_data = [{'username':user.username,"user_id":user.id,"email_id":user.email,"password":user.password,"date_joined":user.date_joined, "last_login":user.last_login}for user in users]

                return JsonResponse({"success":True,"message":"users data fetched successfully","data":user_data}, status=200)
        except Exception as e:
            return JsonResponse({"success":False, "error": str(e)}, status=500)    
        
    # update user details by admin
    def put(self, request):
        try:
            data = json.loads(request.body)
            user_id = data['user_id']

            user = User.objects.get(id=user_id)
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
            user_id = request.GET.get('user_id')
            deleted_user = User.objects.get(id=user_id)
            print(deleted_user)
            deleted_user.delete()
            return JsonResponse({"success":True,"message": "User deleted successfully", "user_id": user_id})
        
        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
        
    
    

class productView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    # create new product entry in the db
    def post(self, request):
        try:
            print(request.data)
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            product_name = serializer.validated_data['product_name']
            description = serializer.validated_data['description']
            price = serializer.validated_data['price']

            new_product = Product(product_name=product_name, description=description, price=price)
            new_product.save()

            if 'image' in request.data:               
                new_product.image = request.data['image']
                new_product.save()
            
            image_url = new_product.image.url if new_product.image else None
            # full_image_url = get_full_image_url(request, image_url)
            # print(full_image_url)

            return Response({"success":True, 
                             "message":"Product inserted successfully",
                             "data":{
                                     "product_name":product_name, 
                                     "description":description, 
                                     "price":price,
                                     "image":image_url
                                    }
                            },status=201)
        
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
                print(product)
            
                product_data = [{'product_name': product.product_name, "description": product.description, "price": product.price,"image":product.image.url}]
                
                return Response({
                                 "success": True, 
                                 "message": "Product data fetched successfully", 
                                 "data": {
                                     "product_name":product_data[0]['product_name'], 
                                     "description":product_data[0]['description'], 
                                     "price":product_data[0]['price'],
                                     "image":product_data[0]['image']
                                    }
                                 }, status=200)
            
            elif product_name:
                try:
                    product = Product.objects.get(product_name=product_name)
                    # print(product)
                    product_data = [{'product_name': product.product_name, "description": product.description, "price": product.price, "image":product.image.url}]
                    
                    print(product_data)
                   
                    return Response({
                                    "success": True, 
                                     "message": "Product data fetched successfully", 
                                     "data": {
                                                "product_name":product_data[0]['product_name'], 
                                                "description":product_data[0]['description'], 
                                                "price":product_data[0]['price'],
                                                "image":product_data[0]['image']
                                    }
                                }, status=200)
                except Product.DoesNotExist:
                    return Response({"success": False, "message": "Product with the given name does not exist"}, status=404)
            
            else:
                products = Product.objects.all()
                print(products)
                product_data = [{'product_id':product.product_id,'product_name': product.product_name, "description": product.description, "price": product.price, "image":product.image.url} for product in products]
                print(product_data)
                
                return Response({
                                 "success": True, 
                                 "message": "Products data fetched successfully", 
                                 "data": [{
                                     "product_id":product["product_id"],
                                     "product_name":product['product_name'], 
                                     "description":product['description'], 
                                     "price":product['price'],
                                     "image":product['image']
                                    } for product in product_data]
                                }, status=200)
        
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)

    # update product details by id
    parser_classes = (MultiPartParser, FormParser)
    def put(self, request):
        try:
            product_id = request.data.get('product_id')

            product = Product.objects.get(product_id=product_id)
            print(product)
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

class CartItems(APIView):
    def post(self, request):
        try:
            req = request.data
            product_id = req['product_id']
            user_id = int(req['user_id'])
            quantity = int(req['quantity'])
            product = Product.objects.get(product_id=product_id)
            product_name = product.product_name

            new_cart_item = Cart(product_id=product_id, product_name=product_name, user_id=user_id, quantity=quantity)
            new_cart_item.save()

            return Response({"success":True, 
                             "message":"Product inserted successfully",
                             "data":{
                                     "product_id":product_id,
                                     "product_name":product_name, 
                                     "quantity":quantity, 
                                     "added_by_user":user_id
                                    }
                            },status=201)
        
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    def put(self, request):
        try:
            data = json.loads(request.body)
            product_id = data['cart_item_id']

            product = Cart.objects.get(id=product_id)
            serializer = CartSerializer(product, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"success": True, "message": "Cart details updated successfully", "data": serializer.data}, status=200)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "User does not exist"}, status=404)

        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "error": "Cart item does not exist"}, status=404)

        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
        
    def get(self, request):
        try:
            product_id = request.GET.get('product_id')
            user_id = request.GET.get('user_id')
            cart_items = Cart.objects.filter(user_id=user_id)

            product_id = [product.product_id for product in cart_items]
            product_dict = {}
    
            for id in product_id:
                product_details = Product.objects.filter(product_id=id)
                product_serializer = ProductSerializer(product_details, many=True)
                product_dict[id] = product_serializer.data
            cart_serializer = CartSerializer(cart_items, many=True)
            
            return Response({"success": True, 
                             "message": "Cart items fetched successfully", 
                             "cart_details": cart_serializer.data,
                             "product_details":product_dict}, status=200)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=500)
    
    # delete cart items
    def delete(self, request):
        cart_item_id = request.GET.get('id')
        cart_item = Cart.objects.get(id=cart_item_id)
        print("+++++++++++++",cart_item)
        cart_serializer = CartSerializer(cart_item)
        print(cart_serializer)
        item_details = cart_serializer.data
        print(item_details)

        cart_item.delete()

        return Response({"success":"true",
                         "message":"Item deleted from the cart",
                         "item_details":item_details
                         },status=200)
        
class ConfirmOrder(APIView):
    def post(self, request):
        request_data = request.data
        cart_item_id = request_data['cart_item_id']
        user_id = request_data['user_id']
        amount = request_data['amount']
        customer_name = request_data['name']
        contact = request_data['contact']
        address = request_data['address']


        cart_items = Cart.objects.filter(id=cart_item_id)
        cart_serializer = CartSerializer(cart_items, many=True)
        print(cart_items)
        order = cart_serializer.data
        print(order)
        product_id = order[0]['product_id']
        # order_status = order[0]['ordered']

        new_order = Orders(cart_item_id=cart_item_id, user_id=user_id, amount=amount, product_id=product_id,customer_name=customer_name,contact=contact, address=address)
        new_order.save()

        Cart.objects.filter(id=cart_item_id).update(ordered=True)
        # cart_items.delete()

        return Response({"success":"true",
                            "message":"Order placed successfully",
                            "order_details":{"ordered_cart_item":cart_item_id,
                                            "ordered_by":user_id,
                                            "order_amount":amount
                                            }
                                        },status=201)
        
    def put(self, request):
        try:
            data = json.loads(request.body)
            order_id = data['order_id']

            order = Orders.objects.get(order_id=order_id)
            serializer = OrderSerializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"success": True, "message": "Order details updated successfully", "data": serializer.data}, status=200)
            return JsonResponse({"success": False, "errors": serializer.errors}, status=400)

        except Cart.DoesNotExist:
            return JsonResponse({"success": False, "error": "Requested order item does not exist"}, status=404)

        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
        
    def get(self, request):
        try:
            order_id = request.GET.get('order_id')
            user_id = request.GET.get('user_id')
           
            if order_id:
                order_item = Orders.objects.get(order_id=order_id)
                print(order_item)
                # product_id = order_item.product_id
                order_serializer = OrderSerializer(order_item)
                order_details = order_serializer.data
                print(order_details)
                product_id = order_details['product_id']
                print(product_id)

                product = Product.objects.get(product_id=product_id)
                product_serializer = ProductSerializer(product)
                product_details = product_serializer.data
            
                return Response({"success":"true",
                                "message":"order details fetched successfully",
                                "order_details":order_details,
                                "product_details": product_details
                                }, status=200)
            
            elif user_id:
                order_item = Orders.objects.get(user_id=user_id)
                print(order_item)
                # product_id = order_item.product_id
                order_serializer = OrderSerializer(order_item)
                order_details = order_serializer.data
                print(order_details)
                product_id = order_details['product_id']
                print(product_id)

                product = Product.objects.get(product_id=product_id)
                product_serializer = ProductSerializer(product)
                product_details = product_serializer.data
            
                return Response({"success":"true",
                                "message":"order details fetched successfully",
                                "order_details":order_details,
                                "product_details": product_details
                                }, status=200)
            
            else:
                order_items = Orders.objects.all()
                order_serializer = OrderSerializer(order_items, many=True)
                orders = order_serializer.data
                order_list = [dict(order) for order in orders]
                
                product_id = [order["product_id"] for order in order_list]
                print(product_id)
                product_dict = {}
                
                for id in product_id:
                    product = Product.objects.get(product_id=id)
                    product_serializer = ProductSerializer(product)
                    product_details = product_serializer.data
                    product_dict[id]=product_details


                return Response({"success":"true",
                                 "message":"order details fetched successfully",
                                 "order_list":order_list,
                                 "product_data":product_dict
                }, status=200)
            
        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
        

    def delete(self, request):
        try:
            order_id = request.GET.get('order_id')
            deleted_product = Orders.objects.get(order_id=order_id)
            deleted_product.delete()
            return JsonResponse({"success":True,"message": "Order deleted successfully", "order_id": order_id})
        
        except Exception as e:
            return JsonResponse({"success":False,"error": str(e)}, status=500)
        

class OrdersCount(APIView):
    def get(self, request):
        orders_count = Orders.objects.count()
        return Response({"orders_count": orders_count}, status=200)
    

def orders_total_amount(request):
    total_amount = Orders.objects.aggregate(total_amount=Sum('amount'))['total_amount']
    return JsonResponse({'total_amount': total_amount})


def fetch_order_data(request):
    try:
        orders = Orders.objects.all()
        order_data = []
        for order in orders:
            order_info = {
                'order_id': order.order_id,
                'cart_item_id': order.cart_item_id,
                'product_id': order.product_id,
                'user_id': order.user_id,
                'order_date': order.order_date.strftime('%Y-%m-%d'),  # Format date as string
                'amount': order.amount,
                'customer_name': order.customer_name,
                'contact': order.contact,
                'address': order.address
            }
            order_data.append(order_info)
        return JsonResponse({'success': True, 'data': order_data})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

class CustomOrder(APIView):
    def post(self, request):
        data = json.loads(request.body)
        # print(request.body)
        custom_order = CustomOrders(
            cake_flavor=data['cake_flavor'],
            filling=data['filling'],
            frosting=data['frosting'],
            decoration_style=data['decoration_style'],
            color_scheme=data['color_scheme'],
            message_on_cake=data['message_on_cake'],
            dietary_restrictions=data['dietary_restrictions'],
            special_instructions=data['special_instructions'],
            name=data['name'],
            contact=data['contact'],
            address=data['address']
        )
        custom_order.save()
        return Response({'message': 'Cake order submitted successfully.'})
    
    def get(self, request):
        custom_orders = CustomOrders.objects.all()
        serializer = CustomOrderSerializer(custom_orders, many=True)
        return Response(serializer.data)