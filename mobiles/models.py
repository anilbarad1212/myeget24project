import email
from gzip import READ
from click import Choice
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=13)


class CustomerAddress(models.Model):
    order_number = models.CharField(max_length=20, blank=True)
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
        return f'{self.id} - {self.order_number }  -  {self.user}  -  {self.email} - {self.address1} - {self.address2} - \
            {self.landmark} - {self.city} - {self.state} - {self.pincode} - {self.mobile_number} - {self.date_added} '


class All_Brands(models.Model):
    brand_name = models.CharField(max_length=200)
    brand_photo = models.ImageField(upload_to='brandimg')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.brand_name} -{self.brand_photo}'


class All_Mobiles(models.Model):
    all_brands = models.ForeignKey(All_Brands, on_delete=models.CASCADE)
    mobile_name = models.CharField(max_length=200)
    release_date = models.CharField(max_length=50)
    display_size = models.CharField(max_length=50)
    mobile_photo = models.ImageField(upload_to='mobileimg')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.all_brands}  -  {self.mobile_name} - {self.mobile_photo}'


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
        return f'{self.all_mobiles} - {self.title} - {self.price} -{self.description} - {self.category} - {self.sub_category} - {self.color} -\
            {self.availability}- {self.accesories_photo}'


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    all_accesories = models.ForeignKey(All_Accesories,
                                       on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.id} - {self.user} - {self.all_accesories} - {self.quantity} - {self.date_added} '

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
    order_number = models.CharField(max_length=20, blank=True)
    payment_status = models.CharField(max_length=15, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    customer_address = models.ForeignKey(CustomerAddress,
                                         on_delete=models.CASCADE)
    all_accesories = models.ForeignKey(All_Accesories,
                                       on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total_price = models.FloatField(default=0)
    expected_delivery_date = models.CharField(max_length=25)
    message = models.TextField(blank=True, default='hello')
    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='Accepted')
    ordered_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.id} -{self.payment_status} - {self.user} - {self.customer_address} - {self.all_accesories} - \
        {self.quantity} - {self.item_total_price} - {self.expected_delivery_date} - {self.message} - {self.status} - {self.ordered_date}'


RETURN_STATUS = (('Processing', 'Processing'), ('Accepted', 'Accepted'),
                 ('Return-Success', 'Return-Success'), ('Cancelled',
                                                        'Cancelled'))


class Return_Order(models.Model):
    order_placed = models.ForeignKey(OrderPlaced, on_delete=models.CASCADE)
    product_return_number = models.CharField(max_length=20, blank=True)
    return_request_message = models.CharField(max_length=45)
    return_status = models.CharField(choices=RETURN_STATUS,
                                     max_length=20,
                                     default='Processing')
    return_request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.order_placed} - {self.product_return_number} - {self.return_request_message} - {self.return_status} - {self.return_request_date}'


class Payment(models.Model):
    order_number = models.CharField(max_length=5, blank=True)
    payment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(max_length=15, default='anilbarad9@gmail.com')
    total_price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.payment_id} - {self.order_number} - {self.user} - {self.email} - {self.total_price}'


class Paytm_Post_Data(models.Model):
    order_number = models.CharField(max_length=20, blank=True)
    marchent_id = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=50, blank=True)
    transaction_amount = models.CharField(max_length=20, blank=True)
    payment_mode = models.CharField(max_length=20, blank=True)
    currency = models.CharField(max_length=20, blank=True)
    transaction_date = models.CharField(max_length=20, blank=True)
    transaction_status = models.CharField(max_length=20, blank=True)
    response_code = models.CharField(max_length=20, blank=True)
    response_message = models.CharField(max_length=20, blank=True)
    gateway_name = models.CharField(max_length=20, blank=True)
    bank_transaction_id = models.CharField(max_length=30, blank=True)
    bank_name = models.CharField(max_length=20, blank=True)
    checksum_hash = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f'{self.id} - {self.order_number} - {self.marchent_id} - {self.transaction_id} - {self.transaction_amount} - \
        {self.payment_mode} - {self.currency} - {self.transaction_date} - {self.transaction_status} - {self.response_code} - {self.response_message} \
        {self.gateway_name} - {self.bank_transaction_id} - {self.bank_name} - {self.checksum_hash}      '