from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import Job

class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'title',
            Row(
                Column('department', css_class='form-group col-md-6 mb-0'),
                Column('category', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),            
            Row(
                Column('start_date', css_class='form-group col-md-4 mb-0'),
                Column('closing_date', css_class='form-group col-md-4 mb-0'),
                Column('salary_low', css_class='form-group col-md-2 mb-0'),
                Column('salary_high', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('reporting_line', css_class='form-group col-md-6 mb-0'),
                Column('stage', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            # Submit('submit', 'Add New Assignment')
        )
        self.helper.form_tag = False

    class Meta:
        model = Job
        fields = ['title','department','category','salary_low','salary_high','start_date',
            'closing_date','reporting_line','stage'] # '__all__'
	