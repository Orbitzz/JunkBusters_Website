from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .models import CustomerProfile


def _rate_limited(key, max_calls, window_seconds):
    """Returns True if this key has exceeded max_calls within window_seconds."""
    count = cache.get(key, 0)
    if count >= max_calls:
        return True
    cache.set(key, count + 1, window_seconds)
    return False


FC_EMBED_URL = 'http://127.0.0.1:8000/marketing/api/embed/{endpoint}/'
FC_API_KEY   = 'davKlbTza0o9W5Aw-7a-y00VDl2q48o_3_GPgsX3BoI'


def _call_fc(endpoint, payload):
    """Call a FieldCommand embed API. Returns parsed JSON dict or None if FC is offline."""
    try:
        import urllib.request as _ur, json as _j
        data = _j.dumps(payload).encode()
        req = _ur.Request(
            FC_EMBED_URL.format(endpoint=endpoint),
            data=data,
            headers={
                'Content-Type': 'application/json',
                'X-FC-EMBED-KEY': FC_API_KEY,
            }
        )
        with _ur.urlopen(req, timeout=3) as resp:
            return _j.loads(resp.read())
    except Exception:
        return None


def _send_verification_email(request, user):
    """Send account verification email to a newly registered (inactive) user."""
    uid   = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    link  = request.build_absolute_uri(f'/portal/verify/{uid}/{token}/')
    send_mail(
        subject='Verify your JunkBusters account',
        message=(
            f'Hi {user.first_name or user.email},\n\n'
            f'Thanks for creating an account with JunkBusters! Click the link below '
            f'to verify your email address and access your portal.\n\n'
            f'{link}\n\n'
            f'This link expires in 3 days. If you didn\'t sign up, you can ignore this email.\n\n'
            f'— Junk Busters\n615-881-2505\njunkbusters.info'
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=True,
    )


# ── Auth views ─────────────────────────────────────────────────────────────────

@require_http_methods(['GET', 'POST'])
def portal_login(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')

    error = None
    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        if _rate_limited(f'login_fail:{ip}', 5, 300):
            error = 'Too many failed attempts. Please try again in a few minutes.'
        else:
            email    = request.POST.get('email', '').strip().lower()
            password = request.POST.get('password', '')
            if not email or not password:
                error = 'Please enter your email and password.'
            else:
                user = authenticate(request, username=email, password=password)
                if user:
                    # Successful login — reset the fail counter
                    cache.delete(f'login_fail:{ip}')
                    login(request, user)
                    return redirect(request.GET.get('next') or 'portal:dashboard')
                elif User.objects.filter(username=email, is_active=False).exists():
                    error = 'Please verify your email address first. Check your inbox for the verification link.'
                else:
                    error = 'Invalid email or password. Please try again.'

    return render(request, 'portal/login.html', {'error': error})


@require_http_methods(['GET', 'POST'])
def portal_register(request):
    if request.user.is_authenticated:
        return redirect('portal:dashboard')

    error = None
    form_data = {}

    if request.method == 'POST':
        ip = request.META.get('REMOTE_ADDR', 'unknown')
        if _rate_limited(f'register:{ip}', 3, 3600):
            error = 'Too many accounts created from this device. Please try again later.'
            return render(request, 'portal/register.html', {'error': error, 'form': {}})

        form_data = request.POST
        email      = request.POST.get('email', '').strip().lower()
        first_name = request.POST.get('first_name', '').strip()
        last_name  = request.POST.get('last_name', '').strip()
        phone      = request.POST.get('phone', '').strip()
        password   = request.POST.get('password', '')
        password2  = request.POST.get('password2', '')

        if not all([email, first_name, password]):
            error = 'Email, first name, and password are required.'
        elif password != password2:
            error = 'Passwords do not match.'
        elif len(password) < 8:
            error = 'Password must be at least 8 characters.'
        elif User.objects.filter(username=email).exists():
            error = 'An account with that email already exists. Try logging in.'
        else:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_active=False,
            )
            CustomerProfile.objects.create(user=user, phone=phone)
            _send_verification_email(request, user)
            return redirect('portal:verify_sent')

    return render(request, 'portal/register.html', {'error': error, 'form': form_data})


def portal_logout(request):
    logout(request)
    return redirect('portal:login')


def verify_sent(request):
    return render(request, 'portal/verify_sent.html')


def verify_email(request, uidb64, token):
    try:
        uid  = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save(update_fields=['is_active'])
        login(request, user)
        return redirect('portal:dashboard')

    return render(request, 'portal/verify_invalid.html')


@require_http_methods(['GET', 'POST'])
def resend_verification(request):
    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        user  = User.objects.filter(username=email, is_active=False).first()
        if user:
            _send_verification_email(request, user)
        # Always redirect — don't reveal whether the email exists
        return redirect('portal:verify_sent')
    return render(request, 'portal/resend_verification.html', {'error': error})


# ── Portal views (login required) ─────────────────────────────────────────────

@login_required(login_url='/portal/')
def dashboard(request):
    user = request.user
    profile, _ = CustomerProfile.objects.get_or_create(user=user)

    # Fetch live data from FieldCommand — falls back gracefully if FC is down
    jobs_data    = _call_fc('jobs',    {'email': user.email})
    loyalty_data = _call_fc('loyalty', {'email': user.email})

    fc_online = jobs_data is not None

    jobs    = jobs_data.get('jobs', [])    if (jobs_data    and jobs_data.get('success'))    else []
    loyalty = loyalty_data                 if (loyalty_data  and loyalty_data.get('success') and loyalty_data.get('found')) else None

    # Split jobs into upcoming vs history
    active_statuses = {'Scheduled', 'En Route', 'In Progress', 'Pending'}
    upcoming = [j for j in jobs if j.get('status') in active_statuses]
    history  = [j for j in jobs if j.get('status') not in active_statuses]

    return render(request, 'portal/dashboard.html', {
        'profile':  profile,
        'upcoming': upcoming,
        'history':  history,
        'loyalty':  loyalty,
        'fc_online': fc_online,
        'total_jobs': len(jobs),
    })


@login_required(login_url='/portal/')
@require_http_methods(['GET', 'POST'])
def profile_view(request):
    user    = request.user
    profile, _ = CustomerProfile.objects.get_or_create(user=user)
    saved   = False

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name', '').strip()
        user.last_name  = request.POST.get('last_name', '').strip()
        user.save(update_fields=['first_name', 'last_name'])

        profile.phone    = request.POST.get('phone', '').strip()
        profile.address  = request.POST.get('address', '').strip()
        profile.city     = request.POST.get('city', '').strip()
        profile.state    = request.POST.get('state', 'TN').strip()
        profile.zip_code = request.POST.get('zip_code', '').strip()
        profile.save()

        # Sync updated contact info to FieldCommand CRM
        _call_fc('customer', {
            'email':      user.email,
            'first_name': user.first_name,
            'last_name':  user.last_name,
            'phone':      profile.phone,
            'address':    profile.address,
            'city':       profile.city,
            'state':      profile.state,
            'zip_code':   profile.zip_code,
        })

        saved = True

    return render(request, 'portal/profile.html', {
        'profile': profile,
        'saved':   saved,
    })


@login_required(login_url='/portal/')
@require_http_methods(['GET', 'POST'])
def password_change(request):
    error = None
    saved = False

    if request.method == 'POST':
        current  = request.POST.get('current_password', '')
        new_pw   = request.POST.get('new_password', '')
        new_pw2  = request.POST.get('new_password2', '')

        if not request.user.check_password(current):
            error = 'Current password is incorrect.'
        elif new_pw != new_pw2:
            error = 'New passwords do not match.'
        elif len(new_pw) < 8:
            error = 'Password must be at least 8 characters.'
        else:
            request.user.set_password(new_pw)
            request.user.save()
            update_session_auth_hash(request, request.user)
            saved = True

    return render(request, 'portal/password_change.html', {
        'error': error,
        'saved': saved,
    })
