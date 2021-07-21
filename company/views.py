from django.shortcuts import render, redirect
from ajax_datatable.views import AjaxDatatableView
from django.http import Http404
from django.contrib import messages
from django_hosts.resolvers import reverse

from myapp.models import Job, JobKeywords, Candidate, Company
from myapp.forms import CandidateForm

get_company = lambda r: r.split('.')[0]


def companyview(request):
    company = get_company(request.get_host())
    if not Company.objects.filter(slug=company):
        raise Http404("Company Doesn't Exist")
    return render(request,'company/company.html',{'company': company})

def jobdetails(request,pk):
    company = get_company(request.get_host())
    job = Job.objects.filter(created_by__company__slug=company, id=pk).first()
    if not job:
        # if somebody access subdomain that is not a company, eg: http://some.suhail.pw
        raise Http404("Job Doesn't Exist")
    return render(request,'company/job.html',{'company': company, 'job': job})

def applyjob(request,pk):
    company = get_company(request.get_host())
    job = Job.objects.filter(created_by__company__slug=company, id=pk).first()
    if not job:
        # if somebody access subdomain that is not a company, eg: http://some.suhail.pw
        raise Http404("Job Doesn't Exist")

    if request.method == 'POST':

        form = CandidateForm(request.POST,request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.job = job
            candidate.save()
            messages.success(request, 'Job submitted successfully!')
            return redirect(f'/') # reverse('company:applyjob', args=(job.pk,), host='wildcard'))
            
    else:
        cand = Candidate(job = job)
        form = CandidateForm(instance=cand)

    return render(request,'company/apply_job.html',{'company': company, 
        'form':form,'job': job})



class JobsAjaxDatatableView(AjaxDatatableView):
    model = Job
    initial_order = [["title", "asc"], ]

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'title', 'visible': True },
        {'name': 'department', 'visible': True, },
        {'name': 'category', 'visible': True},  
        {'name': 'apply', 'title': '', 'searchable': False, 'orderable': False, },
        {'name': 'description', 'visible': False, },
        # {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
    ]

    def get_initial_queryset(self, request=None):
        queryset = self.model.objects.all()
        if 'company' in request.REQUEST:
            company = get_company(request.REQUEST.get('company'))
            queryset = queryset.filter(created_by__company__slug=company)
        
            return queryset


    def customize_row(self, row, obj):
        # https://github.com/morlandi/django-ajax-datatable#id42
        row['apply'] = f"""
        <a class='btn btn-warning btn-sm' href='/job/{obj.id}/'>View Job</a>
        <a class='btn btn-success btn-sm' href='/apply/{obj.id}/'>Apply Job</a>
        """