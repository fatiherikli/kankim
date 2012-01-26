from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from kankim.utils import here

admin.autodiscover()

urlpatterns = patterns('',

    # genel sayfalar
    (r'^$', 'kankim.main.views.index') ,
    (r'^register', 'kankim.main.views.register') ,
    (r'^login', 'kankim.main.views.login') ,
    (r'^logout', 'kankim.main.views.logout') ,
    (r'^profile-edit', 'kankim.main.views.profile_edit') ,
    (r'^change-profile-picture', 'kankim.main.views.change_profile_picture') ,

    #friendship
    (r'^friends/$', 'kankim.accounts.views.my_friends') ,
    (r'^friends/add/(?P<username>.*)', 'kankim.accounts.views.add') ,
    (r'^friends/accept/(?P<username>.*)', 'kankim.accounts.views.accept') ,
    (r'^friends/cancel/(?P<username>.*)', 'kankim.accounts.views.cancel') ,

    #accounts
     (r'^search', 'kankim.accounts.views.search'),
     
    #admin
    (r'^admin/', include(admin.site.urls)),

    
)


#Static dosyalar
urlpatterns += patterns('django.views.static',
    (r'^static/(?P<path>.*)$',
        'serve', {
        'document_root': here('static'),
        'show_indexes': True }),
)

