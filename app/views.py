from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
import hashlib              # for generating hash
from .models import Register,Landdetails,LandRequest,LandRegistration
from .forms import Land
import segno                # for generating qr code
import os
from reportlab.pdfgen import canvas


INDEX_PAGE = 'index.html'
LOGIN_PAGE = 'login.html'
REGISTER_PAGE = 'register.html'
SELLER_HOME_PAGE = 'sellerhome.html'
BUYER_HOME_PAGE = 'buyerhome.html'
VIEW_LAND_DETAILS = 'viewland.html'
REQUST_LAND_PAGE  = 'makerequest.html'
ADD_LAND_PAGE='addland.html'
VIEW_LAND_REQUSTS = 'viewrequest.html'
BUYER_LAND_REQUESTS = 'buyer_landrequests.html'
LAND_REGISTRATION = 'add_registration.html'
SELLER_LANDS = 'sellerlands.html'
BUYER_REGISTRATIONS = 'buyer_registrations.html'


def index(req):
    return render(req, INDEX_PAGE)


def login_user(req):
    if req.method == 'POST':
        username = req.POST['email']
        password = req.POST['password']
        utype = req.POST['utype']

        data = Register.objects.filter(email = username,password = password,usertype=utype).exists()
        
        if data:
            req.session['email']=username
            if utype=="Seller":
                return render(req,'sellerhome.html')
            else:
                return render(req,'buyerhome.html')
        else:
            messages.warning(req,"Details are not valid")
            return render(req,"login.html")

    return render(req, LOGIN_PAGE)


# method to register user
def register_user(req):
    if req.method == 'POST':
        username = req.POST['username']
        password = req.POST['password']
        pno = req.POST['pno']
        addr = req.POST['addr']
        utype = req.POST['utype']
        name = req.POST['name']
        c_password = req.POST['confirm_password']
        if password != c_password:
            messages.error(req, 'Password does not match',
                           extra_tags='alert alert-danger')
            return render(req, REGISTER_PAGE)
        if Register.objects.filter(email=username).exists():
            messages.error(req, 'Username already exists',
                           extra_tags='alert alert-danger')
            return render(req, REGISTER_PAGE)
        user = Register(name=name, email=username, password=password,confirm_password=c_password, usertype=utype,pno=pno,addr=addr)
        user.save()
        messages.success(req, 'User registered successfully',
                         extra_tags='alert alert-success')
        return render(req, LOGIN_PAGE)
    return render(req, REGISTER_PAGE)


def logout_user(req):
    req.session.flush()
    return redirect('index')


# method to add land details
def add_land(req):
    form = Land()
    if req.method == 'POST':
        dc=Register.objects.filter(email=req.session['email'])
        form = Land(req.POST, req.FILES)
        if form.is_valid():
            form.save(commit=False)
            hashed_id = hashlib.sha256(
                    str(form.instance.toJson()).encode()).hexdigest()
            qr = segno.make(f'{hashed_id}')
            path = os.path.join(os.getcwd(),'static',
                                    'images', f'{hashed_id}.png')
            qr.save(path, scale=10)
            form.instance.image = f'{hashed_id}.png'
            form.instance.owner_name=dc[0].name
            form.instance.owner_email=req.session['email']
            form.instance.owner_number=dc[0].pno
            form.save()
            messages.success(req, 'Land details added successfully',
                                extra_tags='alert alert-success')
            return redirect('addland')
      
    return render(req, ADD_LAND_PAGE, {"form": form})


def sellerhome(req):
    return redirect('sellerhome')

def view_land(req):
    return render(req, VIEW_LAND_DETAILS, {"land": Landdetails.objects.filter(land_area__gt=0)})


def request_land(req, id):
    if req.method == 'POST':
        total_amount = req.POST['total_amount']
        total_land = req.POST['total_land']
        buyer = Register.objects.get(email=req.session['email'])
        land = Landdetails.objects.get(id=id)
        LandRequest.objects.create(buyer=buyer, land=land, total_amount=total_amount, total_land=total_land)
        messages.success(req, 'Request sent successfully',extra_tags='alert alert-success')
        return redirect('viewland')
    else:
        land = Landdetails.objects.get(id=id)
        return render(req, REQUST_LAND_PAGE, {"land": land})

def view_land_requests(req):
    return render(req, VIEW_LAND_REQUSTS, {"lands": LandRequest.objects.filter(land__owner_email=req.session['email'],status='pending')})

def update_request(req,id):
    l_request = LandRequest.objects.get(id=id)
    land = Landdetails.objects.get(id=l_request.land.id)
    status = req.GET["status"]
    if status == "accept":
        if land.land_area >= l_request.total_land:
            land.land_area = land.land_area - l_request.total_land
            land.save()
            l_request.status = "accepted"
            l_request.save()
            return redirect('viewrequest')
        else:
            return redirect('viewrequest')
    else:
        l_request.status = "rejected"
        l_request.save()
        return redirect('viewrequest')
    

def buyer_landrequest(req):
    return render(req, BUYER_LAND_REQUESTS, {"lands": LandRequest.objects.filter(buyer__email=req.session['email'])})


def add_registration(req):
    land_requests = LandRequest.objects.filter(land__owner_email=req.session['email'] , status='accepted')
    return render(req, LAND_REGISTRATION, {'land_requests': land_requests})


def seller_lands(req):
    lands = Landdetails.objects.filter(owner_email=req.session['email'])
    return render(req, SELLER_LANDS, {'lands': lands})

def register_land(req,id):
    land_request = LandRequest.objects.get(id=id)
    owner = Register.objects.get(email=req.session['email'])
    

    registration = LandRegistration(land=land_request.land, buyer_name = land_request.buyer.name,
                                    buyer_email = land_request.buyer.email,
                                    buyer_number = land_request.buyer.pno,
                                    total_land = land_request.total_land,
                                    total_amount = land_request.total_amount,
                                    seller = owner)
    
    # save the pdf file

    registration.save()
    open(f"{os.getcwd()}/static/pdf/{registration.id}.pdf", "x")

    pdf = canvas.Canvas(f"{os.getcwd()}/static/pdf/{registration.id}.pdf")
    pdf.drawString(100, 800, f"Land Id: {registration.land.id}")
    pdf.drawString(100, 700, f"Land Location: {registration.land.address}")
    pdf.drawString(100, 650, f"Land Price: {registration.total_amount}")
    pdf.drawString(100, 600, f"Land Owner Name: {registration.seller.name}")
    pdf.drawString(100, 550, f"Land Owner Email: {registration.seller.email}")
    pdf.drawString(100, 500, f"Land Owner Number: {registration.seller.pno}")
    pdf.drawString(100, 450, f"Buyer Name: {registration.buyer_name}")
    pdf.drawString(100, 400, f"Buyer Email: {registration.buyer_email}")
    pdf.drawString(100, 350, f"Buyer Number: {registration.buyer_number}")
    pdf.drawString(100, 300, f"Total Land: {registration.total_land} sq.ft")
    pdf.drawString(100, 250, f"Total Amount: Rs {registration.total_amount} /-")
    pdf.drawString(100, 200, f"Regisered Date: {registration.date}")
    pdf.save()
    registration.pdf_name = f"{registration.id}.pdf"
    registration.save()
    land_request.status = "registered"
    land_request.save()
    return redirect('add_registration')

def delete_land(req,id):
    land = Landdetails.objects.get(id=id)
    land.delete()
    return redirect('seller_lands')


def buyer_registrations(req):
    registrations = LandRegistration.objects.filter(buyer_email=req.session['email'])
    return render(req, BUYER_REGISTRATIONS, {'registrations': registrations})