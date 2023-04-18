from django.forms import ModelForm, EmailInput, TextInput, Textarea, URLInput
from alarms.models import *





class NewGrupoBarrialForm(ModelForm):
    
    class Meta:
        model = GrupoBarrial
        fields = ( 
                  'nombre',
                  'google_account',
                  'descripcion',
                  'whatsapp_group',
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
            
            'whatsapp_group' : URLInput(attrs={
                'class':"form-control",
                'id':"whatsapp_group",
                'placeholder' : "Grupo de WhatsApp"
                }
            ),
            
            
            
            'descripcion' : Textarea(attrs={
                'class':"form-control",
                'id':"descripcion",
                'placeholder' : "Descripcion"
                }
            ),


        }
        