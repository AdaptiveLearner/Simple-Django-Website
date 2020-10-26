from django.conf.urls import url
from django.contrib import admin
from f1app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^admin/', admin.site.urls),

	url(r'^$', views.index),
	url(r'^index/$', views.index),

#	url(r'^post/$', views.post), # POST 傳送表單
	url(r'^new_employee/$', views.new_employee), #資料新增，資料作驗證
	url(r'^new_country/$', views.new_country), #資料新增，資料作驗證
	url(r'^new_agent/$', views.new_agent), #資料新增，資料作驗證
	url(r'^new_dependent/$', views.new_dependent), #資料新增，資料作驗證
	url(r'^new_dependemp/$', views.new_dependemp), #資料新增，資料作驗證

	url(r'^print_employee/(\w+)/$', views.print_employee),
	url(r'^print_country/(\w+)/$', views.print_country),
	url(r'^print_agent/(\w+)/$', views.print_agent),
	url(r'^print_dependent/(\w+)/$', views.print_dependent),
	url(r'^print_dependemp/(\w+)/$', views.print_dependemp),

	url(r'^status_employee/(\w+)/(\w+)/$', views.status_employee),
	url(r'^status_country/(\w+)/(\w+)/$', views.status_country),
	url(r'^delete_agent/(\w+)/$', views.delete_agent),	
	url(r'^delete_dependent/(\w+)/$', views.delete_dependent),	

	url(r'^edit_employee/(\w+)/(\w+)$', views.edit_employee),
	url(r'^edit_country/(\w+)/(\w+)$', views.edit_country),
	url(r'^edit_agent/(.*)/(\w+)$', views.edit_agent),
	url(r'^edit_dependent/(\w+)/(\w+)$', views.edit_dependent),
	url(r'^edit_dependemp/(\w+)/(\w+)$', views.edit_dependemp),

	url(r'^userInterface/$', views.userInterface),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)