from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from .models import Note, Tag

# Utilitário: evita duplicar tags (case-insensitive)
def _get_or_create_tag(raw_name: str):
    name = (raw_name or "").strip()
    if not name:
        return None  # nota sem tag
    # tenta achar por nome, ignorando caixa
    tag = Tag.objects.filter(name__iexact=name).first()
    return tag or Tag.objects.create(name=name)

def index(request):
    """
    GET -> lista notas
    POST -> cria nova nota (title, content, tag opcional)
    """
    if request.method == 'POST':
        title = request.POST.get('titulo', '').strip()
        content = request.POST.get('detalhes', '').strip()
        tag_text = request.POST.get('tag', '').strip()  # novo campo do form

        if title and content:
            tag = _get_or_create_tag(tag_text)
            Note.objects.create(title=title, content=content, tag=tag)
        return redirect('index')

    notes_qs = Note.objects.select_related('tag').all()
    # (opcional) se você tiver created_at/updated_at
    if hasattr(Note, 'updated_at'):
        notes_qs = notes_qs.order_by('-updated_at')
    elif hasattr(Note, 'created_at'):
        notes_qs = notes_qs.order_by('-created_at')

    return render(request, 'notes/index.html', {'notes': notes_qs})

def update(request, pk):
    """
    GET -> mostra o form preenchido
    POST -> atualiza título/conteúdo/tag e volta pra home
    """
    note = get_object_or_404(Note, pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        content = request.POST.get('content', '').strip()
        tag_text = request.POST.get('tag', '').strip()  # novo campo no update

        if title and content:
            note.title = title
            note.content = content
            note.tag = _get_or_create_tag(tag_text)  # pode virar None se vazio
            note.save()
        return redirect('index')

    return render(request, 'notes/update.html', {'note': note})

def delete(request, pk):
    """
    POST -> apaga a nota e volta pra home
    GET  -> só redireciona (não apaga)
    """
    if request.method == 'POST':
        get_object_or_404(Note, pk=pk).delete()
        return redirect('index')
    return redirect('index')

def tag_list(request):
    """
    /tags/ -> lista todas as tags com contagem de notas
    """
    tags = Tag.objects.annotate(total=Count('notes')).order_by('name')
    return render(request, 'notes/tags_list.html', {'tags': tags})

def tag_detail(request, tag_id):
    """
    /tags/<id>/ -> mostra todas as notas que têm essa tag
    """
    tag = get_object_or_404(Tag, pk=tag_id)
    notes = Note.objects.filter(tag=tag).select_related('tag')
    return render(request, 'notes/tag_detail.html', {'tag': tag, 'notes': notes})
