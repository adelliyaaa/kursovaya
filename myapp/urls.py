from django.urls import path

from myapp.views.index import index, project_images, create, login_view, registration_view, edit_project, \
    edit_project_image, search_projects_by_category, send_message, chat_view

urlpatterns = [
    path("index", index, name="index"),
    path('project_images/<int:project_id>/', project_images, name='project_images'),
    path('create/', create, name='create'),
    path('', login_view, name='login_view'),
    path('registration_view/', registration_view.as_view(), name='registration_view'),
    path('edit_project/<int:project_id>/', edit_project, name='edit_project'),
    path('edit_project_image/<int:project_id>/', edit_project_image, name='edit_project_image'),
    path('search/', search_projects_by_category, name='search_projects_by_category'),
    path('chat/', chat_view, name='chat'),
    path('send_message/', send_message, name='send_message'),


]



