from django.views import generic, View
from django.urls import reverse_lazy
from django.http import Http404
from django.shortcuts import render, redirect,reverse, get_object_or_404
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from myapp.models import Job, Keyword, Candidate, JobKeywords, Tag
from myapp.forms import JobForm, CandidateFormset, KeywordFormset


from django.contrib.auth.mixins import UserPassesTestMixin


class SubscriptionRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.subscription and self.request.user.subscription.status == "active"

    def handle_no_permission(self):
        return redirect('payments:home')

class JobListView(SubscriptionRequiredMixin, generic.list.ListView):
    """Return list of all jobs"""
    def get_queryset(self):
        return Job.objects.filter(created_by=self.request.user)

class JobView(LoginRequiredMixin, View):
    frm1 = JobForm
    frm2 = KeywordFormset
    frm3 = CandidateFormset
    template_name = 'myapp/job_form.html'

    def parse_pdf_and_save(self, job):        
        from pdfminer.high_level import extract_text
        candidates = Candidate.objects.filter(job=job,resume__isnull=False)
        for candidate in candidates:
            if not candidate.resume_data and candidate.resume:
                candidate.resume_data = extract_text(candidate.resume.path)
                candidate.save()

    def get(self, request, pk=None):
        if pk:
            # Edit Job
            job = get_object_or_404(Job, pk=pk, created_by=request.user) # Job.objects.get(pk=pk)
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
        """
        This is buggy need to remove it
        """
        post_data = post_data.copy()
        for n in range(int(post_data['jobkeywords_set-TOTAL_FORMS'])):
            # 'jobkeywords_set-4-tags': ['2', 'sadf', 'suhail'],  'jobkeywords_set-1-keyword': ['4'] 
            key1 = f'jobkeywords_set-{n}-keyword'
            key2 = f'jobkeywords_set-{n}-tags'
            if not post_data[key1].isdigit() and post_data[key1]:
                # print('keyword:',key1, post_data[key1])
                post_data.update({key1: str(Keyword.objects.get(name=post_data[key1]).pk)})

            tags = []
            for item in post_data.getlist(key2):
                if not item.isdigit():
                    # update post_data
                    tags.append(str(Tag.objects.get(name=item).pk))
                elif item:
                    tags.append(item)
            post_data.setlist(key2, tags) # https://stackoverflow.com/a/22210263/2351696
            
        return post_data

    def post(self, request, pk=None):
        if pk:
            # Edit Job
            job = get_object_or_404(Job, pk=pk, created_by=request.user) # Job.objects.get(pk=pk)
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
            try:
                self.parse_pdf_and_save(job)
            except:
                messages.warning(request, 'Unable to parse the PDF files.')
            messages.success(request, 'Job saved successfully.')
            return redirect('job:list')
        else:
            # print('|',form.errors,'++',formset.errors,'--',formset2.errors,'|')
            # reselect newly added keyword and tags
            post_data = self.on_error_set_newly_created_tags_and_keyword(request.POST)
            # need to update request.post with keywords and tags
            formset = self.frm2(post_data) 

        return render(request, self.template_name, {'jobform': form,'formset': formset,'formset2': formset2})

class JobDetailView(generic.DetailView):
    model = Job

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobkeywords'] = JobKeywords.objects.filter(job=context['job'])
        return context

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by!=self.request.user:
            raise Http404("Access Denied")
        return obj
    
class JobDeleteView(generic.edit.DeleteView):
    model = Job
    success_url = reverse_lazy('job:list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.created_by!=self.request.user:
            raise Http404("Access Denied")
        return obj