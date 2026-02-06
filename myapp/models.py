from django.db import models

# Create your models here.
class Login(models.Model):
    Email=models.CharField(max_length=255)
    Password=models.CharField(max_length=255)
    Role=models.CharField(max_length=255)
    salt=models.CharField(max_length=222,default=1)



class Cusreg(models.Model):
    Login_id=models.ForeignKey(Login,on_delete=models.CASCADE, null=True, blank=True)
    Cus_Name=models.CharField(max_length=255)
    Profile_pic=models.FileField(upload_to='media/img',null=True)
    Cus_Email=models.CharField(max_length=255)
    Contact = models.CharField(max_length=15)
    Password=models.CharField(max_length=255)
    Address=models.CharField(max_length=255)
    post=models.CharField(max_length=255)
    pin=models.CharField(max_length=6)
    district=models.CharField(max_length=255)
    Gender=models.CharField(max_length=255)
    Status=models.CharField(max_length=1000)
    
    
   

class Busreg(models.Model):
    Login_id=models.ForeignKey(Login,on_delete=models.CASCADE,default=1)
    Business_Name=models.CharField(max_length=255)
    Owner_Name=models.CharField(max_length=255)
    Logo=models.FileField(upload_to='media/img',null=True)
    Bus_Email=models.CharField(max_length=255)
    Password=models.CharField(max_length=255)
    contact=models.CharField(max_length=15)
    Address=models.CharField(max_length=255)
    post=models.CharField(max_length=255)
    pin=models.CharField(max_length=6)
    district=models.CharField(max_length=255)
    Business_type=models.CharField(max_length=255)
    Registration_stat=models.CharField(max_length=255)
    Reg_doc=models.FileField(upload_to='uploads/')
   
    
    
class Products(models.Model):
    Busreg=models.ForeignKey(Busreg,on_delete=models.CASCADE,default=1)
    Prod_Name=models.CharField(max_length=255)
    Prod_cat=models.CharField(max_length=255)
    Prod_des=models.CharField(max_length=255)
    Prod_price=models.FloatField(max_length=10)
    Availability=models.CharField(max_length=255)
    Prod_image=models.FileField(upload_to='media/img',null=True)

class Feedback(models.Model):
    Cusreg=models.ForeignKey(Cusreg,on_delete=models.CASCADE)
    Busreg=models.ForeignKey(Busreg,on_delete=models.CASCADE)
    Rating=models.CharField(max_length=255)
    Message=models.CharField(max_length=255)
    Products=models.ForeignKey(Products,on_delete=models.CASCADE)
    Feedbacktime=models.DateField()

class Enquiry(models.Model):
    Busreg=models.ForeignKey(Busreg,on_delete=models.CASCADE)
    Cusreg=models.ForeignKey(Cusreg,on_delete=models.CASCADE)
    Products=models.ForeignKey(Products,on_delete=models.CASCADE)
    Queries=models.CharField(max_length=255)

class Services(models.Model):
    Busreg=models.ForeignKey(Busreg,on_delete=models.CASCADE,null=True, blank=True)
    Serv_cat=models.CharField(max_length=255,null=True, blank=True)
    Serv_desc=models.CharField(max_length=255, null=True, blank=True)
    



class Category(models.Model):
    Cat_name=models.CharField(max_length=255)


class Servicecat(models.Model):
    Serv_catname=models.CharField(max_length=255)


class Offers(models.Model):
    Products = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)  # Allow NULL values
    Offer_desc = models.CharField(max_length=255, null=True, blank=True)
    Discount = models.CharField(max_length=255, null=True, blank=True)
    Start_date = models.DateField(null=True)
    End_date = models.DateField(null=True)

     

class Contacts(models.Model):
   Busreg=models.ForeignKey(Busreg,on_delete=models.CASCADE) 
   Off_web=models.CharField(max_length=255)
   Linkedin=models.CharField(max_length=255)
   Social=models.CharField(max_length=255)


class Servfeedback(models.Model):
    Cusreg=models.ForeignKey(Cusreg,on_delete=models.CASCADE,default=33)
    Busreg=models.ForeignKey(Busreg,on_delete=models.CASCADE,default=45)
    Rating=models.CharField(max_length=255)
    Message=models.CharField(max_length=255)
    Services=models.ForeignKey(Services,on_delete=models.CASCADE,default=23)
    Feedbacktime=models.DateField()

class RoomImage(models.Model):
    image = models.ImageField(upload_to='rooms/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class SavedDesign(models.Model):
    Cusreg=models.ForeignKey(Cusreg,on_delete=models.CASCADE,default=1,null=True,blank=True)
    image = models.ImageField(upload_to='designs/')
    date=models.DateField()



   


