from django.shortcuts import render, redirect,get_object_or_404
from dashboard.forms import *
from alarms.forms import *
from django.http import JsonResponse

from dashboard.models import Configurations
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import json
from dashboard import setup_config
import os
from django.conf import settings
from django.http import HttpResponse, Http404
from django.contrib.auth.decorators import login_required, permission_required 
import pickle
import mimetypes
from alarms.models import*
from django.conf import settings
from django.core.files.storage import  default_storage
from django.urls import reverse

today = date.today()



def planb(request):
    return render (request, 'dashboard/planb.html', {})

############################################################################################################
#### sistema de alarmas barriales ######

@login_required(login_url='dashboard:login')
def index(request):
    template_name = 'dashboard/index.html'
    barrios = AlarmaVecinal.objects.filter(state="Yes")
    alarmas_this_m = AlarmaEvent.objects.filter(datetime__month=today.month, datetime__year=today.year)
    alarmas = AlarmaEvent.objects.all()
    ultima = alarmas.last()
    usuarios = Miembro.objects.filter(state="Yes")
    viviendas = Vivienda.objects.filter(state="Yes")
    e_this_m = alarmas_this_m.filter(tipo="Emergencia")
    e_last = alarmas.filter(tipo="Emergencia").last()   
    s_this_m = alarmas_this_m.filter(tipo="SOS")
    s_last = alarmas.filter(tipo="SOS").last()     
    f_this_m = alarmas_this_m.filter(tipo="Fuego")
    f_last = alarmas.filter(tipo="Fuego").last() 

    context={
        "barrios" : barrios,
        "alarmas_this_m": alarmas_this_m,
        "ultima": ultima,
        "usuarios": usuarios,
        "viviendas": viviendas,
        "e_this_m": e_this_m,
        "e_last": e_last,
        "s_this_m": s_this_m,
        "s_last": s_last,
        "f_this_m": f_this_m,
        "f_last": f_last,
        "page_title":"Plan B"
    }
    return render(request, template_name,  context)


###########################################################################################
############ monitoreo de alarmas ################################################

# ajax
def latest(request):
    ultima = AlarmaEvent.objects.last()
    userurl = reverse('dashboard:usuario', args=[ultima.miembro.id])

    data = {
        'miembro': str(ultima.miembro),
        'userurl': userurl,
        'tipo': str(ultima.tipo),
        'alarma_vecinal': str(ultima.miembro.vivienda.alarma_vecinal),
        'datetime': str(ultima.datetime.strftime('%d/%m/%Y %H:%M')),
        
    }
    return JsonResponse(data)

def has_new_data(request):
    latest_datetime = request.GET.get('latest_datetime')  # Get the latest datetime from the client-side
    latest_event = AlarmaEvent.objects.last()
    has_new_data = latest_event.datetime.strftime('%d/%m/%Y %H:%M') > latest_datetime  # Compare the latest datetime to the client-side value

    data = {
        'has_new_data': has_new_data
    }
    return JsonResponse(data)




###
@login_required(login_url='dashboard:login')
def alertas(request, pk=None):
    template_name = 'dashboard/sistema/alertas/alertas.html'

    if pk:
        alertas = AlarmaEvent.objects.filter(miembro__id=pk).order_by('-datetime')

    else:
        alertas = AlarmaEvent.objects.all().order_by('-datetime')

    
    
    ultima = alertas.last()
    
    sos = alertas.filter(tipo="SOS", datetime__month=today.month, datetime__year=today.year)
    fuego = alertas.filter(tipo="Fuego", datetime__month=today.month, datetime__year=today.year)
    emerg = alertas.filter(tipo="Emergencia", datetime__month=today.month, datetime__year=today.year)

    context={
        "alertas" : alertas,
        "ultima": ultima,
        "sos": sos,
        "fuego": fuego,
        "emerg": emerg,
        "last_s": sos.last(),
        "last_f": fuego.last(),
        "last_e": emerg.last(),
        "page_title":"Alertas de Alarma"
    }
    return render(request, template_name,  context)



   
   
    # HAGO @LOGIN_REQUIRED?
    
