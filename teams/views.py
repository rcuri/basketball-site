from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def displayteams(request, username):
    """
    Display requesting username's teams only if username matches logged in
    user's username.
    """
    if request.user.username != username:
        return redirect('index')
    teams = request.user.profile.team_set.all()
    return render(request, 'teams/displayteams.html', {'teams': teams})
