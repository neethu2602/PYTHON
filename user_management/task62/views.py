from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm


def home(request):
    return render(request, 'users/home.html')


from django.contrib.auth.forms import UserCreationForm
from django import forms

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views import View
from .forms import RegisterForm  # Ensure this is the correct path
from .models import Portfolio

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})
# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

from .models import Portfolio, Project, WorkExperience, Education, Certification
from .forms import ProjectForm, WorkExperienceForm, EducationForm, CertificationForm,PortfolioForm

from .models import Portfolio
@login_required
def create_or_update_portfolio(request):
    try:
        # Attempt to get the portfolio for the current user
        portfolio = Portfolio.objects.get(user=request.user)
        form = PortfolioForm(instance=portfolio)
    except Portfolio.DoesNotExist:
        # If the portfolio does not exist, create a new form
        portfolio = None
        form = PortfolioForm()

    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.user = request.user  # Ensure the portfolio is associated with the current user
            portfolio.save()
            messages.success(request, "Your portfolio has been updated successfully!")
            return redirect('task62:portfolio_detail')  # Redirect to the portfolio detail page

    return render(request, 'users/create_portfolio.html', {'form': form})

@login_required
def portfolio(request):
    try:
        # Attempt to get the portfolio for the current user
        portfolio = Portfolio.objects.get(user=request.user)
    except Portfolio.DoesNotExist:
        # If the portfolio does not exist, redirect to the create portfolio page
        messages.error(request, "You do not have a portfolio. Please create one.")
        return redirect('task62:create_portfolio')
    portfolio = Portfolio.objects.get(user=request.user)

    portfolio = Portfolio.objects.get(user=request.user)
    projects = Project.objects.filter(portfolio=portfolio)
    work_experience = WorkExperience.objects.filter(portfolio=portfolio)
    education = Education.objects.filter(portfolio=portfolio)
    certifications = Certification.objects.filter(portfolio=portfolio)
    return render(request, 'users/portfolio_detail.html', {
        'portfolio': portfolio,
        'projects': projects,
        'work_experience': work_experience,
        'education': education,
        'certifications': certifications,
    })


@login_required
def portfolio_detail(request):
    portfolio = Portfolio.objects.get(Portfolio, user=request.user)
    projects = portfolio.projects.all()
    work_experience = portfolio.work_experience.all()
    education = portfolio.education.all()
    certifications = portfolio.certifications.all()

    context = {
        'portfolio': portfolio,
        'projects': projects,
        'work_experience': work_experience,
        'education': education,
        'certifications': certifications,
    }
    return render(request, 'users/portfolio_detail.html', context)
def projects_page(request):
    projects = Project.objects.all()  # Replace with your actual model
    return render(request, 'users/projects.html', {'projects': projects})

def work_experience_page(request):
    work_experience = WorkExperience.objects.all()  # Replace with your actual model
    return render(request, 'users/work_experience.html', {'work_experience': work_experience})

def education_page(request):
    education = Education.objects.all()  # Replace with your actual model
    return render(request, 'users/education.html', {'education': education})

def certifications_page(request):
    certifications = Certification.objects.all()  # Replace with your actual model
    return render(request, 'users/certifications.html', {'certifications': certifications})
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.portfolio = Portfolio.objects.get(user=request.user)
            project.save()
            return redirect('task62:portfolio_detail')
    else:
        form = ProjectForm()
    return render(request, 'users/add_project.html', {'form': form})

# portfolio/views.py
from django.shortcuts import render, redirect
from .models import Portfolio, WorkExperience
from .forms import WorkExperienceForm


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Project
from .forms import ProjectForm

def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully!')
            return redirect('task62:portfolio_details')  # or redirect to another page if needed
    else:
        form = ProjectForm(instance=project)

    return render(request, 'users/edit_project.html', {'form': form})


def delete_project(request, pk):
    project = Portfolio.objects.get( pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('task62:portfolio_details')
  # Redirect to the portfolio view or another appropriate view
    return render(request, 'users/confirm_delete.html', {'project': project})



def add_work_experience(request):
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST,request.FILES)
        if form.is_valid():
            work_experience = form.save(commit=False)
            work_experience.portfolio = Portfolio.objects.get(user=request.user)
            work_experience.save()
            return redirect('task62:portfolio_detail')
    else:
        form = WorkExperienceForm()
    return render(request, 'users/add_work_experience.html', {'form': form})

def edit_work_experience(request, pk):
    work_experience = WorkExperience.objects.get(pk=pk)
    if request.method == 'POST':
        form = WorkExperienceForm(request.POST,request.FILES, instance=work_experience)
        if form.is_valid():
            form.save()
            return redirect('task62:portfolio_detail')
    else:
        form = WorkExperienceForm(instance=work_experience)
    return render(request, 'users/edit_work_experience.html', {'form': form})

def delete_work_experience(request, pk):
    work_experience = WorkExperience.objects.get(pk=pk)
    if request.method == 'POST':
        work_experience.delete()
        return redirect('task62:portfolio_detail')
    return render(request, 'users/delete_work_experience.html', {'work_experience': work_experience})


# portfolio/views.py
from .models import Education
from .forms import EducationForm

def add_education(request):
    if request.method == 'POST':
        form = EducationForm(request.POST,request.FILES)
        if form.is_valid():
            education = form.save(commit=False)
            education.portfolio = Portfolio.objects.get(user=request.user)
            education.save()
            return redirect('task62:portfolio_detail')
    else:
        form = EducationForm()
    return render(request, 'users/add_education.html', {'form': form})

def edit_education(request, pk):
    education = Education.objects.get(pk=pk)
    if request.method == 'POST':
        form = EducationForm(request.POST,request.FILES, instance=education)
        if form.is_valid():
            form.save()
            return redirect('task62:portfolio_detail')
    else:
        form = EducationForm(instance=education)
    return render(request, 'users/edit_education.html', {'form': form})

def delete_education(request, pk):
    education = Education.objects.get(pk=pk)
    if request.method == 'POST':
        education.delete()
        return redirect('task62:portfolio_detail')
    return render(request, 'users/delete_education.html', {'education': education})


# portfolio/views.py
from .models import Certification
from .forms import CertificationForm

def add_certification(request):
    if request.method == 'POST':
        form = CertificationForm(request.POST,request.FILES)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.portfolio = Portfolio.objects.get(user=request.user)
            certification.save()
            return redirect('task62:portfolio_detail')
    else:
        form = CertificationForm()
    return render(request, 'users/add_certification.html', {'form': form})

def edit_certification(request, pk):
    certification = Certification.objects.get(pk=pk)
    if request.method == 'POST':
        form = CertificationForm(request.POST,request.FILES, instance=certification)
        if form.is_valid():
            form.save()
            return redirect('task62:portfolio_detail')
    else:
        form = CertificationForm(instance=certification)
    return render(request, 'users/edit_certification.html', {'form': form})

def delete_certification(request, pk):
    certification = Certification.objects.get(pk=pk)
    if request.method == 'POST':
        certification.delete()
        return redirect('task62:portfolio_detail')
    return render(request, 'users/delete_certification.html', {'certification': certification})





































