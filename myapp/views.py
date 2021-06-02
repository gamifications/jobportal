from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views import View

from django.contrib import messages
from django.contrib.auth import get_user_model

@method_decorator([login_required], name='dispatch')
class Profile(View):
    # even inactive users can view/edit their profile
    def get(self, request):
        return render(request,'myapp/home.html')

    def post(self,request):
        # user_id=request.POST['user']
        user = request.user #User.objects.get(id = user_id)
        
        user.first_name = request.POST.get('first_name','')
        user.last_name = request.POST.get('last_name', '')
        user.save()
        messages.success(request, 'User details of {} saved with success!'.format(user.username))
        return redirect('home')