def get_sos(request, pk):
    
    usuario = Miembro.objects.get(id=pk)
    alerta = AlarmaEvent.objects.create(miembro=usuario, tipo="SOS")
    return redirect('success', pk=alerta.pk)


def get_fuego(request, pk):
    usuario = Miembro.objects.get(id=pk)
    alerta = AlarmaEvent.objects.create(miembro=usuario, tipo="Fuego")
    return redirect('success', pk=alerta.pk)



def get_emergencia(request, pk):
    usuario = Miembro.objects.get(id=pk)
    alerta = AlarmaEvent.objects.create(miembro=usuario, tipo="Emergencia")
    alerta.save()
    return redirect('success', pk=alerta.pk)


def success (request, pk):
    alerta = AlarmaEvent.objects.get(id=pk)

    template_name = 'dashboard/sistema/alertas/recibida.html'
    context={
        "alerta" : alerta,
        
    }
    return render(request, template_name, context)


"""
    
    se redirecciona a una página ----->  return redirect template: sistema/alertas/success.html     -

    EL USUARIO VE LA PAGINA DE ÉXITO
"""








########################################################################
########################### crud de barrios #######################################

@login_required(login_url='dashboard:login')
def barrios_list(request):
    template_name = 'dashboard/sistema/barrios/barrios.html'
    
    barrios=AlarmaVecinal.objects.filter(state="Yes")
    alertas = AlarmaEvent.objects.filter(datetime__year=today.year, datetime__month=today.month)
    usuarios=Miembro.objects.filter(state="Yes")
    viviendas= Vivienda.objects.filter(state="Yes")
    ultima = AlarmaEvent.objects.last()

    
    
    if request.method == "GET":
        addform=NewAlarmaVecinalForm()
    if request.method == "POST":
        if "addnew" in request.POST:
            addform = NewAlarmaVecinalForm(request.POST)
            if addform.is_valid():
                newgrupo = addform.save()
                return redirect('dashboard:barrios')
            else:
                return HttpResponse("Something wrong with the form")
    context={
        "barrios": barrios,
        "addform": addform,
        "n_alertas": len(alertas),
        "n_usuarios": len(usuarios),
        "n_casas": len(viviendas),
        "ultima": ultima,

        "page_title":"Alarmas Vecinales"
    }
    return render(request, template_name, context)


@login_required(login_url='dashboard:login')
def barrio_delete(request, pk):
    barrio = get_object_or_404(AlarmaVecinal, id=pk)
    barrio.state = "No"
    barrio.save()
    return redirect('dashboard:barrios')

############################################################################################################
########################### crud de viviendas ###########################

@login_required(login_url='dashboard:login')
def barrio_detail(request, pk): 
    template_name = 'dashboard/sistema/barrios/barrio.html'
    
    barrio = get_object_or_404(AlarmaVecinal, id=pk)
    viviendas = Vivienda.objects.filter(state="Yes", alarma_vecinal = barrio)
    ultima = AlarmaEvent.objects.filter(miembro__vivienda__alarma_vecinal = barrio).last()
    
    emergencias = barrio.get_e
    if len(emergencias) != 0:
        emergencia = barrio.get_e[0]
        e_this_m = []
        for e in emergencias:
            if e.datetime.month == today.month and e.datetime.year == today.year:
                e_this_m.append(e)
    else:
        emergencia = None
        e_this_m = None
            

    soss = barrio.get_s
    if len(soss) != 0:
        sos = barrio.get_s[0]
        s_this_m = []
        for s in soss:
            if s.datetime.month == today.month and s.datetime.year == today.year:
                s_this_m.append(s)
    else:
        sos = None
        s_this_m = None
            
    fuegos = barrio.get_f
    if len(fuegos) != 0:
        fuego = barrio.get_f[0]
        f_this_m = []
        for f in fuegos:
            if f.datetime.month == today.month and f.datetime.year == today.year:
                f_this_m.append(f)
    else:
        fuego = None
        f_this_m = None
            
    
    if request.method == "GET":
        addform=NewViviendaForm()
    if request.method == "POST":
        if "addnew" in request.POST:
            addform = NewViviendaForm(request.POST)
            if addform.is_valid():
                vivienda = addform.save(commit=False)
                vivienda.alarma_vecinal=barrio
                vivienda.save()
                return redirect('dashboard:barrio', pk=barrio.pk)
            else:
                return HttpResponse("Something wrong with the form")
    context={
        "viviendas": viviendas,
        "barrio":barrio,
        "addform": addform,
        "ultima": ultima,
        "page_title":f"Alarma Vecinal {barrio.nombre}",
        "emergencia": emergencia,
        "e_this_m": e_this_m,
        "sos": sos,
        "s_this_m": s_this_m,
        "fuego": fuego,
        "f_this_m": f_this_m,
    }
    return render(request, template_name, context)


