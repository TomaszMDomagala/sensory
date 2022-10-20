from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .models import Sensors
from .serializers import SensorsSerializer
from .forms import ParametersSearchForm
from .utils import get_chart, apply_scale

from django.views.generic import ListView, DetailView
from django.utils import timezone
from django.shortcuts import render

import pandas as pd


class SensorsView(ListView):
    
    model = Sensors

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def parameters(request):
    parameters_df   = None
    chart           = None
    no_data         = None
    search_form = ParametersSearchForm(request.POST or None)

    if request.method == 'POST':
        date_from   = request.POST.get('date_from')
        date_to     = request.POST.get('date_to')
        chart_type  = request.POST.get('chart_type')
        results_by  = request.POST.get('results_by')

        parameters_qs = Sensors.objects.filter(date_time__date__lte=date_to, date_time__date__gte=date_from)

        if len(parameters_qs) > 0:
            parameters_df = pd.DataFrame(parameters_qs.values())
            time_span = apply_scale(parameters_df)

            parameters_df['date_time'] = parameters_df['date_time'].apply(lambda x: x.strftime(time_span))
            parameters_df.drop(['id', 'slave_ip', 'author_id'], axis=1, inplace=True)
            # parameters_df.rename({'customer_id': 'customer', 'salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)

            chart           = get_chart(chart_type, parameters_df, results_by)
            parameters_df   = parameters_df.to_html()

        else:
            messages.warning(request, "Apparently no data available...")

    context = {
        'search_form': search_form,
        'parameters_df': parameters_df,
        'chart': chart,
    }
    return render(request, 'sensors/charts.html', context)


class SensorsListApiView(APIView):

    def get(self, request, *args, **kwargs):
        sensors = Sensors.objects.all()
        serializer = SensorsSerializer(sensors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            'temperature':  round(request.data.get('temperature'), 2),
            'humidity':     round(request.data.get('humidity'), 2),
            'pressure':     round(request.data.get('pressure'), 2),
            'light':        round(request.data.get('light'), 2),
            'moisture':     request.data.get('moisture'),
            'slave_ip':     request.data.get('slave_ip')
            # 'author':     request.data.get('author')
        }
        serializer = SensorsSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
