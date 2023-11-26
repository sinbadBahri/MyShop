from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django_recaptcha.fields import ReCaptchaField

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Confirm Password',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    captcha = ReCaptchaField()

    error_messages = {
        'mismatch': "Passwords did not match"
    }

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')

    def clean_password2(self):
        password1, password2 = self.cleaned_data.get('password1'), self.cleaned_data.get('password2')
        if password1 and password2 and password1 == password2:
            return password2
        raise forms.ValidationError(self.error_messages['mismatch'], code="password_mismatch")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href="../password/">this link</a>'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'first_name', 'last_name',
            'is_active', 'is_staff', 'is_superuser',
        )
