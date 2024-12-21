from datetime import datetime
from django.contrib import admin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.html import format_html
from django_summernote.admin import SummernoteModelAdmin
from apps.scholarship.views import create_or_update_student
from django.utils.translation import gettext as _
from django.db.models import Count
from apps.scholarship.admin_features import *
from apps.scholarship.forms import StudentForm
from apps.scholarship.models import *
from gears.sevima import webservice
from gears.sister import SisterAPI 


sevima_api = webservice.SevimaAPI()
sister_api = SisterAPI


@admin.register(Preference)
class PreferenceAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        # Allow adding only if no instances exist
        return not Preference.objects.exists()

    def changelist_view(self, request, extra_context=None):
        # Redirect to the change form if an object already exists
        try:
            preference = Preference.objects.get()
            return HttpResponseRedirect(reverse("admin:scholarship_preference_change", args=[preference.id]))
        except Preference.DoesNotExist:
            return HttpResponseRedirect(reverse("admin:scholarship_preference_add"))

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('toolbox', self.admin_site.admin_view(ScholarshipTools.as_view(admin_site=self.admin_site)), name="scholarship.toolbox"),
        ]
        return my_urls + urls



class BaseUnitAdmin(admin.ModelAdmin):
    USE_SISTER_API = False
    USE_SEVIMA_API = False

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "unit":
            kwargs['queryset'] = Unit.objects.annotate(
                num__parent=Count('parent__parent')
            ).order_by('num__parent')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def get_sister_unit(self, **kwargs):
        data = []
        if not hasattr(self, 'sister_unit_dict'):
            return data
        for unit_key, unit_value in self.sister_unit_dict.items():
            for x, y in kwargs.items():
                if unit_value.get(x) == y:
                    data.append(unit_value)
        return data
            

    def get_sister_data(self, request):
        self.sister_unit_dict  = {}
        self.sister_profil_pt  = sister_api.get_referensi_profil_pt().get('data', {})
        self.sister_unit_kerja = sister_api.get_referensi_unit_kerja(id_perguruan_tinggi = self.sister_profil_pt.get('id_perguruan_tinggi')).get('data', {})

        try:
            for unit_sister in self.sister_unit_kerja:
                id_unit_kerja = unit_sister.get('id')
                unit_kerja    = sister_api.get_referensi_detail_unit_kerja(id_unit_kerja = id_unit_kerja).get('data', {})
                if type(unit_kerja) is list and len(unit_kerja) > 0:
                    unit_kerja = unit_kerja[0]
                    kode_unit  = unit_kerja.get('kode_unit')
                    if kode_unit:
                        self.sister_unit_dict[kode_unit] = unit_kerja
        except Exception as error:
            messages.warning(request, _('Unable to get data from Sister Live API: %s') % error )            


    def changelist_view(self, request, extra_context = None):
        if self.USE_SISTER_API:
            self.get_sister_data(request)
        return super().changelist_view(request, extra_context)



@admin.register(Unit)
class UnitAdmin(BaseUnitAdmin):
    list_display   = ('name', 'code', 'shortname', 'parent')
    search_fields  = ['name', 'code']
    list_per_page  = 15
    USE_SISTER_API = True

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return Unit.objects.annotate(
            num_parent = Count('parent'),
        ).order_by('num_parent')
        

    def populate_units(self, request):
        response = sevima_api.getAllUnit(limit=50)
        if not response.get('status'):
            messages.warning(request, _('Unable to get units from Sevima Live API: %s') % response.get('message'))
            return

        # Extract units data and initialize counters
        units = response.get('data', [])
        counter = 0
         
        for unit in units:
            kode_unit   = unit.get('kode_unit', '')
            unit_sister = self.sister_unit_dict.get(kode_unit, {})
            instance, created = Unit.objects.get_or_create(
                code = kode_unit,
                defaults = {
                    'name': unit.get('nama_unit', ''),
                    'shortname': unit.get('nama_singkat', ''),
                }
            )
            if unit_sister.get('id') and not instance.id_unit:
                instance.id_unit = unit_sister.get('id')
                instance.save()
            if created:
                counter += 1
                
        # Display success message if any units were created
        if counter:
            messages.success(request, _("Successfully created %s units.") % counter)

        
    def changelist_view(self, request, extra_context=None):
        self.get_sister_data(request)
        self.populate_units(request)
        return super().changelist_view(request, extra_context=extra_context)
    


