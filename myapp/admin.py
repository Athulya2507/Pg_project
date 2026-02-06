from collections import defaultdict
from django.contrib import admin

from .views import login
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils.html import format_html
from django.urls import path, reverse
from .models import Busreg, Login  # Import your models
from .models import Cusreg, Login  # Import your models
from django.core.mail import send_mail

class LoginAdmin(admin.ModelAdmin):
    list_display=["Email","Password","Role"]
    # readonly_fields=["Password"]
    search_fields=["Email","Password","Role"]
    Login._meta.verbose_name = "Login Details"
    Login._meta.verbose_name_plural = "Login Details"
admin.site.register(Login,LoginAdmin)



from django.contrib import admin
from django.utils.html import format_html
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from .models import Cusreg, Login

class CusregAdmin(admin.ModelAdmin):
    list_display = ["Login_id","Cus_Name", "show_profile_pic", "Cus_Email", "Contact", "Address", "district","Password", "Gender", "Status", "action_buttons"]
    readonly_fields = ["Password"]
    search_fields = ["Login_id","Cus_Name","show_profile_pic", "Cus_Email", "Contact", "Address", "district","Password", "Gender", "Status"]
    actions = ["block_customer", "unblock_customer"]

    def show_profile_pic(self, obj):
        """Display profile picture in admin panel."""
        if obj.Profile_pic:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />'.format(obj.Profile_pic.url))
        return "No Image"
    show_profile_pic.short_description = "Profile Picture"

    def action_buttons(self, obj):
        """Add Block/Unblock buttons to admin panel."""
        return format_html(
            '<a href="block/{}/" class="button" style="background-color:red; color:white; padding:5px; border-radius:5px; text-decoration:none;">Block</a> &nbsp;'
            '<a href="unblock/{}/" class="button" style="background-color:green; color:white; padding:5px; border-radius:5px; text-decoration:none;">Unblock</a>',
            obj.id, obj.id
        )
    action_buttons.short_description = "Actions"

    def get_urls(self):
        """Define custom admin URLs for block/unblock actions."""
        urls = super().get_urls()
        custom_urls = [
            path("block/<int:cusreg_id>/", self.admin_site.admin_view(self.block_customer_view), name="block_customer"),
            path("unblock/<int:cusreg_id>/", self.admin_site.admin_view(self.unblock_customer_view), name="unblock_customer"),
        ]
        return custom_urls + urls

    def block_customer_view(self, request, cusreg_id):
        """Block a customer and update their role in the Login table."""
        customer = Cusreg.objects.get(id=cusreg_id)
        customer.Status = "Blocked"
        customer.save()
        if customer.Login_id:
            customer.Login_id.Role = "Blocked"
            customer.Login_id.save()
        messages.success(request, f"Customer {customer.Cus_Name} has been blocked.")
        return redirect(request.META.get('HTTP_REFERER', '/admin/app_name/cusreg/'))

    def unblock_customer_view(self, request, cusreg_id):
        """Unblock a customer and update their role in the Login table."""
        customer = Cusreg.objects.get(id=cusreg_id)
        customer.Status = "Active"
        customer.save()
        if customer.Login_id:
            customer.Login_id.Role = "Customer"
            customer.Login_id.save()
        messages.success(request, f"Customer {customer.Cus_Name} has been unblocked.")
        return redirect(request.META.get('HTTP_REFERER', '/admin/app_name/cusreg/'))

    def block_customer(self, request, queryset):
        """Block selected customers via bulk admin action."""
        for customer in queryset:
            customer.Status = "Blocked"
            customer.save()
            if customer.Login_id:
                customer.Login_id.Role = "Blocked"
                customer.Login_id.save()
        messages.success(request, '''<script>alert("Selected customers have been blocked.");window.location='/login/'</script>''')
    block_customer.short_description = "Block selected customers"

    def unblock_customer(self, request, queryset):
        """Unblock selected customers via bulk admin action."""
        for customer in queryset:
            customer.Status = "Active"
            customer.save()
            if customer.Login_id:
                customer.Login_id.Role = "Customer"
                customer.Login_id.save()
        messages.success(request, "Selected customers have been unblocked.")
    unblock_customer.short_description = "Unblock selected customers"

    Cusreg._meta.verbose_name = "Customer Details"
    Cusreg._meta.verbose_name_plural = "Customer Details"

admin.site.register(Cusreg, CusregAdmin)






