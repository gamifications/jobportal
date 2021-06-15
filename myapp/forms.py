from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib import admin
from .models import Job, Candidate, JobKeywords, Keyword, Tag
from django.core.exceptions import ValidationError

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

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


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
        # create new keyword if not pk
        return Keyword.objects.get_or_create(name=value.title())[0]
        
class TagsChoiceField(forms.ModelMultipleChoiceField):
    def _check_values(self, value):
        """
        Bug: 
            what if there is an existing tag with id -> 44,
            and i want to create tag with name 44
            it will take tag with existing name 'laptop' instead of name 44
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
    keyword = KeywordChoiceField(queryset=Keyword.objects.all())
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
    extra=2,
    min_num=1,
    validate_min=True,
)

CandidateFormset = forms.inlineformset_factory(
    Job,
    Candidate,
    form=CandidateForm,
    extra=5,
    min_num=1,
    validate_min=True,
)