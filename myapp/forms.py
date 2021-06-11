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
        # https://stackoverflow.com/a/30325345/2351696
        if isinstance(value, str):
            # create keyword if not pk
            return Keyword.objects.get_or_create(name=value)[0]
        return super().to_python(value)
        
class TagsChoiceField(forms.ModelMultipleChoiceField):
    def to_python(self, value):
        print(value)
        for pk in value:
            print(type(pk))
        return super().to_python(value)

class JobKeywordsForm(forms.ModelForm):
    keyword = KeywordChoiceField(queryset=Keyword.objects.all())
    # tags = TagsChoiceField(queryset=Tag.objects.all())
    class Meta:
        model = JobKeywords
        fields = ['job','keyword','tags'] # '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    def save(self, commit=True):
        # https://stackoverflow.com/a/4137576/2351696
        keyword_name = self.cleaned_data['keyword']
        print(keyword_name)
        # keyword = Keyword.objects.get_or_create(name=keyword_name)[0]
        # self.instance.keyword = keyword
        return super().save(commit)


KeywordFormset = forms.inlineformset_factory(
    Job,
    JobKeywords,
    # fields=('keyword', 'tags'),
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

) # fields=('name', 'jobtitle','salary'),extra=5)


