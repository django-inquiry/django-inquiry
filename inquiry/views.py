from django.views.generic import TemplateView


class ChartView(TemplateView):
    template_name = 'inquiry/charts.html'
