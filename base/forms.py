from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class RoomForm(ModelForm):

    class Meta:
        model = Room
        # criar um forms com base nos fileds editaveis da classe objeto room
        fields = '__all__'
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:

        model = User
        fields =['username', 'email']
        