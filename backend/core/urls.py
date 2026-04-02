from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('legalcases/', views.legalcase_list, name='legalcase_list'),
    path('legalcases/create/', views.legalcase_create, name='legalcase_create'),
    path('legalcases/<int:pk>/edit/', views.legalcase_edit, name='legalcase_edit'),
    path('legalcases/<int:pk>/delete/', views.legalcase_delete, name='legalcase_delete'),
    path('legalclients/', views.legalclient_list, name='legalclient_list'),
    path('legalclients/create/', views.legalclient_create, name='legalclient_create'),
    path('legalclients/<int:pk>/edit/', views.legalclient_edit, name='legalclient_edit'),
    path('legalclients/<int:pk>/delete/', views.legalclient_delete, name='legalclient_delete'),
    path('legaltimeentries/', views.legaltimeentry_list, name='legaltimeentry_list'),
    path('legaltimeentries/create/', views.legaltimeentry_create, name='legaltimeentry_create'),
    path('legaltimeentries/<int:pk>/edit/', views.legaltimeentry_edit, name='legaltimeentry_edit'),
    path('legaltimeentries/<int:pk>/delete/', views.legaltimeentry_delete, name='legaltimeentry_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
