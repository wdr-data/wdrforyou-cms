from .views import reports, faqs
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'reports', reports.ReportViewSet)
router.register(r'faqs', faqs.FragmentViewSet)
