
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.urls.base import reverse_lazy
from django.utils.translation import gettext as _
from apps.scholarship.models import Department
from apps.scholarship.views import create_or_update_student
from gears.sevima import webservice
from django.contrib import messages



class StudentImporter(LoginRequiredMixin, TemplateView):
    success_url = reverse_lazy('admin:scholarship_student_changelist')
    template_name = "admin/student_importer_form.html"
    admin_site = None
    section_title = _('Student Importer')

    # Require a specific permission
    @method_decorator(permission_required('scholarship.change_student', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    
    def get_students(self, student_ids, sevima_api):
        students = []
        for student_id in student_ids.split(','):
            student_id = student_id.replace(' ', '')
            student    = sevima_api.getSingleMahasiswa(nim_mhs = student_id).get('data', {})
            if student:
                students.append(student)
        return students
            
        
    def create_students(self, students):
        students_created = []
        for student in students:
            instance, created = create_or_update_student(student)
            if created:
                students_created.append(instance)
        return students_created
        
    
    def post(self, request):
        student_ids = request.POST.get('student-ids')
        status = request.POST.get('status')
        action = request.POST.get('action')
        
        sevima_api = webservice.SevimaAPI()
        students   = self.get_students(student_ids, sevima_api) 
        
        if action == 'student-importer-search':
            context_data = self.get_context_data()
            context_data['students'] = students
            return render(request, 'admin/student_importer_choose.html', context = context_data)
        elif action == 'student-importer-execute':
            students_created = self.create_students(students)
            if students_created:
                messages.success(request, _('Successfuly import %s') % ', '.join([f"{x.name} ({x.student_id})" for x in students_created]))
        return redirect(self.success_url)
        
        
    def get_context_data(self, **kwargs):
        context_data  = super().get_context_data()
        context_data['title'] = self.section_title
        admin_context_data = dict(self.admin_site.each_context(self.request))
        admin_context_data.update(context_data)
        return admin_context_data



class ScholarshipTools(TemplateView):
    template_name = "admin/scholarship_tools.html"
    admin_site = None
    section_title = _('Scholarship Tools')

    def get_context_data(self, **kwargs):
        self.toolbox = [
            {
                'id'    : 'student-importer',
                'title' : _('Student Importer'),
                'url'   : f"{reverse_lazy('admin:scholarship_student_changelist')}importer",
                'desc'  : _('Tool to import student data from Sevima or Sister systems, allowing easy management and synchronization of student records.')
            },
            {
                'id'    : 'unit-importer',
                'title' : _('Unit Importer'),
                'url'   : None,
                'desc'  : _('Import unit data from external sources to streamline the setup of academic units within the system.')
            },
            {
                'id'    : 'faculty-importer',
                'title' : _('Faculty Importer'),
                'url'   : None,
                'desc'  : _('Import faculty data to ensure faculty records are synchronized with the academic unit structure.')
            },
            {
                'id'    : 'department-importer',
                'title' : _('Department Importer'),
                'url'   : None,
                'desc'  : _('Import department information to maintain consistent and up-to-date records for academic departments.')
            },
        ]

        context_data  = super().get_context_data()
        context_data['title'] = self.section_title
        context_data['toolbox'] = self.toolbox
        admin_context_data = dict(self.admin_site.each_context(self.request))
        admin_context_data.update(context_data)
        return admin_context_data
