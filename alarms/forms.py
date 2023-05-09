from django.forms import ModelForm, EmailInput,\
        TextInput, Textarea, FileInput, NumberInput,\
        HiddenInput, UUIDField, Select, ModelChoiceField
        
from alarms.models import *

class NewUsuarioForm(ModelForm):
    
    vivienda = UUIDField(widget=HiddenInput())

    class Meta:
        model = Miembro
        fields = ( 
                  'avatar',
                  'nombre',
                  'apellido',
                  'genero',
                  
                  'telefono',                  
                  'fecha_de_nacimiento',
                  'nota',
                  )
                    
        widgets = {
            
            'avatar': FileInput(),

            
            'nota' : TextInput(attrs={'class':"form-control",
            'id':"nota",
            'placeholder':"Nota de información médica",}),
            
            
            'nombre' : TextInput(attrs={'class':"form-control",
            'id':"nombre",
            'placeholder':"Nombre",}),

            'apellido' : TextInput(attrs={'class':"form-control",
            'id':"apellido",
            'placeholder':"Apellido",}),
            


            'genero' : Select(attrs={
                'class':"default-select form-control wide mb-3",
                'id':"genero",
                'placeholder':"Género",}),
            
            'telefono' : TextInput(attrs={'class':"form-control",
            'id':"telefono",
            'placeholder':"Teléfono",}),
            
            'fecha_de_nacimiento' : TextInput(attrs={'class':"datetimepicker form-control",
            'id':"PublishDateTimeTextbox",
            'type':"date",
            'placeholder':"Date",}),
            
            
            


        }
        

class NewUser(NewUsuarioForm):
    
    alarma_vecinal = ModelChoiceField(
        queryset=AlarmaVecinal.objects.filter(state="Yes"),
        empty_label="Seleccione una Alarma Vecinal",
        widget=Select(attrs={
            'class': 'default-select form-control wide mb-3',
            'id': 'alarma_vecinal',
            'name': 'alarma_vecinal',
        }),
    )
    
    vivienda = ModelChoiceField(
        queryset=Vivienda.objects.filter(state="Yes"),
        empty_label="Seleccione una vivienda",
        widget=Select(attrs={
            'class': 'default-select form-control wide mb-3',
            'id': 'vivienda',
            'name': 'vivienda',
        }),
    )


class NewAlarmaVecinalForm(ModelForm):
    
    class Meta:
        model = AlarmaVecinal
        fields = ( 
                  'nombre',
                  'google_account',
                  'descripcion',
                  'whatsapp_group',
                  'latitud',
                  'altitud',
                  'area'
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
            
            'whatsapp_group' : TextInput(attrs={
                'class':"form-control",
                'id':"whatsapp_group",
                'placeholder' : "ID del Grupo de WhatsApp (ej: LkNG2BNQsXK2xfn99DwbFV)"
                }
            ),
            
            
            
            'descripcion' : Textarea(attrs={
                'class':"form-control",
                'id':"descripcion",
                'placeholder' : "Descripcion"
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
             'area' : TextInput(attrs={
                'class':"form-control",
                'id':"area",
                'placeholder' : "area"
                }
            ),


        }

        
        


class NewViviendaForm(ModelForm):
    

    alarma_vecinal = UUIDField(widget=HiddenInput())

    class Meta:
        model = Vivienda
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
        