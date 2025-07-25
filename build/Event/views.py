from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CongregateMember, MosqueCommunity, HeadOfMosqueCommunity
from .models import Event
from .models import Booking
from .models import Payment
from .models import BookingReport

def homepage(request):
    return render(request, 'homepage.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        role = None

        if CongregateMember.objects.filter(con_name=username, con_password=password).exists():
            role = 'congregate'
        elif MosqueCommunity.objects.filter(mc_name=username, mc_password=password).exists():
            role = 'community'
        elif HeadOfMosqueCommunity.objects.filter(homc_name=username, homc_password=password).exists():
            role = 'head'

        if role:
            request.session['username'] = username
            request.session['role'] = role

            messages.success(request, f"Logged in as {role.capitalize()}")

            if role == 'congregate':
                return redirect('homecon')
            elif role == 'community':
                return redirect('homemos')
            elif role == 'head':
                return redirect('homehead')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('homepage')

def signup_view(request):
    if request.method == 'POST':
        name = request.POST.get('name').strip()
        phone = request.POST.get('phone')
        role = request.POST.get('role')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not name or not role:
            messages.error(request, 'Full name and role are required.')
            return render(request, 'signup.html', request.POST)

        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'signup.html', request.POST)

        if role == 'congregate':
            if not phone:
                messages.error(request, 'Phone number is required for Congregate Member.')
                return render(request, 'signup.html', request.POST)
            if CongregateMember.objects.filter(con_name=name).exists():
                messages.error(request, 'Congregate Member already exists.')
                return render(request, 'signup.html', request.POST)
            CongregateMember.objects.create(
                con_name=name,
                con_password=password1,
                con_phone_number=phone
            )
            messages.success(request, 'Congregate Member registered successfully.')

        elif role == 'community':
            if not phone:
                messages.error(request, 'Phone number is required for Mosque Community.')
                return render(request, 'signup.html', request.POST)
            if MosqueCommunity.objects.filter(mc_name=name).exists():
                messages.error(request, 'Mosque Community member already exists.')
                return render(request, 'signup.html', request.POST)
            MosqueCommunity.objects.create(
                mc_name=name,
                mc_password=password1,
                mc_phone_number=phone
            )
            messages.success(request, 'Mosque Community member registered successfully.')

        elif role == 'head':
            if HeadOfMosqueCommunity.objects.filter(homc_name=name).exists():
                messages.error(request, 'Head of Mosque Community already exists.')
                return render(request, 'signup.html', request.POST)
            HeadOfMosqueCommunity.objects.create(
                homc_name=name,
                homc_password=password1,
                homc_phone_number=phone or ''
            )
            messages.success(request, 'Head of Mosque Community registered successfully.')

        else:
            messages.error(request, 'Invalid role selected.')
            return render(request, 'signup.html', request.POST)

        return redirect('login')

    return render(request, 'signup.html')

def homecon_view(request):
    username = request.session.get('username')
    return render(request, 'homecon.html', {'username': username})

def homemos_view(request):
    username = request.session.get('username')
    return render(request, 'homemos.html', {'username': username})

def homehead_view(request):
    username = request.session.get('username')
    return render(request, 'homehead.html', {'username': username})

def event_schedule1_view(request):
    username = request.session.get('username')

    if request.method == 'POST':
        event_id = request.POST.get('delete_event_id')
        if event_id:
            Event.objects.filter(event_id=event_id).delete()
            return redirect('event_schedule1')

    events = Event.objects.all()
    context = {
        'events': events,
        'username': username,
    }
    return render(request, 'event_schedule1.html', context)

def eventBooking(request):
    username = request.session.get('username', '')

    if request.method == 'POST':
        event_name = request.POST.get('event_name')
        event_date = request.POST.get('event_date')
        event_time = request.POST.get('event_time')
        booking_date = request.POST.get('booking_date')

        Event.objects.create(
            event_name=event_name,
            event_date=event_date,
            event_time=event_time,
            booking_date=booking_date,
        )

        return redirect('event_schedule1')

    events = Event.objects.all()

    context = {
        'events': events,
        'username': username,
    }
    return render(request, 'eventBooking.html', context)

def event_schedule2_view(request):
    username = request.session.get('username')

    update_event = None
    edit_event_id = request.GET.get('edit')  # Tangkap dari URL ?edit=ID
    if edit_event_id:
        update_event = get_object_or_404(Event, pk=edit_event_id)

    if request.method == 'POST':
        event_id = request.POST.get('update_event_id')
        if event_id:
            event = get_object_or_404(Event, pk=event_id)
            event.event_name = request.POST.get('event_name')
            event.event_date = request.POST.get('event_date')
            event.event_time = request.POST.get('event_time')
            event.booking_date = request.POST.get('booking_date')
            event.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_schedule2')

    events = Event.objects.all()
    bookings = Booking.objects.select_related('event').all()

    context = {
        'username': username,
        'events': events,
        'bookings': bookings,
        'update_event': update_event,  # Hantar ke template
    }

    return render(request, 'event_schedule2.html', context)


def payment2_view(request):
    username = request.session.get('username')

    # Fetch all bookings with related user and event
    bookings = Booking.objects.select_related('congregate_member', 'event').all()

    context = {
        'username': username,
        'bookings': bookings,
    }

    return render(request, 'payment2.html', context)

def event_schedule(request):
    username = request.session.get('username')
    return render(request, 'event_schedule.html', {'username': username})

def congregate_list_view(request):
    users = CongregateMember.objects.all()
    username = request.session.get('username')
    context = {
        'users': users,
        'username': username,
    }
    return render(request, 'congregate_list.html', context)

def event_update_view(request, event_id):
    return redirect(f'/homemos/event-schedule2/?edit={event_id}')

def event_delete_view(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    event.delete()
    return redirect('event_schedule2')