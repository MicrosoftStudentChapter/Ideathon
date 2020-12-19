from django.db import models


class Team(models.Model):
    '''Model for teams'''
    team_name = models.CharField(max_length=255)
    project_name = models.CharField(max_length=255)
    ppt_url = models.URLField()
    tech_stack = models.CharField(max_length=255, required=False)

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

    def __str__(self):
        return f"{self.name}"