@login_required(login_url='dashboard:login')
def vivienda_delete(request, pk):
    
    vivienda = get_object_or_404(Vivienda, id=pk)
    vivienda.state = "No"
    vivienda.save()
    return redirect('dashboard:barrio', pk=vivienda.alarma_vecinal.pk)


@login_required(login_url='dashboard:login')
def vivienda_detail(request, pk):
    
    vivienda = get_object_or_404(Vivienda, id=pk)
    usuarios = vivienda.miembros.filter(state="Yes")
    alarmas = AlarmaEvent.objects.filter(miembro__vivienda= vivienda.pk)
    ultima = alarmas.last()
    e = alarmas.filter(tipo="Emergencia")
    f = alarmas.filter(tipo="Fuego")
    s = alarmas.filter(tipo="SOS")
    
    template_name= 'dashboard/sistema/barrios/vivienda.html'
    addform=NewUsuarioForm()
         
        
    if request.method == "POST":
        if "addnew" in request.POST:
            addform = NewUsuarioForm(request.POST, request.FILES)
            if addform.is_valid():
                usuario = addform.save(commit=False)
                usuario.vivienda = vivienda
                if 'avatar' in request.FILES:
                    avatar = request.FILES['avatar']
                    filename = default_storage.save('profiles/' + avatar.name, avatar)
                    usuario.avatar = filename
                usuario.save()
                return redirect('dashboard:vivienda', pk=vivienda.pk)
            else:
                return HttpResponse("Something wrong with the form")
            
    context ={
        "vivienda" : vivienda,
        "usuarios": usuarios,
        "ultima": ultima,
        "e":e,
        "f":f,
        "s":s,
        "addform" : addform,
    }
    return render(request, template_name, context)





@login_required(login_url='dashboard:login')
def barrio_edit(request, pk):
    
    barrio = get_object_or_404(AlarmaVecinal, id=pk)
    template_name= 'dashboard/sistema/barrios/barrioedit.html'
    editform=NewAlarmaVecinalForm(instance=barrio)
             
        
    if request.method == "POST":
            editform = NewAlarmaVecinalForm(request.POST, instance=barrio)
            if editform.is_valid():
                editform.save()
                return redirect('dashboard:barrio', pk=barrio.pk)
            else:
                return HttpResponse("Something wrong with the form")
            
    context ={
        "barrio" : barrio,
        "editform" : editform,
    }
    return render(request, template_name, context)



@login_required(login_url='dashboard:login')
def vivienda_edit(request, pk):
    
    vivienda = get_object_or_404(Vivienda, id=pk)
    template_name= 'dashboard/sistema/barrios/viviendaedit.html'
    editform=NewViviendaForm(instance=vivienda)
             
        
    if request.method == "POST":
            editform = NewViviendaForm(request.POST, instance=vivienda)
            if editform.is_valid():
                editform.save()
                return redirect('dashboard:vivienda', pk=vivienda.pk)
            else:
                return HttpResponse("Something wrong with the form")
            
    context ={
        "vivienda" : vivienda,
        "editform" : editform,
    }
    return render(request, template_name, context)


############################################################################################################
####################################### USUARIOS GRAL ###########################


@login_required(login_url='dashboard:login')
def users_list(request, pk=None):
    if pk:
        barrio = get_object_or_404(AlarmaVecinal, id=pk)
        usuarios = Miembro.objects.filter(state="Yes", vivienda__alarma_vecinal=barrio)
        context ={
        "usuarios" : usuarios,
        "barrio": barrio,
        
    }
    else:
        usuarios = Miembro.objects.filter(state="Yes")
        context ={
        "usuarios" : usuarios,
        
    }
        
        
    template_name= 'dashboard/sistema/usuarios.html'
            
    
    return render(request, template_name, context)


