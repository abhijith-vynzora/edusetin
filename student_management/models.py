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
    image = models.ImageField(upload_to='question_media/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = [('question', 'media_type')]
        ordering = ['media_type']

    def __str__(self):
        return f"Q#{self.question_id} — {self.media_type}"
