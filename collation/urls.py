from django.contrib import admin
from django.urls import path

from .views import PollingUnitListView, LgaTotalResultView, AddPollUnitResultView, index

urlpatterns = [
    path('', index, name='home'),
    path('poll-total/', PollingUnitListView.as_view(), name='poll_result'),
    path('lga-total/', LgaTotalResultView.as_view(), name='lga_total'),
    path('poll-add/', AddPollUnitResultView.as_view(), name='poll_add'),
]