############################################################################################################
####################################### crud de usuarios dentro de vivievnda ###########################

@login_required(login_url='dashboard:login')
def usuario_detail(request, pk):
    
    usuario = get_object_or_404(Miembro, id=pk)
    template_name= 'dashboard/sistema/barrios/usuario.html'
    editform=NewUsuarioForm(instance=usuario)
   
            
    if request.method == "POST":
        editform = NewUsuarioForm(request.POST, request.FILES, instance=usuario)
        if editform.is_valid():
            if 'avatar' in request.FILES:
                avatar = request.FILES['avatar']
                filename = default_storage.save('profiles/' + avatar.name, avatar)
                usuario.avatar = filename
            usuario.save()
            return redirect('dashboard:usuario', pk=usuario.pk)
        else:
            return HttpResponse("Something wrong with the form")
        
        

            
    context ={
        "usuario" : usuario,
        "editform" : editform,
    }
    return render(request, template_name, context)



@login_required(login_url='dashboard:login')
def usuario_delete(request, pk):
    
    usuario = get_object_or_404(Miembro, id=pk)
    usuario.state = "No"
    usuario.save()
    return redirect('dashboard:vivienda', pk=usuario.vivienda.pk)
########################################################################################################################












################################################################################################################################################
#### start w3cms views ####
@login_required(login_url='dashboard:login')
@permission_required({'dashboard.view_configurations'}, raise_exception=True)
def all_config(request):
    context={
        "page_title":"Configurations",
        "all_config":Configurations.objects.all()
    }
    return render(request,'dashboard/cms/all-configurations.html',context)

@login_required(login_url='dashboard:login')
@permission_required({'dashboard.view_configurations','dashboard.change_configurations'}, raise_exception=True)
def filter_config(request,prefix=None):
    all_filter_config=None
    if prefix:
        if Configurations.objects.filter(name__startswith=f'{prefix}').exists():
            all_filter_config=Configurations.objects.filter(name__startswith=f'{prefix}').order_by('created_at')
            if all_filter_config.filter(name__icontains='.').exists():
                all_filter_config = all_filter_config.filter(name__startswith=f'{prefix}.').order_by('created_at')

    if request.method == 'POST':
        ids = list(request.POST.dict().keys())
        del ids[0]
        ids = [ id for id in ids if 'image_' not in id ]
        for config_obj in Configurations.objects.filter(id__in=ids):
            config_obj.value = request.POST.get(f'{config_obj.id}')
            config_obj.save()
        setup_config.updateConfig()
            

        if request.FILES:
            from django.core.files.storage import FileSystemStorage
            ids = list(request.FILES.dict().keys())
            ids = [id.replace('image_','') for id in ids]
            for config_obj in Configurations.objects.filter(id__in=ids):
                config_obj.value = ""
                images = request.FILES.getlist(f'image_{config_obj.id}')
                img_count = len(images)
               
                for image in images:

                    fs=FileSystemStorage()
                    filename = fs.save('Configurations/'+image.name, image)
                    uploaded_file_url = fs.url(filename)
                    if img_count > 1:
                        if config_obj.value:
                            config_obj.value = f"{config_obj.value},{uploaded_file_url}"
                        else:
                            config_obj.value = uploaded_file_url
                    else:
                        config_obj.value = uploaded_file_url
                    
                    config_obj.save()

            setup_config.updateConfig()

    context={
        "page_title":"Configurations",
        "all_filter_config":all_filter_config,
    }
    # setup_config.updateConfig()
    return render(request,'dashboard/cms/filter-config-by-prefix.html',context)

@login_required(login_url='dashboard:login')
@permission_required({'dashboard.view_configurations','dashboard.change_configurations','dashboard.add_configurations'}, raise_exception=True)
def add_config(request):
    if request.method == 'POST':
        context={
        "page_title":"Add Configurations",
        "config_form":ConfigurationForm(request.POST)
        }
        config_form = context.get('config_form')
        if config_form.is_valid():
            config_obj = config_form.save()

            setup_config.updateConfig()
            prefix = config_obj.name.split('.')[0]

            messages.success(request, "Configuration Add Successfully") 
            return redirect(f'/dashboard/configurations/prefix/{prefix}')
        else:
            messages.error(request, "Somthing Want Wrong") 
            
    else:
        context={
        "page_title":"Add Configurations",
        "config_form":ConfigurationForm()
        }
    return render(request,'dashboard/cms/add-edit-config.html',context)

