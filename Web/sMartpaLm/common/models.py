from django.contrib.auth.models import PermissionsMixin, AbstractBaseUser, BaseUserManager, Group, Permission
from django.utils import timezone
from django.db import models
from django.apps import apps

class UserManager(BaseUserManager):
    """User 에서 사용하기 위한 UserManager 생성"""
    def create_user(self, email, password=None, **extra_fields):
        """일반 유저로 생성할 경우"""
        if not email:
            raise ValueError('이메일을 입력해주세요')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.username = email.split('@')[0]
        user.is_active = True
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """superuser 로 user 를 생성할 경우 필드값을 True 로 변경"""
        user = self.create_user(email, password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    """UserManager 를 objects 필드에 사용"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(null=True, default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(null=True, max_length=20, default="")
    last_name = models.CharField(null=True, max_length=20, default="")
    nick_name = models.CharField(null=True, max_length=45, default="")

    # alias = models.CharField(max_length=20, null=True)
    # profile_img = models.ImageField(upload_to='profile', null=True)
    # cover_img = models.ImageField(upload_to='cover', null=True)
    # introduce = models.TextField(max_length=255)

    # UserManager 을 재정의하여 사용
    objects = UserManager()
    # USERNAME 를 email 로 사용
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'auth_user'
        ordering = ('-date_joined',)
    def __str__(self):
        return self.email

    def get_name(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_superuser

class Farm(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=45, unique=True)
    start_date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=500, null=True)
    autocontrol_yn = models.BooleanField(null=True,default=False)
    use_yn = models.BooleanField(null=True, default=True)
    plant_id = models.BooleanField(null=True)

    class Meta:
        db_table = 'farm'
    def __str__(self):
        return self.name
class Crop(models.Model):
    # id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=45)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    nutrition = models.CharField(max_length=500, null=True)
    description = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'crop'
class FarmPlant(models.Model):
    # id = models.BigIntegerField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    plant = models.ManyToManyField('Crop')
    date_planted = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'farm_plant'

class Disease(models.Model):
    # id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=45)
    plant = models.ForeignKey(Crop, on_delete=models.CASCADE)
    img = models.CharField(max_length=100, null=True)
    symptom = models.CharField(max_length=200, null=True)
    action = models.CharField(max_length=500, null=True)

    class Meta:
        db_table = 'disease'

class Cure(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    action = models.CharField(max_length=500)
    syptom = models.CharField(max_length=500)

    class Meta:
        db_table = 'cure'

class SensoredData(models.Model):
    user_id = models.BigIntegerField(null=False, primary_key=True)
    farm_id = models.BigIntegerField(null=False, primary_key=True)
    sensor_date = models.DateTimeField(null=False, primary_key=True)
    sensor_cnt = models.BigIntegerField(null=False, primary_key=True)
    co2_density = models.FloatField(max_length=45, null=True)
    light_amount = models.FloatField(null=True)
    temperature = models.FloatField(null=True)
    humidity = models.FloatField(null=True)
    nutrition_amt = models.FloatField(null=True)
    status_img = models.CharField(max_length=200, null=True)
    predicted_status = models.CharField(max_length=500, null=True)
    class Meta:
        db_table = 'sensored_data'
    def __str__(self):
        return f"SensorData {self.sensor_date}"