from django.db import models
from django.contrib.auth.models import User
from registration.models import Customer
from math import floor
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_delete

# Create your models here.
class Category(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField()

    def __str__(self):
        return self.title

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title

FEATURED_CHOICES = (
    ('Featured', 'Featured'),
    ('Non-featured', 'Non-featured'),
)

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    # desc = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    featured = models.CharField(choices=FEATURED_CHOICES, max_length=100, default='Non-featured')
    weight = models.CharField(max_length=100)
    marked_price = models.FloatField()
    selling_price = models.FloatField()
    available_quantity = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='cosmeproducts/', default='')
    return_policy = models.CharField(max_length=255)
    slug = models.SlugField()
    tags = models.CharField(max_length=300)
    meta_keywords = models.CharField(max_length=255)
    meta_description = models.TextField()
    modified_date = models.DateField(auto_now=True)
    users_wishlist = models.ManyToManyField(User, blank=True, related_name='user_wishlist')

    def __str__(self):
        return self.name + '......'+self.weight

    @property
    def discount_percent(self):
        discount = (self.marked_price - self.selling_price)/self.marked_price
        discountper = floor(discount * 100)
        rounddiscount = 0
        if( discountper > 0 and discountper < 7.5 ):
            rounddiscount = 5
        elif(discountper >= 7.5 and discountper < 12.5):
            rounddiscount = 10
        elif(discountper >= 12.5 and discountper < 17.5):
            rounddiscount = 15
        elif(discountper >= 17.5 and discountper < 22.5):
            rounddiscount = 20
        elif(discountper >= 22.5 and discountper < 27.5):
            rounddiscount = 25
        elif(discountper >= 27.5 and discountper < 32.5):
            rounddiscount = 30
        elif(discount >= 32.5 and discountper < 37.5):
            rounddiscount = 35
        elif(discountper >= 37.5 and discountper < 42.5):
            rounddiscount = 40
        elif(discountper >= 42.5 and discountper < 47.5):
            rounddiscount = 45
        elif(discountper >= 47.5 and discountper < 52.5):
            rounddiscount = 50
        elif(discountper >= 52.5 and discountper < 57.5):
            rounddiscount = 55
        elif(discountper >= 57.5 and discountper < 62.5):
            rounddiscount = 60
        elif(discountper >= 62.5 and discountper < 67.5):
            rounddiscount = 65
        elif(discountper >= 67.5 and discountper < 72.5):
            rounddiscount = 70
        elif(discountper >= 72.5 and discountper < 77.5):
            rounddiscount = 75
        elif(discountper >= 77.5 and discountper < 82.5):
            rounddiscount = 80
        elif(discountper >= 82.5 and discountper < 87.5):
            rounddiscount = 85
        elif(discountper >= 87.5 and discountper < 92.5):
            rounddiscount = 90
        elif(discountper >= 92.5 and discountper < 97.5):
            rounddiscount = 95
        return str(rounddiscount)

@receiver(post_delete, sender=Product)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.photo.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=Product)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).photo.path
        try:
            new_img = instance.photo.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

class MyCart(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    @property
    def sub_total(self):
        return str(self.quantity * self.product.selling_price)

STATUS_CHOICES = (
    ('pending', 'pending'),
    ('received', 'received'),
    ('packed', 'packed'),
    ('on_the_way', 'on_the_way'),
    ('delivered', 'delivered'),
    ('cancel', 'cancel'),
)

class OrderPlaced(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.PositiveBigIntegerField(default=0)
    unique_order_id = models.CharField(max_length=300, default='')
    delivery_charge = models.PositiveIntegerField(default=100)
    promo_discount = models.PositiveIntegerField(default=0)
    total_cost = models.PositiveBigIntegerField(default=0)
    ordered_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    ##--------------For Payment Integration--------------##
    #Payment_Method_Choices_Char_Field
    #Payment_Completed_Boolean_Field

    def __str__(self):
        return str(self.user.username + '----' + self.customer.full_name + '----' + self.product.name)

class Contact(models.Model):
    sno = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=10)
    preference = models.CharField(max_length=100, default="Phone")
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.message[0:15] + '...' + '    By   ' + self.full_name)

class SubscriptionEmail(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=100)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id) + '.....' + self.email
        

class SlideContent(models.Model):
    id = models.AutoField(primary_key=True)
    small_title = models.CharField(max_length=200)
    main_title = models.CharField(max_length=80)
    third_title = models.CharField(max_length=255)
    button_text = models.CharField(max_length=25)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='slides/', default='')
    link_to = models.URLField(max_length=300, default='')

    def __str__(self):
        return self.main_title

@receiver(post_delete, sender=SlideContent)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.photo.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=SlideContent)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).photo.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

class BannerContent(models.Model):
    id = models.AutoField(primary_key=True)
    small_title = models.CharField(max_length=200)
    main_title = models.CharField(max_length=80)
    third_title = models.CharField(max_length=255)
    button_text = models.CharField(max_length=25)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='banners/', default='')
    link_to = models.URLField(max_length=300, default='')

    def __str__(self):
        return self.main_title

@receiver(post_delete, sender=BannerContent)
def post_save_image(sender, instance, *args, **kwargs):
    """ Clean Old Image file """
    try:
        instance.photo.delete(save=False)
    except:
        pass

@receiver(pre_save, sender=BannerContent)
def pre_save_image(sender, instance, *args, **kwargs):
    """ instance old image file will delete from os """
    try:
        old_img = instance.__class__.objects.get(id=instance.id).photo.path
        try:
            new_img = instance.image.path
        except:
            new_img = None
        if new_img != old_img:
            import os
            if os.path.exists(old_img):
                os.remove(old_img)
    except:
        pass

class PromoCodeDiscount(models.Model):
    id = models.AutoField(primary_key=True)
    discount_price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.discount_price)

class PromoCode(models.Model):
    id = models.AutoField(primary_key=True)
    promo_code_text = models.CharField(max_length=100)
    promo_code_discount = models.ForeignKey(PromoCodeDiscount, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.promo_code_text + '....' + str(self.promo_code_discount.discount_price)