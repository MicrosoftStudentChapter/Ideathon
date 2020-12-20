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
    can_delete=True
)


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        exclude = ()

    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3 create-label'
        self.helper.field_class = 'col-md-9'
        self.helper.layout = Layout(
            Div(
                Field('team_name'),
                Field('project_name'),
                Field('ppt_url'),
                Field('tech_stack'),
                Field('leader_email'),
                Field('leader_mobile'),
                Fieldset('Add Members',
                    Formset('members')),
                Field('note'),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'save')),
                )
            )