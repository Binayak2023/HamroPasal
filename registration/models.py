from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

DISTRICT_CHOICES = (
    ('Achham', 'Achham'), 
    ('Arghakhanchi', 'Arghakhanchi'), 
    ('Baglung', 'Baglung'), 
    ('Baitadi', 'Baitadi'), 
    ('Bajhang', 'Bajhang'), 
    ('Bajura', 'Bajura'), 
    ('Banke', 'Banke'), 
    ('Bara', 'Bara'), 
    ('Bardiya', 'Bardiya'), 
    ('Bhaktapur', 'Bhaktapur'), 
    ('Bhojpur', 'Bhojpur'), 
    ('Chitwan', 'Chitwan'), 
    ('Dadeldhura', 'Dadeldhura'), 
    ('Dailekh', 'Dailekh'), 
    ('Dang', 'Dang'), 
    ('Darchula', 'Darchula'), 
    ('Dhading', 'Dhading'), 
    ('Dhankuta', 'Dhankuta'), 
    ('Dhanusa', 'Dhanusa'), 
    ('Dolakha', 'Dolakha'), 
    ('Dolpa', 'Dolpa'), 
    ('Doti', 'Doti'), 
    ('Gorkhak', 'Gorkha'), 
    ('Gulmi', 'Gulmi'), 
    ('Humla', 'Humla'), 
    ('Ilam', 'Ilam'), 
    ('Jajarkot', 'Jajarkot'), 
    ('Jhapa', 'Jhapa'), 
    ('Jumla', 'Jumla'), 
    ('Kailali', 'Kailali'), 
    ('Kalikot', 'Kalikot'), 
    ('Kanchanpur', 'Kanchanpur'), 
    ('Kapilvastu', 'Kapilvastu'), 
    ('Kaski', 'Kaski'), 
    ('Kathmandu', 'Kathmandu'), 
    ('Kavrepalanchok', 'Kavrepalanchok'), 
    ('Khotang', 'Khotang'), 
    ('Lalitpur', 'Lalitpur'), 
    ('Lamjung', 'Lamjung'), 
    ('Mahottari', 'Mahottari'), 
    ('Makawanpur', 'Makawanpur'), 
    ('Manang', 'Manang'), 
    ('Morang', 'Morang'), 
    ('Mugu', 'Mugu'), 
    ('Mustang', 'Mustang'), 
    ('Myagdi', 'Myagdi'), 
    ('Nawalpur', 'Nawalpur'), 
    ('Nuwakot', 'Nuwakot'), 
    ('Okhaldhunga', 'Okhaldhunga'), 
    ('Palpa', 'Palpa'), 
    ('Panchthar', 'Panchthar'), 
    ('Parasi', 'Parasi'), 
    ('Parbat', 'Parbat'), 
    ('Parsa', 'Parsa'), 
    ('Pyuthan', 'Pyuthan'), 
    ('Ramechhap', 'Ramechhap'), 
    ('Rasuwa', 'Rasuwa'), 
    ('Rautahat', 'Rautahat'), 
    ('Rolpa', 'Rolpa'), 
    ('Rukum', 'Rukum'), 
    ('Rukum Paschim', 'Rukum Paschim'), 
    ('Rupandehi', 'Rupandehi'), 
    ('Salyan', 'Salyan'), 
    ('Sankhuwasabha', 'Sankhuwasabha'), 
    ('Saptari', 'Saptari'), 
    ('Sarlahi', 'Sarlahi'), 
    ('Sindhuli', 'Sindhuli'), 
    ('Sindhupalchok', 'Sindhupalchok'), 
    ('Siraha', 'Siraha'), 
    ('Solukhumbu', 'Solukhumbu'), 
    ('Sunsari', 'Sunsari'), 
    ('Surkhet', 'Surkhet'), 
    ('Syangja', 'Syangja'), 
    ('Tanahu', 'Tanahu'), 
    ('Taplejung', 'Taplejung'), 
    ('Terhathum', 'Terhathum'), 
    ('Udayapur', 'Udayapur'),
    )

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer', null=False, blank=False)
    full_name = models.CharField(max_length=100)
    district = models.CharField(choices=DISTRICT_CHOICES, max_length=100, default='Kathmandu')
    address = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    phone_no = models.PositiveBigIntegerField()
    house_no = models.PositiveIntegerField(blank=True, null=True)
    zip_code = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name