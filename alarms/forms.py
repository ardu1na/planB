from django.forms import ModelForm, EmailInput, TextInput, Textarea
from alarms.models import *





class NewGrupoBarrialForm(ModelForm):
    
    class Meta:
        model = GrupoBarrial
        fields = ( 
                  'nombre',
                  'google_account',
                  'descripcion',
                  )
                    
        widgets = {

            'nombre' : TextInput(attrs={'class':"form-control",
            'id':"nombre",
            'placeholder':"Alarma Vecinal",}),
            


            'google_account' : EmailInput(attrs={
                'class':"form-control",
                'id':"google_account",
                'placeholder' : "Google Account"
                }
            ),
            
            
            
            'descripcion' : Textarea(attrs={
                'class':"form-control",
                'id':"descripcion",
                'placeholder' : "Descripcion"
                }
            ),


        }
        