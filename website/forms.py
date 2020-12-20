# Collection title -- Team Member - Child
# collection -- team - parent

from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        exclude = ()
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                },
            ),
            'roll_number': forms.TextInput(
                attrs={
                    'class': 'form-control'
                },
            ),
            'year': forms.Select(
                attrs={
                    'class': 'custom-select'
                },
            ),
            'discord_id': forms.TextInput(
                attrs={
                    'class': 'form-control'
                },
            ),
        }


TeamMemberFormSet = inlineformset_factory(
    Team,
    TeamMember,
    form=TeamMemberForm,
    fields=[
        'name',
        'roll_number',
        'year',
        'discord_id',
    ],
    extra=1,
    can_delete=True,
    max_num=3,
)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = ''
        self.helper.label_class = 'form-label'
        self.helper.field_class = 'form-control'
        self.helper.layout = Layout(
            Div(
                Field('team_name', css_class="form-control"),
                HTML("<br>"),
                Field('project_name', css_class="form-control"),
                HTML("<br>"),
                Field('project_name', css_class="form-control"),
                HTML("<br>"),
                Field('ppt_url', css_class="form-control"),
                HTML("<br>"),
                Field('tech_stack', css_class="form-control"),
                HTML("<br>"),
                Field('leader_mobile', css_class="form-control"),
                HTML("<br>"),
                Fieldset('Add Members',
                    Formset('members')),
                Field('note'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )