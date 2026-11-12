from django.urls import path
from .api import Dlist, Dhtviews
from . import views

urlpatterns = [
    # Web Views (Tailwind CSS)
    path("", views.dashboard, name="dashboard"),
    path("history/", views.history, name="history"),
    path("export-csv/", views.export_csv, name="export-csv"),
    
    # REST API Endpoints
    path("list/", Dlist, name="dht-list"),
    path("post/", Dhtviews.as_view(), name="dht-create"),
]
