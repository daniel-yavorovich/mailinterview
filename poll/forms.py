# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class LaunchPollForm(forms.Form):
    author_name = forms.CharField(label="Your or company name", max_length=300)
    author_email= forms.EmailField(label="Your E-mail")
    title       = forms.CharField(max_length=300)
    description = forms.CharField(widget=forms.Textarea(), max_length=1000)
    clients     = forms.CharField(
        widget=forms.Textarea(),
        label="Clients (one per line)"
    )

    def clean(self):
        cleaned_data = super(LaunchPollForm, self).clean()

        # Clients
        emails = []
        if cleaned_data.has_key('clients'):
            for email in cleaned_data['clients'].split('\n'):
                email = email.replace('\r', '')
                try:
                    validate_email(email)
                    emails.append(email)
                except ValidationError:
                    self._errors["clients"] = self.error_class(["Please check E-mail syntax"])

        cleaned_data['emails'] = emails

        # Variants list
        variants = []
        for var in self.data:
            if 'variant' in var:
                variants.append(self.data[var])

        if len(variants) < 2:
            raise forms.ValidationError(u"You must specify at least 2 variants.")

        cleaned_data['variants'] = variants

        return cleaned_data
