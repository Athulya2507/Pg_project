from datetime import date
import json
from django.forms import FloatField
from django.shortcuts import  get_object_or_404, redirect, render
from django.http import HttpResponse, HttpResponseBadRequest
from .models import *
from django.core.mail import send_mail
import hashlib
import random
import string
# Create your views here.


def login(request):
    return render(request,'customer/newlogin_form.html')
def login_post(request):
    email = request.POST['log_email']
    password = request.POST['log_pass']

    print(email, password)

    # 1. Check user exists
    user = Login.objects.filter(Email=email).first()
    if not user:
        return HttpResponse(
            '''<script>alert('User Not Exists');window.location='/login/'</script>'''
        )

    salt = user.salt
    print("salt:", salt)

    # 2. Hash correctly (password + salt)
    hashed_pwd = hashlib.md5((password + salt).encode('utf-8')).hexdigest()
    print("hashed:", hashed_pwd)

    # 3. Match login
    lg = Login.objects.filter(Email=email, Password=hashed_pwd)

    if lg.exists():
        lgg = lg.first()
        request.session['lid'] = lgg.id

        if lgg.Role == 'Customer':
            return redirect('/homecus/')
        elif lgg.Role == 'business':
            return redirect('/homebus/')
        elif lgg.Role == 'admin':
            return redirect('/homeadmin/')
        else:
            return HttpResponse(
                '''<script>alert('Role not assigned');window.location='/login/'</script>'''
            )
    else:
        return HttpResponse(
            '''<script>alert('Email and Password not match');window.location='/login/'</script>'''
        )

def logout(request):
    request.session['lid'] == ''
    return HttpResponse('''<script>alert('Logout Sucessful');window.location='/roomify/'</script>''')


def cus_reg(request):
    return render(request,'customer/cust_reg_form.html')
def cusreg_post(request):
    cus_name=request.POST['cus_name'] #here we are storing the value fetch from the form to the corresponding table columns
    photo=request.FILES['photoupload']
    cus_email=request.POST['cus_email']
    cus_contact=request.POST['cus_contact']
    cus_pass=request.POST['cus_pass']
    salt = ''.join(random.choices(string.ascii_letters, k=7))
    cus_pass = hashlib.md5((cus_pass + salt).encode('utf-8')).hexdigest()

    cus_addr=request.POST['cus_addr']
    cus_gender=request.POST['gender']
    if Cusreg.objects.filter(Cus_Email=cus_email).exists():
        return HttpResponse('''<script>alert("An account with the provided email or phone number already exists.");window.location="/login/"</script>''')
    hgh=Login() #here storing the registration table value to the login table like password and the email.
    hgh.Email=cus_email
    hgh.Password=cus_pass
    hgh.Role='Customer'
    hgh.salt=salt
    hgh.save()
    var_cus= Cusreg() #here the cusreg table storing into var_cus variable.
    var_cus.Cus_Name=cus_name
    var_cus.Profile_pic=photo
    var_cus.Cus_Email=cus_email
    var_cus.Contact=cus_contact
    var_cus.Password=cus_pass
    var_cus.Address=cus_addr
    var_cus.Gender=cus_gender
    var_cus.Login_id=hgh #here the login table is added as foreign key thats why we are giving its id like this.
    var_cus.Status='Customer'
    var_cus.save()
    return redirect('/login/')

# def cusprofile_view(request):
#     profile=Cusreg.objects.get(Login_id=request.session['lid'])
#     return render(request,'customer/customer_profile.html',{'prof':profile}) 


def editprofile_cus(request):
    profile=Cusreg.objects.get(Login_id=request.session['lid'])
    return render(request,'customer/editprofile_form.html',{'prof':profile})

def editprofile_cus_post(request):
    id=request.POST['id']
    cus_name=request.POST['cus_name']
    photo=request.FILES['photoupload']
    cus_email=request.POST['cus_email']
    cus_contact=request.POST['cus_contact']
    cus_pass=request.POST['cus_pass']
    cus_addr=request.POST['cus_addr']
    cus_gender=request.POST['gender']

    vareditprof_cus=Cusreg.objects.get(id=id)
    vareditprof_cus.Cus_Name=cus_name
    vareditprof_cus.Profile_pic=photo
    vareditprof_cus.Cus_Email=cus_email
    vareditprof_cus.Contact=cus_contact
    vareditprof_cus.Password=cus_pass
    vareditprof_cus.Address=cus_addr
    vareditprof_cus.Gender=cus_gender
    vareditprof_cus.Login_id_id=request.session['lid']
    log=Login.objects.get(id=request.session['lid'])
    log.Email=cus_email
    log.Password=cus_pass
    log.save()
    vareditprof_cus.save()
    return HttpResponse('''<script>alert('Profile updated Sucessfully');window.location='/homecus/'</script>''')  

