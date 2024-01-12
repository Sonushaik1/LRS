from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from app.models import Landdetails,LandRegistration



class Land(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary w-100'))
    helper.form_action = '/addland/'
    helper.form_id = 'p_form'
    class Meta:
        model = Landdetails
        fields = ['address','land_area','landmark','cost_unit','photo']


class LandRegistrationForm(ModelForm):
    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Submit', css_class='btn btn-primary w-100'))
    helper.form_action = '/add_registration/'
    helper.form_id = 'lr_form'
    class Meta:
        model = LandRegistration
        fields = "__all__"
        exclude = ['seller']

    def __init__(self, user_email, *args, **kwargs):
        super(LandRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['land'].queryset = Landdetails.objects.filter(owner_email=user_email)
    
    