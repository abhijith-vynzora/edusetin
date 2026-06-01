from django.db import models
from PIL import Image, ImageOps
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.image_optimizer import optimize_image, optimize_flag
from django.utils.text import slugify


class OptimizedImageModel(models.Model):
    """
    Base class: any model inheriting this can declare image_fields = []
    to auto-optimize images on save.
    """

    image_fields = []  # override in child models

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Optimize all declared image fields
        for field in self.image_fields:
            image_field = getattr(self, field, None)
            if image_field and hasattr(image_field, "path"):
                optimize_image(image_field.path)


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    flag = models.ImageField(upload_to="countries/flags/")
    image = models.ImageField(upload_to="countries/images/", blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to="country_pdfs/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ["order","name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-generate slug
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

        # --- Resize Flag (make it small like logo 40x40) ---
        if self.flag:
            flag_path = self.flag.path
            with Image.open(flag_path) as img:
                img = img.convert("RGB")
                img = img.resize((40, 40), Image.LANCZOS)
                img.save(flag_path, quality=90)


class University(OptimizedImageModel):
    country = models.ForeignKey(
        Country, related_name="universities", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True,null=True)
    image = models.ImageField(upload_to="universities/")
    description = models.TextField(blank=True, null=True)
    pdf = models.FileField(upload_to="university_pdfs/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0, db_index=True)

    # Tell base model which images to optimize
    image_fields = ["image"]

    class Meta:
        ordering = ["order","name"]

    def __str__(self):
        return f"{self.name} ({self.country.name})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class CourseCategory(OptimizedImageModel):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="course_categories/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0) 

    # Tell base model which images to optimize
    image_fields = ["image"]

    class Meta:
        verbose_name_plural = "Course Categories"
        ordering = ["order","name"]
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Course(OptimizedImageModel):
    university = models.ForeignKey(
        University, related_name="courses", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    category = models.ForeignKey(
        CourseCategory,
        related_name="courses",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    image = models.ImageField(upload_to="courses/")
    description = models.TextField(blank=True, null=True)
    duration = models.CharField(max_length=100)  # e.g. "3 Years", "6 Months"
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.PositiveIntegerField(default=0) 

    # Tell base model which images to optimize
    image_fields = ["image"]

    class Meta:
        ordering = ["order","id"]

    def __str__(self):
        return f"{self.title} ({self.university.name})"


class TeamMember(OptimizedImageModel):
    name = models.CharField(max_length=100, help_text="Full name of the team member")
    profession = models.CharField(
        max_length=100, help_text="Role or profession (e.g. Software Engineer)"
    )
    image = models.ImageField(
        upload_to="team/", blank=True, null=True, help_text="Profile picture"
    )

    # Social links (can expand later)
    linkedin = models.URLField(max_length=200, blank=True, null=True)
    github = models.URLField(max_length=200, blank=True, null=True)
    twitter = models.URLField(max_length=200, blank=True, null=True)


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Tell base model which images to optimize
    image_fields = ["image"]

    class Meta:
        ordering = ["name"]
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"

    def __str__(self):
        return f"{self.name} - {self.profession}"


class Testimonial(OptimizedImageModel):
    name = models.CharField(
        max_length=100, help_text="Name of the person giving the testimonial"
    )
    image = models.ImageField(
        upload_to="testimonials/", blank=True, null=True, help_text="Profile picture"
    )
    review = models.TextField(help_text="Customer or client review")
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Rating out of 5 stars",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Tell base model which images to optimize
    image_fields = ["image"]

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} ({self.rating}⭐)"


from django.core.exceptions import ValidationError


# --------- Services ---------
class Service(OptimizedImageModel):
    image = models.ImageField(upload_to="services/", help_text="Service image")
    title = models.CharField(max_length=200, help_text="Service title")
    description = models.TextField(help_text="Service description")
    created_at = models.DateTimeField(auto_now_add=True)
    pdf = models.FileField(upload_to="service_pdfs/", blank=True, null=True)
    order = models.IntegerField(default=0, db_index=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Service, self).save(*args, **kwargs)

    # Tell base model which images to optimize
    image_fields = ["image"]

    class Meta:
        ordering = ["order","-created_at"]

    def __str__(self):
        return self.title


# --------- Blogs ---------
class Blog(OptimizedImageModel):
    image = models.ImageField(upload_to="blogs/", help_text="Blog cover image")
    slug = models.SlugField(unique=True, blank=True, null=True)
    title = models.CharField(max_length=200, help_text="Blog title")
    description = models.TextField(help_text="Blog description")
    created_at = models.DateTimeField(auto_now_add=True)

    # Tell base model which images to optimize
    image_fields = ["image"]

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class GalleryImage(OptimizedImageModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="images"
    )
    title = models.CharField(max_length=150, blank=True, null=True)
    image = models.ImageField(upload_to="gallery/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    # Tell base model which images to optimize
    image_fields = ["image"]

    def __str__(self):
        return self.title if self.title else f"Image {self.id}"


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()
    course_subject = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"


class Application(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    qualification = models.CharField(max_length=255, blank=True, null=True)
    marks = models.DecimalField(
        max_digits=5, decimal_places=2, help_text="Enter graduation marks (e.g., 75.50)"
    )
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.course}"


class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField(verbose_name="Inquiry Details")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.email})"


class ChatbotUser(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=100)
    year_completed = models.CharField(max_length=10)
    last_interaction = models.DateTimeField(auto_now=True)
    preference = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.phone}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
