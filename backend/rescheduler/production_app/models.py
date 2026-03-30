from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=10)        # P1, P2
    priority = models.CharField(max_length=10, choices=[('low','Low'), ('medium','Medium'), ('high','High')])
    due_day = models.IntegerField()               # Day 10
    delay_penalty = models.IntegerField()         # 5000 per late day

class Machine(models.Model):
    name = models.CharField(max_length=10)        # M1, M2
    type = models.CharField(max_length=10)        # CNC, VMC
    available_from = models.IntegerField(default=1)
    maintenance_start = models.IntegerField(null=True, blank=True)
    maintenance_end = models.IntegerField(null=True, blank=True)

class Operation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    machine_type = models.CharField(max_length=10)  # CNC
    duration = models.IntegerField()                # 2 days