def cusprod_view(request):
    Prodvc_get=Products.objects.all()
    return render(request,'customer/productview.html',{'data': Prodvc_get})
def cusprod_view_post(request):
    Prodvc_post=Products.objects.all()
    return render(request,'customer/productview.html',{'data': Prodvc_post})

def cusserv_view(request):
    servvc_get=Services.objects.all()
    return render(request,'customer/Serviceview.html',{'data': servvc_get})

def sendmailserv(request,id):
    try:
      user = Services.objects.get(id=id)
    except Services.DoesNotExist:
     return HttpResponse("Service not found", status=404)

    customer=Cusreg.objects.get(Login_id=request.session['lid'])
    send_mail(
            'Service Enquiry Message',
            f' Customer:{customer.Cus_Name} has send an enquiry about service:{user.Serv_cat}.\ncontact information of customer are given below-\ncontact:{customer.Contact}\nAddress:{customer.Address}',
            'nayanadominic25@gmail.com',
            [user.Busreg.Bus_Email],
            fail_silently=False,
        )
    return HttpResponse('''<script>alert('Service enquiry email send succesfully'); window.location='/cusserv_view/'</script>''')

def cusserv_view_post(request):
    servvc_post=Services.objects.all()
    return render(request,'customer/Serviceview.html',{'data': servvc_post})

# def cusoffers_view(request):
#     offvc_get=Offers.objects.filter(Products__Busreg__Login_id=request.session['lid'])
#     return render(request,'customer/Offersview.html',{'data': offvc_get})
# def cusoffers_view_post(request):
#     offvc_post=Offers.objects.all()
#     return render(request,'customer/Offersview.html',{'data': offvc_post})

def cuscontact_view(request):
    convc_get=Contacts.objects.all()
    return render(request,'customer/Contactview.html',{'data': convc_get})
def cuscontact_view_post(request):
    convc_post=Contacts.objects.all()
    return render(request,'customer/Contactview.html',{'data': convc_post})

def ind_contact(request,id):
    business_selected=Busreg.objects.get(id=id)
    business_contact=Contacts.objects.filter(Busreg=business_selected)
    return render(request,'customer/ind_contact.html',{'business': business_selected,'contact':business_contact})

def cusbus_view(request):
    cusbus=Products.objects.all()
    return render(request,'customer/business_view.html',{'data': cusbus})
def cusbus_view_post(request):
    cusbus=Products.objects.all()
    return render(request,'customer/business_view.html',{'data': cusbus})


def feedback(request,id):

    return render(request,'customer/Feedback_form.html',{'id':id})
from django.http import HttpResponse
from datetime import datetime
from .models import Feedback, Products, Cusreg

def feedbackview_post(request):
    if request.method == 'POST':
        prod_id = request.POST['id']
        rating_feed = request.POST['rating']
        message_feed = request.POST['message']
        customer = Cusreg.objects.get(Login_id=request.session['lid'])

        # Check for existing feedback from the same customer for the same product
        already_given = Feedback.objects.filter(Cusreg=customer, Products_id=prod_id).exists()

        if already_given:
            return HttpResponse('''<script>alert('You cannot submit multiple feedback. Only the first feedback is considered.'); window.location='/products_page/'</script>''')

        # If not already submitted, save new feedback
        product = Products.objects.get(id=prod_id)

        var_feed = Feedback()
        var_feed.Products = product
        var_feed.Rating = rating_feed
        var_feed.Feedbacktime = datetime.now()
        var_feed.Message = message_feed
        var_feed.Busreg = product.Busreg
        var_feed.Cusreg = customer
        var_feed.save()

        return HttpResponse('''<script>alert('Feedback submitted successfully'); window.location='/products_page/'</script>''')


def enquiry(request,id):
    return render(request,'customer/Enquiry_form.html',{'id':id})
def enquiry_post(request):
    id=request.POST['id']
    queries=request.POST['queries']
    if Cusreg.objects.filter(Cus_Email=Cusreg.cus_email).exists():
        return HttpResponse('''<script>alert("An account with the provided email or phone number already exists.");window.location="/login/"</script>''')
    var_enq=Enquiry()
    var_enq.Cusreg=Cusreg.objects.get(Login_id=request.session['lid'])
    var_enq.Busreg_id=Products.objects.get(id=id).Busreg.id
    var_enq.Queries=queries
    var_enq.save()
    # Enq_post=Enquiry.objects.all()
    return HttpResponse('''<script>alert('Product Enquiry submited succesfully'); window.location='/cusprod_view/'</script>''')




