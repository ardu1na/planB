from dashboard.users.forms import EmailValidationOnForgotPassword
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.urls import path ,include
from dashboard import dashboard_views
from dashboard.users import users_views
app_name='dashboard'
urlpatterns = [

#########################################################################    
################  PLANB 

    path('',dashboard_views.index,name="index"),
    path('index/',dashboard_views.index,name="index"),
    
    
    ###  USERS module

    path('usuarios/',dashboard_views.users_list,name="usuarios"),
    path('usuario/add/',dashboard_views.useradd,name="useradd"),    
    path('usuario/<uuid:pk>/',dashboard_views.usuario_detail, name="usuario"),
    path('usuario/<uuid:pk>/delete/',dashboard_views.usuario_delete, name="usuariodelete"),
    
  ###  ALARMS ALERTS module
    path('alarmas/user/<uuid:pk>', dashboard_views.alertas, name="usuarioalertas"),

    
    path('alarmas/', dashboard_views.alertas, name="alertas"),
    
    # ajax monitoreo de alarmas
    path('alarmas/latest/', dashboard_views.latest, name='latest'),
    path('alarmas/has_new_data/', dashboard_views.has_new_data, name='has_new_data'),
    path('api/alarms/', dashboard_views.AlarmaEventAPIView.as_view(), name='apialarm'),



  ###  BARRIOS VIVIENDA  module

    path('barrios/',dashboard_views.barrios_list, name="barrios"),
    path('barrio/add/',dashboard_views.barrioadd,name="barrioadd"),    

    path('barrio/<uuid:pk>/delete/',dashboard_views.barrio_delete, name="barriodelete"),
    path('barrio/<uuid:pk>/',dashboard_views.barrio_detail, name="barrio"),
    path('barrio/<uuid:pk>/change/',dashboard_views.barrio_edit, name="barrioedit"),
    path('usuarios/<uuid:pk>/',dashboard_views.users_list,name="usuariosbarrio"),

    path('vivienda/<uuid:pk>/delete/',dashboard_views.vivienda_delete, name="viviendadelete"),
    path('vivienda/<uuid:pk>/',dashboard_views.vivienda_detail, name="vivienda"),
    path('vivienda/<uuid:pk>/change/',dashboard_views.vivienda_edit, name="viviendaedit"),
    path('vivienda/add/',dashboard_views.viviendaadd,name="viviendaadd"),    
    

################   end PLANB += index


#########################################################################3    
    
    
    
	path('users/',users_views.users,name="users"),
	path('user-details/<int:id>/',users_views.user_details,name="user-details"),
	path('add-user/',users_views.add_user,name="add-user"),
	path('edit-user/<int:id>/',users_views.edit_user,name="edit-user"),
	path('delete-user/<int:id>/',users_views.delete_user,name="delete-user"),
	path('delete-multiple-user/',users_views.delete_multiple_user,name="delete-multiple-user"),

	path('login/',users_views.login_user,name="login"),
	path('logout/',users_views.logout_user,name="logout"),
	path('groups/',users_views.groups_list,name="groups"),
	path('group-edit/<int:id>/',users_views.group_edit,name="group-edit"),
	path('group-delete/<int:id>/',users_views.group_delete,name="group-delete"),
	path('group-add/',users_views.group_add,name="group-add"),
	path('permissions/',users_views.permissions,name="permissions"),
	path('edit-permissions/<int:id>/',users_views.edit_permissions,name="edit-permissions"),
	path('delete-permissions/<int:id>/',users_views.delete_permissions,name="delete-permissions"),
	path('assign-permissions-to-user/<int:id>/',users_views.assign_permissions_to_user,name="assign-permissions-to-user"),
	path('signup/',users_views.signup,name="signup"),
	path('activate/<uidb64>/<token>/',users_views.activate, name='activate'),


    #CMS_Start-------------------

    path('pages/', include('dashboard.cms.pages.urls', namespace='pages')),
    path('blogs/', include('dashboard.cms.blog.urls', namespace='blog')),
    path('menus/', include('dashboard.cms.menu.urls', namespace='menu')),
    path('subscribe/', include('dashboard.cms.subscribe.urls', namespace='subscribe')),
    path('contact-us/', include('dashboard.cms.contactus.urls', namespace='contactus')),


    path('configurations/',dashboard_views.all_config,name='all-config'),
    path('configurations/reset/',dashboard_views.reset_config,name='reset-config'),
    path('configurations/download/',dashboard_views.download_config,name='download-config'),

    
    path('configurations/prefix/<str:prefix>/',dashboard_views.filter_config,name='filter-config'),
    path('add-configurations/',dashboard_views.add_config,name='add-config'),
    path('edit-configurations/<int:id>/',dashboard_views.edit_config,name='edit-config'),
    path('delete-configurations/<int:id>/',dashboard_views.delete_config,name='delete-config'),
    #CMS_End-----------------
    path('',dashboard_views.index,name="index"),
    path('index/',dashboard_views.index,name="index"),
    path('activity/',dashboard_views.activity,name="activity"),
    path('profile/',dashboard_views.profile,name="profile"),
    path('page-lock-screen/',dashboard_views.page_lock_screen,name="page-lock-screen"),
    path('page-error-400/',dashboard_views.page_error_400,name="page-error-400"),
    path('page-error-403/',dashboard_views.page_error_403,name="page-error-403"),
    path('page-error-404/',dashboard_views.page_error_404,name="page-error-404"),
    path('page-error-500/',dashboard_views.page_error_500,name="page-error-500"),
    path('page-error-503/',dashboard_views.page_error_503,name="page-error-503"),
    path('empty-page/',dashboard_views.empty_page,name="empty-page"),


    path('', users_views.password_change, name='password_change'),






    # This Route for PasswordChange
    path('password/', users_views.password_change, name='password_change'),

    # These Routes for PasswordReset
    path('password_reset/', auth_views.PasswordResetView.as_view(
        form_class=EmailValidationOnForgotPassword,
        success_url=reverse_lazy('dashboard:password_reset_done')),name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('dashboard:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]