from django.shortcuts import render, redirect
from ajax_datatable.views import AjaxDatatableView
from django.http import Http404
from django.contrib import messages
from django_hosts.resolvers import reverse

from myapp.models import Job, JobKeywords, Candidate
from myapp.forms import CandidateForm

get_company = lambda r: r.split('.')[0]


def companyview(request):
    company = get_company(request.get_host())
    if not Job.objects.filter(created_by__company=company):
        raise Http404("Access Denied")
    return render(request,'company/company.html',{'company': company})

# def applyjob(request,pk):
#     company = get_company(request.get_host())
#     job = Job.objects.filter(created_by__company=company, id=pk).first()
#     if not job:
#         # if somebody access subdomain that is not a company, eg: http://some.suhail.pw
#         raise Http404("Access Denied")

#     return render(request,'company/apply_job.html',{'company': company, 
#         'form':CandidateForm(),'job': job, 
#         'jobkeywords': JobKeywords.objects.filter(job=job)})


def applyjob(request,pk):
    company = get_company(request.get_host())
    job = Job.objects.filter(created_by__company=company, id=pk).first()
    if not job:
        # if somebody access subdomain that is not a company, eg: http://some.suhail.pw
        raise Http404("Access Denied")

    if request.method == 'POST':

        form = CandidateForm(request.POST,request.FILES)
        if form.is_valid():
            print('form save')
            candidate = form.save(commit=False)
            candidate.job = job
            candidate.save()
            messages.success(request, 'Job saved with success!')
            return redirect(f'/apply/{job.pk}/') # reverse('company:applyjob', args=(job.pk,), host='wildcard'))
            #)
        else:
            print('form errr')
    else:
        cand = Candidate(job = job)
        form = CandidateForm(instance=cand)

    return render(request,'company/apply_job.html',{'company': company, 
        'form':form,'job': job, 
        'jobkeywords': JobKeywords.objects.filter(job=job)})



class JobsAjaxDatatableView(AjaxDatatableView):
    model = Job
    initial_order = [["title", "asc"], ]

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'title', 'visible': True },
        {'name': 'description', 'visible': True, },
        {'name': 'department', 'visible': True, },
        {'name': 'apply', 'title': 'Apply Now', 'searchable': False, 'orderable': False, },
        {'name': 'category', 'visible': False},  
        # {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
    ]

    def get_initial_queryset(self, request=None):
        queryset = self.model.objects.all()
        if 'company' in request.REQUEST:
            company = get_company(request.REQUEST.get('company'))
            queryset = queryset.filter(created_by__company=company)
        
        return queryset


    def customize_row(self, row, obj):
        # https://github.com/morlandi/django-ajax-datatable#id42
        row['apply'] = """
            <a style="cursor:pointer" onclick="const id=this.closest('tr').id.substr(4);
                window.location.replace('/apply/'+id+'/');">
               Apply Job
            </a>
        """