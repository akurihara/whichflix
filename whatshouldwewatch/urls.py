from django.contrib import admin
from django.urls import path

from whatshouldwewatch.elections.views import ElectionsView

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
    # Elections
    path("v1/elections", ElectionsView.as_view(), name="elections"),
]
