from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Tournament, Teams, Contact, Payment
from .forms import RForm

# Create your views here.


def Home(request):
    tournament = Tournament.objects.all().order_by('last_date')[:1]
    if request.user.is_authenticated:
        try:
            team = Teams.objects.filter(
                user=request.user, registered=False).exists()
            registered_team = Teams.objects.filter(
                user=request.user, registered=True).exists()
        except TypeError:
            messages.info(request, "Please Login")

        context = {
            'tournaments': tournament,
            'team': team,
            'rt': registered_team
        }
        return render(request, 'index.html', context)
    else:
        context = {
            'tournaments': tournament
        }
        return render(request, 'index.html', context)


def TournamentDetail(request, slug):
    tournament = Tournament.objects.get(slug=slug)
    context = {
        'tournament': tournament
    }

    return render(request, 'detail.html', context)


@login_required(login_url='login/')
def Register(request, slug):
    t = Tournament.objects.get(slug=slug)
    form = RForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        user = request.user
        team_name = form.cleaned_data['team_name']
        team_tag = form.cleaned_data['team_tag']
        team_number = form.cleaned_data['team_number']
        player1_ign = form.cleaned_data['player1_ign']
        player1_id = form.cleaned_data['player1_id']
        player2_ign = form.cleaned_data['player2_ign']
        player2_id = form.cleaned_data['player2_id']
        player3_ign = form.cleaned_data['player3_ign']
        player3_id = form.cleaned_data['player3_id']
        player4_ign = form.cleaned_data['player4_ign']
        player4_id = form.cleaned_data['player4_id']
        player5_ign = form.cleaned_data['player5_ign']
        player5_id = form.cleaned_data['player5_id']
        payment_method = form.cleaned_data['payment_method']

        # Checks to stop registering duplicate team.
        if Teams.objects.filter(team_name=team_name).exists():
            messages.warning(request, f"{team_name} is already registered.")
            return redirect('core:Register', slug=slug)

        elif Teams.objects.filter(team_tag=team_tag).exists():
            messages.warning(request, f"{team_tag} is already registered.")
            return redirect('core:Register', slug=slug)

        elif Teams.objects.filter(team_number=team_number).exists():
            messages.warning(request, f"{team_number} is already Used.")
            return redirect('core:Register', slug=slug)

        # TODO: Check Indivisual Player if they are registered

        # elif Teams.objects.filter(player1_id=player1_id).exists():
        #     messages.warning(request, f"{player1_ign} is already registered by another Team.")
        #     return redirect('core:Register', slug=slug)

        # elif Teams.objects.filter(player2_id=player2_id).exists():
        #     messages.warning(request, f"{player2_ign} is already registered by another Team.")
        #     return redirect('core:Register', slug=slug)

        # elif Teams.objects.filter(player3_id=player3_id).exists():
        #     messages.warning(request, f"{player3_ign} is already registered by another Team.")
        #     return redirect('core:Register', slug=slug)

        # elif Teams.objects.filter(player4_id=player4_id).exists():
        #     messages.warning(request, f"{player4_ign} is already registered by another Team.")
        #     return redirect('core:Register', slug=slug)

        # elif Teams.objects.filter(player5_id=player5_id).exists():
        #     messages.warning(request, f"{player5_ign} is already registered by another Team.")
        #     return redirect('core:Register', slug=slug)

        # Checks If user had already registered a Team.
        elif Teams.objects.filter(user=user, registered=False).exists():
            messages.warning(
                request, f"You have one pending Payment. Please Pay registeration fee to Continue.")
            return redirect('core:Home')

        elif Teams.objects.filter(user=user).exists():
            messages.warning(request, f"You have already registered a Team.")
            return redirect('core:Home')

        # If not then Proceed.

        new_team = Teams(
            user=user,
            tournament=t,
            team_name=team_name,
            team_tag=team_tag,
            team_number=team_number,
            player1_ign=player1_ign, player1_id=player1_id,
            player2_ign=player2_ign, player2_id=player2_id,
            player3_ign=player3_ign, player3_id=player3_id,
            player4_ign=player4_ign, player4_id=player4_id,
            player5_ign=player5_ign, player5_id=player5_id,
            payment_method=payment_method
        )
        new_team.save()

        if payment_method == 'HBL':
            return redirect('core:Payment', payment_option='HBL')
        else:
            messages.warning(
                request, "Invalid Payment Method or Selected method is not Supported.")
            new_team.delete()
            return redirect('core:Register', slug=slug)

        messages.success(request, "Submitted Succsfully")
        return redirect('core:Home')

    return render(request, 'register.html', context)


