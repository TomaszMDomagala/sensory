import uuid, base64
from .models import *
from io import BytesIO
from matplotlib import pyplot
from .forms import (
    CHART_CHOICES,
    RESULTS_CHOICES
        )


def generate_code():
    return str(uuid.uuid4()).replace('-', '').upper()[:12]


def get_key(res_by):
    return dict(RESULTS_CHOICES)[res_by].lower()


def get_graph():
    buffer = BytesIO()
    pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph


def get_chart(chart_type, data, results_by, **kwargs):
    pyplot.switch_backend('AGG')
    fig = pyplot.figure(figsize=(10, 4))
    key = get_key(results_by)
    d = data.groupby(key, as_index=False, sort=False)['date_time'].agg('sum')

    if chart_type == '#1':
        pyplot.bar(d['date_time'], d[key])
    elif chart_type == '#2':
        pyplot.pie(data=d,x='date_time', labels=d[key])
    elif chart_type == '#3':
        pyplot.plot(d['date_time'], d[key], color='gray', marker='o', linestyle='dashed')
        pyplot.savefig('chart.png')
    else:
        print("Apparently...chart_type not identified")
    pyplot.tight_layout()
    chart = get_graph()
    return chart