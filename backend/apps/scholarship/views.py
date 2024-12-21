from datetime import datetime
from apps.scholarship.models import Department, Student, make_random_chars
from apps.scholarship.models import Student
from django.contrib.auth.models import User


def create_or_get_student_user(student_sevima):
    username = student_sevima.get('nim_mhs')
    email    = student_sevima.get('email', '')                
    fullname = student_sevima.get('nama_mhs', '')
    password = make_random_chars()
    user, created = User.objects.get_or_create(
        username = username,
        defaults = {
            'email': email,
            'first_name': fullname.split(' ')[0],
            'last_name': ' '.join(fullname.split(' ')[1:]),
            'password': password
        }
    )
    return user


def create_or_update_student(student_sevima):
    user = create_or_get_student_user(student_sevima)

    try:
        department = Department.objects.get(unit__code = student_sevima.get('units', ''))
    except Department.DoesNotExist:
        department = None
    
    student, created = Student.objects.update_or_create(
        user = user,
        defaults = {
            'name': student_sevima.get('nama_mhs'),
            'student_id': student_sevima.get('nim_mhs'),
            'sex': student_sevima.get('jenis_kelamin'),
            'status': student_sevima.get('status', Student.StudentStatus.AKTIF),
            'source': student_sevima.get('source', Student.DataSource.SEVIMA),
            'place_birth': student_sevima.get('tempat_lahir', ''),
            'date_birth': datetime.strptime(student_sevima.get('tanggal_lahir'), "%Y-%m-%d").date(),
            'address': student_sevima.get('alamat'),
            'postal_code': student_sevima.get('kodepos'),
            'mobile_number': student_sevima.get('hp'),
            'department': department,
        }
    )            
    return (student, created)
