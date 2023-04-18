from django.forms import ModelForm, EmailInput, TextInput, Textarea, URLInput, NumberInput, HiddenInput, UUIDField
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

        
        


class NewCasaForm(ModelForm):
    
    #                     c

    grupo_barrial = UUIDField(widget=HiddenInput())

    class Meta:
        model = Casa
        fields = ( 
                  'calle',
                  'numero',
                  'departamento',
                  
                  'nota',                  
                  'municipio',
                  'provincia',
                  
                  'altitud',
                  'latitud',
                  )
                    
        widgets = {
            
            'nota' : TextInput(attrs={'class':"form-control",
            'id':"nota",
            'placeholder':"Nota",}),

            'calle' : TextInput(attrs={'class':"form-control",
            'id':"calle",
            'placeholder':"Calle",}),
            


            'numero' : TextInput(attrs={
                'class':"form-control",
                'id':"numero",
                'placeholder' : "Número"
                }
            ),
            
            'departamento' : TextInput(attrs={
                'class':"form-control",
                'id':"departamento",
                'placeholder' : "Departamento (opcional)"
                }
            ),
            
            'municipio' : TextInput(attrs={
                'class':"form-control",
                'id':"Municipio",
                'placeholder' : "Municipio"
                }
            ),
            
            
            
            'provincia' : TextInput(attrs={
                'class':"form-control",
                'id':"provincia",
                'placeholder' : "Provincia"
                }
            ),
            
            'latitud' : NumberInput(attrs={
                'class':"form-control",
                'id':"latitud",
                'placeholder' : "latitud"
                }
            ),
            
            'altitud' : NumberInput(attrs={
                'class':"form-control",
                'id':"altitud",
                'placeholder' : "altitud"
                }
            ),
            
            


        }
        