@login_required(login_url='dashboard:login')
@permission_required({'dashboard.view_configurations','dashboard.change_configurations',}, raise_exception=True)
def edit_config(request,id):
    config_obj = get_object_or_404(Configurations,id=id)
    if request.method == 'POST':
        context={
        "page_title":"Edit Configurations",
        "config_form":ConfigurationForm(request.POST, instance=config_obj)
        }
        config_form = context.get('config_form')

        if config_form.is_valid():
            config_obj = config_form.save()
            setup_config.updateConfig()

            prefix = config_obj.name.split('.')[0]
            messages.success(request, "Configuration Update Successfully") 
            return redirect(f'/dashboard/configurations/prefix/{prefix}')
        else:
            messages.error(request, "Somthing Want Wrong")

    else:
        context={
        "page_title":"Edit Configurations",
        "config_form":ConfigurationForm(instance=config_obj)
        }
    return render(request,'dashboard/cms/add-edit-config.html',context)

@login_required(login_url='dashboard:login')
@permission_required({'dashboard.view_configurations','dashboard.delete_configurations'}, raise_exception=True)
def delete_config(request,id):
    config_obj = Configurations.objects.get(id=id)
    if config_obj:
        config_obj.delete()
        setup_config.updateConfig()
        messages.success(request, "Configuration Delete Successfully") 
    else:
        messages.error(request, "Configuration Not Valid") 

    return redirect("dashboard:all-config")



def count(d):
    return max(count(v) if isinstance(v,dict) else 0 for v in d.values()) + 1


@login_required(login_url='dashboard:login')
@permission_required({'dashboard.view_configurations','dashboard.delete_configurations','dashboard.add_configurations'}, raise_exception=True)
def reset_config(request):
    path = "configurations/config.json"
    full_path = os.path.join(settings.BASE_DIR,path)
    Configurations.objects.all().delete()

    with open(full_path,'r') as f:
        configdata = json.load(f)
       
        for key1, value1 in configdata.items():
            if count(value1) == 2:
                for key2, value2 in value1.items():
                    name = key1+"."+key2
                    value = value2.get('value')
                    title = value2.get('title')
                    description = value2.get('description')
                    input_type = value2.get('input_type')
                    editable = value2.get('editable')
                    order = value2.get('order')
                    params = value2.get('params')
                    config_obj = Configurations(
                                    name=name,
                                    value=value,
                                    title=title,
                                    description=description,
                                    input_type=input_type,
                                    editable=editable,
                                    order=order,
                                    params=params
                                )
                    config_obj.save()
    setup_config.updateConfig()
    return redirect("dashboard:all-config")
        
        


@login_required(login_url='dashboard:login')
def download_config(request):
    path = "configurations/Config"
    pickle_file_path = os.path.join(settings.BASE_DIR, path)
   
    dbfile = open(pickle_file_path, 'rb')
    config_data = pickle.load(dbfile)
    dbfile.close()
    
    json_file_path =os.path.join(settings.BASE_DIR,'configurations/config.json')
    json_file = open(json_file_path,'w')
    json_file.write(json.dumps(config_data,indent=4))
    json_file.close()
    mime_type, _ = mimetypes.guess_type(json_file_path)
    
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as fh:
            response = HttpResponse(fh, content_type=mime_type)
            response['Content-Disposition'] = "attachment; filename=%s" % 'config.json'
            return response
    raise Http404



#######################################################################################


@login_required(login_url='dashboard:login')
def index2(request):
    context={
        "page_title":"Dashboard"
    }
    return render(request,'dashboard/index-2.html',context)

@login_required(login_url='dashboard:login')
def schedule(request):
    context={
        "page_title":"Schedule"
    }
    return render(request,'dashboard/schedule.html',context)

@login_required(login_url='dashboard:login')
def instructors(request):
    context={
        "page_title":"Instructors"
    }
    return render(request,'dashboard/instructors.html',context)

