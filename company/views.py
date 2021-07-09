from django.shortcuts import render

def applyjob(request):
    return render(request,'company/apply_job.html',{'company': request.get_host().split('.')[0]})
