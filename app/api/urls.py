from .views import reports, faqs, translations
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'reports', reports.ReportViewSet, base_name='Report')
router.register(r'translations', translations.ReportTranslationViewSet)
router.register(r'faqs', faqs.FragmentViewSet)
