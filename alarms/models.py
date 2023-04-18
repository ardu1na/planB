import uuid
from datetime import date

from django.db import models


class AlarmaEvent(models.Model):
    
    FUEGO="Fuego"
    SOS="SOS"
    EMERGENCIA="Emergencia"
    
    TYPE_CHOICES=[
        (FUEGO, ('Fuego')),
        (SOS, ('SOS')),
        (EMERGENCIA, ('Emergencia')),]
    
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    
    tipo = models.CharField(
        choices=TYPE_CHOICES,
        max_length=50, null=True, blank=False, default=None)
    
    datetime = models.DateTimeField(auto_now_add=True)
    
    miembro = models.ForeignKey(
        'Miembro', on_delete=models.SET_NULL,
        null=True, blank=False,
        related_name="alertas")


    def __str__ (self):
        return f'Alarma {self.tipo} en {self.miembro.casa.grupo_barrial}, {self.miembro.casa.get_direccion}' 

    
    

class GrupoBarrial(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    nombre =  models.CharField(max_length=150)
    descripcion =  models.TextField(null=True, blank=True)

    #add zona in coordenadas and rango
    google_account = models.EmailField(blank=True, null=True)
    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)  
    YES="Yes"
    NO="No"
    STATE_CHOICES = [
        (YES, ('Yes')),
        (NO, ('No')),]    
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default="Yes")
    deleted_at = models.DateField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.state == "No":
            self.deleted_at = date.today()
        super(GrupoBarrial, self).save(*args, **kwargs)    
        
    def __str__ (self):
        return self.nombre
    
    
class Miembro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   

    casa = models.ForeignKey('Casa', on_delete=models.CASCADE, related_name="miembros")

    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    
    es_referente = models.BooleanField(default=False)
    
    fecha_de_nacimiento = models.DateField(blank=True, null=True)

    contacto_nombre = models.CharField(max_length=150,  blank=True, null=True)
    contacto_telefono = models.CharField(max_length=150, blank=True, null=True)
    
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    YES="Yes"
    NO="No"
    STATE_CHOICES = [
        (YES, ('Yes')),
        (NO, ('No')),]    
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default="Yes")
    deleted_at = models.DateField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.state == "No":
            self.deleted_at = date.today()
        super(Miembro, self).save(*args, **kwargs)


    def __str__ (self):
        return f'{self.apellido}, {self.nombre}'
    
        
class Casa(models.Model):    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   

    grupo_barrial = models.ForeignKey(GrupoBarrial, on_delete=models.CASCADE, blank=True, null=True, related_name="casas")
       
    calle = models.CharField(max_length=300, blank=True, null=True, verbose_name="CALLE")
    numero = models.IntegerField(blank=True, null=True)
    municipio = models.CharField(max_length=300, blank=True, null=True, verbose_name="MUNICIPIO")
    provincia = models.CharField(max_length=100, null=True, blank=True)

    altitud = models.DecimalField(decimal_places=30, max_digits=80, blank=True, null=True,  verbose_name="ALTITUD")
    latitud = models.DecimalField(decimal_places=30, max_digits=80, blank=True, null=True,  verbose_name="LATITUD")

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    YES="Yes"
    NO="No"
    STATE_CHOICES = [
        (YES, ('Yes')),
        (NO, ('No')),]    
    state = models.CharField(max_length=50, choices=STATE_CHOICES, default="Yes")
    deleted_at = models.DateField(blank=True, null=True)







    @property
    def get_miembros_string(self, *args, **kwargs):
        miembros = Miembro.objects.filter(casa__id=self.id)
        nombres = ["{} {}".format(miembro.nombre, miembro.apellido) for miembro in miembros]
        return ", ".join(nombres)
    
    
    @property
    def get_miembros(self, *args, **kwargs):
        miembros = Miembro.objects.filter(casa__id=self.id)
        return miembros
    
    
    @property
    def get_referencia(self, *args, **kwargs):
        try:            
            referencia = Miembro.objects.get(casa__id=self.id, es_referente=True)
            return f"{referencia.nombre} {referencia.apellido}"
        except:
            return "None"
        
    @property
    def get_coordenadas(self, *args, **kwargs):
        return f"{self.altitud}, {self.latitud}"
    
    
    @property
    def get_direccion_con_municipio_y_provincia(self, *args, **kwargs):
        return f"{self.calle} {self.numero}, {self.municipio}, {self.provincia}"
    
    @property
    def get_direccion(self, *args, **kwargs):
        return f"{self.calle} {self.numero}"
    
    def save(self, *args, **kwargs):
        if self.state == "No":
            self.deleted_at = date.today()
        super(Casa, self).save(*args, **kwargs)


    def __str__ (self):
        return f'{self.grupo_barrial}: {self.get_direccion}'
    
    
    
