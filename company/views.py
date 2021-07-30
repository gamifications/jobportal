from django.shortcuts import render, redirect
from ajax_datatable.views import AjaxDatatableView
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django_hosts.resolvers import reverse

from myapp.models import Job, JobKeywords, Candidate, Company
from myapp.forms import CandidateForm


def get_company_or_404(host):
    company_slug = host.split('.')[0]
    company = Company.objects.filter(slug=company_slug).first()
    if company:
        return company
    raise Http404("Company Doesn't Exist")

def get_job_or_404(host,pk):
    company = get_company_or_404(host)
    job = Job.objects.filter(created_by__company=company, id=pk).exclude(stage='hired').first()
    if job:
        return job
    raise Http404("Job Doesn't Exist")

def jobs(request):
    company = get_company_or_404(request.get_host())
    jobs = Job.objects.filter(created_by__company=company).exclude(stage='hired')
    return render(request,'company/jobs.html',{'jobs': jobs, 'company':company})

def companyview(request):
    company = get_company_or_404(request.get_host())
    return render(request,'company/company.html',{'company': company})
    

def jobdetails(request,pk):
    job = get_job_or_404(request.get_host(),pk)

    return render(request,'company/job.html',{'company': job.created_by.company, 'job': job})

def applyjob(request,pk):
    job = get_job_or_404(request.get_host(),pk)

    if request.method == 'POST':

        form = CandidateForm(request.POST,request.FILES)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.job = job
            candidate.save()
            messages.success(request, 'Job submitted successfully!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER')) # redirect() # reverse('company:applyjob', args=(job.pk,), host='wildcard'))
            
    else:
        cand = Candidate(job = job)
        form = CandidateForm(instance=cand)

    return render(request,'company/apply_job.html',{'company': job.created_by.company, 
        'form':form,'job': job})


# Need to delete this, since datatable is used in company page
# and it needs to modify.
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
            company = request.REQUEST['company'].split('.')[0]
            queryset = queryset.filter(created_by__company__slug=company)
        
            return queryset


    def customize_row(self, row, obj):
        # https://github.com/morlandi/django-ajax-datatable#id42
        row['apply'] = f"""
        <a class='btn btn-warning btn-sm' href='/job/{obj.id}/'>View Job</a>
        <a class='btn btn-success btn-sm' href='/apply/{obj.id}/'>Apply Job</a>
        """