@login_required(login_url='dashboard:login')
def message(request):
    context={
        "page_title":"Message"
    }
    return render(request,'dashboard/message.html',context)

@login_required(login_url='dashboard:login')
def activity(request):
    context={
        "page_title":"Activity"
    }
    return render(request,'dashboard/activity.html',context)

@login_required(login_url='dashboard:login')
def profile(request):
    context={
        "page_title":"Profile"
    }
    return render(request,'dashboard/profile.html',context)

@login_required(login_url='dashboard:login')
def courses(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'dashboard/courses/courses.html',context)


@login_required(login_url='dashboard:login')
def course_details_1(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'dashboard/courses/course-details-1.html',context)

@login_required(login_url='dashboard:login')
def course_details_2(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'dashboard/courses/course-details-2.html',context)

@login_required(login_url='dashboard:login')
def instructor_dashboard(request):
    context={
        "page_title":"Dashboard"
    }
    return render(request,'dashboard/instructor/instructor-dashboard.html',context)

@login_required(login_url='dashboard:login')
def instructor_courses(request):
    context={
        "page_title":"Courses"
    }
    return render(request,'dashboard/instructor/instructor-courses.html',context)

@login_required(login_url='dashboard:login')
def instructor_schedule(request):
    context={
        "page_title":"Instructor Schedule"
    }
    return render(request,'dashboard/instructor/instructor-schedule.html',context)

@login_required(login_url='dashboard:login')
def instructor_students(request):
    context={
        "page_title":"Instructor Students"
    }
    return render(request,'dashboard/instructor/instructor-students.html',context)

@login_required(login_url='dashboard:login')
def instructor_resources(request):
    context={
        "page_title":"Instructor Resources"
    }
    return render(request,'dashboard/instructor/instructor-resources.html',context)

@login_required(login_url='dashboard:login')
def instructor_transactions(request):
    context={
        "page_title":"Instructor Transactions"
    }
    return render(request,'dashboard/instructor/instructor-transactions.html',context)

@login_required(login_url='dashboard:login')
def instructor_liveclass(request):
    context={
        "page_title":"Live Class"
    }
    return render(request,'dashboard/instructor/instructor-liveclass.html',context)

@login_required(login_url='dashboard:login')
def app_profile(request):
    context={
        "page_title":"Profile"
    }
    return render(request,'dashboard/apps/app-profile.html',context)

@login_required(login_url='dashboard:login')
def post_details(request):
    context={
        "page_title":"Post Details"
    }
    return render(request,'dashboard/apps/post-details.html',context)

@login_required(login_url='dashboard:login')
def email_compose(request):
    context={
        "page_title":"Compose"
    }
    return render(request,'dashboard/apps/email/email-compose.html',context)

@login_required(login_url='dashboard:login')
def email_inbox(request):
    context={
        "page_title":"Inbox"
    }
    return render(request,'dashboard/apps/email/email-inbox.html',context)

@login_required(login_url='dashboard:login')
def email_read(request):
    context={
        "page_title":"Read"
    }
    return render(request,'dashboard/apps/email/email-read.html',context)

@login_required(login_url='dashboard:login')
def app_calender(request):
    context={
        "page_title":"Calendar"
    }
    return render(request,'dashboard/apps/app-calender.html',context)

@login_required(login_url='dashboard:login')
def ecom_product_grid(request):
    context={
        "page_title":"Product-Grid"
    }
    return render(request,'dashboard/apps/shop/ecom-product-grid.html',context)

@login_required(login_url='dashboard:login')
def ecom_product_list(request):
    context={
        "page_title":"Product-List"
    }
    return render(request,'dashboard/apps/shop/ecom-product-list.html',context)

@login_required(login_url='dashboard:login')
def ecom_product_detail(request):
    context={
        "page_title":"Product-Detail"
    }
    return render(request,'dashboard/apps/shop/ecom-product-detail.html',context)

@login_required(login_url='dashboard:login')
def ecom_product_order(request):
    context={
        "page_title":"Product-Order"
    }
    return render(request,'dashboard/apps/shop/ecom-product-order.html',context)

