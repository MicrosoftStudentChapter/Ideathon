from .models import *
from .forms import *
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.db import transaction


class HomepageView(TemplateView):
    template_name = "website/base.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teams'] = Team.objects.order_by('id')
        return context


class TeamDetailView(DetailView):
    model = Team
    template_name = 'website/team_detail.html'

    def get_context_data(self, **kwargs):
        context = super(TeamDetailView, self).get_context_data(**kwargs)
        return context


class TeamCreate(CreateView):
    model = Team
    template_name = 'website/team_create.html'
    form_class = TeamForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(TeamCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['members'] = TeamMemberFormSet(self.request.POST)
        else:
            data['members'] = TeamMemberFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        members = context["members"]
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if members.is_valid():
                members.instance = self.object
                members.save()
        return super(TeamCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('website:collection_detail', kwargs={'pk': self.object.pk})


class TeamUpdate(UpdateView):
    model = Team
    template_name = 'website/team_create.html'
    form_class = TeamForm
    success_url = None

    def get_context_data(self, **kwargs):
        data = super(TeamUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['members'] = TeamMemberFormSet(self.request.POST, instance=self.object)
        else:
            data['members'] = TeamMemberFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        members = context["members"]
        with transaction.atomic():
            form.instance.created_by = self.request.user
            self.object = form.save()
            if members.is_valid():
                members.instance = self.object
                self.object = form.save()
        return super(TeamUpdate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('website:collection_detail', kwargs={'pk': self.object.pk})
