from django.urls import path

from .views import (
    get_records,
    upload_csv,
    update_status
)

urlpatterns = [
    path(
        'records/',
        get_records
    ),

    path(
        'upload/',
        upload_csv
    ),

    path(
        'update-status/<int:record_id>/',
        update_status
    ),
]