@login_required(login_url='dashboard:login')
def ecom_checkout(request):
    context={
        "page_title":"Checkout"
    }
    return render(request,'dashboard/apps/shop/ecom-checkout.html',context)

@login_required(login_url='dashboard:login')
def ecom_invoice(request):
    context={
        "page_title":"Invoice"
    }
    return render(request,'dashboard/apps/shop/ecom-invoice.html',context)

@login_required(login_url='dashboard:login')
def ecom_customers(request):
    context={
        "page_title":"Customers"
    }
    return render(request,'dashboard/apps/shop/ecom-customers.html',context)

@login_required(login_url='dashboard:login')
def chart_flot(request):
    context={
        "page_title":"Chart-Flot"
    }
    return render(request,'dashboard/charts/chart-flot.html',context)

@login_required(login_url='dashboard:login')
def chart_morris(request):
    context={
        "page_title":"Chart-Morris"
    }
    return render(request,'dashboard/charts/chart-morris.html',context)

@login_required(login_url='dashboard:login')
def chart_chartjs(request):
    context={
        "page_title":"Chart-Chartjs"
    }
    return render(request,'dashboard/charts/chart-chartjs.html',context)

@login_required(login_url='dashboard:login')
def chart_chartist(request):
    context={
        "page_title":"Chart-Chartist"
    }
    return render(request,'dashboard/charts/chart-chartist.html',context)

@login_required(login_url='dashboard:login')
def chart_sparkline(request):
    context={
        "page_title":"Chart-Sparkline"
    }
    return render(request,'dashboard/charts/chart-sparkline.html',context)

@login_required(login_url='dashboard:login')
def chart_peity(request):
    context={
        "page_title":"Chart-Peity"
    }
    return render(request,'dashboard/charts/chart-peity.html',context)

@login_required(login_url='dashboard:login')
def ui_accordion(request):
    context={
        "page_title":"Accordion"
    }
    return render(request,'dashboard/bootstrap/ui-accordion.html',context)

@login_required(login_url='dashboard:login')
def ui_alert(request):
    context={
        "page_title":"Alert"
    }
    return render(request,'dashboard/bootstrap/ui-alert.html',context)

@login_required(login_url='dashboard:login')  
def ui_badge(request):
    context={
        "page_title":"Badge"
    }
    return render(request,'dashboard/bootstrap/ui-badge.html',context)

@login_required(login_url='dashboard:login')
def ui_button(request):
    context={
        "page_title":"Button"
    }
    return render(request,'dashboard/bootstrap/ui-button.html',context)

@login_required(login_url='dashboard:login')
def ui_modal(request):
    context={
        "page_title":"Modal"
    }
    return render(request,'dashboard/bootstrap/ui-modal.html',context)

@login_required(login_url='dashboard:login')
def ui_button_group(request):
    context={
        "page_title":"Button Group"
    }
    return render(request,'dashboard/bootstrap/ui-button-group.html',context)

@login_required(login_url='dashboard:login')
def ui_list_group(request):
    context={
        "page_title":"List Group"
    }
    return render(request,'dashboard/bootstrap/ui-list-group.html',context)

@login_required(login_url='dashboard:login')
def ui_media_object(request):
    context={
        "page_title":"Media Object"
    }
    return render(request,'dashboard/bootstrap/ui-media-object.html',context)

@login_required(login_url='dashboard:login')
def ui_card(request):
    context={
        "page_title":"Card"
    }
    return render(request,'dashboard/bootstrap/ui-card.html',context)

@login_required(login_url='dashboard:login')
def ui_carousel(request):
    context={
        "page_title":"Carousel"
    }
    return render(request,'dashboard/bootstrap/ui-carousel.html',context)

@login_required(login_url='dashboard:login')
def ui_dropdown(request):
    context={
        "page_title":"Dropdown"
    }
    return render(request,'dashboard/bootstrap/ui-dropdown.html',context)

@login_required(login_url='dashboard:login')
def ui_popover(request):
    context={
        "page_title":"Popover"
    }
    return render(request,'dashboard/bootstrap/ui-popover.html',context)

@login_required(login_url='dashboard:login')
def ui_progressbar(request):
    context={
        "page_title":"Progressbar"
    }
    return render(request,'dashboard/bootstrap/ui-progressbar.html',context)

