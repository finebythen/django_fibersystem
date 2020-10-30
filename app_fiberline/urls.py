from django.urls import path
from . import views

urlpatterns = [
    # --> Main
    path('', views.main, name="Main"),

    # --> Views
    path('view/technikstandort/<str:pk>/', views.view_technikstandort, name="Technikstandort"),
    path('view/schacht-kvz/<str:pk>/', views.view_schacht_kvz, name="SchachtKvz"),

    # --> Create
    path('create/technikstandort/default/<str:pk>/', views.create_technikstandort_default, name="CreateTechnikstandortDefault"),
    path('create/schacht-kvz/<str:pk>/', views.create_schacht_kvz, name="CreateSchachtKvz"),
    path('create/kabel/<str:pk>/', views.create_kabel, name="CreateKabel"),
    path('create/rohr/<str:pk>/', views.create_rohr, name="CreateRohr"),
    path('create/einzelrohr/<str:pk>/', views.create_einzelrohr, name="CreateEinzelrohr"),
    path('create/wohneinheiten/<str:pk>/', views.create_wohneinheiten, name="CreateWohneinheiten"),

    # --> Combine
    path('combine/schacht-kvz-kabel/<str:pk>/', views.combine_schacht_kvz_kabel, name="CombineSchachtKvzKabel"),

    # --> Update
    path('update/technikstandort/default/<str:pk>/', views.update_technikstandort_default, name="UpdateTechnikstandortDefault"),
    path('update/schacht-kvz/<str:pk>/', views.update_schacht_kvz, name="UpdateSchachtKvz"),
    path('update/kabel/<str:pk>/', views.update_kabel, name="UpdateKabel"),

    # --> Delete
    path('delete/wohneinheit/<str:pk>/', views.delete_wohneinheit, name="DeleteWohneinheit"),
]
