       🛒 Electron Market REST API
A fully functional Ecommerce REST API built with Django and Django REST Framework.
This project provides backend functionality for an online electronics store, including product management, 
cart operations, and order processing with proper stock control and transaction safety.
            Features:
User registration & authentication (JWT)
Product listing and management
Category-based products
Cart management (add, remove, clear)
Order creation from cart
Automatic stock reduction
Order cancellation with stock rollback
Order status progression (admin only)
Role-based permissions (User / Admin)
Transaction-safe order processing
            Tech Stack:
Python
Django
Django REST Framework
SQLite (default database)
JWT Authentication

                  AUTH
http://127.0.0.1:8000/auth/sign-up/
sign up :
POST
{
    "username": "testuser",
    "first_name": "nurmanova",
    "email": "test@example.com",
    "password": "testuser",
    "confirm_pass": "testuser"
}

http://127.0.0.1:8000/auth/login/
 login:
POST
{
    "username": "testuser",
    "password": "testuser",
}

http://127.0.0.1:8000/auth/logout/
logout:
POST
{
"refresh" : "refresh_token"
}

http://127.0.0.1:8000/auth/profile/
Profile:
GET


http://127.0.0.1:8000/auth/profile/update/
UPDATE PROFILE:
PATCH
{
   "first_name":"Jasmin"
}


http://127.0.0.1:8000/auth/profile/photo/
Photo profile update
PATCH:
file 


http://127.0.0.1:8000/auth/profile/change-pass/
Change-password
POST
{
   "old_password":"testuser",
   "new_password":"testuserrr",
   "confirm_password":"testuserrr"
}

                  PRODUCT
http://127.0.0.1:8000/products/create-product/
Create Product
POST
{
    "title": "MacBook Air M2",
    "category": 1,
    "quantity": 125,
    "description": "Apple laptop",
    "price": "1200.00"
    
}
        
http://127.0.0.1:8000/products/create-category/
Create Category
POST
{
    "name": "Candy"
}     


http://127.0.0.1:8000/products/products/
Products List
GET

http://127.0.0.1:8000/products/detail/2/
Product detail
GET

http://127.0.0.1:8000/products/delete-update/2/
Delete Update Product
PATCH DELETE


                      COMMENTS
http://127.0.0.1:8000/products/cr-comment/2/
CREATE READ Comment
GET POST
{
    "text": "Krossovki zormas yoqmadi"
    
}


http://127.0.0.1:8000/products/ud-comment/1/ 
Update Delete Comment
PATCH PUT DELETE
{
    "text": "Krossovki zor ekan"
    
}



Search
GET
http://127.0.0.1:8000/products/search/?q=macbook



http://127.0.0.1:8000/products/comment-list/
GET
Comments list of user or all for admin



                   CART
CART VIew
GET
http://127.0.0.1:8000/cart/cart/


http://127.0.0.1:8000/cart/cart-add/
Cart add 
POST
{
    "product_id":2,
    "quantity":13
}

http://127.0.0.1:8000/cart/cart-update/
Cart update
PATCH 
{
    "product_id":2,
    "quantity":15
}


http://127.0.0.1:8000/cart/cart-remove/
Cart remove
DELETE
{
    "product_id":2,
}


http://127.0.0.1:8000/cart/cart-clear/
Clear Cart
DELETE


                          Orders
http://127.0.0.1:8000/orders/create/
Create Order
POST


http://127.0.0.1:8000/orders/list/
Order List
GET

http://127.0.0.1:8000/orders/detail/1/
Order Detail
GET


http://127.0.0.1:8000/orders/status/1/
Order status
PATCH

http://127.0.0.1:8000/orders/cancel/1/
Order cancel for client
DELETE