@admin.register(University)
class UniversityAdmin(BaseUnitAdmin):
    list_display = ('unit', 'english_name', 'date_establish', 'email', 'website')
    search_fields = ('unit__name', 'english_name', 'email')
    list_filter = ('date_establish',)
    USE_SISTER_API = True


    def has_add_permission(self, request):
        return not University.objects.exists()
        
    def populate_university(self, request):
        try:
            data = sister_api.get_referensi_profil_pt().get('data', {})
        except Exception as error:
            messages.warning(request, _('Unable to get university data from Sister APi: %s') % error)
            return
            
        try:
            unit = Unit.objects.get(code = data.get('kode_perguruan_tinggi').replace(' ', ''))
        except Unit.DoesNotExist:
            unit = None
        if unit is None:
            return
        
        __, created = University.objects.get_or_create(
            unit = unit, 
            defaults = {
                'legality_number': data.get('sk_pendirian', ''),
                'email': data.get('email', ''),
                'address': data.get('jalan', ''),
                'website': data.get('website', ''),
                'description': '',
            }
        )
        if created:
            messages.success(request, _('University data is created from Sister API'))
            
             
        
    def changelist_view(self, request, extra_context=None):
        super().changelist_view(request, extra_context=extra_context)
        try:
            university = University.objects.get()
            return HttpResponseRedirect(reverse("admin:scholarship_university_change", args=[university.id]))
        except University.DoesNotExist:
            self.populate_university(request)
            university = University.objects.get()
            return HttpResponseRedirect(reverse("admin:scholarship_university_change", args=[university.id]))
    
    

@admin.register(Faculty)
class FacultyAdmin(BaseUnitAdmin):
    list_display = ('unit', 'english_name', 'date_establish', 'email', 'website')
    search_fields = ('unit__name', 'english_name', 'email')
    USE_SISTER_API = True

    def populate_faculty(self, request):
        sister_faculties = self.get_sister_unit(id_jenis_unit = 1) # 1 is faculty
        counter = 0
        for faculty in sister_faculties:
            try:
                unit = Unit.objects.get(code = faculty.get('kode_unit').replace(' ', ''))
            except Unit.DoesNotExist:
                unit = None
            if unit:
                __, created = Faculty.objects.get_or_create(unit = unit, defaults = {
                    'description': '',
                    'legality_number': faculty.get('sk_penyelenggara', ''),
                })
                if created:
                    counter += 1
        # Display success message if any units were created
        if counter:
            messages.success(request, _("Successfully created %s faculties") % counter)


    def changelist_view(self, request, extra_context = None):
        self.get_sister_data(request)
        self.populate_faculty(request)
        return super().changelist_view(request, extra_context=extra_context)



@admin.register(Department)
class DepartmentAdmin(BaseUnitAdmin):
    list_display = ('unit', 'grade', 'email', 'website')
    search_fields = ('unit__name', 'english_name', 'email')
    list_filter = ('date_establish',)
    USE_SISTER_API = True

    def populate_department(self, request):
        sister_departments = self.get_sister_unit(id_jenis_unit = 3) # 3 is department
        counter = 0
        for department in sister_departments:
            try:
                unit = Unit.objects.get(code = department.get('kode_unit').replace(' ', ''))
            except Unit.DoesNotExist:
                unit = None
            if unit:
                __, created = Department.objects.update_or_create(defaults = {
                    'description': '',
                    'grade': department.get('grade', Department.GradeLevel.S1),
                    'legality_number': department.get('sk_penyelenggara', ''),
                }, unit = unit)
                if created:
                    counter += 1
        # Display success message if any units were created
        if counter:
            messages.success(request, _("Successfully created %s departments") % counter)


    def changelist_view(self, request, extra_context = None):
        self.get_sister_data(request)
        self.populate_department(request)
        return super().changelist_view(request, extra_context=extra_context)


@admin.register(Office)
class OfficeAdmin(BaseUnitAdmin):
    list_display = ('unit', 'english_name', 'date_establish', 'email', 'website')
    search_fields = ('unit__name', 'english_name', 'email')
    list_filter = ('date_establish',)
        
        
