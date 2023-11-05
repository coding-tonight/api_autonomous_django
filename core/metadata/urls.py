from django.urls import path
from . import views
urlpatterns = [
    path('metadata/', views.MetaDataView.as_view())
]
