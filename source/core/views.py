# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from planner.core.models import UserProfileForm, UserProfile, Institution, Course, Subject
import kao

# DEBUG
from planner.core.models import Subject

from django import forms

@login_required
def index(request):
    template = "core/index.html"
    form = None
    results = None
    
    try:
        user_profile_exists = True
        
        profile = request.user.get_profile()
        
        class StudyForm(forms.Form):
            subjects = forms.ModelMultipleChoiceField(profile.institution.subject_set.all(), required=False, widget=forms.CheckboxSelectMultiple)
            prefer_sparse_schedule = forms.BooleanField(required=False)
        
        results = None
            
        if request.method == 'POST': # If the form has been submitted...
            form = StudyForm(request.POST)
            
            if form.is_valid():
                # results = profile.get_recommended_subjects(form.cleaned_data['subjects'])
                request.session['form_subject_codes'] = [ subject.code for subject in form.cleaned_data['subjects'] ]
                request.session['form_prefer_sparse_schedule'] = form.cleaned_data['prefer_sparse_schedule']
                results = kao.get_recommended_subjects(form.cleaned_data['subjects'], form.cleaned_data['prefer_sparse_schedule'], profile)
                template = "core/result.html"
        else:
            try:
                subjects = Subject.objects.filter(code__in=request.session['form_subject_codes'])
                prefer_sparse_schedule = request.session['form_prefer_sparse_schedule']
                form = StudyForm(initial={'subjects': subjects, 'prefer_sparse_schedule': prefer_sparse_schedule})
            except KeyError:
                print "KeyError"
                form = StudyForm()
            
    except UserProfile.DoesNotExist:
        user_profile_exists = False
        
    return render_to_response(template,
        {
            'user_profile_exists': user_profile_exists,
            'form': form,
            'results': results,
        }, context_instance=RequestContext(request)
    )
    
@login_required
def profile(request):       
    saved = False
    
    if request.method == 'POST': # If the form has been submitted...
        try:
            form = UserProfileForm(request.POST, instance=request.user.get_profile()) # A form bound to the POST data
        except UserProfile.DoesNotExist:
            form = UserProfileForm(request.POST) # A form bound to the POST data
        if form.is_valid():
            form.save()
            saved = True
    else:
        try:
            profile = request.user.get_profile()
            form = UserProfileForm(instance=request.user.get_profile())
        except UserProfile.DoesNotExist:
            form = UserProfileForm(initial={'user': request.user})
        
    return render_to_response("core/profile.html",
        {
            'user_id': request.user.id,
            'form': form,
            'saved': saved,
        }, context_instance=RequestContext(request)
    )
    
def register(request):
    if request.method == 'POST': # If the form has been submitted...
        form = UserCreationForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            form.save()
            return HttpResponseRedirect(reverse('core-index')) # Redirect after POST
    else:
        form = UserCreationForm() # An unbound form
    
    return render_to_response("core/register.html",
        {
            'form': form,
        }, context_instance=RequestContext(request)
    )
