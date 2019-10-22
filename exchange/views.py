from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout, authenticate, login
from .models import Game, TicketOffering
from .forms import SellForm, UserCreateForm
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.utils import timezone


@login_required(login_url='/login')
def index(request):
    context = {}
    return render(request, 'exchange/home-page.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('/activation-successful/')
    else:
        return render(request, 'exchange/activation-invalid.html')

@login_required(login_url='/login')
def activation_successful(request):
    return render(request, 'exchange/activation-successful.html')

def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.email = "{}@clemson.edu".format(user.username) 
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your CU Exchange Account'
            message = render_to_string('exchange/account-activation-email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('/activation-sent/')
    else:
        form = UserCreateForm()
    return render(request, 'exchange/home.html', {'form': form})


@login_required(login_url='/login')
def games(request):
    game_list = Game.objects.order_by('game_dt')
    context = {
        'game_list': game_list
    }
    return render(request, 'exchange/games.html', context)

@login_required(login_url='/login')
def profile(request):
    context = {}
    return render(request, 'exchange/profile-page.html')

@login_required(login_url='/login')
def game(request, game_id):
    game = get_object_or_404(Game, pk=game_id)
    context = {
        'game': game
    }
    
    return render(request, 'exchange/game.html', context)



def activation_sent(request):
    context={}
    return render(request, 'exchange/activation-sent.html', context)

@login_required
def success(request):
    context = {}
    return render(request, 'exchange/sell-confirmation.html')

@login_required(login_url='/login')
def logout_request(request):
    logout(request)
    return redirect('exchange:index')

def login_request(request):
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
    form = AuthenticationForm()
    return render(request, 'exchange/login.html', context={'form': form})


@login_required(login_url='/login')
def post_denied(request):
    context = {}
    return render(request, 'exchange/post-denied.html', context)


@login_required(login_url='/login')
def sell(request):
    if request.method == 'POST':
        form = SellForm(request.POST)
        yesterday = timezone.now() - timezone.timedelta(days=1)
        if TicketOffering.objects.filter(username=request.user.username, created__gt=yesterday).exists():
            return redirect('/post-denied/')
        if form.is_valid():
            username = request.user.username
            price = form.cleaned_data['price']
            location = form.cleaned_data['location']
            game=form.cleaned_data['game']
            t = TicketOffering(username=username, price=price, location=location, game=game)
            t.save()
            return HttpResponseRedirect('/success/')
    else:
        form = SellForm
    return render(request, 'exchange/sell.html', {'form': form})

