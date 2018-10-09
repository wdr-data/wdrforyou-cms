from .views import reports
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'reports', reports.ReportViewSet)