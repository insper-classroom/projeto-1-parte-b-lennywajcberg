from django.shortcuts import render, redirect, get_object_or_404
from .models import Note

def index(request):
    # LISTAR + CRIAR
    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '').strip()

        if title and content:
            Note.objects.create(title=title, content=content)
        return redirect('index')

    notes_qs = Note.objects.all()
    if hasattr(Note, 'updated_at'):
        notes_qs = notes_qs.order_by('-updated_at')
    elif hasattr(Note, 'created_at'):
        notes_qs = notes_qs.order_by('-created_at')

    return render(request, 'notes/index.html', {'notes': notes_qs})


def update(request, pk):
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()

        if title and content:
            note.title = title
            note.content = content
            note.save()
        return redirect('index')

    return render(request, 'notes/update.html', {'note': note})


def delete(request, pk):
    if request.method == 'POST':
        note = get_object_or_404(Note, pk=pk)
        note.delete()
        return redirect('index')
    return redirect('index')