@login_required(login_url='dashboard:login')
def ui_tab(request):
    context={
        "page_title":"Tab"
    }
    return render(request,'dashboard/bootstrap/ui-tab.html',context)

@login_required(login_url='dashboard:login')
def ui_typography(request):
    context={
        "page_title":"Typography"
    }
    return render(request,'dashboard/bootstrap/ui-typography.html',context)

@login_required(login_url='dashboard:login')
def ui_pagination(request):
    context={
        "page_title":"Pagination"
    }
    return render(request,'dashboard/bootstrap/ui-pagination.html',context)

@login_required(login_url='dashboard:login')
def ui_grid(request):
    context={
        "page_title":"Grid"
    }
    return render(request,'dashboard/bootstrap/ui-grid.html',context)

@login_required(login_url='dashboard:login')
def uc_select2(request):
    context={
        "page_title":"Select"
    }
    return render(request,'dashboard/plugins/uc-select2.html',context)

@login_required(login_url='dashboard:login')
def uc_nestable(request):
    context={
        "page_title":"Nestable"
    }
    return render(request,'dashboard/plugins/uc-nestable.html',context)

@login_required(login_url='dashboard:login')
def uc_noui_slider(request):
    context={
        "page_title":"UI Slider"
    }
    return render(request,'dashboard/plugins/uc-noui-slider.html',context)

@login_required(login_url='dashboard:login')
def uc_sweetalert(request):
    context={
        "page_title":"Sweet Alert"
    }
    return render(request,'dashboard/plugins/uc-sweetalert.html',context)

@login_required(login_url='dashboard:login')
def uc_toastr(request):
    context={
        "page_title":"Toastr"
    }
    return render(request,'dashboard/plugins/uc-toastr.html',context)

@login_required(login_url='dashboard:login')
def map_jqvmap(request):
    context={
        "page_title":"Jqvmap"
    }
    return render(request,'dashboard/plugins/map-jqvmap.html',context)

@login_required(login_url='dashboard:login')
def uc_lightgallery(request):
    context={
        "page_title":"LightGallery"
    }
    return render(request,'dashboard/plugins/uc-lightgallery.html',context)

@login_required(login_url='dashboard:login')
def widget_basic(request):
    context={
        "page_title":"Widget"
    }
    return render(request,'dashboard/widget-basic.html',context)

@login_required(login_url='dashboard:login')
def form_element(request):
    context={
        "page_title":"Form Element"
    }
    return render(request,'dashboard/forms/form-element.html',context)

@login_required(login_url='dashboard:login')
def form_wizard(request):
    context={
        "page_title":"Form Wizard"
    }
    return render(request,'dashboard/forms/form-wizard.html',context)

@login_required(login_url='dashboard:login')
def form_ckeditor(request):
    context={
        "page_title":"Ckeditor"
    }
    return render(request,'dashboard/forms/form-ckeditor.html',context)

@login_required(login_url='dashboard:login')
def form_pickers(request):
    context={
        "page_title":"Pickers"
    }
    return render(request,'dashboard/forms/form-pickers.html',context)

@login_required(login_url='dashboard:login')
def form_validation(request):
    context={
        "page_title":"Form Validation"
    }
    return render(request,'dashboard/forms/form-validation-jquery.html',context)


@login_required(login_url='dashboard:login')
def table_bootstrap_basic(request):
    context={
        "page_title":"Table Bootstrap"
    }
    return render(request,'dashboard/table/table-bootstrap-basic.html',context)

@login_required(login_url='dashboard:login')
def table_datatable_basic(request):
    context={
        "page_title":"Table Datatable"
    }
    return render(request,'dashboard/table/table-datatable-basic.html',context)





def page_lock_screen(request):
    return render(request,'dashboard/pages/page-lock-screen.html')





def page_error_400(request):
    return render(request,'400.html')
    
def page_error_403(request):
    return render(request,'403.html')

def page_error_404(request):
    return render(request,'404.html')

def page_error_500(request):
    return render(request,'500.html')

def page_error_503(request):
    return render(request,'503.html')

def empty_page(request):
    context={
        "page_title":"Page Empty"
    }
    return render(request,'dashboard/pages/empty-page.html',context)

