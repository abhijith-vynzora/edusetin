from django import forms
from .models import (
    Country,
    University,
    Course,
    TeamMember,
    Testimonial,
    Blog,
    Service,
    Category,
    GalleryImage,
    ContactMessage,
    Application,
    CourseCategory,
    Inquiry,
    NewsletterSubscriber,
)


class CountryForm(forms.ModelForm):
    remove_pdf = forms.BooleanField(required=False, label="Remove Current PDF")

    class Meta:
        model = Country
        fields = ["name", "flag", "image", "description", "pdf", "remove_pdf"]

    def save(self, commit=True):
        country = super().save(commit=False)

        # Handle remove PDF checkbox
        if self.cleaned_data.get("remove_pdf"):
            if country.pdf:
                country.pdf.delete(save=False)  # delete file from storage
            country.pdf = None

        if commit:
            country.save()
        return country


class UniversityForm(forms.ModelForm):
    remove_pdf = forms.BooleanField(required=False, label="Remove Current PDF")

    class Meta:
        model = University
        fields = ["country", "name", "image", "description", "pdf", "remove_pdf"]

    def save(self, commit=True):
        university = super().save(commit=False)

        # Handle remove PDF checkbox
        if self.cleaned_data.get("remove_pdf"):
            if university.pdf:
                university.pdf.delete(save=False)  # delete file from storage
            university.pdf = None

        if commit:
            university.save()
        return university


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["title", "image", "description", "duration", "university", "category"]


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ["name", "image", "review", "rating"]


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = ["name", "profession", "image", "linkedin", "github", "twitter"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image"].required = False


# --------- Service Form ---------
class ServiceForm(forms.ModelForm):
    remove_pdf = forms.BooleanField(required=False, label="Remove Current PDF")

    class Meta:
        model = Service
        fields = ["image", "title", "description", "pdf", "remove_pdf"]

    def save(self, commit=True):
        service = super().save(commit=False)

        # Handle remove PDF checkbox
        if self.cleaned_data.get("remove_pdf"):
            if service.pdf:
                service.pdf.delete(save=False)  # delete file from storage
            service.pdf = None

        if commit:
            service.save()
        return service


# --------- Blog Form ---------
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ["image", "title", "description"]


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name"]


class GalleryImageForm(forms.ModelForm):  # no need
    class Meta:
        model = GalleryImage
        fields = ["category", "title", "image"]


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message", "course_subject"]


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = [
            "full_name",
            "email",
            "phone",
            "qualification",
            "course",
            "country",
            "marks",
        ]


class CourseCategoryForm(forms.ModelForm):
    class Meta:
        model = CourseCategory
        fields = ["name", "image", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "form-control modern-input",
                    "placeholder": "Enter Category Name",
                    "required": True,
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control modern-input",
                    "id": "description",
                    "rows": 5,
                    "placeholder": "Enter Category Description",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "class": "form-control modern-input",
                }
            ),
        }


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ["name", "email", "phone", "message"]


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ["email"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if NewsletterSubscriber.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already subscribed.")
        return email
