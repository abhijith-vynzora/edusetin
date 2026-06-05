from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Question(models.Model):
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
        ('E', 'E'),
    ]
    SOURCE_CHOICES = [
        ('PYQ', 'PYQ'),
        ('EDUSETIN', 'EDUSETIN'),
        ('OTHER', 'OTHER'),
    ]

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    option_e = models.TextField(blank=True, null=True)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    explanation = models.TextField(blank=True, null=True)
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES, blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Per-slot media requirement flags (set by import or manual create/edit)
    requires_question_image = models.BooleanField(default=False)
    requires_option_a_image = models.BooleanField(default=False)
    requires_option_b_image = models.BooleanField(default=False)
    requires_option_c_image = models.BooleanField(default=False)
    requires_option_d_image = models.BooleanField(default=False)
    requires_option_e_image = models.BooleanField(default=False)

    # Derived/cached flag: True when all required slots have a QuestionMedia row
    media_uploaded = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question_text[:80]

    @property
    def has_media(self):
        """True if any media slot is required."""
        return any([
            self.requires_question_image,
            self.requires_option_a_image,
            self.requires_option_b_image,
            self.requires_option_c_image,
            self.requires_option_d_image,
            self.requires_option_e_image,
        ])


# ─────────────────────────────────────────────
# MEDIA LIBRARY
# ─────────────────────────────────────────────

class MediaLibrary(models.Model):
    """
    Reusable media asset repository.
    Images uploaded here can be referenced by multiple QuestionMedia records
    without duplicating the physical file.
    """
    name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='media_library/')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    @property
    def usage_count(self):
        return self.usages.count()

    @property
    def is_in_use(self):
        return self.usages.exists()


class QuestionMedia(models.Model):
    MEDIA_TYPES = [
        ('QUESTION', 'Question'),
        ('OPTION_A', 'Option A'),
        ('OPTION_B', 'Option B'),
        ('OPTION_C', 'Option C'),
        ('OPTION_D', 'Option D'),
        ('OPTION_E', 'Option E'),
    ]

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='media_files'
    )
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    image = models.ImageField(upload_to='question_media/', blank=True, default='')

    # Optional reference to the MediaLibrary asset this image came from.
    # NULL = manually uploaded file. Non-NULL = sourced from library.
    media_library = models.ForeignKey(
        MediaLibrary,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='usages'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('question', 'media_type')]
        ordering = ['media_type']

    def __str__(self):
        return f"Q#{self.question_id} — {self.media_type}"

    @property
    def effective_image(self):
        """
        Returns the authoritative image for this media record.

        - If sourced from Media Library (media_library FK set): returns the
          library asset's current image so any replacement to the library
          asset is automatically reflected here without touching this record.
        - If manually uploaded: returns the locally stored image.
        """
        if self.media_library_id and self.media_library:
            return self.media_library.image
        return self.image


# ─────────────────────────────────────────────
# PENDING MEDIA REFERENCES
# ─────────────────────────────────────────────

class PendingMediaReference(models.Model):
    """
    Stores a record when an Excel import references a MediaLibrary asset
    by name but the asset does not exist at import time.

    This allows the admin to see which images are still needed for a question
    even after the import report is dismissed.
    """
    MEDIA_TYPES = QuestionMedia.MEDIA_TYPES

    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='pending_media_refs'
    )
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    expected_media_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('question', 'media_type')]
        ordering = ['media_type']

    def __str__(self):
        return f"Q#{self.question_id} — {self.media_type} — {self.expected_media_name}"
