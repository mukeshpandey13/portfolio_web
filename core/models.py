from django.db import models
from django.utils import timezone


class MetaData(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    logo_charecter = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Hero(models.Model):
    greeting = models.CharField(max_length=255, default="Hello I'm", null=True, blank=True)
    full_name = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            Hero.objects.exclude(pk=self.pk).update(is_active=False)
        super(Hero, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.greeting} {self.full_name} {self.title}'


class About(models.Model):
    about = models.TextField(null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)
    # avatar = models.ImageField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if self.is_active:
            About.objects.exclude(pk=self.pk).update(is_active=False)
        super(About, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.about[:50]}...'


class Project(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    image = models.URLField(null=True, blank=True)
    # image = models.ImageField(null=True, blank=True)
    demo_url = models.URLField(null=True, blank=True)
    source_url = models.URLField(default='https://github.com/', null=True, blank=True)
    skill = models.ManyToManyField('Skill', blank=True)
    is_active = models.BooleanField(default=True)
    ordering_index = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        ordering = ['ordering_index', '-created']

    def __str__(self):
        return f'{self.title}'


class SlkillGroup(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Skill(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    icon = models.TextField(null=True, blank=True)
    group = models.ForeignKey(SlkillGroup, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class GetInTouch(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class InfoItem(models.Model):
    key = models.CharField(max_length=255, null=True, blank=True)
    value = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)
    get_in_touch = models.ForeignKey(GetInTouch, related_name='info_items', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.key}'


class SocialLink(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    icon = models.TextField(null=True, blank=True)
    get_in_touch = models.ForeignKey(GetInTouch, related_name='social_links', on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title}'


class Sections(models.Model):
    '''visible or hide section'''
    about_me = models.BooleanField(default=True)
    projects = models.BooleanField(default=True)
    skills = models.BooleanField(default=True)
    education = models.BooleanField(default=True)
    get_in_touch = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Sections'
        verbose_name_plural = 'Sections'


class Message(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name}'


############ education section
class Education(models.Model):
    DEGREE_CHOICES = [
        ("high_school", "High School"),
        ("associate", "Associate Degree"),
        ("bachelor", "Bachelor's Degree"),
        ("master", "Master's Degree"),
        ("phd", "PhD / Doctorate"),
        ("certificate", "Certificate / Diploma"),
        ("other", "Other"),
    ]

    institution = models.CharField(max_length=200)
    degree = models.CharField(max_length=20, choices=DEGREE_CHOICES, default="bachelor")
    field_of_study = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_studying = models.BooleanField(default=False)
    grade = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="education_logos/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.get_degree_display()} - {self.institution}"

    @property
    def duration_display(self):
        start = self.start_date.strftime("%b %Y") if self.start_date else ""
        end = "Present" if (self.currently_studying or not self.end_date) else self.end_date.strftime("%b %Y")
        return f"{start} - {end}"


class AchievementCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name_plural = "Achievement categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Achievement(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(AchievementCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name="achievements")
    issuer = models.CharField(max_length=200, blank=True)
    date_awarded = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)
    credential_url = models.URLField(blank=True)
    featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-date_awarded"]

    def __str__(self):
        return self.title


# Experience 
class Experience(models.Model):
    EMPLOYMENT_TYPE_CHOICES = [
        ("full_time", "Full-time"),
        ("part_time", "Part-time"),
        ("internship", "Internship"),
        ("contract", "Contract"),
        ("freelance", "Freelance"),
    ]

    company = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, default="full_time")
    location = models.CharField(max_length=200, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to="experience_logos/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.role} at {self.company}"

    @property
    def duration_display(self):
        start = self.start_date.strftime("%b %Y") if self.start_date else ""
        end = "Present" if (self.currently_working or not self.end_date) else self.end_date.strftime("%b %Y")
        return f"{start} - {end}"