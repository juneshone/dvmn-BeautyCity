from django import forms


class PhoneForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'class': 'contacts__form_iunput',
            'placeholder': '+7(999)999--99-99',
            'required': 'required'
        })
    )
    consent = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={
            'class': 'contacts__form_checkbox',
            'checked': 'checked'
        })
    )


class PinForm(forms.Form):
    pin = forms.CharField(
        max_length=4,
        widget=forms.TextInput(attrs={
            'class': 'tipsPopup__form_inputNum popup__input',
            'placeholder': '9999',
            'required': 'required'
        })
    )