def servenq(request,id):

    return render(request)
def servenq_post(request):
    return HttpResponse('''<script>alert('Service needed notification sent successfully'); window.location='/cusserv_view/'</script>''')

def servfeedback(request,id):
    ss=Services.objects.get(id=id)
    return render(request,'customer/servfeedback_form.html',{'ss':ss})
def servfeedback_post(request):
    if request.method == 'POST':
      
       id=request.POST['id']
       rating_feed=request.POST['rating']
       message_feed=request.POST['message']
       customer=Cusreg.objects.get(Login_id_id=request.session['lid'])
       serv_name=Services.objects.get(id=id)
       already_given=Servfeedback.objects.filter(Cusreg=customer,Services_id=serv_name).exists()
       if already_given:
            return HttpResponse('''<script>alert('You cannot submit multiple feedback. Only the first feedback is considered.'); window.location='/cusserv_view/'</script>''')
     # If not already submitted, save new feedback
       service = Services.objects.get(id=id)

           
    var_servfeed=Servfeedback()
    var_servfeed.Services=service
    var_servfeed.Services_id=Services.objects.get(id=id).id
    var_servfeed.Rating=rating_feed
    from datetime import datetime 
    var_servfeed.Feedbacktime=datetime.now()
    var_servfeed.Message=message_feed

    var_servfeed.Busreg_id=Services.objects.get(id=id).Busreg.id
    var_servfeed.Cusreg_id=Cusreg.objects.get(Login_id_id=request.session['lid']).id
    # var_feed.Products=Products.objects.get(Login_id_id=request.session['lid']).id
    var_servfeed.save()
    return HttpResponse('''<script>alert('Service Feedback submited succesfully'); window.location='/cusserv_view/'</script>''')

from django.db.models.functions import Cast
from django.db.models import Avg, FloatField

def roomify(request):
    products = Products.objects.all()
    # offers = Offers.objects.all()

    today = date.today()

    for product in products:
        # Get only active offer (if any)
        offer = Offers.objects.filter(
            Products=product,
            Start_date__lte=today,
            End_date__gte=today
        ).first()

        if offer and offer.Discount:
           discount_str = offer.Discount.strip().replace('%', '')  # remove the '%' sign
           discount = float(discount_str)  # now it's safe to convert
           discounted_price = product.Prod_price - (product.Prod_price * discount / 100)
           product.discounted_price = round(discounted_price, 2)
           product.has_offer = True
           product.offer_desc = offer.Offer_desc
           product.discount_percentage = discount
        else:
            product.discounted_price = product.Prod_price
            product.has_offer = False
            product.offer_desc = None
            product.discount_percentage = None

        # Calculate average rating
        avg_rating = Feedback.objects.filter(Products=product).aggregate(
            avg_rating=Avg(Cast('Rating', FloatField()))
        )['avg_rating'] or 0

        product.avg_rating = round(avg_rating, 1)
    return render(request, 'customer/Home.html', {'products': products, 'offers': offers})

def homecus(request):
    return render(request,'customer/NewcusHome.html')
def homecus_post(request):
    return HttpResponse("ok")

from django.shortcuts import render
from datetime import date
from django.db.models.functions import Cast
from django.db.models import Avg, FloatField
from .models import Products, Offers, Feedback

def products_page(request):
    products = Products.objects.all()
    today = date.today()

    for product in products:
        # Get only active offer (if any)
        offer = Offers.objects.filter(
            Products=product,
            Start_date__lte=today,
            End_date__gte=today
        ).first()

        if offer and offer.Discount:
            discount_str = offer.Discount.strip().replace('%', '')  # Remove % if present
            discount = float(discount_str)
            discounted_price = product.Prod_price - (product.Prod_price * discount / 100)
            product.discounted_price = round(discounted_price, 2)
            product.has_offer = True
            product.offer_desc = offer.Offer_desc
            product.discount_percentage = discount
        else:
            product.discounted_price = product.Prod_price
            product.has_offer = False
            product.offer_desc = None
            product.discount_percentage = None

        # Calculate average rating
        avg_rating = Feedback.objects.filter(Products=product).aggregate(
            avg_rating=Avg(Cast('Rating', FloatField()))
        )['avg_rating'] or 0

        product.avg_rating = round(avg_rating, 1)

    return render(request, 'customer/product_page.html', {'products': products})

# def cusoffers_view(request):
#     offvc_get=Offers.objects.filter(Products__Busreg__Login_id=request.session['lid'])
#     return render(request,'customer/Offersview.html',{'data': offvc_get})
def service_page(request):
    service_table = Services.objects.all()
    return render(request,'customer/Service_page.html', {'service' : service_table})

