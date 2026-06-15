from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category, BrandReview
from django.contrib import messages


def home(request):
    featured = Product.objects.filter(is_featured=True, in_stock=True)[:6]
    categories = Category.objects.all()
    top_reviews = BrandReview.objects.filter(approved=True).order_by('-created_at')[:3]
    return render(request, 'shop/home.html', {
        'featured': featured,
        'categories': categories,
        'top_reviews': top_reviews,
    })


def shop(request):
    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=selected_category)
    return render(request, 'shop/shop.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category, in_stock=True).exclude(id=product.id)[:4]
    reviews = product.reviews.filter(approved=True).order_by('-created_at')

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment')
        if name and comment:
            from .models import Review
            Review.objects.create(
                product=product,
                name=name,
                location=location,
                rating=rating,
                comment=comment,
            )
            return redirect('product_detail', slug=slug)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related': related,
        'reviews': reviews,
    })


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        cart[key]['quantity'] += 1
    else:
        cart[key] = {
            'name': product.name,
            'price': str(product.price),
            'quantity': 1,
            'image': product.image.url if product.image else '',
        }
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.META.get('HTTP_REFERER', 'shop'))


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    if key in cart:
        del cart[key]
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    key = str(product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0 and key in cart:
        cart[key]['quantity'] = quantity
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'shop/cart.html', {'cart': cart, 'total': total})

    from .models import BrandReview

def reviews_page(request):
    reviews = BrandReview.objects.filter(approved=True).order_by('-created_at')
    submitted = False

    if request.method == 'POST':
        name = request.POST.get('name')
        location = request.POST.get('location')
        rating = int(request.POST.get('rating', 5))
        comment = request.POST.get('comment')
        if name and comment:
            BrandReview.objects.create(
                name=name,
                location=location,
                rating=rating,
                comment=comment,
            )
            submitted = True

    return render(request, 'shop/reviews.html', {
        'reviews': reviews,
        'submitted': submitted,
    })

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            from .models import Newsletter
            from django.db import IntegrityError
            try:
                Newsletter.objects.create(email=email)
                messages.success(request, '🎉 Thanks for subscribing!')
            except IntegrityError:
                messages.info(request, 'You are already subscribed!')
        else:
            messages.error(request, 'Please enter a valid email.')
    return redirect(request.META.get('HTTP_REFERER', 'home'))

    from django.http import HttpResponse

def setup_admin(request):
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'your@email.com', 'yourpassword123')
        return HttpResponse('Superuser created!')
    return HttpResponse('Admin already exists!')