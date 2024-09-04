from django.db import models
from django.contrib.auth.models import User,auth
# Create your models here.

class Userdetails(User):
    user=models.OneToOneField(User,parent_link=True,primary_key=True,on_delete=models.CASCADE)
    address=models.CharField(max_length=1000)
    phone=models.IntegerField(default=0)
    image=models.ImageField(upload_to="gallery",null=True)
    def __str__(self):
        return self.user.username


class category(models.Model):
    name=models.CharField(max_length=100)
    price=models.IntegerField(default=0)
    slug=models.CharField(max_length=100,null=True,unique=True)
    image=models.ImageField(upload_to="gallery")
    offer=models.IntegerField(null=False,default=0)
    
    
    def __str__(self):
        return self.name
class video(models.Model):
    select_course=models.ForeignKey(category,on_delete=models.CASCADE)
    tittle=models.CharField(max_length=200)
    serial_num=models.IntegerField(null=False)
    video_id=models.FileField(null=True)

    def __str__(self):
        return str(self.serial_num)
class Test(models.Model):
    user=models.ForeignKey(Userdetails,on_delete=models.CASCADE)
    test=models.FileField(upload_to="file")
    test_name=models.CharField(max_length=200)
    
    def __str__(self) :
        return self.test_name
    
class Certificate(models.Model):
    user=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    certificate=models.ImageField(upload_to="gallery")
    def __str__(self):
        return self.user.username



class Usercourse(models.Model):
    user=models.ForeignKey(User,null=False,on_delete=models.CASCADE)
    select_course=models.ForeignKey(category,null=False,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username} - {self.select_course.name}'

class Payment(models.Model):
    order_id=models.CharField(max_length=100,null=False)        
    payment_id=models.CharField(max_length=100,null=True)
    user_course=models.ForeignKey(Usercourse,on_delete=models.CASCADE,null=True,blank=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    course=models.ForeignKey(category,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=False)        
class Testsoulution(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)        
    doc=models.FileField(upload_to="file")
    def __str__(self) -> str:
        return self.user.username + "--" + self.user.email