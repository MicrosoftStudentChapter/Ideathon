from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


MOBILE_REGEX = "^(\+\d{1,3}[- ]?)?\d{10}$"  # noqa


class Team(models.Model):
    '''Model for teams'''
    team_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    ppt_url = models.URLField()
    tech_stack = models.CharField(max_length=255, blank=True, null=True)
    leader_mobile = models.CharField(
        max_length=16,
        validators=[
            RegexValidator(
                regex=MOBILE_REGEX,
                message="Enter a valid mobile number",
                code="invalid_mobile",
            )
        ],
    )
    created_by = models.ForeignKey(
        User,
        related_name="collections",
        blank=True, null=True,
        on_delete=models.SET_NULL
    )

    def __str__(self):
        return f"Registration for {self.team_name}"


class TeamMember(models.Model):
    '''Model for team members'''
    YEAR_CHOICES = (
        ('1', 'First'),
        ('2', 'Second')
    )
    name = models.CharField(max_length=255)
    roll_number = models.CharField(max_length=9)
    year = models.CharField(max_length=1, choices=YEAR_CHOICES)
    team = models.ForeignKey(
        Team,
        related_name='members',
        on_delete=models.CASCADE
    )
    discord_id = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"