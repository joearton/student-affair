from django.db import models
from apps.api.models import BaseModel
from django_summernote.fields import SummernoteTextField as RichTextField
from django.utils.translation import gettext as _
from django.contrib.auth.models import User
from apps.worldmap.models import BaseWorldMapModel
import uuid
import random
import string


def make_random_chars(length = 9):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))
    

class Preference(BaseModel):
    
    class EnableDisableChoice(models.TextChoices):
        ENABLED  = 'enabled', _('Enabled')
        DISABLED = 'disabled', _('Disabled')

    sister_api = models.CharField(_('Sister API'), max_length=15, choices=EnableDisableChoice.choices, default=EnableDisableChoice.ENABLED)
    sevima_api = models.CharField(_('Sevima API'), max_length=15, choices=EnableDisableChoice.choices, default=EnableDisableChoice.ENABLED)
            
    class Meta:
        verbose_name = _('Preference')
        verbose_name_plural = _('Preference')
        
    def __str__(self):
        return self.sister_api

    
    
class ScholarshipAttachment(BaseModel):

    class ScholarshipAttachmentType(models.TextChoices):
        PDF = 'pdf', _('PDF')
        IMAGE = 'image', _('Image (JPG, PNG, JPEG)')
        BOTH = 'both', _('PDF and Image')
    
    name = models.CharField(_('Name'), max_length=255)
    description = RichTextField(_('Description'), help_text=_('Brief description of the scholarship'), null=True, blank=True)
    types = models.CharField(_('Types'), choices=ScholarshipAttachmentType.choices, default=ScholarshipAttachmentType.BOTH, max_length=30)
    max_size = models.IntegerField(_('Max Size (Kb)'), default=1000)
    
    class Meta:
        verbose_name = _('Scholarship Attachment')
        verbose_name_plural = _('Scholarship Attachments')
        
    def __str__(self):
        return self.name



class ScholarshipTarget(BaseModel):
    slug = models.SlugField(_('Slug'), max_length=21, unique=True)
    name = models.CharField(_('Name'), max_length=255)
    
    class Meta:
        verbose_name = _('Scholarship Status')
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return self.name
    
        
        