class BusregAdmin(admin.ModelAdmin):
    list_display = ["Business_Name","Owner_Name","Logo","Bus_Email","Password","contact","Address","post","pin","district","Business_type","Reg_doc","Registration_stat", "action_buttons"]
    search_fields = ["Business_Name","Owner_Name","Logo","Bus_Email","Password","contact","Address","post","pin","district","Business_type","Reg_doc", "Registration_stat"]
    readonly_fields=["Password"]
    actions = ["accept_business", "reject_business"]
    # def show_profile_pic(self, obj):
    #     """Display profile picture in admin panel."""
    #     if obj.Profile_pic:
    #         return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />'.format(obj.Profile_pic.url))
    #     return "No Image"
    # show_profile_pic.short_description = "Profile Picture"

    def action_buttons(self, obj):
        """Add Block/Unblock buttons to admin panel."""
        return format_html(
            '<a href="Reject/{}/" class="button" style="background-color:red; color:white; padding:5px; border-radius:5px; text-decoration:none;">Reject</a> &nbsp;'
            '<a href="Accept/{}/" class="button" style="background-color:green; color:white; padding:5px; border-radius:5px; text-decoration:none;">Accept</a>',
            obj.id, obj.id
        )
    action_buttons.short_description = "Actions"

    def get_urls(self):
        """Define custom admin URLs for block/unblock actions."""
        urls = super().get_urls()
        custom_urls = [
            path("Reject/<int:busreg_id>/", self.admin_site.admin_view(self.reject_business_view), name="reject_business"),
            path("Accept/<int:busreg_id>/", self.admin_site.admin_view(self.accept_business_view), name="Accept_business"),
        ]
        return custom_urls + urls

    def reject_business_view(self, request,busreg_id):
        """Block a customer and update their role in the Login table."""
        business = Busreg.objects.get(id=busreg_id)
        business. Registration_stat= "Rejected"
        business.save()
        if business.Login_id:
            business.Login_id.Role = "Pending"
            business.Login_id.save()
        messages.success(request, f"Business {business.Business_Name} has been rejected.")
        return redirect(request.META.get('HTTP_REFERER', '/admin/app_name/Busreg/'))

    def accept_business_view(self, request, busreg_id):
        """Unblock a customer and update their role in the Login table."""
        business = Busreg.objects.get(id=busreg_id)
        business. Registration_stat = "Active"
        business.save()
        if business.Login_id:
            business.Login_id.Role = "business"
            business.Login_id.save()
            user_email=business.Bus_Email

            send_mail(
                    'Approval Message',
                    f'Congratulations! Admin has accepted you as a business\nEmail:{business.Bus_Email}\nPassword:{business.Password}',
                    'nayanadominic25@gmail.com',
                    [user_email],
                    fail_silently=False,
            )
        messages.success(request, f"Business {business.Business_Name} has been Accepted.")
        return redirect(request.META.get('HTTP_REFERER', '/admin/app_name/Busreg/'))

    def reject_business(self, request, queryset):
        """Block selected customers via bulk admin action."""
        for business in queryset:
            business. Registration_stat = "Rejected"
            business.save()
            if business.Login_id:
                business.Login_id.Role = "Pending"
                business.Login_id.save()
        messages.success(request, '''<script>alert("Selected business have been rejected.");window.location='/login/'</script>''')
    reject_business.short_description = "Reject selected business"

    def accept_business(self, request, queryset):
        """Unblock selected customers via bulk admin action."""
        for business in queryset:
            business. Registration_stat = "Active"  
            business.save()
            user_email=business.Bus_Email
            send_mail(
                    'Approval Message',
                    f'Congratulations! Admin has accepted you as a business',
                    'nayanadominic25@gmail.com',
                    [user_email],
                    fail_silently=False,
            )
            if business.Login_id:
                business.Login_id.Role = "business"
                business.Login_id.save()
        messages.success(request, "Selected business have been accepted.")
    accept_business.short_description = "Accept selected business"

    Busreg._meta.verbose_name = "Business Details"
    Busreg._meta.verbose_name_plural = "Business Details"
   
admin.site.register(Busreg, BusregAdmin)

class SavedDesignView(admin.ModelAdmin):
      list_display=["image","date"]
      search_fields=["image","date"]
      SavedDesign._meta.verbose_name = "Saved Design"
      SavedDesign._meta.verbose_name_plural = "Saved Design"
admin.site.register(SavedDesign,SavedDesignView)


  
  


class FeedbackView(admin.ModelAdmin):
    list_display=["customer_name","business_name","product_name","rating_message","Message"]
    search_fields=["rating_message","Message"]
   
    def customer_name(self, obj):
        return obj.Cusreg.Cus_Name  # Replace `name` with actual field in Cusreg

    def business_name(self, obj):
        return obj.Busreg.Business_Name  # Replace `name` with actual field in Busreg

    def product_name(self, obj):
        return obj.Products.Prod_Name  # Replace `name` with actual field in Products
    def rating_message(self, obj):
        rating_map = {
            "1": "Very Bad",
            "2": "Bad",
            "3": "Average",
            "4": "Good",
            "5": "Excellent"
        }
        return rating_map.get(obj.Rating, "Not Rated")

    customer_name.short_description ='Customer'
    business_name.short_description ='Business'
    product_name.short_description ='Product'
    rating_message.short_description = 'Rating'
    Feedback._meta.verbose_name = "Product Feedbacks"
    Feedback._meta.verbose_name_plural = "Product Feedbacks"
admin.site.register(Feedback,FeedbackView)
# class EnquiryView(admin.ModelAdmin):
#     list_display = ["Busreg_id", "Cusreg_id", "get_Cus_Name", "get_Cus_Contact", "Queries"]
#     search_fields = ["Busreg__id", "Cusreg__id", "Cusreg__Cus_Name", "Cusreg__Contact", "Queries"]

#     def get_Cus_Name(self, obj):
#         return obj.Cusreg.Cus_Name
#     get_Cus_Name.admin_order_field = "Cusreg__Cus_Name"  # Allows sorting by this field
#     get_Cus_Name.short_description = "Customer Name"

#     def get_Cus_Contact(self, obj):
#         return obj.Cusreg.Contact
#     get_Cus_Contact.admin_order_field = "Cusreg__Contact"
#     get_Cus_Contact.short_description = "Customer Contact"
    # user_email=business.Bus_Email

    # send_mail(
    #             'Approval Message',
    #             f'Congratulations! Admin has accepted you as a business\nEmail:{business.Bus_Email}\nPassword:{business.Password}',
    #             'nayanadominic25@gmail.com',
    #             [user_email],
    #             fail_silently=False,
    #         )

# admin.site.register(Enquiry, EnquiryView)

class ServfeedbackView(admin.ModelAdmin):
    list_display=["customer_name","business_name","rating_message","Message","service_name","Feedbacktime"]
    search_fields=["customer_name","business_name","rating_message","Message","service_name","Feedbacktime"]
    def customer_name(self, obj):
        return obj.Cusreg.Cus_Name
    def business_name(self, obj):
        return obj.Busreg.Business_Name
    def service_name(self, obj):
        return obj.Services.Serv_cat
    def rating_message(self, obj):
        rating_mapserv = {
            "1": "Very Bad",
            "2": "Bad",
            "3": "Average",
            "4": "Good",
            "5": "Excellent"
        }
        return rating_mapserv.get(obj.Rating,"Not Rated")
    
    customer_name.shortdescription="Customer"
    business_name.shortdescription="Business"
    service_name.shortdescription="Service"
    Servfeedback._meta.verbose_name = "Service Feedbacks"
    Servfeedback._meta.verbose_name_plural = "Service Feedbacks"

admin.site.register(Servfeedback,ServfeedbackView)


class ProductView(admin.ModelAdmin):
    list_display=["Prod_Name","Prod_cat","Prod_des","Prod_price","Availability","Prod_image"]
    search_fields=["Prod_Name","Prod_cat","Prod_des","Prod_price","Availability","Prod_image"]
    Products._meta.verbose_name = "Product Details"
    Products._meta.verbose_name_plural = "Product Details"
admin.site.register(Products,ProductView)

class CatgoryView(admin.ModelAdmin):
    list_display=["Cat_name"]
    search_fields=["Cat_name"]
    Category._meta.verbose_name = "Product Category"
    Category._meta.verbose_name_plural = "Product Category"
admin.site.register(Category,CatgoryView)

class SercatView(admin.ModelAdmin):
    list_display=["Serv_catname"]
    search_fields=["Serv_catname"]
    Servicecat._meta.verbose_name = "Service Category"
    Servicecat._meta.verbose_name_plural = "Service Category"
admin.site.register(Servicecat,SercatView) 

class ServView(admin.ModelAdmin):
    list_display=["business","Serv_cat"]
    search_fields=["business","Serv_cat"]
    def business(self,obj):
        return obj.Busreg.Business_Name
    business.shortdescription="Business Name"
    Services._meta.verbose_name = "Services Details"
    Services._meta.verbose_name_plural = "Services details"
admin.site.register(Services,ServView) 

class RoomImageView(admin.ModelAdmin):
    list_display=["image","uploaded_at"]
    search_fields=["image","uploaded_at"]
    RoomImage._meta.verbose_name = "Room Images"
    RoomImage._meta.verbose_name_plural = "Room Images"
admin.site.register(RoomImage,RoomImageView)

class OffersView(admin.ModelAdmin):
    list_display = [ "Offer_desc", "Discount", "Start_date", "End_date"]
    search_fields = ["Offer_desc", "Discount", "Start_date", "End_date"]

#     def get_Prod_Name(self, obj):  
#         return obj.Products.Prod_Name if obj.Products else "No Product"
    
#     get_Prod_Name.admin_order_field = "Products__Prod_Name"  
#     get_Prod_Name.short_description = "Product Name" 
    Offers._meta.verbose_name = "Offers Details"
    Offers._meta.verbose_name_plural = "Offers Details" 

admin.site.register(Offers, OffersView)