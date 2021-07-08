import re
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import Job, Candidate, JobKeywords, Keyword, Tag

class JobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            # 'title',
            Row(
                Column('title', css_class='form-group col-md-4 mb-0'),
                Column('description', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),     
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

    # def clean(self):
    #     """ Bug: if error, Keyword Form all tags are required"""
    #     cleaned_data = super().clean()
    #     if cleaned_data.get("closing_date")<cleaned_data.get("start_date"):
    #         raise forms.ValidationError("Closing date should be greater than start date.")

    #     if cleaned_data.get("salary_high")<cleaned_data.get("salary_low"):
    #         raise forms.ValidationError("Salary high should be greater than Salary low.")
    #     return cleaned_data


    class Meta:
        model = Job
        fields = ['title','description','department','category','salary_low','salary_high','start_date',
            'closing_date','reporting_line','stage'] # '__all__'

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.use_custom_control = False
        self.fields['resume_data'].widget.attrs = {'rows': 4}
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-3 mb-0'),
                Column('email', css_class='form-group col-md-3 mb-0'),
                Column('jobtitle', css_class='form-group col-md-3 mb-0'),
                Column('salary', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('resume_data',css_class='form-group col-md-8 mb-0'),
                Column('resume', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.form_tag = False


class KeywordChoiceField(forms.ModelChoiceField):
    def to_python(self, value):
        """
        Bug: 
            what if there is an existing keyword with id -> 44,
            and i want to create keyword with name 44
            it will take keyword with existing name 'laptop' instead of name 44
        """

        # https://stackoverflow.com/a/30325345/2351696
        if value.isdigit() and Keyword.objects.filter(id=value):
            return super().to_python(value)
        # if not re.match(r'^[A-Za-z]', value):
        #     raise ValidationError('Keyword must startwith Character.', code='character')

        # create new keyword if not pk
        return Keyword.objects.get_or_create(name=value.title())[0] if value else None
        
class TagsChoiceField(forms.ModelMultipleChoiceField):
    def _check_values(self, value):
        """
        Bug: 
            what if there is an existing tag with id -> 44,
            and i want to create tag with name 44
            it will take tag with existing name 'laptop' instead of name 44

        Bug2: Django model validator not working(min_length=2)
        """
        new_value = []
        for pk in value:            
            if pk.isdigit() and Tag.objects.filter(id=pk):
                # tag is existing
                new_value.append(pk)
            else:
                # new tag
                new_tag = Tag.objects.get_or_create(name=pk.lower())[0]
                new_value.append(str(new_tag.pk))
        return super()._check_values(new_value)

class JobKeywordsForm(forms.ModelForm):
    """
    Bug: Django model validator not working(min_length=2)
    """
    keyword = KeywordChoiceField(queryset=Keyword.objects.all(), required=True)
    tags = TagsChoiceField(queryset=Tag.objects.all())
    class Meta:
        model = JobKeywords
        fields = ['job','keyword','tags'] # '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        self.fields['keyword'].empty_label = ''

KeywordFormset = forms.inlineformset_factory(
    Job,
    JobKeywords,
    form=JobKeywordsForm,
    can_delete=True,
    extra=4,
    min_num=1,
    validate_min=True,
)

CandidateFormset = forms.inlineformset_factory(
    Job,
    Candidate,
    form=CandidateForm,
    extra=1,
    min_num=0,
    # validate_min=True,
)