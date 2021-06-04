from django import forms
from django.views import generic
from django.urls import reverse_lazy
from myapp.models import Job, Keyword, Candidate, JobKeywords, Tag
from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages


class JobListView(generic.list.ListView):
    """Return list of all jobs"""
    model = Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title'] #,'candidate'] '__all__'


def job_view(request):
    KeywordFormset = inlineformset_factory(Job,JobKeywords,fields=('keyword', 'tags'),extra=5)
    if request.method == 'POST':
        job = Job.objects.create(title=request.POST['title'], created_by=request.user)
        get_data = lambda n: {'keyword':request.POST[f'jobkeywords_set-{n}-keyword'], 'tags':request.POST.getlist(f'jobkeywords_set-{n}-tags')}
        for n in range(int(request.POST['jobkeywords_set-TOTAL_FORMS'])):
            data = get_data(n)
            keyword = Keyword.objects.get_or_create(name=data['keyword'].title())[0]
            tags = [Tag.objects.get_or_create(name=t.title())[0] for t in data['tags']]
            job_keywords = JobKeywords.objects.create(job=job, keyword=keyword)
            job_keywords.tags.add(*tags)

        messages.success(request, 'Job saved successfully.')
        return redirect('job:list')
        
    form = JobForm()
    formset = KeywordFormset() # (instance=question)
    return render(request, 'myapp/job_form.html', {'form': form,'formset': formset})