@login_required(login_url='login/')
def PaymentView(request, payment_option):

    try:
        teams = Teams.objects.get(user=request.user, registered=False)

    except Teams.DoesNotExist:
        messages.info(
            request, "Your team is already registered. No Need to Pay!")
        return redirect('core:Home')

    context = {
        'teams': teams.tournament.entry_fee
    }

    if request.method == 'POST':
        card = request.POST.get('card')

        # Checks IF user has no team registered.
        if Payment.objects.filter(user=request.user).exists():
            messages.warning(
                request, "Your team is already registered. No Need to Pay!")
            return redirect('core:Home')

        if card != '':
            PAYMENT = Payment(
                user=request.user,
                card_number=card,
                paid_date=timezone.now(),
                amount=teams.tournament.entry_fee,
                tournament_fee=teams.tournament.entry_fee
            )
            PAYMENT.save()

            T = Tournament.objects.get(title=teams.tournament)
            T.slots -= 1
            T.save()

            teams.registered = True
            teams.payment = PAYMENT
            teams.save()
            messages.success(
                request, "Payment Successfull. And Your team is registered now.")
            return redirect('core:Home')
        else:
            messages.error(request, "Card Number cannot be empty")
            return redirect('core:Payment', payment_option='HBL')

    return render(request, 'payment.html', context)


def AllTeams(request, slug):
    tournament = Tournament.objects.get(slug=slug)
    teams = Teams.objects.all()
    context = {
        'teams': teams,
        't': tournament
    }
    return render(request, 'teams.html', context)


@login_required(login_url='login/')
def CancelRegisteration(request):
    try:
        teams = Teams.objects.get(user=request.user, registered=False)
    except Teams.DoesNotExist:
        messages.info(request, "You Have no team registered!")
        return redirect('core:Home')

    # Delete the selected object and cancel the registeration.
    teams.delete()
    messages.info(request, "Registeration Cancelled.")
    return redirect('core:Home')


@login_required(login_url='login/')
def CancelTeamRegisteration(request):
    try:
        teams = Teams.objects.get(user=request.user)
        payment = Payment.objects.get(user=request.user)
    except Teams.DoesNotExist:
        messages.info(request, "You Have no team registered!")
        return redirect('core:Home')

    T = Tournament.objects.get(title=teams.tournament)
    T.slots += 1
    T.save()
    # Delete the selected object and cancel the registeration.
    teams.delete()
    payment.delete()
    messages.info(request, "Registeration Cancelled.")
    return redirect('core:Home')


@login_required(login_url='login/')
def ContactView(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        MESSAGE = Contact(
            user=request.user,
            name=name,
            email=email,
            message=message
        )
        MESSAGE.save()
        messages.success(request, "Your message has been sent.")
        return redirect('core:Home')

    return render(request, 'contact.html')


# Accounts Logic

def Signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Checks if input is not empty
        if username != '' and email != '' and len(pass1) > 5:
            if pass1 == pass2:
                # Checks if Email and USernaME is already Regisetered
                if User.objects.filter(email=email).exists():
                    messages.info(request, 'Email is already Registered')
                    return redirect('core:Signup')
                elif User.objects.filter(username=username).exists():
                    messages.info(request, 'Username is already taken!')
                    return redirect('core:Signup')

                user = User.objects.create_user(
                    username=username, email=email, password=pass1)
                user.save()
                return redirect('core:Login')

            else:
                messages.error(request, "Password didn't match")
                return redirect('core:Signup')
        else:
            messages.warning(request, "Please Fill out all the fields.")
            return redirect('core:Signup')

    return render(request, 'signup.html')


def Login(request):
    if request.method == 'POST':
        username = request.POST['un']
        password = request.POST['password']

        # Checks an empty field if present
        if username != '' and password != '':
            # Authenticating user
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # Logging In
                auth.login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('core:Home')
            else:
                messages.error(
                    request, f"Invalid Credentials {username}-{password}")
                return redirect('core:Login')
        else:
            messages.info(request, 'Please Fill out all the details')
            return redirect('core:Login')

    return render(request, 'login.html')


def Logout(request):
    auth.logout(request)
    return redirect('core:Home')