def ind_prod(request,id):
    product_selected = Products.objects.get(id=id)
    individual_prod=Products.objects.filter(id=id)
    return render(request,'customer/individualproduct.html', {'selected_product' : product_selected, 'ind_prod':individual_prod})
def sendmail(request,id):
    user = Products.objects.get(id=id)
    customer=Cusreg.objects.get(Login_id=request.session['lid'])
    send_mail(
            'Product Enquiry Message',
            f' Customer:{customer.Cus_Name} has shows an intrest to know more about the product:{user.Prod_Name}.\ncustomer contacting informations are given below-\ncontact:{customer.Contact}\nAddress:{customer.Address}',
            'nayanadominic25@gmail.com',
            [user.Busreg.Bus_Email],
            fail_silently=False,
        )
    return HttpResponse('''<script>alert('Product enquiry email send succesfully'); window.location='/products_page/'</script>''')

def business_logos(request):
    bus_names_table = Busreg.objects.all()
    return render(request,'customer/business_logos.html', {'bus_names': bus_names_table})

from datetime import date
from django.db.models import Avg, FloatField
from django.db.models.functions import Cast
from .models import Busreg, Products, Offers, Feedback

def business_products(request, id):
    business_selected = Busreg.objects.get(id=id)
    bus_products_table = Products.objects.filter(Busreg=business_selected)
    today = date.today()

    for product in bus_products_table:
        # Get only active offer (if any)
        offer = Offers.objects.filter(
            Products=product,
            Start_date__lte=today,
            End_date__gte=today
        ).first()

        if offer and offer.Discount:
           discount_str = offer.Discount.strip().replace('%', '')  # remove the '%' sign
           discount = float(discount_str)  # now it's safe to convert
           discounted_price = product.Prod_price - (product.Prod_price * discount / 100)
           product.discounted_price = round(discounted_price, 2)
           product.has_offer = True
           product.offer_desc = offer.Offer_desc
           product.discount_percentage = discount
        else:
            product.discounted_price = product.Prod_price
            product.has_offer = False
            product.offer_desc = None
            product.discount_percentage = None

        # Calculate average rating
        avg_rating = Feedback.objects.filter(Products=product).aggregate(
            avg_rating=Avg(Cast('Rating', FloatField()))
        )['avg_rating'] or 0

        product.avg_rating = round(avg_rating, 1)

    return render(request, 'customer/business_products.html', {
        'bus_products': bus_products_table,
        'business': business_selected
        
    })

def bus_reg(request):
    return render(request,'business/Business_reg_form.html')
def busreg_post(request):
    bus_name=request.POST['bus_name']
    own_name=request.POST['own_name']
    logo=request.FILES['logoupload']
    bus_email=request.POST['official_email']
    bus_contact=request.POST['official_contact']
    bus_pass=request.POST['bus_pass']
    salt = ''.join(random.choices(string.ascii_letters, k=7))
    bus_pass = hashlib.md5((bus_pass + salt).encode('utf-8')).hexdigest()

    bus_addr=request.POST['bus_addr']
    bus_type=request.POST['bus_type']
    reg_stat=request.POST['reg_stat']
    reg_det=request.FILES['regdet_upload']
    if Busreg.objects.filter(Bus_Email=bus_email).exists():
        return HttpResponse('''<script>alert("An account with the provided email or phone number already exists.");window.location="/login/"</script>''')
    ghi=Login()
    ghi.Email=bus_email
    ghi.Password=bus_pass
    ghi.Role='pending'
    ghi.salt=salt
    ghi.save()
    var_bus=Busreg()
    var_bus.Business_Name=bus_name
    var_bus.Owner_Name=own_name
    var_bus.Logo=logo
    var_bus.Bus_Email= bus_email
    var_bus.Password=bus_pass
    var_bus.contact=bus_contact
    var_bus.Address= bus_addr
    var_bus.Business_type=bus_type
    var_bus.Registration_stat= reg_stat
    var_bus.Reg_doc=reg_det
    var_bus.Login_id=ghi
    var_bus.Status='pending'
    var_bus.save()
    return redirect('/login/')

def editprofile_bus(request):
    id=Busreg.objects.get(Login_id=request.session['lid'])
    return render(request,'business/editprofile_bus.html',{'prof':id})
