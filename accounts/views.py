from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.contrib import messages


class EduTrackLoginView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


def edutrack_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

