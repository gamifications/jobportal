from django.views import generic
from django.urls import reverse_lazy

from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib import messages

from myapp.models import Job, Keyword, Candidate, JobKeywords, Tag
from myapp.forms import JobForm, CandidateFormset, KeywordFormset

class JobListView(generic.list.ListView):
    """Return list of all jobs"""
    model = Job


def job_view(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        formset = KeywordFormset(request.POST) # (instance=question)
        formset2 = CandidateFormset(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid() and formset2.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()

            # need to fix this.
            f1=KeywordFormset(request.POST, instance=job)
            f2 = CandidateFormset(request.POST, request.FILES, instance=job)
            if f1.is_valid() and f2.is_valid():
                f1.save()
                f2.save()
            # formset.save(job=job)
            # formset2.save(job=job)

            # get_data = lambda n: {'keyword':request.POST[f'jobkeywords_set-{n}-keyword'], 'tags':request.POST.getlist(f'jobkeywords_set-{n}-tags')}
            # for n in range(int(request.POST['jobkeywords_set-TOTAL_FORMS'])):
            #     data = get_data(n)
            #     keyword = Keyword.objects.get_or_create(name=data['keyword'].title())[0]
            #     tags = [Tag.objects.get_or_create(name=t.title())[0] for t in data['tags']]
            #     job_keywords = JobKeywords.objects.get(job=job, keyword=keyword)
            #     job_keywords.tags.add(*tags)

            messages.success(request, 'Job saved successfully.')
            return redirect('job:list')
        else:
            # reselect new keyword and tags
            request.POST = request.POST.copy()
            # need to update request.post with keywords and tags
            formset = KeywordFormset(request.POST) 

    else:
        pk = request.GET.get('pk')
        if pk:
            job = Job.objects.get(pk=pk)
            # if edit
            form = JobForm(instance=job)
            formset = KeywordFormset(instance=job) # (instance=question)
            formset2 = CandidateFormset(instance=job)
        else:
            form = JobForm()
            formset = KeywordFormset() # (instance=question)
            formset2 = CandidateFormset()
    # print(formset)
    return render(request, 'myapp/job_form.html', 
        {'form': form,'formset': formset,'formset2': formset2})
