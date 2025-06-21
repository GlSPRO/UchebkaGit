from rest_framework.routers import DefaultRouter
from .views import (
    CarCategoryViewSet, CarStatusViewSet, CarViewSet, CarImageViewSet,
    RoleViewSet, CustomUserViewSet, BookingViewSet,
    PaymentTypeViewSet, OrderViewSet, ReviewViewSet
)

router = DefaultRouter()
router.register(r'car-categories', CarCategoryViewSet)
router.register(r'car-statuses', CarStatusViewSet)
router.register(r'cars', CarViewSet)
router.register(r'car-images', CarImageViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'users', CustomUserViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'payment-types', PaymentTypeViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls
