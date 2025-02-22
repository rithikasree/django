from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import Customer, Booking
import secrets

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

def submit(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password != confirmpassword:
            messages.error(request, "❌ Passwords do not match. Please try again!")
            return HttpResponse("Passwords do not match!")

        register = Customer(name=name, email=email, password=password)
        register.save()
        messages.success(request, "Registered Successfully! 🎉")
        return render(request, "register.html")

    return HttpResponse("Invalid request") 

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Admin Hardcoded Login
        if email == "rithikagowri6@gmail.com" and password == "Rithikaa@06":
            print("✅ Redirecting to Dashboard")
            response = redirect('booking_list')
            token = secrets.token_hex(16)  # Generate a random token
            response.set_cookie("auth_token", token, httponly=False, max_age=3600)  # Set token in cookies
            return response  

        # User Login
        user = Customer.objects.filter(email=email).first()

        if user:
            if user.password == password:  # (Use password hashing in production)
                print(f"✅ User found in database: {user.email}")
                response = redirect('menu')
                token = secrets.token_hex(16)
                response.set_cookie("auth_token", token, httponly=False, max_age=3600)
                return response
            else:
                messages.error(request, "❌ Invalid Password")
                return redirect('login')  # Redirect to login page instead of rendering

        else:
            messages.error(request, "❌ User doesn't exist")
            return redirect('login')  # Redirect to login page if user does not exist

    return render(request, 'login.html')


def menu(request):
    return render(request, "menu.html")

from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Booking  # Ensure you have a Booking model
from django.contrib import messages

def booking(request):
    if request.method == "POST":
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        date = request.POST.get('date')

        # Fetch service and price from GET request
        service = request.GET.get('service', 'Not Selected')
        price = request.GET.get('price', '0')

        if service == 'Not Selected' or price == '0':
            return HttpResponse("Error: Service or price missing!")

        # Save to database
        new_booking = Booking(name=name, address=address, phone=phone, service=service, price=price, date=date)
        new_booking.save()

        return redirect(f'/booking?success=true&name={name}&address={address}&phone={phone}&service={service}&price={price}&date={date}')

    service = request.GET.get('service', 'Not Selected')
    price = request.GET.get('price', '0')
    success = request.GET.get('success', False)
    
    return render(request, 'booking.html', {'service': service, 'price': price, 'success': success})

def booking_list(request):
    bookings = Booking.objects.all().order_by('-date')
    return render(request, 'booking_list.html', {'bookings': bookings})

def delete_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.delete()
    return redirect('booking_list')

def update_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        booking.name = request.POST.get("name")
        booking.address = request.POST.get("address")
        booking.phone = request.POST.get("phone")
        booking.date = request.POST.get("date")
        booking.service = request.POST.get("service")
        booking.price = request.POST.get("price")
        booking.save()
        return redirect("booking_list")

    return render(request, "update_booking.html", {"booking": booking})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Logs out the user
    request.session.flush()  # Clears session data

    response = redirect('login')  # Redirects to login page
    response.delete_cookie("auth_token")  # Deletes authentication cookie
    
    return response


def protected_page(request):
    if not request.COOKIES.get("auth_token"):
        return redirect('login')  # Redirect to login if token is missing
    return render(request, 'menu.html')
