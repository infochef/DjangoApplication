from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.urls import reverse
from .services.programms_service import ProgramServiceImpl
from .models import Programs_Offered, Programs_Scheduled
import logging
import json

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

class ProgramServiceView(View):

    def __init__(self):
        self.service = ProgramServiceImpl()
        super().__init__()

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        program_id = kwargs.get('program_id')
        if 'search' in request.path:
            return self.search_program_for_update(request)
        if program_id:
            if 'update' in request.path:
                return self.update_program_offered(request, program_id)
            return self.program_detail(request, program_id)
        if 'create' in request.path:
            return render(request, 'create_program.html')
        return self.list_programs_offered(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'create' in request.path:
            return self.create_program_offered(request, *args, **kwargs)
        if 'update' in request.path:
            program_id = kwargs.get('program_id')
            return self.update_program_offered(request, program_id)
        if 'delete' in request.path:
            program_id = kwargs.get('program_id')
            return self.delete_program_offered(request, program_id)
        if 'search' in request.path:
            return self.search_program_for_update(request, is_post=True)
        return JsonResponse({'error': 'Invalid request'}, status=400)

    def put(self, request, *args, **kwargs):
        program_id = kwargs.get('program_id')
        return self.update_program_offered(request, program_id)

    def delete(self, request, *args, **kwargs):
        program_id = kwargs.get('program_id')
        return self.delete_program_offered(request, program_id)

    def list_programs_offered(self, request, *args, **kwargs):
        try:
            programs = self.service.list_all_programs()
            if request.headers.get('Content-Type') == 'application/json':
                programs_data = [program.__dict__ for program in programs]
                return JsonResponse({'programs_offered': programs_data})
            return render(request, 'programs_offered.html', {'programs_offered': programs})
        except Exception as e:
            logger.error(f"Error fetching programs: {e}")
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)

    def program_detail(self, request, program_id):
        try:
            program = get_object_or_404(Programs_Offered, pk=program_id)
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse(program.__dict__)
            return render(request, 'program_detail.html', {'program': program})
        except Exception as e:
            logger.error(f"Unexpected error while fetching program details: {e}")
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)

    def create_program_offered(self, request, *args, **kwargs):
        if request.headers.get('Content-Type') == 'application/json':
            try:
                data = json.loads(request.body)
                new_program = Programs_Offered(
                    ProgramName=data['ProgramName'],
                    Description=data['Description'],
                    Applicant_eligibility=data['Applicant_eligibility'],
                    Duration=data['Duration'],
                    Degree_certificate_offered=data['Degree_certificate_offered']
                )
                self.service.add_program_offered(new_program)
                return JsonResponse({'message': 'Program added successfully'}, status=201)
            except ValidationError as e:
                return JsonResponse({'error': f"Validation error: {e.messages}"}, status=400)
            except Exception as e:
                logger.error(f"Unexpected error while adding program offered: {e}")
                return JsonResponse({'error': 'Unexpected error occurred'}, status=500)
        else:
            try:
                data = request.POST
                new_program = Programs_Offered(
                    ProgramName=data.get('ProgramName'),
                    Description=data.get('Description'),
                    Applicant_eligibility=data.get('Applicant_eligibility'),
                    Duration=data.get('Duration'),
                    Degree_certificate_offered=data.get('Degree_certificate_offered')
                )
                self.service.add_program_offered(new_program)
                return redirect(reverse('programms:program_detail', args=[new_program.id]))
            except ValidationError as e:
                logger.error(f"Validation error while adding program offered: {e}")
                return render(request, 'create_program.html', {'error': f"Validation error: {e.messages}"})
            except Exception as e:
                logger.error(f"Unexpected error while adding program offered: {e}")
                return render(request, 'create_program.html', {'error': 'Unexpected error occurred'})

    def search_program_for_update(self, request, is_post=False):
        if is_post:
            description = request.POST.get('Description')
            if not description:
                return render(request, 'search_program_for_update.html', {'error': 'Description is required'})
            try:
                # Search for the program based on Description
                program = Programs_Offered.objects.get(Description=description)
                return redirect(reverse('programms:update_program_offered', args=[program.pk]))
            except ObjectDoesNotExist:
                return render(request, 'search_program_for_update.html', {'error': 'Program not found'})
        return render(request, 'search_program_for_update.html')


    def update_program_offered(self, request, program_id):
        try:
            if request.method == 'GET':
                # Fetch and display the program details for updating
                program = get_object_or_404(Programs_Offered, pk=program_id)
                return render(request, 'update_program.html', {'program': program})

            elif request.method == 'POST':
                # Handle form submission to update the program
                data = request.POST
                program = get_object_or_404(Programs_Offered, pk=program_id)
                program.ProgramName = data.get('ProgramName', program.ProgramName)
                program.Description = data.get('Description', program.Description)
                program.Applicant_eligibility = data.get('Applicant_eligibility', program.Applicant_eligibility)
                program.Duration = data.get('Duration', program.Duration)
                program.Degree_certificate_offered = data.get('Degree_certificate_offered', program.Degree_certificate_offered)
                self.service.update_program_offered(program)
                return redirect(reverse('programms:program_detail', args=[program.pk]))

            elif request.method == 'PUT':
                # Handle API request for updating the program
                data = json.loads(request.body)
                program = get_object_or_404(Programs_Offered, pk=program_id)
                program.ProgramName = data.get('ProgramName', program.ProgramName)
                program.Description = data.get('Description', program.Description)
                program.Applicant_eligibility = data.get('Applicant_eligibility', program.Applicant_eligibility)
                program.Duration = data.get('Duration', program.Duration)
                program.Degree_certificate_offered = data.get('Degree_certificate_offered', program.Degree_certificate_offered)
                self.service.update_program_offered(program)
                return JsonResponse({'message': 'Program updated successfully'})

        except ValidationError as e:
            return JsonResponse({'error': f"Validation error: {e.messages}"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Program not found'}, status=404)
        except Exception as e:
            logger.error(f"Unexpected error while updating program offered: {e}")
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)

    def delete_program_offered(self, request, *args, **kwargs):
        try:
            if request.method == 'GET':
                program_id = kwargs.get('program_id')
                program = get_object_or_404(Programs_Offered, pk=program_id)
                return render(request, 'delete_program.html', {'program': program})

            elif request.method == 'POST':
                program_id = kwargs.get('program_id')
                program = get_object_or_404(Programs_Offered, pk=program_id)
                self.service.delete_program_offered(program)
                return redirect(reverse('programms:list_programs_offered'))

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Program not found'}, status=404)
        except Exception as e:
            logger.error(f"Unexpected error while deleting program offered: {e}")
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)


