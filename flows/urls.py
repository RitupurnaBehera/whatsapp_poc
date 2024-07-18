from django.urls import path
from . import views

urlpatterns = [
    path('create-flow/', views.CreateFlowView.as_view(), name='create-flow'),
    path('handle-flow-response/', views.handle_flow_response, name='handle-flow-response'),
    path('webhook/', views.WebhookVerificationView.as_view(), name='webhook-verification'),
]
