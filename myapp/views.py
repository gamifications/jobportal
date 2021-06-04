from django import forms
from django.views import generic
from django.urls import reverse_lazy
from myapp.models import Job, Keyword, Candidate, JobKeywords
from django.shortcuts import render
from django.forms import inlineformset_factory
class JobListView(generic.list.ListView):
    """Return list of all jobs"""
    model = Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title'] #['title'] #,'keywords'] #'__all__'


def job_view(request):
    KeywordFormset = inlineformset_factory(Job,JobKeywords,fields=('keyword', 'tags'),extra=5)
    if request.method == 'POST':
        print(request.POST)
        # <QueryDict: 'jobkeywords_set-TOTAL_FORMS': ['5'], 'jobkeywords_set-INITIAL_FORMS': ['0'], 
        # 'jobkeywords_set-MIN_NUM_FORMS': ['0'], 'jobkeywords_set-MAX_NUM_FORMS': ['1000'], 
        # 'title': ['Software developer'], 'jobkeywords_set-0-keyword': ['8'], 
        # 'jobkeywords_set-0-tags': ['python', 'django'], 'jobkeywords_set-1-keyword': [''], 
        #'jobkeywords_set-2-keyword': [''], 'jobkeywords_set-3-keyword': [''], 'jobkeywords_set-4-keyword': ['']}>

        
    form = JobForm()
    formset = KeywordFormset() # (instance=question)
    return render(request, 'myapp/job_form.html', {'form': form,'formset': formset})

class JobCreateView(generic.edit.CreateView):
    form_class = JobForm
    model = Job
    success_url = reverse_lazy('job:list')

    def post(self, request, *args, **kwargs):
        print(request.POST)
        # {'csrfmiddlewaretoken': ['BlGXXgfwJW9FTfEBTMeHBaMOuLKyIv6NSfcgccRTvD0puKcwAnEgteMOsHAhYmWH'], 
        # 'title': ['Software'], 'created_by': ['1'], 'keywords': ['suhail', 'sufail']}

        post = request.POST.copy() # to make it mutable

        post.setlist('keywords',[Keyword.objects.get_or_create(name=k)[0].id for k in request.POST.getlist('keywords')])
        # or set several values from dict
        # post.update({'postvar': 'some_value', 'var': 'value'})
        # or set list
        # post.setlist('list_var', ['some_value', 'other_value']))
        print(post)

        # and update original POST in the end
        request.POST = post
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        print(form.instance)
        print(self.request.POST, 'post data')
        import json
        print(self.request.body)
        print(self.request.POST.getlist('keywords'), 'post data')
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super().form_valid(form)