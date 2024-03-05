# urls.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your existing URL patterns
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
