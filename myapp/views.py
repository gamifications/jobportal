from django.views import generic, View
from django.urls import reverse_lazy

from django.shortcuts import render, redirect,reverse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from myapp.models import Job, Keyword, Candidate, JobKeywords, Tag
from myapp.forms import JobForm, CandidateFormset, KeywordFormset

class JobListView(LoginRequiredMixin, generic.list.ListView):
    """Return list of all jobs"""
    model = Job

class MyUpdateView(generic.UpdateView):
    form_class = JobForm
    template_name = 'myapp/job_form.html'
  
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.get_object()
        print(job)
        if job:
            context['formset']=KeywordFormset(instance=job)
            context['formset2'] = CandidateFormset(instance=job)
        else:
            context['formset']=KeywordFormset()
            context['formset2'] = CandidateFormset()
        return context

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get_queryset(self):
        return Job.objects.all()

    def get_success_url(self):
       return reverse('job:list')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
        return self.render_to_response(self.get_context_data(object=self.object, form=self.form_class))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
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

            messages.success(request, 'Job saved successfully.')
            return redirect('job:list')
        else:
            return self.render_to_response(self.get_context_data(form=form))


class JobView(LoginRequiredMixin, View):
    frm1 = JobForm
    frm2 = KeywordFormset # (instance=question)
    frm3 = CandidateFormset
    # initial = {'key': 'value'}
    template_name = 'myapp/job_form.html'

    def get(self, request, pk=None):
        if pk:
            # Edit Job
            job = Job.objects.get(pk=pk)
            form = self.frm1(instance=job)
            formset = self.frm2(instance=job)
            formset2 = self.frm3(instance=job)
        else:
            # Add New Job
            form = self.frm1()
            formset = self.frm2()
            formset2 = self.frm3()

        return render(request, self.template_name, {'jobform': form,'formset': formset,'formset2': formset2})

    def post(self, request, pk=None):
        if pk:
            # Edit Job
            job = Job.objects.get(pk=pk)
            form = self.frm1(request.POST, instance=job)
            formset = self.frm2(request.POST, instance=job)
            formset2 = self.frm3(request.POST, request.FILES, instance=job)
        else:
            # Add New Job
            form = self.frm1(request.POST)
            formset = self.frm2(request.POST)
            formset2 = self.frm3(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid() and formset2.is_valid():
            print('success'*10)
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()

            # need to fix this.
            f1=self.frm2(request.POST, instance=job)
            f2 = self.frm3(request.POST, request.FILES, instance=job)
            if f1.is_valid() and f2.is_valid():
                f1.save()
                f2.save()
            messages.success(request, 'Job saved successfully.')
            return redirect('job:list')
        # else:
        #     print('success'*10)
        #     # reselect new keyword and tags
        #     request.POST = request.POST.copy()
        #     # need to update request.post with keywords and tags
        #     formset = self.formset_class(request.POST) 

        print(form.errors,'//',formset.errors,'==',formset2.errors)
        return render(request, self.template_name, {'jobform': form,'formset': formset,'formset2': formset2})

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
