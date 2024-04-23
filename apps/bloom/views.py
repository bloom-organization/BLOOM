from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentForm
from .models import Payment

# Create your views here.
def payment_new(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save()
            return redirect('bloom:payment_pay', pk=payment.pk)
    else:
        form = PaymentForm()
    return render(request, 'bloom/payment_new.html', {'form': form})

def payment_pay(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    
    return render(request, 'bloom/payment_pay.html', {'payment': payment})