def editprofile_bus_post(request):
    id=request.POST['id']
    bus_name=request.POST['bus_name']
    own_name=request.POST['own_name']
    logo=request.FILES['logoupload']
    bus_email=request.POST['official_email']
    bus_contact=request.POST['official_contact']
    bus_pass=request.POST['bus_pass']
    bus_addr=request.POST['bus_addr']
    bus_type=request.POST['bus_type']
    reg_stat=request.POST['reg_stat']
    reg_det=request.FILES['regdet_upload']
    var_editprofile=Busreg.objects.get(id=id)
    var_editprofile.Business_Name=bus_name
    var_editprofile.Owner_Name=own_name
    var_editprofile.Logo=logo
    var_editprofile.Bus_Email=bus_email
    var_editprofile.Password=bus_pass
    var_editprofile.contact=bus_contact
    var_editprofile.Address= bus_addr
    var_editprofile.Business_type=bus_type
    var_editprofile.Registration_stat=reg_stat
    var_editprofile.Reg_doc=reg_det
    var_editprofile.Login_id_id=request.session['lid']
    log=Login.objects.get(id=request.session['lid'])
    log.Email=bus_email
    log.Password=bus_pass
    log.save()
    var_editprofile.save()
    return HttpResponse('''<script>alert('Profile updated succesfully'); window.location='/editprofile_bus/'</script>''')

# def viewprofile_bus(request):
#     return render(request,'business/bus_profile.html')
# def viewprofile_bus_post(request):
#     return HttpResponse("ok")










def products(request):
    return render(request,'business/Product_form.html')

def products_post(request):
    prod_name=request.POST['prod_name']
    prod_cat=request.POST['prod_cat']
    prod_price=request.POST['prod_price']
    prodavb_stat=request.POST['avb_stat']
    prod_des=request.POST['prod_des']
    prod_img=request.FILES['prod_img']
    var_prod=Products()
    var_prod. Prod_Name=prod_name
    var_prod. Busreg_id=Busreg.objects.get(Login_id=request.session['lid']).id
    var_prod.Prod_cat=prod_cat
    var_prod.Prod_price= prod_price
    var_prod.Availability= prodavb_stat
    var_prod.Prod_image=prod_img
    var_prod.Prod_des=prod_des
    var_prod.save()
    return HttpResponse('''<script>alert('product added succesfully'); window.location='/products/'</script>''')

from datetime import date
from django.shortcuts import render
from .models import Products, Offers

def prodview_bus(request):
    today = date.today()
    
    # Get products belonging to the logged-in business
    sel_bus = Products.objects.filter(Busreg__Login_id=request.session['lid'])

    # Get only active offers (not expired)
    active_offers = Offers.objects.filter(
        Start_date__lte=today,
        End_date__gte=today
    )

    return render(request, 'business/product.html', {'data': sel_bus, 'offers': active_offers})



# def prodview_bus_post(request):
#     Prodvb_post=Products.objects.all()
#     return render(request,'business/product.html',{'data':Prodvb_post})

def editprod(request,id):#this is the third step of edit.where we getting the values which we are passed in the form.
    aa= Products.objects.get(id=id)#this line is used to fetch a specific product from the database based on its id.Understanding id=id .The first id refers to the field name in the Products model.The second id is the parameter received by the function (editprod(request, id)).here we check both id are equal.
    return render(request,'business/editproduct_form.html',{'edit_prod':aa})#return render is used to load the page.




def editprod_post(request):

    # id=request.POST['id']
    prod_name=request.POST['prod_name']
    prod_cat=request.POST['prod_cat']
    prod_price=request.POST['prod_price']
    prodavb_stat=request.POST['avb_stat']
    prod_des=request.POST['prod_des']
    prod_img=request.FILES['prod_img']
    var_editprod=Products.objects.get(id=id)#this is the final step of edit.here we are storing the id of the particular product to this variable
    var_editprod.Prod_Name=prod_name
    var_editprod.Busreg_id=Busreg.objects.get(Login_id=request.session['lid']).id
    var_editprod.Prod_cat=prod_cat
    var_editprod.Prod_price= prod_price
    var_editprod.Availability= prodavb_stat
    var_editprod.Prod_image=prod_img
    var_editprod.Prod_des=prod_des
    var_editprod.save()
    return HttpResponse('''<script>alert('product edited succesfully'); window.location='/products/'</script>''')#to show the alerts message





# def editprod_post(request):

#     id=request.POST['id']
#     prod_name=request.POST['prod_name']
#     prod_cat=request.POST['prod_cat']
#     prod_price=request.POST['prod_price']
#     prodavb_stat=request.POST['avb_stat']
#     prod_des=request.POST['prod_des']
#     prod_img=request.POST['prod_img']
    
#     t = Products.objects.get(id=id)








def editprodview_bus(request):
    editprodvb_get=Products.objects.all()
    return render(request,'business/editproductview.html',{'data':editprodvb_get})
