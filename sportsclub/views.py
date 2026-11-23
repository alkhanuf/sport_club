from typing import Any

from django.contrib.auth.models import User
from django.views.generic import TemplateView


class ShowClientsView(TemplateView):
    template_name = "clients/show_clients.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['clients'] = User.objects.all()
        return context