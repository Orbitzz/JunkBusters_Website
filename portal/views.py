from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from functools import wraps


def customer_login_required(view_func):
    """Decorator that redirects to portal login if no customer session."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('customer_id'):
            return redirect('portal:login')
        return view_func(request, *args, **kwargs)
    return wrapper


def get_current_customer(request):
    """Return the Customer object for the current session, or None."""
    customer_id = request.session.get('customer_id')
    if not customer_id:
        return None
    try:
        from crm.models import Customer
        return Customer.objects.get(pk=customer_id)
    except Exception:
        return None


@require_http_methods(['GET', 'POST'])
def portal_login(request):
    # Already logged in → go to dashboard
    if request.session.get('customer_id'):
        return redirect('portal:dashboard')

    error = None
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if email:
            try:
                from crm.models import Customer
                customer = Customer.objects.get(email__iexact=email)
                request.session['customer_id'] = customer.pk
                request.session['customer_name'] = customer.display_name or f"{customer.first_name} {customer.last_name}"
                return redirect('portal:dashboard')
            except Exception:
                error = "No account found with that email. Please check your email or contact us."
        else:
            error = "Please enter your email address."

    return render(request, 'portal/login.html', {'error': error})


def portal_logout(request):
    request.session.flush()
    return redirect('portal:login')


@customer_login_required
def dashboard(request):
    customer = get_current_customer(request)
    if not customer:
        request.session.flush()
        return redirect('portal:login')

    jobs = []
    total_spent = 0
    try:
        from service.models import Job
        jobs = list(Job.objects.filter(customer=customer).order_by('-scheduled_datetime', '-created_at'))
        total_spent = sum(j.total_price or 0 for j in jobs if j.status == 'completed')
    except Exception:
        pass

    return render(request, 'portal/dashboard.html', {
        'customer': customer,
        'jobs': jobs,
        'total_spent': total_spent,
    })


@customer_login_required
def job_detail(request, job_id):
    customer = get_current_customer(request)
    if not customer:
        return redirect('portal:login')

    try:
        from service.models import Job
        job = get_object_or_404(Job, pk=job_id, customer=customer)
    except Exception:
        return redirect('portal:dashboard')

    return render(request, 'portal/job_detail.html', {
        'customer': customer,
        'job': job,
    })


@customer_login_required
def invoice(request, job_id):
    customer = get_current_customer(request)
    if not customer:
        return redirect('portal:login')

    try:
        from service.models import Job
        job = get_object_or_404(Job, pk=job_id, customer=customer)
    except Exception:
        return redirect('portal:dashboard')

    return render(request, 'portal/invoice.html', {
        'customer': customer,
        'job': job,
    })
