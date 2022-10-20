from django import forms


CHART_CHOICES = (
    ('#1', 'Bar Graph'),
    ('#2', 'Line Graph')
)

RESULTS_CHOICES = (
    ('#1', 'Temperature'),
    ('#2', 'Humidity'),
    ('#3', 'Pressure'),
    ('#4', 'Light'),
    ('#5', 'Moisture')
)


class ParametersSearchForm(forms.Form):
    date_from = forms.DateTimeField(
        label='Select starting date',
        widget=forms.DateTimeInput(
            attrs={'type': 'date'}
        )
    )
    date_to = forms.DateTimeField(
        label='Select ending date',
        widget=forms.DateTimeInput(
            attrs={'type': 'date'}
        )
    )
    chart_type  = forms.ChoiceField(label="Select chart type", choices=CHART_CHOICES)
    results_by  = forms.ChoiceField(label="Select data type", choices=RESULTS_CHOICES)
    
