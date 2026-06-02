from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404
from django.conf import settings
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from student_portal.models import Student
from .models import Subject, Question


# ─────────────────────────────────────────────
# DASHBOARD
# ─────────────────────────────────────────────

@login_required(login_url='admin_login')
def student_management_dashboard(request):
    total_students = Student.objects.count()
    total_subjects = Subject.objects.count()
    total_questions = Question.objects.count()
    total_pyqs = Question.objects.filter(source='PYQ').count()
    active_questions = Question.objects.filter(is_active=True).count()
    inactive_questions = Question.objects.filter(is_active=False).count()

    recent_students = Student.objects.select_related('user').order_by('-created_at')[:5]
    recent_subjects = Subject.objects.order_by('-created_at')[:5]
    recent_questions = Question.objects.select_related('subject').order_by('-created_at')[:5]

    return render(request, 'student_management/dashboard.html', {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_questions': total_questions,
        'total_pyqs': total_pyqs,
        'active_questions': active_questions,
        'inactive_questions': inactive_questions,
        'recent_students': recent_students,
        'recent_subjects': recent_subjects,
        'recent_questions': recent_questions,
    })


# ─────────────────────────────────────────────
# STUDENTS
# ─────────────────────────────────────────────

@login_required(login_url='admin_login')
def student_list(request):
    students = Student.objects.select_related('user').order_by('-created_at')
    return render(request, 'student_management/student_list.html', {'students': students})


@login_required(login_url='admin_login')
def student_detail(request, id):
    student = get_object_or_404(Student.objects.select_related('user'), id=id)
    return render(request, 'student_management/student_detail.html', {'student': student})


@login_required(login_url='admin_login')
def student_activate(request, id):
    student = get_object_or_404(Student, id=id)
    if student.is_active:
        messages.warning(request, "Student is already active.")
    else:
        student.is_active = True
        student.save()
        student.user.is_active = True
        student.user.save()
        messages.success(request, "Student activated successfully.")
    return redirect('student_management:student_detail', id=student.id)


@login_required(login_url='admin_login')
def student_deactivate(request, id):
    student = get_object_or_404(Student, id=id)
    if not student.is_active:
        messages.warning(request, "Student is already inactive.")
    else:
        student.is_active = False
        student.save()
        student.user.is_active = False
        student.user.save()
        messages.warning(request, "Student deactivated successfully.")
    return redirect('student_management:student_detail', id=student.id)


