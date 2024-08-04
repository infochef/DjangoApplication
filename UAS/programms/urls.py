from django.urls import path
from .views import ProgramServiceView

app_name = 'programms'

urlpatterns = [
    path('programs/', ProgramServiceView.as_view(), name='list_programs_offered'),
    path('programs/<int:program_id>/', ProgramServiceView.as_view(), name='program_detail'),
    path('programs/search/', ProgramServiceView.as_view(), name='search_program_for_update'),
    path('programs/update/<int:program_id>/', ProgramServiceView.as_view(), name='update_program_offered'),
    path('programs/delete/<int:program_id>/', ProgramServiceView.as_view(), name='delete_program_offered'),
    path('program/create/', ProgramServiceView.as_view(), name='create_program_offered'),
]
