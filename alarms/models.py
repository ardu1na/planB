import uuid
from datetime import date
from PIL import Image

from django.db import models
from django.contrib.auth.models import Group


from dashboard.users.models import CustomUser

today = date.today()

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
        return f'Alarma {self.tipo} en {self.miembro.vivienda.alarma_vecinal}, {self.miembro.vivienda.get_direccion}' 

    class Meta:
        get_latest_by = "-datetime"
        ordering = ["datetime"]

    

class AlarmaVecinal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)           
    nombre =  models.CharField(max_length=150)
    descripcion =  models.TextField(null=True, blank=True)

    altitud = models.DecimalField(decimal_places=7, max_digits=9, blank=True, null=True,  verbose_name="ALTITUD")
    latitud = models.DecimalField(decimal_places=7, max_digits=9, blank=True, null=True,  verbose_name="LATITUD")
    area = models.CharField(max_length=10, null=True, blank=True)
    
    google_account = models.EmailField(blank=True, null=True)
    whatsapp_group = models.CharField(max_length=300, blank=True, null=True)
    
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
            
        created = not self.pk 
        super().save(*args, **kwargs)  

    


        
    def __str__ (self):
        return self.nombre
    
    
    
    
    @property
    def get_n_usuarios(self):
        usuarios = []
        viviendas = self.viviendas.filter(state="Yes")
        for vivienda in viviendas:
            for usuario in vivienda.miembros.filter(state="Yes"):
                usuarios.append(usuario)
        return len(usuarios)  
    
    @property
    def get_n_viviendas(self):
        viviendas = self.viviendas.filter(state="Yes")
        return len(viviendas)

    @property
    def get_viviendas(self):
        viviendas = self.viviendas.filter(state="Yes")
        return viviendas
    
    
    @property  
    def get_alarmas(self):
        usuarios = []
        viviendas = self.viviendas.all()
        for vivienda in viviendas:
            for usuario in vivienda.miembros.all():
                usuarios.append(usuario)
        alarmas = []
        for usuario in usuarios:
            for alerta in usuario.alertas.all():
                alarmas.append(alerta)
        return alarmas
    
    @property  
    def get_alarmas_this_m(self):
        este_mes = []
        alarmas = self.get_alarmas
        for alarma in alarmas:
            if alarma.datetime.year == today.year and alarma.datetime.month == today.month:
                este_mes.append(alarma)
        return este_mes
                
    @property
    def get_f(self):
        f = []
        alarmas = self.get_alarmas
        for alarma in alarmas:
            if alarma.tipo == "Fuego":
                f.append(alarma)
        return f
            
    @property
    def get_s(self):
        s = []
        alarmas = self.get_alarmas
        for alarma in alarmas:
            if alarma.tipo == "SOS":
                s.append(alarma)
        return s
            
    @property
    def get_e(self):
        e = []
        alarmas = self.get_alarmas
        for alarma in alarmas:
            if alarma.tipo =="Emergencia":
                e.append(alarma)
        return e
    
    
    
    
