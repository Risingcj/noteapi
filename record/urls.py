from django.urls import path
from . import views


urlpatterns = [
    path('links/', views.display_records, name='list_of links_and_headers'),
    path('links/<int:record_id>/', views.display_record, name='requested_link'),
    path('edit_links/<int:record_id>/', views.edit_record, name='edit_record'),
    path('del_links/<int:record_id>/', views.delete_record, name='delete_record'),
    path('search_links/', views.search_record, name='Search_record'),
    path('save/', views.save_records, name='save_a_link')
]