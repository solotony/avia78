from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'phone', 'address', 'org_name', 'org_inn')

    def as_div(self):

        return self._html_output(
            normal_row = u'<div class="bx-authform-formgroup-container">%(label)s '
                         u'<div class="bx-authform-input-container">%(field)s</div>  '
                         u'%(help_text)s'
                         u'</div>',
            error_row = u'%s',
            row_ender = '</div>',
            help_text_html = u'<div class="bx-authform-description-container">%s</div>',
            errors_on_separate_row = True,
            #error_css_class='class-error',
            #required_css_class = 'class-required',
        )


    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = ''

class ProfileForm(forms.ModelForm):
    required_css_class = 'required'
    error_css_class = 'error'

    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'phone', 'address', 'org_name', 'org_inn')

    def as_div(self):

        return self._html_output(
            normal_row = u'<div class="bx-authform-formgroup-container">%(label)s '
                         u'<div class="bx-authform-input-container">%(field)s</div>  '
                         u'%(help_text)s'
                         u'</div>',
            error_row = u'%s',
            row_ender = '</div>',
            help_text_html = u'<div class="bx-authform-description-container">%s</div>',
            errors_on_separate_row = True,
            #error_css_class='class-error',
            #required_css_class = 'class-required',
        )


    def __init__(self, *args, **kwargs):
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        # adding css classes to widgets without define the fields:
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = ''