@admin.register(Student)
class StudentAdmin(BaseUnitAdmin):
    form = StudentForm
    list_display = ('name', 'student_id', 'department', 'source', 'status', 'mobile_number')
    search_fields = ('name', 'student_id', 'university_email', 'mobile_number')
    list_filter = ('department', 'date_birth')
    ordering = ('name',)
    autocomplete_fields = ['province', 'regency', 'district', 'village']
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'student_id', 'department')
        }),
        (_('Personal Information'), {
            'fields': ('mobile_number', 'university_email')
        }),
        (_('Address Info'), {
            'fields': ('province', 'regency', 'district', 'village', 'address', 'postal_code',)
        }),
    )
    readonly_fields = ['user', 'name', 'student_id', 'department']
    
    
    def get_readonly_fields(self, request, obj):
        readonly_fields = super().get_readonly_fields(request, obj)
        if request.user.is_superuser:
            return []
        return readonly_fields


    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        if object_id:
            student = self.get_object(request, object_id)
            student_sevima = sevima_api.getSingleMahasiswa(nim_mhs = student.student_id).get('data', {})
            if student_sevima:
                student, created = create_or_update_student(student_sevima)
        return super().changeform_view(request, object_id, form_url, extra_context)


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('importer', self.admin_site.admin_view(StudentImporter.as_view(admin_site=self.admin_site)), name="scholarship.student.import"),
        ]
        return my_urls + urls
    


@admin.register(ScholarshipAttachment)
class ScholarshipAttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'types', 'max_size', 'description_preview')
    search_fields = ('name', 'types')
    list_filter = ('types',)
    ordering = ('name',)
    
    def description_preview(self, obj):
        """Menampilkan potongan singkat dari deskripsi."""
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "-"
    description_preview.short_description = "Description"
    
@admin.register(ScholarshipTarget)
class ScholarshipTargetAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

    
class ScholarshipAttachmentRequirementInline(admin.TabularInline):
    model = ScholarshipAttachmentRequirement
    extra = 1  
    fields = ['attachment', 'is_required']  
    verbose_name = "Attachment Requirement"
    verbose_name_plural = "Attachment Requirements"


    
class ScholarshipApplicationInline(admin.TabularInline):
    model = ScholarshipApplication
    extra = 1
    fields = ('scholarship', 'status', 'application_date')
    readonly_fields = ('application_date',)
    
    
@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'source', 'destination', 'start_date', 'end_date', 'quota')
    list_filter = ('status', 'source', 'destination', 'targets')
    search_fields = ('name', 'description')
    filter_horizontal = ('faculties', 'departments', 'targets')
    date_hierarchy = 'start_date'
    ordering = ('-start_date',)
    inlines = [ScholarshipAttachmentRequirementInline] 
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'source', 'thumbnail', 'destination', 'targets')
        }),
        ('Schedule & Quota', {
            'fields': ('status', 'start_date', 'end_date', 'quota')
        }),
        ('Eligibility', {
            'fields': ('requirement', 'faculties', 'departments')
        }),
    )


class ScholarshipApplicationAttachmentInline(admin.TabularInline):
    model = ScholarshipApplicationAttachment
    extra = 1  # Jumlah form kosong yang ditampilkan
    fields = ['attachment', 'file', 'url', 'description']
    readonly_fields = ['description']  # Misalkan hanya baca untuk deskripsi
    verbose_name = "Attachment"
    verbose_name_plural = "Attachments"


@admin.register(Reviewer)
class ReviewerAdmin(admin.ModelAdmin):
    list_display = ('user', 'expertise', 'active', 'bio_summary')
    list_filter = ('active',)
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'expertise')
    ordering = ('user__username',)
    
    def bio_summary(self, obj):
        return obj.bio[:50] + "..." if obj.bio else "-"
    bio_summary.short_description = "Bio Summary"
    
    

class ApplicationReviewInline(admin.StackedInline):
    model = ApplicationReview
    extra = 1  # Menambahkan satu form kosong untuk menambahkan review
    fields = ('reviewer', 'recommended_status', 'review_comment')
    show_change_link = True  


@admin.register(ScholarshipApplication)
class ScholarshipApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'scholarship', 'status', 'application_date')
    list_filter = ('status', 'application_date')
    search_fields = ('student__name', 'scholarship__name')
    ordering = ('-application_date',)
    inlines = [ScholarshipApplicationAttachmentInline, ApplicationReviewInline]





