import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count
from .models import LegalCase, LegalClient, LegalTimeEntry


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/dashboard/')
    error = ''
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/dashboard/')
        error = 'Invalid credentials. Try admin / Admin@2024'
    return render(request, 'login.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required
def dashboard_view(request):
    ctx = {}
    ctx['legalcase_count'] = LegalCase.objects.count()
    ctx['legalcase_civil'] = LegalCase.objects.filter(case_type='civil').count()
    ctx['legalcase_criminal'] = LegalCase.objects.filter(case_type='criminal').count()
    ctx['legalcase_corporate'] = LegalCase.objects.filter(case_type='corporate').count()
    ctx['legalclient_count'] = LegalClient.objects.count()
    ctx['legalclient_individual'] = LegalClient.objects.filter(client_type='individual').count()
    ctx['legalclient_corporate'] = LegalClient.objects.filter(client_type='corporate').count()
    ctx['legalclient_total_total_billed'] = LegalClient.objects.aggregate(t=Sum('total_billed'))['t'] or 0
    ctx['legaltimeentry_count'] = LegalTimeEntry.objects.count()
    ctx['legaltimeentry_research'] = LegalTimeEntry.objects.filter(activity='research').count()
    ctx['legaltimeentry_drafting'] = LegalTimeEntry.objects.filter(activity='drafting').count()
    ctx['legaltimeentry_court'] = LegalTimeEntry.objects.filter(activity='court').count()
    ctx['legaltimeentry_total_hours'] = LegalTimeEntry.objects.aggregate(t=Sum('hours'))['t'] or 0
    ctx['recent'] = LegalCase.objects.all()[:10]
    return render(request, 'dashboard.html', ctx)


@login_required
def legalcase_list(request):
    qs = LegalCase.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(case_type=status_filter)
    return render(request, 'legalcase_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def legalcase_create(request):
    if request.method == 'POST':
        obj = LegalCase()
        obj.title = request.POST.get('title', '')
        obj.case_number = request.POST.get('case_number', '')
        obj.client_name = request.POST.get('client_name', '')
        obj.case_type = request.POST.get('case_type', '')
        obj.status = request.POST.get('status', '')
        obj.court = request.POST.get('court', '')
        obj.next_hearing = request.POST.get('next_hearing') or None
        obj.save()
        return redirect('/legalcases/')
    return render(request, 'legalcase_form.html', {'editing': False})


@login_required
def legalcase_edit(request, pk):
    obj = get_object_or_404(LegalCase, pk=pk)
    if request.method == 'POST':
        obj.title = request.POST.get('title', '')
        obj.case_number = request.POST.get('case_number', '')
        obj.client_name = request.POST.get('client_name', '')
        obj.case_type = request.POST.get('case_type', '')
        obj.status = request.POST.get('status', '')
        obj.court = request.POST.get('court', '')
        obj.next_hearing = request.POST.get('next_hearing') or None
        obj.save()
        return redirect('/legalcases/')
    return render(request, 'legalcase_form.html', {'record': obj, 'editing': True})


@login_required
def legalcase_delete(request, pk):
    obj = get_object_or_404(LegalCase, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/legalcases/')


@login_required
def legalclient_list(request):
    qs = LegalClient.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(name__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(client_type=status_filter)
    return render(request, 'legalclient_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def legalclient_create(request):
    if request.method == 'POST':
        obj = LegalClient()
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.client_type = request.POST.get('client_type', '')
        obj.company = request.POST.get('company', '')
        obj.active_cases = request.POST.get('active_cases') or 0
        obj.total_billed = request.POST.get('total_billed') or 0
        obj.retainer = request.POST.get('retainer') == 'on'
        obj.save()
        return redirect('/legalclients/')
    return render(request, 'legalclient_form.html', {'editing': False})


@login_required
def legalclient_edit(request, pk):
    obj = get_object_or_404(LegalClient, pk=pk)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '')
        obj.email = request.POST.get('email', '')
        obj.phone = request.POST.get('phone', '')
        obj.client_type = request.POST.get('client_type', '')
        obj.company = request.POST.get('company', '')
        obj.active_cases = request.POST.get('active_cases') or 0
        obj.total_billed = request.POST.get('total_billed') or 0
        obj.retainer = request.POST.get('retainer') == 'on'
        obj.save()
        return redirect('/legalclients/')
    return render(request, 'legalclient_form.html', {'record': obj, 'editing': True})


@login_required
def legalclient_delete(request, pk):
    obj = get_object_or_404(LegalClient, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/legalclients/')


@login_required
def legaltimeentry_list(request):
    qs = LegalTimeEntry.objects.all()
    search = request.GET.get('search', '')
    if search:
        qs = qs.filter(case_title__icontains=search)
    status_filter = request.GET.get('status', '')
    if status_filter:
        qs = qs.filter(activity=status_filter)
    return render(request, 'legaltimeentry_list.html', {'records': qs, 'search': search, 'status_filter': status_filter})


@login_required
def legaltimeentry_create(request):
    if request.method == 'POST':
        obj = LegalTimeEntry()
        obj.case_title = request.POST.get('case_title', '')
        obj.attorney = request.POST.get('attorney', '')
        obj.hours = request.POST.get('hours') or 0
        obj.rate = request.POST.get('rate') or 0
        obj.amount = request.POST.get('amount') or 0
        obj.date = request.POST.get('date') or None
        obj.activity = request.POST.get('activity', '')
        obj.description = request.POST.get('description', '')
        obj.billable = request.POST.get('billable') == 'on'
        obj.save()
        return redirect('/legaltimeentries/')
    return render(request, 'legaltimeentry_form.html', {'editing': False})


@login_required
def legaltimeentry_edit(request, pk):
    obj = get_object_or_404(LegalTimeEntry, pk=pk)
    if request.method == 'POST':
        obj.case_title = request.POST.get('case_title', '')
        obj.attorney = request.POST.get('attorney', '')
        obj.hours = request.POST.get('hours') or 0
        obj.rate = request.POST.get('rate') or 0
        obj.amount = request.POST.get('amount') or 0
        obj.date = request.POST.get('date') or None
        obj.activity = request.POST.get('activity', '')
        obj.description = request.POST.get('description', '')
        obj.billable = request.POST.get('billable') == 'on'
        obj.save()
        return redirect('/legaltimeentries/')
    return render(request, 'legaltimeentry_form.html', {'record': obj, 'editing': True})


@login_required
def legaltimeentry_delete(request, pk):
    obj = get_object_or_404(LegalTimeEntry, pk=pk)
    if request.method == 'POST':
        obj.delete()
    return redirect('/legaltimeentries/')


@login_required
def settings_view(request):
    return render(request, 'settings.html')


@login_required
def api_stats(request):
    data = {}
    data['legalcase_count'] = LegalCase.objects.count()
    data['legalclient_count'] = LegalClient.objects.count()
    data['legaltimeentry_count'] = LegalTimeEntry.objects.count()
    return JsonResponse(data)
