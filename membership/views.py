from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import CustomSignupForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import authenticate, login
from .models import Customer
import stripe


stripe.api_key = "sk_test_51HEtJjKPNZZN53LZVv5iWor9s05C1QhWo4npzvEpTLldjTDxOMgUAWdQKAHrpphNtnWDljf6FmnxAdMdqOG9i1fT00bsnZ4OfW"


def home(request):
    return render(request, 'membership/home.html')


@login_required
def settings(request):
    return render(request, 'registration/settings.html')


def join(request):
    return render(request, 'membership/join.html')


def success(request):
    if request.method == 'GET' and 'session_id' in request.GET:
        session = stripe.checkout.Session.retrieve(request.GET['session_id'],)
        customer = Customer()
        customer.user = request.user
        customer.stripeid = session.customer
        customer.membership = True
        customer.cancel_at_period_end = False
        customer.stripe_subscription_id = session.subscription
        customer.save()
    return render(request, 'membership/success.html')


def cancel(request):
    return render(request, 'membership/cancel.html')


@login_required
def checkout(request):

    try:
        if request.user.customer.membership:
            return redirect('settings')
    except Customer.DoesNotExist:
        pass

    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_dollar = 10
        membership_id = 'price_1HI7iKKPNZZN53LZEYa55mwX'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1HI7ikKPNZZN53LZQxjBkO1e'
                final_dollar = 100

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            customer_email = request.user.email,
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
        )

        return render(request, 'membership/checkout.html', {'final_dollar': final_dollar, 'session_id': session.id})


class SignUp(generic.CreateView):
    form_class = CustomSignupForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        valid = super(SignUp, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid
