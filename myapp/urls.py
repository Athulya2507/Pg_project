from django.contrib import admin
from django.urls import path


from myapp import views

urlpatterns=[
    path('login/',views.login,name='login'),
    path('login_post/',views.login_post,name='login_post'),

    path('logout/',views.logout,name='logout'),

    path('cus_reg/',views.cus_reg,name='cus_reg'),
    path('cusreg_post/',views.cusreg_post,name='cusreg_post'),

    path('cusprod_view/',views.cusprod_view,name='cusprod_view'),
    path('cusprod_view_post/',views.cusprod_view_post,name='cusprod_view_post'),

    path('cusserv_view/',views.cusserv_view,name='cusserv_view'),
    path('sendmailserv/<int:id>/', views.sendmailserv, name='sendmailserv'),

    path('cusserv_view_post/',views.cusserv_view_post,name='cusserv_view_post'),

    # path('cusoffers_view/',views.cusoffers_view,name='cusoffers_view'),
    # path('cusoffers_view_post/',views.cusoffers_view_post,name='cusoffers_view_post'),

    path('cuscontact_view/',views.cuscontact_view,name='cuscontact_view'),
    path('cuscontact_view_post/',views.cuscontact_view_post,name='cuscontact_view_post'),
    path('ind_contact/<id>/',views.ind_contact,name='ind_contact'),

    path('servenq/',views.servenq,name='servenq'),
    path('servenq_post/',views.servenq_post,name='servenq_post'),
    

    path('servfeedback/<id>/',views.servfeedback,name='servfeedback'),
    path('servfeedback_post/',views.servfeedback_post,name='servfeedback_post'),

    path('products_page/',views.products_page,name='products_page'),
    path('service_page/',views.service_page,name='service_page'),
    path('ind_prod/<id>/',views.ind_prod,name='ind_prod'),
    path('business_logos/',views.business_logos,name='business_logos'),
    path('business_products/<id>/',views.business_products,name='business_products'),
    path('sendmail/<id>/',views.sendmail,name='sendmail'),
    


    # path('cusprofile_view/',views.cusprofile_view,name='cusprofile_view'),
    

    path('editprofile_cus/',views.editprofile_cus,name='editprofile_cus'),
    path('editprofile_cus_post/',views.editprofile_cus_post,name='editprofile_cus_post'),

    path('feedback/<id>/',views.feedback,name='feedback'),
    path('feedbackview_post/',views.feedbackview_post,name='feedbackview_post'),

    path('enquiry/<id>/',views.enquiry,name='enquiry'),
    path('enquiry_post/',views.enquiry_post,name='enquiry_post'),


    path('cusbus_view/',views.cusbus_view,name='cusbus_view'),
    path('cusbus_view_post/',views.cusbus_view_post,name='cusbus_view_post'),

    path('roomify/',views.roomify,name='roomify'),

    path('homecus/',views.homecus,name='homecus'),
    path('homecus_post/',views.homecus_post,name='homecus_post'),

    
    
    path('bus_reg/',views.bus_reg,name='bus_reg'),
    path('busreg_post/',views.busreg_post,name='busreg_post'),

    path('editprofile_bus/',views.editprofile_bus,name='editprofile_bus'),
    path('editprofile_bus_post/',views.editprofile_bus_post,name='editprofile_bus_post'),

    # path('viewprofile_bus/',views.viewprofile_bus,name='viewprofile_bus'),
    # path('viewprofile_bus_post/',views.viewprofile_bus_post,name='viewprofile_bus_post'),

    
    
    
    
    path('products/',views.products,name='products'),
    path('products_post/',views.products_post,name='products_post'),

    path('prodview_bus/',views.prodview_bus,name='prodview_bus'),
    # path('prodview_bus_post/',views.prodview_bus_post,name='prodview_bus_post'),

    path('editprod/<id>',views.editprod,name='editprod'),#here we have to pass the id of the particular product to show only its edited details.
    path('editprod_post/',views.editprod_post,name='editprod_post'),

    path('editprodview_bus/',views.editprodview_bus,name='editprodview_bus'),
    path('editprodviewbus_post/',views.editprodviewbus_post,name='editprodviewbus_post'),

    path('addprod/',views.addprod,name='addprod'),
    path('addprod_post/',views.addprod_post,name='addprod_post'),

    path('deleteproduct/<id>',views.deleteproduct,name='deleteproduct'),
   

    
    
    path('offers/',views.offers,name='offers'),
    # path('offers_post/',views.offers_post,name='offers_post'),
   
    path('addoffers/<id>',views.addoffers,name='addoffers'),
    path('addoffers_post/',views.addoffers_post,name='addoffers_post'),

    path('editoffers/<id>/',views.editoffers,name='editoffers'),
    path('editoffers_post/',views.editoffers_post,name='editoffers_post'),

    path('editoffersview/',views.editoffersview,name='editoffersview'),
    # path('editoffersview_post/',views.editoffersview_post,name='editoffersview_post'),


    path('deloffers/<id>/',views.deloffers,name='deloffers'),
   

    
    path('addservice/',views.addservice,name='addservice'),
    path('addservice_post/',views.addservice_post,name='addservice_post'),

    path('service/',views.service,name='service'),
    # path('service_post/',views.service_post,name='service_post'),

    path('editservice/<id>',views.editservice,name='editservice'),
    path('editservice_post/',views.editservice_post,name='editservice_post'),

    path('delserv/<id>',views.delserv,name='delserv'),
   

    
    
    
    path('contact/',views.contact,name='contact'),
    # path('contact_post/',views.contact_post,name='contact_post'),

    path('addcontact/',views.addcontact,name='addcontact'),
    path('addcontact_post/',views.addcontact_post,name='addcontact_post'),

    path('editcontact/<id>',views.editcontact,name='editcontact'),
    path('editcontact_post/',views.editcontact_post,name='editcontact_post'),

    path('delcontact/<id>',views.delcontact,name='delcontact'),
   



    path('viewfeed_bus/',views.viewfeed_bus,name='viewfeed_bus'),
    # path('viewfeed_bus_post/',views.viewfeed_bus_post,name='viewfeed_bus_post'),

    path('viewservfeed_bus/',views.viewservfeed_bus,name='viewservfeed_bus'),
    
    path('homebus/',views.homebus,name='homebus'),
    path('homebus_post/',views.homebus_post,name='homebus_post'),

     path('log_out/',views.log_out,name='log_out'),

    
    
    
    path('bustab_admin/',views.bustab_admin,name='bustab_admin'),
    path('bustab_admin_post/',views.bustab_admin_post,name='bustab_admin_post'),

    path('custab_admin/',views.custab_admin,name='custab_admin'),
    path('custab_admin_post/',views.custab_admin_post,name='custab_admin_post'),

    path('viewfeed_admin/',views.viewfeed_admin,name='viewfeed_admin'),
    path('viewfeed_admin_post/',views.viewfeed_admin_post,name='viewfeed_admin_post'),

    path('viewenq_admin/',views.viewenq_admin,name='viewenq_admin'),
    path('viewenq_admin_post/',views.viewenq_admin_post,name='viewenq_admin_post'),

    path('homeadmin/',views.homeadmin,name='homeadmin'),
    path('homeadmin_post/',views.homeadmin_post,name='homeadmin_post'),

     path('upload/',views.upload,name='upload'),
     path('upload_images/',views. upload_images,name=' upload_images'),
     path('save_design/',views.save_design,name='save_design'),
     path('design/',views.design,name='design')
]