class Scholarship(BaseModel):

    class ScholarshipStatus(models.TextChoices):
        ONGOING = 'on-going', _('On Going')
        COMING_SOON = 'coming-soon', _('Coming Soon')
        CLOSED = 'closed', _('Closed')

    class ScholarshipSource(models.TextChoices):
        INTERNAL = 'internal', _('Internal')
        EXTERNAL = 'external', _('External')

    class ScholarshipDest(models.TextChoices):
        INTERNAL = 'internal', _('Internal')
        EXTERNAL = 'external', _('External')


    name = models.CharField(_('Name'), max_length=255)
    description = RichTextField(_('Description'), help_text=_('Brief description of the scholarship'), null=True, blank=True)
    requirement = RichTextField(_('Requirement'), help_text=_('Requirement for proposing the scholarship'), null=True, blank=True)
    attachments = models.ManyToManyField('ScholarshipAttachment', through='ScholarshipAttachmentRequirement', related_name='attachments', verbose_name=_('Attachments'))
    status = models.CharField(
        verbose_name=_('Scholarship Status'),
        max_length=30,
        choices=ScholarshipStatus.choices,
        default=ScholarshipStatus.COMING_SOON,
    )
    source = models.CharField(
        verbose_name=_('Scholarship Source'), max_length=30,
        choices=ScholarshipSource.choices,
        default=ScholarshipSource.INTERNAL,
        help_text=_('Whether the scholarship is internal or external')
    )
    destination = models.CharField(
        verbose_name=_('Scholarship Destination'), max_length=30,
        choices=ScholarshipDest.choices,
        default=ScholarshipDest.INTERNAL,
        help_text=_('Destination of scholarship funds')
    )
    start_date = models.DateTimeField(_('Start Date'))
    end_date = models.DateTimeField(_('End Date'))
    quota = models.PositiveIntegerField(_('Quota'), help_text=_('Number of recipients available'))
    faculties = models.ManyToManyField('Faculty', blank=True, related_name='scholarships', verbose_name=_('Faculties'))
    departments = models.ManyToManyField('Department', blank=True, related_name='scholarships', verbose_name=_('Departments'))
    targets = models.ManyToManyField('ScholarshipTarget', blank=True, related_name='scholarships', verbose_name=_('Targets'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Scholarship'
        verbose_name_plural = 'Scholarships'
        ordering = ['start_date']


class ScholarshipAttachmentRequirement(BaseModel):
    scholarship = models.ForeignKey('Scholarship', on_delete=models.CASCADE, related_name='attachment_requirements', verbose_name=_('Scholarship'))
    attachment = models.ForeignKey('ScholarshipAttachment', on_delete=models.CASCADE, related_name='scholarship_requirements', verbose_name=_('Attachment'))
    is_required = models.BooleanField(_('Is Required'), default=False)
    
    class Meta:
        verbose_name = _('Scholarship Attachment Requirement')
        verbose_name_plural = _('Scholarship Attachment Requirements')

    def __str__(self):
        return f"{self.attachment.name} for {self.scholarship.name} ({'Required' if self.is_required else 'Optional'})"



class Unit(BaseModel):
    id_unit = models.UUIDField(default=uuid.uuid4, editable=False, null=True, blank=True)
    code = models.CharField(_('Code'), max_length=16, unique=True)
    name = models.CharField(_('Name'), max_length=256)
    shortname = models.CharField(_('Shortname'), max_length=32)
    parent = models.ForeignKey('self', verbose_name=_("Parent"),
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='children'
    )
    date_created = models.DateTimeField(_("Date Created"), auto_now_add = True)

    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.name} ({self.code})"



class University(BaseModel):
    unit = models.ForeignKey(Unit, on_delete = models.PROTECT)
    english_name = models.CharField(_("University Name (English)"), max_length = 256, null = True, blank = True)
    date_establish = models.DateField(null = True, blank = True)
    legality_number = models.CharField(max_length = 32, null = True, blank = True)
    date_legality = models.DateField(null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    address = models.CharField(_("Address"), max_length = 256, null = True, blank = True)
    website = models.URLField(null = True, blank = True)
    description = RichTextField(null = True, blank = True)

    class Meta:
        verbose_name = _('University')
        verbose_name_plural = _('Universities')

    def __str__(self):
        return self.unit.name


class Office(BaseModel):
    unit = models.ForeignKey(Unit, on_delete = models.PROTECT)
    english_name = models.CharField(_("Office Name (English)"), max_length = 256, null = True, blank = True)
    date_establish = models.DateField(null = True, blank = True)
    legality_number = models.CharField(max_length = 32, null = True, blank = True)
    date_legality = models.DateField(null = True, blank = True)
    website = models.URLField(null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    address = models.CharField(_("Address"), max_length = 256, null = True, blank = True)
    description = RichTextField(null = True, blank = True)

    class Meta:
        verbose_name = _('Office')

    def __str__(self):
        return self.unit.name



class Faculty(BaseModel):
    unit = models.ForeignKey(Unit, on_delete = models.PROTECT)
    english_name = models.CharField(_("Faculty Name (English)"), max_length = 256, null = True, blank = True)
    date_establish = models.DateField(null = True, blank = True)
    legality_number = models.CharField(max_length = 32, null = True, blank = True)
    date_legality = models.DateField(null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    address = models.CharField(_("Address"), max_length = 256, null = True, blank = True)
    website = models.URLField(null = True, blank = True)
    description = RichTextField(null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = _('Faculty')
        verbose_name_plural = _('Faculties')

    def __str__(self):
        return "{0}".format(self.unit.name)



class Department(BaseModel):
    class GradeLevel(models.TextChoices):
        SMA = "6", "SMA / sederajat"
        D1 = "20", "D1"
        D2 = "21", "D2"
        D3 = "22", "D3"
        D4 = "23", "D4"
        S1 = "30", "S1"
        PROFESI = "31", "Profesi"
        SP1 = "32", "Sp-1"
        S2 = "35", "S2"
        S2_TERAPAN = "36", "S2 Terapan"
        SP2 = "37", "Sp-2"
        S3 = "40", "S3"
        S3_TERAPAN = "41", "S3 Terapan"

    unit = models.ForeignKey(Unit, on_delete = models.PROTECT)
    english_name = models.CharField(_("Department Name (English)"), max_length = 256, null = True, blank = True)
    date_establish = models.DateField(null = True, blank = True)
    legality_number = models.CharField(max_length = 32, null = True, blank = True)
    date_legality = models.DateField(null = True, blank = True)
    website = models.URLField(null = True, blank = True)
    email = models.EmailField(null = True, blank = True)
    address = models.CharField(_("Address"), max_length = 256, null = True, blank = True)
    grade = models.CharField(max_length = 32, choices = GradeLevel.choices, default = GradeLevel.S1)
    description = RichTextField(null = True, blank = True)
    date_created = models.DateTimeField(auto_now_add = True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return f"{self.get_grade_display()} - {self.unit.name}"


class Student(BaseModel, BaseWorldMapModel):

    class DataSource(models.TextChoices):
       SEVIMA = 'sevima', _('Sevima')
       SISTER = 'sister', _('Sister')
       MANUAL = 'manual', _('Manual')

    class StudentStatus(models.TextChoices):
        AKTIF = 'A', 'Aktif'
        BELUM_YUDISIUM = 'BY', 'Belum Yudisium'
        CUTI = 'C', 'Cuti'
        DROP_OUT = 'D', 'Drop Out / Dikeluarkan'
        DOUBLE_DEGREE = 'G', 'Sedang Double Degree'
        HILANG = 'H', 'Menghilang / Tanpa Kabar'
        MENGUNDURKAN_DIRI = 'K', 'Mengundurkan Diri / Keluar'
        KAMPUS_MERDEKA = 'KM', 'Kampus Merdeka'
        LULUS = 'L', 'Lulus'
        LAINNYA = 'LL', 'Lainnya'
        NON_AKTIF = 'N', 'Non Aktif'
        PUTUS_STUDI = 'P', 'Putus Studi'
        PASSING_OUT = 'PO', 'Gugur Studi / Passing Out'
        TRANSFER = 'T', 'Transfer / Pindah'
        MENUNGGU_UKOM = 'U', 'Menunggu Ukom'
        WAFAT = 'W', 'Wafat'

    class Religion(models.TextChoices):
        ISLAM = '1', 'Islam'
        KRISTEN = '2', 'Kristen'
        KHATOLIK = '3', 'Khatolik'
        HINDU = '4', 'Hindu'
        BUDHA = '5', 'Budha'
        KONGHUCU = '6', 'Konghucu'
        LAIN_LAIN = '7', 'Lain-lain'
    
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(_("Name"), max_length = 64)
    student_id = models.CharField(_("Student ID"), max_length = 12)
    department = models.ForeignKey(Department, verbose_name=_("Department"), on_delete = models.PROTECT)
    sex = models.CharField(_("Sex"), choices = [('L', _('Male')), ('P', _('Female'))], max_length = 11, null = True, blank = True)
    status = models.CharField(_("Status"), choices = StudentStatus.choices, default=StudentStatus.AKTIF, max_length = 11)
    source = models.CharField(_("Source"), choices = DataSource.choices, default=DataSource.SEVIMA, max_length = 11)
    religion = models.CharField(_("Religion"), max_length = 3, choices= Religion.choices, default = Religion.ISLAM)
    place_birth = models.CharField(_("Place of Birth"), max_length = 64)
    date_birth = models.DateField(_("Date of Birth"))
    address = models.TextField(_("Address"), help_text = _("Write complete address"), null = True, blank = True)
    postal_code = models.CharField(_("Postal code"), max_length = 8, null = True, blank = True)
    university_email = models.EmailField(_("University E-mail"), blank = True, null = True)
    mobile_number = models.CharField(_("Mobile Number"), max_length = 17,
        help_text = _("Number must be always active"), null = True, blank = True)

    class Meta:
        verbose_name = _('Student')
        verbose_name_plural = _('Students')
        ordering = ['name']

    def __str__(self):
        return self.name
    
    
    
class ScholarshipApplication(BaseModel):
    
    class ApplicationStatus(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        ACCEPTED = 'ACCEPTED', 'Accepted'
        REJECTED = 'REJECTED', 'Rejected'
        
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications', verbose_name=_('Student'))
    scholarship = models.ForeignKey(Scholarship, on_delete=models.CASCADE, related_name='applications', verbose_name=_('Scholarship'))
    application_date = models.DateField(_('Application Date'), auto_now_add=True)
    note = RichTextField(_('Note'), null = True, blank = True)
    status = models.CharField(_('Application Status'), max_length=20, choices=ApplicationStatus.choices, default=ApplicationStatus.PENDING)
   
    class Meta:
        verbose_name = _('Scholarship Application')
        verbose_name_plural = _('Scholarship Applications')

    def __str__(self):
        return f'{self.student.user.get_full_name()} - {self.scholarship.name}'



class Reviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='as_reviewer')
    expertise = models.CharField(_('Expertise'), max_length=255, null=True, blank=True)
    bio = models.TextField(_('Bio'), null=True, blank=True)
    active = models.BooleanField(_('Active'), default=True) 

    class Meta:
        verbose_name = _('Reviewer')
        verbose_name_plural = _('Reviewers')

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - Reviewer"
    
    

class ApplicationReview(BaseModel):
    application = models.ForeignKey(ScholarshipApplication, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Reviewer, on_delete=models.SET_NULL, null=True, blank=True)
    recommended_status = models.CharField(_('Recommended Status'), max_length=20, choices=ScholarshipApplication.ApplicationStatus.choices, null=True, blank=True)
    review_comment = models.TextField(_('Review Comment'), null=True, blank=True)
    
    class Meta:
        verbose_name = _('Application Review')
        verbose_name_plural = _('Application Reviews')
    
    def __str__(self):
        return f"Review by {self.reviewer} for {self.application.scholarship}"



class ScholarshipApplicationAttachment(models.Model):
    application = models.ForeignKey('ScholarshipApplication', on_delete=models.CASCADE, related_name='attachments', verbose_name=_('Scholarship Application'))
    attachment = models.ForeignKey('ScholarshipAttachment', on_delete=models.CASCADE, related_name='application_attachments', verbose_name=_('Attachment Type'))
    file = models.FileField(_('File'), upload_to='scholarship_applications/files/', blank=True, null=True)
    url = models.URLField(_('URL'), max_length=512, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    class Meta:
        verbose_name = _('Application Attachment')
        verbose_name_plural = _('Application Attachments')

    def __str__(self):
        return f"{self.application} - {self.attachment.name}"
