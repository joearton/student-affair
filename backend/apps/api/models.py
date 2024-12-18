from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class BaseModel(models.Model):
    """
    BaseModel dengan field date_created, date_modified, dan date_deleted.
    Field ini otomatis menangani waktu pembuatan, modifikasi, dan penghapusan logis.
    """
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True) 
    date_modified = models.DateTimeField(auto_now=True, null=True, blank=True)
    date_deleted = models.DateTimeField(null=True, blank=True, editable=False)
    
    class Meta:
        abstract = True  # Model ini tidak akan dibuat tabelnya di database

    def delete(self, using=None, keep_parents=False):
        """
        Override metode delete untuk mendukung soft delete.
        Mengisi field date_deleted alih-alih menghapus dari database.
        """
        self.date_deleted = now()
        self.save(update_fields=['date_deleted'])
        
        
    def restore(self):
        """
        Metode untuk mengembalikan objek yang telah dihapus (soft delete).
        """
        self.date_deleted = None
        self.save(update_fields=['date_deleted'])
        

    @property
    def is_deleted(self):
        """
        Properti untuk memeriksa apakah objek telah dihapus secara logis.
        """
        return self.date_deleted is not None
    


def user_str(self):
    user_str = f"{self.username}"
    fullname = f"{self.first_name} {self.last_name}"
    if len(fullname) > 1:
        user_str = f"{user_str} - {fullname}"
    return user_str


User.add_to_class('__str__', user_str)