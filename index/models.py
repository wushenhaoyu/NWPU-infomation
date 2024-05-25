from django.db import models
from datetime import timezone

class User(models.Model):
    userName = models.CharField(max_length=40)
    password = models.CharField(max_length=30)

class Patient(models.Model):
    name = models.CharField(max_length=40)
    age = models.IntegerField()
    IDcard = models.CharField(max_length=18)
    gender = models.BooleanField()

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

class PatientOutHospital(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    timeInHospital = models.DateTimeField()
    TimeOutHospital = models.DateTimeField()
