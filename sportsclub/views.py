from typing import Any

from django.views.generic import TemplateView

from sportsclub.models import Client

class ShowClientsView(TemplateView):
    template_name = "clients/show_clients.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['clients'] = Client.objects.all()

        return context
     
# Create your views here.
