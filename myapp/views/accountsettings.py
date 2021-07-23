from PIL import Image
import os

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.conf import settings

from myapp.models import Company
from myapp.forms import validate_company_slug

@method_decorator([login_required], name='dispatch')
class Profile(View):
    # even inactive users can view/edit their profile
    def get(self, request):
        return render(request,'settings/profile.html')

    def post(self,request):
        # user_id=request.POST['user']
        user = request.user #User.objects.get(id = user_id)

        username = request.POST.get('username', '')
        if len(username) < 3:
            messages.error(request, 'Error: Username must have atleast 3 characters.')
            return redirect('job:profile')

        if username != user.username:
            # if username doesn't changed while editing
            if get_user_model().objects.filter(username=username).exists():
                messages.error(request, 'Error: Username already exists.')
                return redirect('job:profile')
            user.username = username    

        
        user.first_name = request.POST.get('first_name','')
        user.last_name = request.POST.get('last_name', '')
        # user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, 'User details of {} saved with success!'.format(user.username))
        return redirect('job:profile')



@method_decorator([login_required], name='dispatch')
class CompanyView(View):
    # company view
    def get(self, request):
        return render(request,'settings/company.html')

    def resize_rectangular_image(self, fname):
        '''
        https://stackoverflow.com/a/55489909/2351696
        Reshapes the non-square image by pasting
        it to the centre of a black canvas of size
        n*n where n is the biggest dimension of
        the non-square image. 
        '''
        image = Image.open(os.path.join(settings.MEDIA_ROOT,fname))
        image.save(os.path.join(settings.MEDIA_ROOT,f'original_{fname}'))
        max_dimension, min_dimension = max(image.size), min(image.size)
        desired_size = (max_dimension, int(max_dimension/2))
        position = int(max_dimension/2) - int(min_dimension/2) 
        blank_image = Image.new("RGB", desired_size, color='white')
        if image.height<image.width:
            blank_image.paste(image, (0, position))
        else:
            blank_image.paste(image, (position, 0))

        blank_image.save(os.path.join(settings.MEDIA_ROOT,fname)) # f'rect_{fname}'))

    def post(self,request):
        user = request.user 
        slug = request.POST.get('slug', '')
        msg = validate_company_slug(slug.lower(), user.company if hasattr(user, 'company') else None)
        if msg != 'success':
            messages.error(request, f'Error: {msg}')
            return redirect('job:company')

        if hasattr(user, 'company'):
            company = user.company
            company.slug=slug
            company.name=request.POST['name']
            company.description = request.POST['description']
        else:
            company=Company.objects.create(user=user, slug=slug, 
                name=request.POST['name'],description = request.POST['description'])

        if request.FILES.get('logo'):
            company.logo = request.FILES['logo']

        if request.FILES.get('cover'):
            company.cover = request.FILES['cover']
        company.save()
        if request.FILES.get('cover'):
            self.resize_rectangular_image(company.cover.name)
        
        messages.success(request, 'Company details of {} saved with success!'.format(company.slug))
        return redirect('job:company')

@login_required
def billing(request):
  return render(request, "settings/billing.html",{'subscription':request.user.subscription})
