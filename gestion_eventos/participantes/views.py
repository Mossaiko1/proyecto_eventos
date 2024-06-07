from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ParticipantForm
from .models import Participant
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Participant

def participant_list(request):
    form = ParticipantForm(request.POST or None)
    participants = Participant.objects.all()
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, 'Participante registrado con éxito.')
            return redirect('participant_list')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrar el participante: {e}')
    return render(request, "participantes/participant_list.html", {'form': form, 'participants': participants})

def confirm_delete_participant(request, participant_id):
    participant = get_object_or_404(Participant, id=participant_id)
    
    if request.method == 'POST':
        participant.delete()
        messages.success(request, 'El participante ha sido eliminado con éxito.')
        return redirect('participant_list')
    
    return render(request, 'participantes/confirm_delete_participant.html', {'participant': participant})

def delete_participant(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
        participant.delete()
        messages.success(request, 'Participante eliminado con éxito.')
    except Participant.DoesNotExist:
        messages.error(request, 'El participante no existe.')
    return redirect('participant_list')

def edit_participant(request, participant_id):
    try:
        participant = Participant.objects.get(id=participant_id)
    except Participant.DoesNotExist:
        messages.error(request, 'El participante no existe.')
        return redirect('participant_list')

    form = ParticipantForm(request.POST or None, instance=participant)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, 'Participante actualizado con éxito.')
            return redirect('participant_list')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al actualizar el participante: {e}')
    return render(request, "participantes/edit_participant.html", {'form': form})

@csrf_exempt
def change_status(request):
    if request.method == 'POST':
        participant_id = request.POST.get('id')
        new_status = request.POST.get('status') == 'true'
        try:
            participant = Participant.objects.get(id=participant_id)
            participant.status = new_status
            participant.save()
            return JsonResponse({'success': True})
        except Participant.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Participant not found'})
    return JsonResponse({'success': False, 'error': 'Invalid request'})