def editprodviewbus_post(request):
    id=request.POST['id']
    prod_name=request.POST['prod_name']
    prod_cat=request.POST['prod_cat']
    prod_price=request.POST['prod_price']
    prodavb_stat=request.POST['avb_stat']
    prod_des=request.POST['prod_des']
    prod_img=request.FILES['prod_img']
    var_editprod=Products.objects.get(id=id)
    var_editprod.Prod_Name=prod_name
    var_editprod.Busreg_id=Busreg.objects.get(Login_id=request.session['lid']).id
    var_editprod.Prod_cat=prod_cat
    var_editprod.Prod_price= prod_price
    var_editprod.Availability= prodavb_stat
    var_editprod.Prod_image=prod_img
    var_editprod.Prod_des=prod_des
    var_editprod.save()
    return HttpResponse('''<script>alert('product edited succesfully'); window.location='/prodview_bus/'</script>''')


    # return HttpResponse("ok")

def addprod(request):
    return render(request,'business/Product_form.html')
def addprod_post(request):
    prod_name=request.POST['prod_name']
    prod_cat=request.POST['prod_cat']
    prod_price=request.POST['prod_price']
    prodavb_stat=request.POST['avb_stat']
    prod_des=request.POST['prod_des']
    prod_img=request.FILES['prod_img']
    var_addprod=Products()
    var_addprod. Prod_Name=prod_name
    var_addprod.Busreg_id=Busreg.objects.get(Login_id=request.session['lid']).id
    var_addprod.Prod_cat=prod_cat
    var_addprod.Prod_price= prod_price
    var_addprod.Availability= prodavb_stat
    var_addprod.Prod_image=prod_img
    var_addprod.Prod_des=prod_des
    var_addprod.save()
    return HttpResponse('''<script>alert('product added succesfully'); window.location='/addprod/'</script>''')



def deleteproduct(request,id):
    product = Products.objects.get(id=id)
    product.delete()
    return HttpResponse('''<script>alert('product deleted succesfully'); window.location='/prodview_bus/'</script>''')





def offers(request):
    off_get=Offers.objects.filter(Products__Busreg__Login_id=request.session['lid'])
    return render(request,'business/Offers.html',{'data':off_get})
# def offers_post(request):
#     off_get=Offers.objects.all()
#     return render(request,'business/Offers.html',{'data':off_get})

def addoffers(request,id):
    dd=Products.objects.get(id=id)
    print(dd.id)
    return render(request,'business/Addoffers_form.html',{'id':id})
def addoffers_post(request):
    id=request.POST['id']
    print(id)
    dis_per=request.POST['discount']
    s_date=request.POST['s_date']
    e_date=request.POST['e_date']
    offer_desc=request.POST['offer_desc']
    var_addoffer=Offers()
    # var_addoffer.Prod_name=prod_name
    var_addoffer.Products=Products.objects.get(id=id)
    var_addoffer.Discount=dis_per
    var_addoffer.Start_date= s_date
    var_addoffer.End_date= e_date
    var_addoffer.Offer_desc=offer_desc
    var_addoffer.save()
    return HttpResponse('''<script>alert('offers added succesfully'); window.location='/prodview_bus/'</script>''')


from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Offers  # Assuming Offers model is in the same app

def editoffers(request, id):
    off = get_object_or_404(Offers, id=id)
    return render(request, 'business/Editoffers_form.html', {'edit_offer': off})

def editoffers_post(request):
    if request.method == "POST":
        id = request.POST.get('id')
        dis_per = request.POST.get('discount')
        s_date = request.POST.get('s_date')
        e_date = request.POST.get('e_date')
        offer_desc = request.POST.get('offer_desc')

        try:
            var_editoffer = Offers.objects.get(id=id)
            var_editoffer.Discount = dis_per
            var_editoffer.Start_date = s_date
            var_editoffer.End_date = e_date
            var_editoffer.Offer_desc = offer_desc
            var_editoffer.save()
            return HttpResponse(
                '''<script>alert('Offer updated successfully'); window.location='/prodview_bus/'</script>'''
            )
        except Offers.DoesNotExist:
            return HttpResponse("Offer not found", status=404)
    else:
        return HttpResponse("Invalid request method", status=405)



def editoffersview(request):
    off_get=Offers.objects.all()
    return render(request,'business/Editoffersview.html',{'data':off_get})
# def editoffersview_post(request):
#     off_get=Offers.objects.all()
#     return HttpResponse('''<script>alert('offers updated succesfully'); window.location='/editoffers/'</script>''')




