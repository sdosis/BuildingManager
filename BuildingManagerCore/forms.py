from django import forms

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    email = forms.EmailField(required=False,label='Your email address')
    message = forms.CharField(widget=forms.Textarea)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words")
        return message

class NotificationForm(forms.Form):
    districts = [("Kungsholmen","Kungsholmen"),
                 ("Norrmalm","Norrmalm"),
                 ("Södermalm","Södermalm"),
                 ("Östermalm","Östermalm"),
                 ("Enskede-Årsta-Vantör","Enskede-Årsta-Vantör"),
                 ("Farsta","Farsta"),
                 ("Hägersten-Liljeholmen","Hägersten-Liljeholmen"),
                 ("Skarpnäck","Skarpnäck"),
                 ("Skärholmen","Skärholmen"),
                 ("Bromma","Bromma"),
                 ("Hässelby-Vällingby","Hässelby-Vällingby"),
                 ("Rinkeby-Kista","Rinkeby-Kista"),
                 ("Spånga-Tensta","Spånga-Tensta")
                 ]
    district = forms.ChoiceField(choices=districts)

    def clean_message(self):
        district = self.cleaned_data['district']
        if not district in self.districts:
            raise forms.ValidationError("Invalid district")
        return district