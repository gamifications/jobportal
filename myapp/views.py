from django import forms
from django.views import generic
from django.urls import reverse_lazy
from myapp.models import Job

class JobListView(generic.list.ListView):
    """Return list of all jobs"""
    model = Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title'] #,'keywords'] #'__all__'

class JobCreateView(generic.edit.CreateView):
    form_class = JobForm
    model = Job
    success_url = reverse_lazy('job:list')
    def form_valid(self, form):
        print(form.instance)
        print(self.request.POST, 'post data')
        import json
        print(self.request.body)
        print(self.request.POST.getlist('keywords'), 'post data')
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super().form_valid(form)