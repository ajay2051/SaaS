from django.shortcuts import render

from subscriptions.models import SubscriptionPrice


def subscription_price_view(request):
    qs = SubscriptionPrice.objects.filter(featured=True)
    monthly_qs = qs.filter(interval=SubscriptionPrice.IntervalChoices.MONTHLY)
    yearly_qs = qs.filter(interval=SubscriptionPrice.IntervalChoices.YEARLY)
    context = {'qs': qs, "monthly_qs": monthly_qs, "yearly_qs": yearly_qs}
    return render(request, 'subscriptions/subscription_price_view.html', context=context)