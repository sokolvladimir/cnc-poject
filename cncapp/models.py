from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse


class CncProg(models.Model):
    MATERIAL_LIST = (
        ('plastic', 'Plastic Material'),
        ('plexiglas', 'Plexiglas Material'),
        ('wood', 'Wood Material'),
        ('non-ferrous metal', 'Non-ferrous Metal Material'),
        ('aluminium', 'Aluminium Material'),
        ('magnesium', 'Magnesium Material'),
        ('steel', 'Steel Material'),
        ('cast iron', 'Cast Iron Material'),
        ('titanium', 'Titanium Material'),)
    TEETH_NUM = ((1, 'one'),
                 (2, 'two'),
                 (3, 'three'),
                 (4, 'four'),
                 (5, 'five'),
                 (6, 'six'),)
    DIAMETR = tuple((x / 10, str(x/10)) for x in range(3, 101, 1))
    # Данные которые мы должны запашивать у пользователя
    material = models.CharField(max_length=20, choices=MATERIAL_LIST, default='plastic')
    teeth_numbers = models.IntegerField(choices=TEETH_NUM, default='one')
    cutter_diameter = models.FloatField(choices=DIAMETR, default='2.0')
    # Данные из таблицы
    cut_speed_min = models.IntegerField()
    cut_speed_max = models.IntegerField()
    feed_per_tooth = models.FloatField()
    # Данные которые мы вычисляем по формулам
    spindel_speed_min = models.IntegerField()
    spindel_speed_max = models.IntegerField()
    moving_speed_min = models.IntegerField()
    moving_speed_max = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    birthday = models.DateTimeField(null=True, blank=True)
    photo = models.ImageField(upload_to='user/%Y/%m/%d/', blank=True)

    def __str__(self):
        return self.user


class MyCutter(models.Model):
    MATERIAL_LIST = (
        ('Plastic', 'Plastic Material'),
        ('Plexiglas', 'Plexiglas Material'),
        ('Wood', 'Wood Material'),
        ('Non-ferrous metal', 'Non-ferrous Metal Material'),
        ('Aluminium', 'Aluminium Material'),
        ('Magnesium', 'Magnesium Material'),
        ('Steel', 'Steel Material'),
        ('Cast iron', 'Cast Iron Material'),
        ('Titanium', 'Titanium Material'),)
    TEETH_NUM = ((1, 'one'),
                 (2, 'two'),
                 (3, 'three'),
                 (4, 'four'),
                 (5, 'five'),
                 (6, 'six'),)
    DIAMETR = tuple((x / 10, str(x/10)) for x in range(3, 101, 1))

    material = models.CharField(max_length=20, choices=MATERIAL_LIST, default='plastic')
    teeth_numbers = models.IntegerField(choices=TEETH_NUM, default='one')
    cutter_diameter = models.FloatField(choices=DIAMETR, default='2.0')

    spindel_speed = models.IntegerField()
    moving_speed = models.IntegerField()


class InformationCategory(models.Model):
    name = models.CharField(max_length=50, db_index=True)
    slug = models.SlugField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cncapp:category_details',
                       args=[self.slug, ])


class Information(models.Model):

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    note = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey('InformationCategory', on_delete=models.PROTECT, null=True)
    photo = models.ImageField(upload_to='cutters/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cncapp:information_details',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    material = models.ForeignKey(Information,
                                 on_delete=models.CASCADE,
                                 related_name='comment')
    name = models.CharField(max_length=100)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
