"""RocketData URL Configuration

The `urlpatterns` list routes URLs to views.py. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views.py
    1. Add an import:  from my_app import views.py
    2. Add a URL to urlpatterns:  path('', views.py.home, name='home')
Class-based views.py
    1. Add an import:  from other_app.views.py import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from app.api.views import EnterpriseView, EnterpriseFromCountryView, StatisticsEnterpriseView, ProductsEnterpriseView, \
    ProductsView, DeleteProductsView, SupplyChainView, DeleteSupplyChainView, UpdateProductView, UpdateSupplyChainView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/schema/swagger-ui/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),

    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

    path('custom/list_enterprise', EnterpriseView.as_view()),
    path('custom/list_enterprise_from_country/<str:country>/', EnterpriseFromCountryView.as_view()),
    path('custom/list_enterprise_statistics', StatisticsEnterpriseView.as_view()),
    path('custom/list_enterprise_product/<int:product_id>/', ProductsEnterpriseView.as_view()),

    path('custom/add_product', ProductsView.as_view()),
    path('custom/update_product/<str:product_name>/', UpdateProductView.as_view()),
    path('custom/delete_product/<str:product_name>/', DeleteProductsView.as_view()),

    path('custom/add_supply_chain/', SupplyChainView.as_view()),
    path('custom/update_supply_chain/<str:provider_name>/<str:request_name>', UpdateSupplyChainView.as_view()),
    path('custom/delete_supply_chain/<str:provider_name>/<str:request_name>/', DeleteSupplyChainView.as_view()),
]

