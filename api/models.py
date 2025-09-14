from django.db import models
from django.conf import settings


# ---------- Profile ----------
class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    pincode = models.BigIntegerField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"


# ---------- BaseModel (timestamps + created_by/modified_by) ----------
class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='created_%(class)s_set'
    )
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='modified_%(class)s_set'
    )

    class Meta:
        abstract = True


# ---------- PetType ----------
class PetType(BaseModel):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


# ---------- Pet ----------
GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

class Pet(BaseModel):
    name = models.CharField(max_length=200)
    pet_type = models.ForeignKey(PetType, on_delete=models.SET_NULL, null=True, related_name='pets')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    breed = models.CharField(max_length=200, blank=True)
    color = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    weight = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    address = models.TextField(blank=True)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    pincode = models.BigIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='pets/', blank=True, null=True)
    is_diseased = models.BooleanField(default=False)
    is_vaccinated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.pet_type})"


# ---------- PetMedicalHistory ----------
class PetMedicalHistory(BaseModel):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='medical_history')
    last_vaccinated_date = models.DateField(null=True, blank=True)
    vaccination_name = models.CharField(max_length=200, blank=True)
    disease_name = models.CharField(max_length=200, blank=True)
    stage = models.IntegerField(null=True, blank=True)
    no_of_years = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Medical History for {self.pet.name}"


# ---------- PetReport ----------
PET_STATUS_CHOICES = (
    ('lost', 'Lost'),
    ('found', 'Found'),
    ('adopted', 'Adopted'),
)

REPORT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
    ('resolved', 'Resolved'),
    ('reunited', 'Reunited'),
)

class PetReport(BaseModel):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='reports')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    pet_status = models.CharField(max_length=10, choices=PET_STATUS_CHOICES)
    report_status = models.CharField(max_length=10, choices=REPORT_STATUS_CHOICES, default='pending')
    image = models.ImageField(upload_to='reports/', blank=True, null=True)
    is_resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Report: {self.pet.name} - {self.pet_status}"


# ---------- PetAdoption ----------
ADOPTION_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
)

class PetAdoption(BaseModel):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='adoptions')
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=ADOPTION_STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Adoption request for {self.pet.name} by {self.requester}"


# ---------- Notification ----------
class Notification(BaseModel):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_notifications')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_notifications')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification from {self.sender} to {self.receiver}"
