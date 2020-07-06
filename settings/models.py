from django.db import models

# Create your models here.


class SiteInfo(models.Model):
    site_name = models.CharField(max_length=255)
    site_phone = models.CharField(max_length=20)
    site_email = models.EmailField()

    class Meta:
        verbose_name = 'SiteInfo'
        verbose_name_plural = '1.SiteInfo'

    def __str__(self):
        return self.site_name


class ApplicationInstruction(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Application Instruction'
        verbose_name_plural = '2.Application Instruction'

    def __str__(self):
        return self.title


class ApplicationInstructionList(models.Model):
    instruction = models.ForeignKey(
        ApplicationInstruction, on_delete=models.CASCADE, related_name='instructions')
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Instruction'
        verbose_name_plural = '3. Instruction'

    def __str__(self):
        return self.name


class SiteFaq(models.Model):
    question = models.CharField(max_length=255)
    answer = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = '4.FAQ'

    def __str__(self):
        return self.question
