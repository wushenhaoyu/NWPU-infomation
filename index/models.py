from django.db import models

from django.db.models import signals
from django.dispatch import receiver
from django.utils import timezone

class User(models.Model):
    userName = models.CharField(max_length=40)
    password = models.CharField(max_length=30)

class Patient(models.Model):
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    IDcard = models.CharField(max_length=18)
    gender = models.CharField(max_length=18)

class PatientOutHospital(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timeInHospital = models.DateTimeField()
    TimeOutHospital = models.DateTimeField()


class PatientInHospital(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timeInHospital = models.DateTimeField()

    def OutHospital(self):
        out_hospital = PatientOutHospital(
            patient=self.patient,
            timeInHospital=self.timeInHospital,
            TimeOutHospital=timezone.now(),
        )
        out_hospital.save()

        # 删除对应的PatientInHospital记录
        self.delete()

# 使用信号处理器来监听PatientOutHospital的保存操作
@receiver(signals.post_save, sender=PatientOutHospital)
def delete_patient_in_hospital(sender, instance, created, **kwargs):
    if created:
        # 检查是否与PatientInHospital中的记录匹配
        in_hospital = PatientInHospital.objects.filter(patient=instance.patient, timeInHospital=instance.timeInHospital).first()
        if in_hospital:
            in_hospital.delete()



