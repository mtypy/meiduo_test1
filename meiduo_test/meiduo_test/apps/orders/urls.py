from django.conf.urls import url
from orders import views

urlpatterns = [
    url(r'^orders/settlement/$', views.OrdersSettlmentView.as_view()),
]