class Miembro(models.Model):
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    avatar = models.ImageField(upload_to='profiles/', null=True, blank=True)
    from PIL import Image

    vivienda = models.ForeignKey('Vivienda', on_delete=models.CASCADE, related_name="miembros")

    nombre = models.CharField(max_length=150)
    apellido = models.CharField(max_length=150)
    M="Mujer"
    H="Hombre"
    GENERO_CHOICES = (
        (M, ("Mujer")),
        (H, ("Hombre")),
    )
    genero = models.CharField(max_length=34, choices=GENERO_CHOICES, null=True, default=None)
    es_referente = models.BooleanField(default=False)
    
    telefono = models.CharField(max_length=90, null=True, blank=True)
    fecha_de_nacimiento = models.DateField(blank=True, null=True)
    nota =  models.CharField(max_length=400, null=True, blank=True, verbose_name="Nota de información médica")

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


    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True)   
    email = models.EmailField(unique=True, blank=False, null=False)  
    
    
    def save(self, *args, **kwargs):
        if self.state == "No":
            self.deleted_at = date.today()
            
        super().save(*args, **kwargs)  

        if not self.user:
            new_user = CustomUser.objects.create(              # hacer doc para esto
                email=self.email,
                password=f"{self.nombre.lower().replace(' ', '_')}_{self.apellido.lower().replace(' ', '_')}*pass",
                is_active=True
            )
            self.user = new_user
                  
        super().save(*args, **kwargs)       
        
        if self.user.groups == None and self.vivienda.alarma_vecinal:
            try:
                group = Group.objects.get(name=self.vivienda.alarma_vecinal.nombre)
                
            except:
                group = Group.objects.create(name=self.vivienda.alarma_vecinal.nombre)
            
            user = self.user
                
            user.groups.add(group)
            user.save()
        
        super().save(*args, **kwargs)  
        
        
        
        # prevent collapse hd with images and bad display
        if self.avatar:
            image = Image.open(self.avatar.path)
            output_size = (300, 300)
            image.thumbnail(output_size)
            if image.width < output_size[0] or image.height < output_size[1]:
                background = Image.new('RGB', output_size, (255, 255, 255))
                offset = ((output_size[0] - image.width) // 2, (output_size[1] - image.height) // 2)
                background.paste(image, offset)
                image = background
            image.save(self.avatar.path)
            
            
            
            
        
    @property
    def get_wp(self):
        try:
            wp = self.vivienda.alarma_vecinal.whatsapp_group
        except:
            wp = "no registrado"
        return wp
    
    @property
    def get_edad(self):
        if self.fecha_de_nacimiento:
            hoy = date.today()
            edad = (hoy - self.fecha_de_nacimiento).days // 365.25
            return int(edad)
        else:
            return None
    
    @property
    def get_nombre_completo(self):
        return f'{self.nombre} {self.apellido}'
    
    @property
    def get_barrio(self):
        return self.vivienda.alarma_vecinal

    @property
    def alarmas_this_m(self):
        return self.alertas.filter(datetime__month=today.month, datetime__year=today.year)
    
    @property
    def alarmas_this_y(self):
        return self.alertas.filter(datetime__year=today.year)

    def __str__ (self):
        return self.get_nombre_completo

 
 
 
 
 
        
class Vivienda(models.Model):    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   

    alarma_vecinal = models.ForeignKey(AlarmaVecinal, on_delete=models.CASCADE, blank=True, null=True, related_name="viviendas")
    nota =  models.CharField(max_length=400, null=True, blank=True)
       
    calle = models.CharField(max_length=300, blank=True, null=True, verbose_name="CALLE")
    numero = models.IntegerField(blank=True, null=True, default=0)
    sin_numero = models.BooleanField(default=False)
    
    departamento = models.CharField(max_length=300, blank=True, null=True, verbose_name="DEPARTAMENTO (opcional)")

    municipio = models.CharField(max_length=300, blank=True, null=True, verbose_name="MUNICIPIO")
    provincia = models.CharField(max_length=100, null=True, blank=True)

    altitud = models.DecimalField(decimal_places=7, max_digits=9, blank=True, null=True,  verbose_name="ALTITUD")
    latitud = models.DecimalField(decimal_places=7, max_digits=9, blank=True, null=True,  verbose_name="LATITUD")
    area = models.CharField(max_length=10, null=True, blank=True)

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
    def get_map(self):
        enlace = f"https://www.google.com/maps/place/{self.calle}+{self.numero},+{self.municipio},+{self.provincia}/"
        return enlace




    @property
    def get_miembros_string(self, *args, **kwargs):
        miembros = Miembro.objects.filter(vivienda__id=self.id, state="Yes")
        nombres = ["{} {}".format(miembro.nombre, miembro.apellido) for miembro in miembros]
        return ", ".join(nombres)
    
    
    @property
    def get_miembros(self, *args, **kwargs):
        miembros = Miembro.objects.filter(vivienda__id=self.id, state="Yes")
        return miembros
    
    @property
    def get_miembros_number(self, *args, **kwargs):
        miembros = Miembro.objects.filter(vivienda__id=self.id, state="Yes")
        return len(miembros)
    
    @property
    def get_referencia(self, *args, **kwargs):
        try:            
            referencia = Miembro.objects.get(vivienda__id=self.id, es_referente=True)
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
        
        if self.sin_numero == True:
            self.numero = 0
        super(Vivienda, self).save(*args, **kwargs)


    def __str__ (self):
        return self.get_direccion
    
    
    
