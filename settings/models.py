from django.db import models

# Create your models here.


class ApplicationInstruction(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Application Instruction'
        verbose_name_plural = '1.Application Instruction'

    def __str__(self):
        return self.title


class ApplicationInstructionList(models.Model):
    instruction = models.ForeignKey(
        ApplicationInstruction, on_delete=models.CASCADE, related_name='instructions')
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Instruction'
        verbose_name_plural = '2. Instruction'

    def __str__(self):
        return self.name
