from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password,check_password
from Store.models.product import Product
from Store.models.category import Category
from Store.models.customer import Customer
from django.views import View


# Create your views here.
class Index(View):

    def post(selfself,request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart :
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1
            else:
                cart[product] = 1

        else:
            cart = {}
            cart[product] = 1
        request.session['cart']=cart
        print('cart ',request.session['cart'])
        return redirect('homepage')

    def get(self,request ):
        products = None
        cart = request.session.get('cart')
        if not cart:
            request.session['cart']={}

        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_product_by_categoryid(categoryID)
        else:
            products = Product.get_all_products();
        data = {}
        data['products'] = products
        data['categories'] = categories
        print('You are : ', request.session.get('email'))
        return render(request, 'index.html', data)

