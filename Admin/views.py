import base.models as models
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def AdminPage(request):
    table_heads = ['Name', 'Username', "Email", "Bio", 'Action']
    users = models.User.objects.filter(is_active=True)

    context = {
        'users': users,
        'page_title': 'Users',
        'table_heads': table_heads,
    }

    return render(request, 'admin/users.html', context)


@login_required(login_url='login')
def EditUser(request):
    if request.method.lower() == 'post':
        bio = request.POST.get('bio', '').strip()
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = models.User.objects.get(email=email)

        if name:
            user.name = name

        if username:
            user.username = username

        if bio:
            user.bio = bio

        if password:
            user.set_password(password)

        user.save()

        return JsonResponse({'status': True, 'message': 'User info edited successfully'})

    return JsonResponse({'status': False, 'message': 'Something went wrong'})


@login_required(login_url='login')
def AddUser(request):
    if request.method.lower() == 'post':
        name = request.POST.get('name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        bio = request.POST.get('bio', '').strip()
        password = request.POST.get('password', '').strip()

        if models.User.objects.filter(email=email):
            return JsonResponse({'status': False, 'message': 'Email already exists'})

        user = models.User(email=email, username=username, name=name, bio=bio)
        user.set_password(password)
        user.save()

        return JsonResponse({'status': True, 'message': 'User added successfully'})

    return JsonResponse({'status': False, 'message': 'Something went wrong'})


@login_required(login_url='login')
def DeleteUser(request):
    try:
        email = request.GET.get('email', '')

        user = models.User.objects.get(email=email, is_active=True)
        user.is_active = False
        user.save()

        return JsonResponse({'status': True, 'message': 'User deleted successfully'})

    except models.User.DoesNotExist:
        return JsonResponse({'status': False, 'message': 'User not found'})


@login_required(login_url='login')
def RoomsPage(request):
    table_heads = ['Host', 'Room Name', "Description", "Topic", 'Creation Date', 'Action']
    rooms = models.Room.objects.all()

    context = {
        'rooms': rooms,
        'page_title': 'Rooms',
        'table_heads': table_heads,
    }

    return render(request, 'admin/rooms.html', context)


@login_required(login_url='login')
def TopicsPage(request):
    table_heads = ['Host', 'Topic Name']
    topics = models.Room.objects.all()

    context = {
        'topics': topics,
        'page_title': 'Topics',
        'table_heads': table_heads,
    }

    return render(request, 'admin/topics.html', context)


@login_required(login_url='login')
def MessagesPage(request):
    table_heads = ['User', 'Room Name', "Description", 'Creation Date', 'Action']
    messages = models.Message.objects.all()

    context = {
        'messages': messages,
        'page_title': 'Messages',
        'table_heads': table_heads,
    }

    return render(request, 'admin/messages.html', context)