def deloffers(request,id):
    deloffer= Offers.objects.get(id=id)
    deloffer.delete()
    return HttpResponse('''<script>alert('offers deleted succesfully'); window.location='/prodview_bus/'</script>''')



def service(request):
    serv_get=Services.objects.filter(Busreg__Login_id=request.session['lid'])
    return render(request,'business/Service.html',{'data':serv_get})
# def service_post(request):
#     serv_post=Services.objects.all()
#     return render(request,'business/Service.html',{'data':serv_post})

def addservice(request):
    return render(request,'business/Addservice_form.html')
def addservice_post(request):
    serv_cat=request.POST['serv_cat']
    serv_desc=request.POST['serv_desc']
    var_addserv=Services()
    var_addserv. Busreg_id=Busreg.objects.get(Login_id=request.session['lid']).id
    var_addserv.Serv_cat=serv_cat
    var_addserv.Serv_desc= serv_desc
    var_addserv.save()
    return HttpResponse('''<script>alert('Service added succesfully'); window.location='/addservice/'</script>''')

 
def editservice(request,id):
    service=Services.objects.get(id=id)
    return render(request,'business/Editservice_form.html',{'edit_serv': service})
def editservice_post(request):
    id=request.POST['id']
    serv_cat=request.POST['serv_cat']
    serv_charge=request.POST['serv_charge']
    var_editserv=Services.objects.get(id=id)
    var_editserv.Busreg_id=Busreg.objects.get(Login_id=request.session['lid']).id
    var_editserv.Serv_cat=serv_cat
    var_editserv.Serv_charge= serv_charge
    var_editserv.save()
    return HttpResponse('''<script>alert('Services updated succesfully'); window.location='/homebus/'</script>''')

def delserv(request,id):
    delserv=Services.objects.get(id=id)
    delserv.delete()
    return HttpResponse('''<script>alert('Services deleted succesfully'); window.location='/homebus/'</script>''')




def contact(request):
    con_get=Contacts.objects.filter(Busreg__Login_id=request.session['lid'])
    return render(request,'business/Contact.html',{'data': con_get})
# def contact_post(request):
#     con_post=Contacts.objects.all()
#     return render(request,'business/Contact.html',{'data': con_post})

def addcontact(request):
    return render(request,'business/Addcontact_form.html')
def addcontact_post(request):
    off_web=request.POST['off_web']
    linkedin=request.POST['linkedin']
    social=request.POST['social']
    var_addcontact=Contacts()
    var_addcontact.Busreg_id=Busreg.objects.get(Login_id=request.session['lid']).id
    var_addcontact.Off_web=off_web
    var_addcontact.Linkedin= linkedin
    var_addcontact.Social=social
    var_addcontact.save()
    return HttpResponse('''<script>alert('Contact added succesfully'); window.location='/addcontact/'</script>''')

def editcontact(request,id):
     contact=Contacts.objects.get(id=id)
     return render(request,'business/Editcontact_form.html',{'edit_con':contact})
def editcontact_post(request):
    id=request.POST['id']
    off_web=request.POST['off_web']
    linkedin=request.POST['linkedin']
    social=request.POST['social']
    var_addcontact=Contacts.objects.get(id=id)
    var_addcontact.Busreg_id=Busreg.objects.get(Login_id=request.session['lid']).id
    var_addcontact.Off_web=off_web
    var_addcontact.Linkedin= linkedin
    var_addcontact.Social=social
    var_addcontact.save()
    return HttpResponse('''<script>alert('Contact updated succesfully'); window.location='/contact/'</script>''')

def delcontact(request,id):
    delcon=Contacts.objects.get(id=id)
    delcon.delete()
    return HttpResponse('''<script>alert('Contact deleted succesfully'); window.location='/homebus/'</script>''')



def viewfeed_bus(request):
    feedbus_get=Feedback.objects.filter(Busreg__Login_id=request.session['lid'])
    return render(request,'business/Feedbackview.html',{'data':feedbus_get})
# def viewfeed_bus_post(request):
#     feedbus_post=Feedback.objects.all()
#     return render(request,'business/Feedbackview.html',{'data':feedbus_post})

def viewservfeed_bus(request):
    servfeedbus_get=Servfeedback.objects.filter(Busreg__Login_id=request.session['lid'])
    return render(request,'business/Servfeedview.html',{'data':servfeedbus_get})
# def viewenq_bus_post(request):
#     enqbus_post=Enquiry.objects.all()
#     return render(request,'business/Enquiry.html',{'data':enqbus_post})

def homebus(request):
    return render(request,'business/NewbusHome.html')
def homebus_post(request):
    return HttpResponse("ok")