class ScheduledProgramServiceView(View):

    def __init__(self):
        self.service = ProgramServiceImpl()

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list_scheduled_programs(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create_scheduled_program(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update_scheduled_program(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete_scheduled_program(request, *args, **kwargs)

    def list_scheduled_programs(self, request, *args, **kwargs):
        try:
            program_name = request.GET.get('program_name')
            if program_name:
                programs = self.service.list_all_scheduled_programs(program_name)
            else:
                programs = Programs_Scheduled.objects.all()
            if request.headers.get('Content-Type') == 'application/json':
                programs_data = [program.__dict__ for program in programs]
                return JsonResponse({'programs_scheduled': programs_data})
            return render(request, 'scheduled_programs.html', {'programs_scheduled': programs})
        except Exception as e:
            logger.error(f"Error fetching scheduled programs: {e}")
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)

    def create_scheduled_program(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            new_program = Programs_Scheduled(
                ProgramName=data['ProgramName'],
                Location=data['Location'],
                Start_Date=data['Start_Date'],
                End_Date=data['End_Date'],
                sessions_per_week=data['sessions_per_week']
            )
            self.service.create_scheduled_program(new_program)
            return JsonResponse({'message': 'Scheduled program created successfully'}, status=201)
        except ValidationError as e:
            return JsonResponse({'error': f"Validation error: {e.messages}"}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)

    def update_scheduled_program(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            program_id = data['Scheduled_program_id']
            program = get_object_or_404(Programs_Scheduled, pk=program_id)
            program.ProgramName = data.get('ProgramName', program.ProgramName)
            program.Location = data.get('Location', program.Location)
            program.Start_Date = data.get('Start_Date', program.Start_Date)
            program.End_Date = data.get('End_Date', program.End_Date)
            program.sessions_per_week = data.get('sessions_per_week', program.sessions_per_week)
            self.service.update_scheduled_program(program)
            return JsonResponse({'message': 'Scheduled program updated successfully'}, status=200)
        except ValidationError as e:
            return JsonResponse({'error': f"Validation error: {e.messages}"}, status=400)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Scheduled program not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)

    def delete_scheduled_program(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            program_id = data['Scheduled_program_id']
            self.service.delete_scheduled_program(program_id)
            return JsonResponse({'message': 'Scheduled program deleted successfully'}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Scheduled program not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'Unexpected error occurred'}, status=500)
