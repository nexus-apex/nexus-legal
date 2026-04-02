from django.db import models

class LegalCase(models.Model):
    title = models.CharField(max_length=255)
    case_number = models.CharField(max_length=255, blank=True, default="")
    client_name = models.CharField(max_length=255, blank=True, default="")
    case_type = models.CharField(max_length=50, choices=[("civil", "Civil"), ("criminal", "Criminal"), ("corporate", "Corporate"), ("family", "Family"), ("ip", "IP"), ("labor", "Labor")], default="civil")
    status = models.CharField(max_length=50, choices=[("open", "Open"), ("in_progress", "In Progress"), ("hearing", "Hearing"), ("settled", "Settled"), ("closed", "Closed")], default="open")
    court = models.CharField(max_length=255, blank=True, default="")
    next_hearing = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class LegalClient(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    client_type = models.CharField(max_length=50, choices=[("individual", "Individual"), ("corporate", "Corporate")], default="individual")
    company = models.CharField(max_length=255, blank=True, default="")
    active_cases = models.IntegerField(default=0)
    total_billed = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    retainer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class LegalTimeEntry(models.Model):
    case_title = models.CharField(max_length=255)
    attorney = models.CharField(max_length=255, blank=True, default="")
    hours = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    rate = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    date = models.DateField(null=True, blank=True)
    activity = models.CharField(max_length=50, choices=[("research", "Research"), ("drafting", "Drafting"), ("court", "Court"), ("meeting", "Meeting"), ("review", "Review")], default="research")
    description = models.TextField(blank=True, default="")
    billable = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.case_title
