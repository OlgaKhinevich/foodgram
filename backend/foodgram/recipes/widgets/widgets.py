from django.forms.widgets import Input


class ColorWidget(Input):
    input_type = 'color'
    template_name = 'django/forms/widgets/input.html'
