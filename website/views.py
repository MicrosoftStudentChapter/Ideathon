from .models import *
from .forms import *

from django.contrib.auth import authenticate, login, logout
from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from django.db import IntegrityError
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy, reverse
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("website:homepage"))
        else:
            return render(request, "website/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "website/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("website:homepage"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "website/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "website/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("website:homepage"))
    else:
        return render(request, "website/register.html")


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


@method_decorator(login_required, name='dispatch')
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
        return reverse_lazy('website:team_detail', kwargs={'pk': self.object.pk})


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
        return reverse_lazy('website:team_detail', kwargs={'pk': self.object.pk})
