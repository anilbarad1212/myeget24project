import numbers
from django.db import models
import random
from mobiles.models import CustomUser


# Create your models here.
class Code(models.Model):
    otp = models.CharField(max_length=5, blank=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.otp} - {self.user} - {self.date_added}'

    def save(self, *args, **kwargs):
        number_list = [x for x in range(10)]
        code_items = []

        for i in range(5):
            num = random.choice(number_list)
            code_items.append(num)
        code_string = "".join(str(item) for item in code_items)
        self.otp = code_string
        super().save(*args, **kwargs)
