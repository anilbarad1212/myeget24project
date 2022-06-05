from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13)


class CustomerAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=30, default='anilbarad9@gmail.com')
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    landmark = models.CharField(max_length=500)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=13)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.user }  -  {self.city}  -  {self.pincode} '


class All_Brands(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_photo = models.ImageField(upload_to='brandimg')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand_name}'


class All_Mobiles(models.Model):
    all_brands = models.ForeignKey(All_Brands, on_delete=models.CASCADE)
    mobile_name = models.CharField(max_length=200)
    release_date = models.CharField(max_length=50)
    display_size = models.CharField(max_length=50)
    mobile_photo = models.ImageField(upload_to='mobileimg')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.all_brands}  -  {self.mobile_name}'


CATEGORY_CHOICES = (
    ('BCK-PNEL-CVR', 'BACK-PANEL-COVER'),
    ('BTR-CNCTR', 'BETTRY-CONNECTOR'),
    ('BTR', 'BETTRY'),
    ('CMR-LNS', 'CAMERA-LENSE-BLACK'),
    ('CHRG-CNTR', 'CHARGING-CONNECTOR'),
    ('CHRG-PCB', 'CHARGING-PCB'),
    ('EAR-SPK', 'EAR-SPEAKER'),
    ('FNGP-SN-FLX-CB', 'FINGERPRINT-SENSOR-FLEX-CABLE'),
    ('FNGP-SN-BTN-PLST', 'FINGERPRINT-SENSOR-BUTTON-PLASTIC'),
    ('FLBD-HOU', 'FULLBODY-HOUSING'),
    ('HNDFR-JK', 'HANDSFREE-JACK'),
    ('LCD-CONT', 'LCD-CONNECTOR'),
    ('LCD-FLX', 'LCD-FLEX'),
    ('LCD-FRM-MDL-CH', 'LCD-FRAME-MIDDLE-CHASSIS'),
    ('LUD-SPK-RIG', 'LOUD-SPEAKER-RINGER'),
    ('MN-BD-FLX-CB', 'MAIN-BOARD-FLEX-CABLE'),
    ('MC-CONT', 'MMC-CONNECTOR'),
    ('PWR-BTN-FLX-CB', 'POWER-BUTTON-FLEX-CABLE'),
    ('VLM-BTN-FLX-CB', 'VOLUME-BUTTON-FLEX-CABLE'),
    ('PWR-BTN-OTR-PLS', 'POWER-BUTTON-OUTER-PLASTIC'),
    ('BK-CMR', 'BACK-CAMERA'),
    ('FRT-CMR-SLF', 'FRONT-CAMERA-SELFIE'),
    ('FRT-MN-GLS', 'FRONT-MAIN-GLASS'),
    ('FRT-MN-TC', 'FRONT-MAIN-TOUCH'),
    ('SIM-HLD-TRY', 'SIMCARD-HOLDER-TRAY'),
    ('SIM-CONT', 'SIM-CONNECTOR'),
    ('SPKR-JL', 'SPEAKER-JAALI'),
    ('VBR', 'VIBRATOR'),
    ('VLM-BTN-PLS', 'VOLUME-BUTTON-PLASTIC'),
    ('ANTN-NET-WR', 'ANTENA-NETWORK-WIRE'),
    ('FLP-CVR', 'FLIP-COVER'),
)
SUB_CATEGORY_CHOICES = (('NA', 'NEWLY-ARRIVAL'), ('TP', 'TRENDING-PRODUCTS'))

AVAILABILITY = (('IN-STK', 'ITEM-IN-STOCK'), ('OUT-OF-STK',
                                              'ITEM-OUT-OF-STOCK'))


class All_Accesories(models.Model):
    all_mobiles = models.ForeignKey(All_Mobiles, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES,
                                max_length=20,
                                blank=True)
    sub_category = models.CharField(choices=SUB_CATEGORY_CHOICES,
                                    max_length=20,
                                    blank=True)
    color = models.CharField(max_length=100, blank=True)
    availability = models.CharField(choices=AVAILABILITY, max_length=20)
    accesories_photo = models.ImageField(upload_to='accesoriesimg')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.all_mobiles} - {self.title} - {self.color}'


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    all_accesories = models.ForeignKey(All_Accesories,
                                       on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.user} - {self.all_accesories} - {self.quantity} '

    @property
    def total_cost(self):
        return self.quantity * self.all_accesories.price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    order_number = models.CharField(max_length=5, null=True)
    payment_status = models.CharField(max_length=15, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    customer_address = models.ForeignKey(CustomerAddress,
                                         on_delete=models.CASCADE)
    all_accesories = models.ForeignKey(All_Accesories,
                                       on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total_price = models.FloatField(default=0)
    expected_delivery_date = models.CharField(max_length=20)
    message = models.TextField(null=True)
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='Accepted')
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} - {self.user} - {self.customer_address} - {self.all_accesories} - \
        {self.quantity} - {self.ordered_date} - {self.status}'


class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=5, null=True)
    email = models.EmailField(max_length=15, default='anilbarad9@gmail.com')
    total_price = models.FloatField(default=0)
