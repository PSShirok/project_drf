from rest_framework.routers import DefaultRouter

from payments.views import PaymentViewSet

app_name = 'payment'
router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
              ] + router.urls