def log_out(request):
    request.session['lid'] == ''
    return HttpResponse('''<script>alert('Logout Sucessful');window.location='/login/'</script>''')



def bustab_admin(request):
    busadmin_get=Busreg.objects.all()
    return render(request,'admin/business_admin.html',{'data':'busadmin_get'})
def bustab_admin_post(request):
    busadmin_post=Busreg.objects.all()
    return render(request,'admin/business_admin.html',{'data':'busadmin_get'})

def custab_admin(request):
    cusadmin_get=Cusreg.objects.all()
    return render(request,'admin/customer_admin.html',{'data':'cusadmin_get'})
def custab_admin_post(request):
    cusadmin_post=Cusreg.objects.all()
    return render(request,'admin/customer_admin.html',{'data':'cusadmin_get'})

def viewfeed_admin(request):
    feedadmin_get=Cusreg.objects.all()
    return render(request,'admin/feedback.html',{'data': feedadmin_get})
def viewfeed_admin_post(request):
    feedadmin_post=Cusreg.objects.all()
    return render(request,'admin/feedback.html',{'data': feedadmin_post})

def viewenq_admin(request):
    enqadmin_get=Enquiry.objects.all()
    return render(request,'admin/Enquiry.html',{'data':'enqadmin_get'})
def viewenq_admin_post(request):
    enqadmin_post=Enquiry.objects.all()
    return render(request,'admin/Enquiry.html',{'data':'enqadmin_get'})

def homeadmin(request):
    return render(request,'admin/home page.html')
def homeadmin_post(request):
    return HttpResponse("ok")













#Room Visualisation


# product_overlay/views.py
from django.shortcuts import redirect, render
from .models import RoomImage, Products, SavedDesign

def upload(request):
        rooms = RoomImage.objects.all()
        products = Products.objects.all()
        return render(request, 'Visualisation/fileupload.html', {'rooms': rooms, 'products': products})

def upload_images(request):
    if request.method == "POST":
        # product = request.FILES.get('product')
        # name = request.POST.get('name')
        
        # Check if room image is provided
        room = request.FILES.get('room')
        if room:
            room_form = RoomImage()
            room_form.image = room
            room_form.save()

        # Ensure product image and name are provided
       
        return redirect('/design/')
    else:
        return HttpResponseBadRequest("Invalid request method.")
import os
from django.http import JsonResponse
from django.core.files.base import ContentFile
from django.utils.timezone import now
import base64, json
from .models import SavedDesign
from .models import Cusreg  # Make sure it's imported

def save_design(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_data = data.get('image', '')

            if not image_data.startswith('data:image/'):
                return JsonResponse({'status': 'error', 'message': 'Invalid image data'})

            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            file_name = f'room_design_{now().strftime("%Y%m%d%H%M%S")}.{ext}'

            image_content = ContentFile(base64.b64decode(imgstr), name=file_name)

            # 🧠 Get customer using session-stored Login_id
            login_id = request.session.get('lid')  # 🛑 Ensure 'lid' is set on login

            if not login_id:
                return JsonResponse({'status': 'error', 'message': 'User not logged in'})

            # 🧠 If Cusreg has ForeignKey to Login model
            customer = Cusreg.objects.get(Login_id=login_id)

            design = SavedDesign.objects.create(
                Cusreg=customer,
                image=image_content,
                date=now().date()
            )

            return JsonResponse({'status': 'success', 'path': design.image.url})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
# import base64
# import os

# def save_design(request):
#     if request.method == 'POST':
#         import json
#         data = json.loads(request.body)
#         image_data = data.get('image', '')
#         format, imgstr = image_data.split(';base64,')
#         ext = format.split('/')[-1]

#         file_path = os.path.join('media', 'designs', f'room_design.{ext}')
#         with open(file_path, 'wb') as f:
#             f.write(base64.b64decode(imgstr))
#             product_form = SavedDesign()
#             product_form.image = file_path
#             from datetime import datetime
#             product_form.date = datetime.now()
#             product_form.save()
#         return JsonResponse({'status': 'success', 'path': file_path})
#     return JsonResponse({'status': 'error'})

def design(request):
    login_id = request.session.get('lid')  # 🛑 again, make sure it's set
    if not login_id:
        return redirect('/login/')  # or handle accordingly

    # 🧠 Fetch the correct customer
    customer = Cusreg.objects.get(Login_id=login_id)

    # 🔥 Filter only this user's designs
    droom = SavedDesign.objects.filter(Cusreg=customer)

    rooms = RoomImage.objects.all()
    products = Products.objects.all()

    return render(request, 'Visualisation/overlay.html', {
        'rooms': rooms,
        'products': products,
        'droom': droom
    })

