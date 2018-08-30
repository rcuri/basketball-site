from django.shortcuts import render

# Create your views here.
def displayteams(request, username):
    teams = request.user.profile.team_set.all()
    return render(request, 'teams/displayteams.html', {'teams': teams})
