from django.shortcuts import render
from ajax_datatable.views import AjaxDatatableView

from myapp.models import Job

def applyjob(request):
    return render(request,'company/apply_job.html',{'company': request.get_host().split('.')[0]})

class JobsAjaxDatatableView(AjaxDatatableView):
    model = Job
    initial_order = [["title", "asc"], ]

    column_defs = [
        AjaxDatatableView.render_row_tools_column_def(),
        {'name': 'id', 'visible': False, },
        {'name': 'title', 'visible': True },
        {'name': 'description', 'visible': True, },
        {'name': 'department', 'visible': True, },
        {'name': 'category', 'visible': False},  
        # {'name': 'app_label', 'foreign_field': 'content_type__app_label', 'visible': True, },
    ]

    def get_initial_queryset(self, request=None):
    	queryset = self.model.objects.all()
    	if 'company' in request.REQUEST:
            company = request.REQUEST.get('company').split('.')[0]
            print(company)
            queryset = queryset.filter(created_by__company=company)
    	
    	return queryset