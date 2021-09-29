from django.shortcuts import render, get_object_or_404,  redirect
from cart.forms import CartAddProductForm
from .models import Category, Product
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# from django.views import generic


# class IndexView(generic.ListView):
#     template_name = 'shop/index.html'
#     context_object_name = 'products'

#     def get_queryset(self):
#         '''Return five lattest products
#         '''
#         return Product.objects.filter(created__lte=timezone.now()
#         ).order_by('-created')[:5]



def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    context = {'category': category, 'categories': categories, 'products': products}
    return render(request, 'shop/product/list.html', context)


# class ProductListView(generic.ListView):
#     template_name = 'shop/product/list.html'

#     def get_queryset(self):
#         return Product.objects.filter(available=True)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         category = None
#         if category_slug:
#             category = get_object_or_404(Category, slug=category_slug)
#         context['category'] = category
#         context['categories'] = Category.objects.all()





def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'shop/product/detail.html', context)


# class ProductDetialView(generic.DetailView):

#     template_name = 'shop/product/detail.html'
#     model = Product
#     form_class = CartAddProductForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['products'] = get_object_or_404(Product, 
#         id=id, slug=slug, available=True)
#         return context



def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in.')
            return redirect('shop:product_list')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('shop:login')
    return render(request, 'shop/login.html')



def register(request):
    if request.method == 'POST':
        if request.method == 'POST':
            name = request.POST['name']
            username = request.POST['username']
            email = request.POST['email']

            password = request.POST['password']
            confirm_password = request.POST['confirm_password']

            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists!')
                    return redirect('shop:register')
                else:
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'Email already exists!')
                        return redirect('shop:register')
                    else:
                        user = User.objects.create_user( email=email,
                                                        username=username, password=password)
                        auth.login(request, user)
                        messages.success(request, 'You are now logged in.')
                        return redirect('shop:product_list')
                        user.save()
                        messages.success(request, 'Congrats, You are registered successfully.')
                        return redirect('shop:login')
            else:
                messages.error(request, 'Password do not match')
                return redirect('shop:register')


    else:
            return render(request, 'shop/register.html')
    #return render(request, 'shop/register.html')