@login_required(login_url='admin_login')
def student_delete(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        user = student.user
        student.delete()
        user.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect('student_management:student_list')
    return redirect('student_management:student_detail', id=student.id)


# ─────────────────────────────────────────────
# SUBJECTS
# ─────────────────────────────────────────────

@login_required(login_url='admin_login')
def subject_list(request):
    subjects = Subject.objects.order_by('-created_at')
    return render(request, 'student_management/subject_list.html', {'subjects': subjects})


@login_required(login_url='admin_login')
def subject_create(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        if not name:
            messages.error(request, "Subject name is required.")
            return render(request, 'student_management/subject_create.html', {
                'post_data': request.POST
            })

        if Subject.objects.filter(name__iexact=name).exists():
            messages.error(request, f"A subject with the name \"{name}\" already exists.")
            return render(request, 'student_management/subject_create.html', {
                'post_data': request.POST
            })

        subject = Subject.objects.create(
            name=name,
            description=description or None,
            is_active=is_active,
        )
        messages.success(request, f"Subject \"{subject.name}\" created successfully.")
        return redirect('student_management:subject_list')

    return render(request, 'student_management/subject_create.html', {})


@login_required(login_url='admin_login')
def subject_edit(request, id):
    subject = get_object_or_404(Subject, id=id)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        is_active = request.POST.get('is_active') == 'on'

        if not name:
            messages.error(request, "Subject name is required.")
            return render(request, 'student_management/subject_edit.html', {'subject': subject})

        if Subject.objects.filter(name__iexact=name).exclude(id=id).exists():
            messages.error(request, f"Another subject with the name \"{name}\" already exists.")
            return render(request, 'student_management/subject_edit.html', {'subject': subject})

        subject.name = name
        subject.description = description or None
        subject.is_active = is_active
        subject.save()
        messages.success(request, f"Subject \"{subject.name}\" updated successfully.")
        return redirect('student_management:subject_list')

    return render(request, 'student_management/subject_edit.html', {'subject': subject})


@login_required(login_url='admin_login')
def subject_activate(request, id):
    subject = get_object_or_404(Subject, id=id)
    if subject.is_active:
        messages.warning(request, "Subject is already active.")
    else:
        subject.is_active = True
        subject.save()
        messages.success(request, "Subject activated successfully.")
    return redirect('student_management:subject_list')


@login_required(login_url='admin_login')
def subject_deactivate(request, id):
    subject = get_object_or_404(Subject, id=id)
    if not subject.is_active:
        messages.warning(request, "Subject is already inactive.")
    else:
        subject.is_active = False
        subject.save()
        messages.warning(request, "Subject deactivated successfully.")
    return redirect('student_management:subject_list')


@login_required(login_url='admin_login')
def subject_delete(request, id):
    subject = get_object_or_404(Subject, id=id)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f"Subject \"{name}\" deleted successfully.")
    return redirect('student_management:subject_list')


# ─────────────────────────────────────────────
# QUESTIONS
# ─────────────────────────────────────────────

@login_required(login_url='admin_login')
def question_list(request):
    questions = Question.objects.select_related('subject').order_by('-created_at')
    return render(request, 'student_management/question_list.html', {'questions': questions})


@login_required(login_url='admin_login')
def question_create(request):
    subjects = Subject.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        question_text = request.POST.get('question_text', '').strip()
        option_a = request.POST.get('option_a', '').strip()
        option_b = request.POST.get('option_b', '').strip()
        option_c = request.POST.get('option_c', '').strip()
        option_d = request.POST.get('option_d', '').strip()
        option_e = request.POST.get('option_e', '').strip()
        correct_answer = request.POST.get('correct_answer', '').strip()
        source = request.POST.get('source', '').strip() or None
        year_raw = request.POST.get('year', '').strip()
        explanation = request.POST.get('explanation', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        question_image = request.FILES.get('question_image')

        errors = []
        subject = None
        year = None

        if not subject_id:
            errors.append("Please select a subject.")
        else:
            subject = Subject.objects.filter(id=subject_id).first()
            if not subject:
                errors.append("Selected subject does not exist.")

        if not question_text:
            errors.append("Question text is required.")
        if not option_a:
            errors.append("Option A is required.")
        if not option_b:
            errors.append("Option B is required.")
        if not option_c:
            errors.append("Option C is required.")
        if not option_d:
            errors.append("Option D is required.")
        if not correct_answer:
            errors.append("Please select the correct answer.")

        if year_raw:
            try:
                year = int(year_raw)
                if year < 1900 or year > 2100:
                    errors.append("Please enter a valid year between 1900 and 2100.")
            except ValueError:
                errors.append("Year must be a valid number.")

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'student_management/question_create.html', {
                'subjects': subjects,
                'post_data': request.POST,
            })

        Question.objects.create(
            subject=subject,
            question_text=question_text,
            question_image=question_image,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            option_e=option_e or None,
            correct_answer=correct_answer,
            explanation=explanation or None,
            source=source,
            year=year,
            is_active=is_active,
        )
        messages.success(request, "Question created successfully.")
        return redirect('student_management:question_list')

    return render(request, 'student_management/question_create.html', {
        'subjects': subjects,
    })


@login_required(login_url='admin_login')
def question_detail(request, id):
    question = get_object_or_404(Question.objects.select_related('subject'), id=id)
    question_options = [
        ('A', question.option_a),
        ('B', question.option_b),
        ('C', question.option_c),
        ('D', question.option_d),
    ]
    if question.option_e:
        question_options.append(('E', question.option_e))
    return render(request, 'student_management/question_detail.html', {
        'question': question,
        'question_options': question_options,
    })


@login_required(login_url='admin_login')
def question_edit(request, id):
    question = get_object_or_404(Question.objects.select_related('subject'), id=id)
    subjects = Subject.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        question_text = request.POST.get('question_text', '').strip()
        option_a = request.POST.get('option_a', '').strip()
        option_b = request.POST.get('option_b', '').strip()
        option_c = request.POST.get('option_c', '').strip()
        option_d = request.POST.get('option_d', '').strip()
        option_e = request.POST.get('option_e', '').strip()
        correct_answer = request.POST.get('correct_answer', '').strip()
        source = request.POST.get('source', '').strip() or None
        year_raw = request.POST.get('year', '').strip()
        explanation = request.POST.get('explanation', '').strip()
        is_active = request.POST.get('is_active') == 'on'
        question_image = request.FILES.get('question_image')
        clear_image = request.POST.get('clear_image') == 'on'

        errors = []
        subject = None
        year = None

        if not subject_id:
            errors.append("Please select a subject.")
        else:
            subject = Subject.objects.filter(id=subject_id).first()
            if not subject:
                errors.append("Selected subject does not exist.")

        if not question_text:
            errors.append("Question text is required.")
        if not option_a:
            errors.append("Option A is required.")
        if not option_b:
            errors.append("Option B is required.")
        if not option_c:
            errors.append("Option C is required.")
        if not option_d:
            errors.append("Option D is required.")
        if not correct_answer:
            errors.append("Please select the correct answer.")

        if year_raw:
            try:
                year = int(year_raw)
                if year < 1900 or year > 2100:
                    errors.append("Please enter a valid year between 1900 and 2100.")
            except ValueError:
                errors.append("Year must be a valid number.")

        if errors:
            for err in errors:
                messages.error(request, err)
            return render(request, 'student_management/question_edit.html', {
                'question': question,
                'subjects': subjects,
            })

        question.subject = subject
        question.question_text = question_text
        question.option_a = option_a
        question.option_b = option_b
        question.option_c = option_c
        question.option_d = option_d
        question.option_e = option_e or None
        question.correct_answer = correct_answer
        question.explanation = explanation or None
        question.source = source
        question.year = year
        question.is_active = is_active

        if clear_image:
            question.question_image = None
        elif question_image:
            question.question_image = question_image

        question.save()
        messages.success(request, "Question updated successfully.")
        return redirect('student_management:question_detail', id=question.id)

    return render(request, 'student_management/question_edit.html', {
        'question': question,
        'subjects': subjects,
    })


@login_required(login_url='admin_login')
def question_activate(request, id):
    question = get_object_or_404(Question, id=id)
    if question.is_active:
        messages.warning(request, "Question is already active.")
    else:
        question.is_active = True
        question.save()
        messages.success(request, "Question activated successfully.")
    return redirect('student_management:question_detail', id=question.id)


@login_required(login_url='admin_login')
def question_deactivate(request, id):
    question = get_object_or_404(Question, id=id)
    if not question.is_active:
        messages.warning(request, "Question is already inactive.")
    else:
        question.is_active = False
        question.save()
        messages.warning(request, "Question deactivated successfully.")
    return redirect('student_management:question_detail', id=question.id)


@login_required(login_url='admin_login')
def question_delete(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == 'POST':
        question.delete()
        messages.success(request, "Question deleted successfully.")
        return redirect('student_management:question_list')
    return redirect('student_management:question_detail', id=question.id)


@login_required(login_url='admin_login')
def question_import(request):
    if request.method == 'POST':
        messages.info(request, "Question import functionality will be implemented soon.")
        return redirect('student_management:question_import')
        
    return render(request, 'student_management/question_import.html')


@login_required(login_url='admin_login')
def download_question_template(request):
    file_path = os.path.join(
        settings.BASE_DIR, 
        'student_management', 'static', 'student_management', 'downloads', 'sample_question_import.xlsx'
    )
    
    if os.path.exists(file_path):
        response = FileResponse(
            open(file_path, 'rb'), 
            as_attachment=True, 
            filename="sample_question_import.xlsx"
        )
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        return response
    else:
        messages.error(request, "Sample template file not found.")
        return redirect('student_management:question_import')

