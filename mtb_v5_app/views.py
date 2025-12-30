

from django.shortcuts import render
from django.http import JsonResponse
from .models import Media, History

def home(request):
    current_phase = request.GET.get('phase', '01').zfill(2)  # Ensure phase is a string with leading zeros
    media_list = Media.objects.filter(phase=current_phase)
    history_list = History.objects.filter(phase=current_phase)
    phases = [(1, '1959 - 1962'), (2, '1962 - 1966'), (3, '1966 - 1970'), (4, '1970 - 9999'), (5, 'Karaokes')]

    context = {
        'current_phase': current_phase,
        'media_list': media_list,
        'history_list': history_list,
        'phases': [(str(phase).zfill(2), label) for phase, label in phases]  # Ensure phases are strings with leading zeros
    }
    
    return render(request, 'home.html', context)


def health(request):
    """Simple health check for uptime / monitoring."""
    return JsonResponse({'status': 'ok'})
