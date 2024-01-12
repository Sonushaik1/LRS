from django.db import models
import json
import os

class Register(models.Model):
    name = models.CharField(max_length=50,null=True)
    email = models.EmailField()
    password = models.CharField(max_length=50 ,null=True)
    confirm_password=models.CharField(max_length=50 ,null=True)
    usertype = models.CharField(max_length=10 ,null=True )
    pno = models.CharField(max_length=255 ,null=True)
    addr = models.CharField(max_length=255 ,null=True)

    def __str__(self):
        return self.name + ' - ' + self.email


class Landdetails(models.Model):
    owner_name=models.CharField(max_length=50,null=True)
    owner_email=models.CharField(max_length=50,null=True)
    owner_number = models.CharField(max_length=255 ,null=True)
    land_area=models.IntegerField(default=0,null=True)
    address=models.CharField(max_length=20,null=True)
    landmark=models.CharField(max_length=200,null=True)
    cost_unit=models.PositiveIntegerField(null=True)
    photo = models.FileField(upload_to='static/images/', default='None')

    def __str__(self):
        return self.address + ' - ' + self.landmark

    @property
    def photo_name(self):
        return os.path.basename(self.photo.name)

    def toJson(self):
        return json.dumps({'name': self.owner_name,
            'land_area': self.land_area,
            'cost_unit': self.cost_unit,
            'image': self.photo_name}, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    


class LandRequest(models.Model):
    buyer = models.ForeignKey(Register, on_delete=models.CASCADE)
    land = models.ForeignKey(Landdetails, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField()
    total_land = models.PositiveIntegerField()
    status = models.CharField(max_length=10, null=True ,default='pending')

    def __str__(self):
        return self.buyer.name + ' - ' + self.land.owner_name
    

class LandRegistration(models.Model):
    land = models.ForeignKey(Landdetails, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=50, null=True)
    buyer_email = models.EmailField()
    buyer_number = models.CharField(max_length=255 ,null=True)
    seller = models.ForeignKey(Register, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField()
    total_land = models.PositiveIntegerField()
    pdf_name = models.CharField(max_length=255, null=True)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.buyer_name + ' - ' + self.seller.name
    
    def toJSON(self):
        return json.dumps({'land': self.land.toJson(),
            'buyer': self.buyer.name,
            'seller': self.seller.name,
            'total_amount': self.total_amount,
            'total_land': self.total_land,
            'date': self.date.strftime('%d/%m/%Y')}, default=lambda o: o.__dict__, sort_keys=True, indent=4)