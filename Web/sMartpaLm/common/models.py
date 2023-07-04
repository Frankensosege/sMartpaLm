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
    # id = models.BigIntegerField(unique=True, primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(null=True, default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(null=True, max_length=20, default="")
    last_name = models.CharField(null=True, max_length=20, default="")

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
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=45, unique=True)
    date_set = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'farms'
    def __str__(self):
        return self.name
class Plant(models.Model):
    # id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=45)

    class Meta:
        db_table = 'plant'
class FarmPlant(models.Model):
    # id = models.BigIntegerField(unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    plant = models.ManyToManyField('Plant')
    date_planted = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'farm_plant'

class Disease(models.Model):
    # id = models.BigIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=45)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    class Meta:
        db_table = 'disease'

class Cure(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE)
    cure = models.CharField(max_length=45)

    class Meta:
        db_table = 'cure'

class SensorData(models.Model):
    # farmpalnt = models.ForeignKey(FarmPlant, on_delete=models.DO_NOTHING)
    # date_sent = models.DateTimeField(default=timezone.now)
    # jason = models.CharField(max_length=300, null=True)
    timestamp = models.DateTimeField()
    ch0 = models.FloatField()
    ch1 = models.FloatField()
    class Meta:
        db_table = 'sensor_data'
    def __str__(self):
        return f"SensorData {self.timestamp}"