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


class JobView(LoginRequiredMixin, View):
    frm1 = JobForm
    frm2 = KeywordFormset
    frm3 = CandidateFormset
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

        return render(request, self.template_name, {'jobform': form,'formset': formset,
            'formset2': formset2, 'pk':pk})

    def on_error_set_newly_created_tags_and_keyword(self, post_data):
        post_data = post_data.copy()
        for n in range(int(post_data['jobkeywords_set-TOTAL_FORMS'])):
            # 'jobkeywords_set-4-tags': ['2', 'sadf', 'suhail'],  'jobkeywords_set-1-keyword': ['4'] 
            key1 = f'jobkeywords_set-{n}-keyword'
            key2 = f'jobkeywords_set-{n}-tags'
            if not post_data[key1].isdigit():
                post_data.update({key1: str(Keyword.objects.get(name=post_data[key1]).pk)})

            tags = []
            for item in post_data.getlist(key2):
                if not item.isdigit():
                    # update post_data
                    tags.append(str(Tag.objects.get(name=item).pk))
                else:
                    tags.append(item)
            post_data.setlist(key2, tags) # https://stackoverflow.com/a/22210263/2351696
            
        return post_data

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
            # from django.db import transaction
            # with transaction.atomic():
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
        else:
            # reselect newly added keyword and tags
            post_data = self.on_error_set_newly_created_tags_and_keyword(request.POST)
            # need to update request.post with keywords and tags
            formset = self.frm2(post_data) 

        return render(request, self.template_name, {'jobform': form,'formset': formset,'formset2': formset2})


class JobDeleteView(generic.edit.DeleteView):
    model = Job
    success_url = reverse_lazy('job:list')