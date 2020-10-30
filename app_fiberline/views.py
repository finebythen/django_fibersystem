from django.contrib import messages
from django.shortcuts import render, redirect
from django_pandas.io import read_frame

import folium

from .models import *
from .forms import *
from .filters import *
from .functions import *


def main(request):
    # --> Database-Querys
    customer_db = Customer.objects.all()
    project_db = Project.objects.all()
    cluster_db = Cluster.objects.all()
    technikstandorte_db = Technikstandort.objects.all()

    # --> create filter (django_filters)
    tst_filter = TstFilter(request.GET, queryset=technikstandorte_db)
    technikstandorte_db = tst_filter.qs

    # --> load query into dataframe (pandas)
    technikstandorte_df = read_frame(technikstandorte_db)
    technikstandorte_df['value_sum'] = 1

    # --> calculations
    customer_amount = customer_db.count()
    project_amount = project_db.count()
    cluster_amount = cluster_db.count()

    tst_grouped_df = technikstandorte_df.groupby(['type'])[['value_sum']].agg('sum').reset_index()
    chart_1_label = tst_grouped_df['type'].tolist()
    chart_1_data = tst_grouped_df['value_sum'].tolist()

    context = {'technikstandorte_db': technikstandorte_db, 'chart_1_label': chart_1_label, 'chart_1_data': chart_1_data,
               'customer_amount': customer_amount, 'project_amount': project_amount, 'cluster_amount': cluster_amount,
               'filter': tst_filter}
    return render(request, 'app_fiberline/main.html', context)


def view_technikstandort(request, pk):
    # --> Database-Querys
    tst_db = Technikstandort.objects.get(id=pk)
    try:
        tst_default = TechnikstandortDefault.objects.get(technikstandort_name=tst_db.name)
        schacht_kvz_db = Schacht_Kvz.objects.filter(technikstandort=tst_db.name)
        kabel_db = Kabel.objects.filter(technikstandort=tst_db.id)
    except Exception as e:
        tst_default = None
        schacht_kvz_db = None
        kabel_db = None

    # --> check wether query is empty or not

    default_exists = [0 if not tst_default else 1]
    default_exists = default_exists[0]

    context = {'tst_db': tst_db, 'schacht_kvz_db': schacht_kvz_db, 'kabel_db': kabel_db, 'default_exists': default_exists}
    return render(request, 'app_fiberline/view_technikstandort.html', context)


def view_schacht_kvz(request, pk):
    # --> Database-Query
    schacht_kvz_db = Schacht_Kvz.objects.get(id=pk)
    rohre_db = Rohr.objects.filter(schacht_kvz=schacht_kvz_db.name)
    ha_rohre_db = Hausanschlussrohr.objects.filter(schacht_kvz=schacht_kvz_db.name)
    ha_rohre_db_func = ha_rohre_db.filter(einzelrohr_malfunction=False)

    # --> create filter (django_filters)
    my_filter = HausanschlussrohrFilter(request.GET, queryset=ha_rohre_db_func)
    ha_rohre_db_func = my_filter.qs

    # --> Calculations
    list_rohr_name = []
    list_rohre = []
    for item in rohre_db:
        amount = ha_rohre_db.filter(rohr_name=item.name).count()
        list_rohre.append(amount)
        list_rohr_name.append(item.name)

    # --> create dictionary from two lists
    dict_rohre = {list_rohr_name[i]: list_rohre[i] for i in range(len(list_rohr_name))}

    # --> Create Map (folium)
    m = folium.Map(width='100%', height='100%', location=[schacht_kvz_db.geo_latitude, schacht_kvz_db.geo_longitude], zoom_start=12)

    # --> add Marker to Map
    folium.Marker(
        location=[schacht_kvz_db.geo_latitude, schacht_kvz_db.geo_longitude],
        popup=schacht_kvz_db.name,
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

    # --> update Map
    m = m._repr_html_()

    context = {'schacht_kvz_db': schacht_kvz_db, 'rohre_db': rohre_db, 'my_map': m, 'dict_rohre': dict_rohre,
               'ha_rohre_db_func': ha_rohre_db_func, 'filter': my_filter}
    return render(request, 'app_fiberline/view_schacht_kvz.html', context)


def create_technikstandort_default(request, pk):
    # --> Database-Query
    tst_db = Technikstandort.objects.get(id=pk)

    form = Create_Technikstandort_Default_Form()

    if request.method == 'POST':
        form = Create_Technikstandort_Default_Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.customer = tst_db.customer
            form.instance.project = tst_db.project
            form.instance.cluster = tst_db.cluster
            form.instance.technikstandort_name = tst_db.name
            form.instance.technikstandort_id = int(pk)
            form.instance.user_created = request.user
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Grundeinstellungen für {} erfolgreich gespeichert!'.format(tst_db.name))
            return redirect("Technikstandort", tst_db.id)
        else:
            messages.add_message(request, messages.WARNING, 'Grundeinstellungen für {} konnten nicht gespeichert werden!'.format(tst_db.name))

    context = {'formset': form, 'tst_db': tst_db}
    return render(request, 'app_fiberline/create_technikstandort_default.html', context)


def create_schacht_kvz(request, pk):
    # --> Database-Querys
    tst_db = Technikstandort.objects.get(id=pk)

    form = Create_Schacht_Kvz_Form()

    if request.method == 'POST':
        form = Create_Schacht_Kvz_Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.customer = tst_db.customer
            form.instance.project = tst_db.project
            form.instance.cluster = tst_db.cluster
            form.instance.technikstandort_id = tst_db.id
            form.instance.technikstandort = tst_db.name
            form.instance.user_created = request.user
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Der Eintrag wurde gespeichert!')
            return redirect("Technikstandort", tst_db.id)
        else:
            messages.add_message(request, messages.WARNING, 'Der Eintrag konnte nicht gespeichert werden!')

    context = {'formset': form, 'tst_db': tst_db}
    return render(request, 'app_fiberline/create_schacht_kvz.html', context)


def create_rohr(request, pk):
    # --> Database-Query
    schacht_kvz_db = Schacht_Kvz.objects.get(id=pk)
    rohre_db = Rohr.objects.filter(schacht_kvz=schacht_kvz_db.name)

    rohre_count = rohre_db.count()

    form = Create_Rohr_Form()

    if request.method == 'POST':
        form = Create_Rohr_Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.customer = schacht_kvz_db.customer
            form.instance.project = schacht_kvz_db.project
            form.instance.cluster = schacht_kvz_db.cluster
            form.instance.technikstandort = schacht_kvz_db.technikstandort
            form.instance.technikstandort_id = schacht_kvz_db.technikstandort_id
            form.instance.schacht_kvz = schacht_kvz_db.name
            form.instance.user_created = request.user
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Rohr wurde erstellt!')
            return redirect("SchachtKvz", schacht_kvz_db.id)
        else:
            messages.add_message(request, messages.WARNING, 'Rohr konnte nicht erstellt werden!')

    context = {'formset': form, 'schacht_kvz_db': schacht_kvz_db, 'rohre_db': rohre_db, 'rohre_count': rohre_count}
    return render(request, 'app_fiberline/create_rohr.html', context)


def create_einzelrohr(request, pk):
    # --> Database-Query
    rohr_db = Rohr.objects.get(name=pk)
    schacht_kv_db = Schacht_Kvz.objects.get(name=rohr_db.schacht_kvz)
    tst_default_db = TechnikstandortDefault.objects.get(technikstandort_name=rohr_db.technikstandort)
    einzelrohr_typ_db = EinzelrohrTyp.objects.filter(rohr_typ=rohr_db.type)
    ha_rohre_db = Hausanschlussrohr.objects.filter(rohr_name=rohr_db.name)

    ha_rohre_db_func = ha_rohre_db.filter(einzelrohr_malfunction=False)
    ha_rohre_db_malfunc = ha_rohre_db.filter(einzelrohr_malfunction=True)

    # --> get all 'einzelrohre_typ' from 'rohre_typ' into list (unfiltered)
    list_einzelrohr_typ_all = [item.name for item in einzelrohr_typ_db]

    # --> get every used 'einzelrohre_typ' from 'rohre_typ' into list (unfiltered)
    list_einzelrohr_typ_used = [item.einzelrohr_name for item in ha_rohre_db]

    # --> get difference between top lists and keep not used 'einzelrohre'
    list_einzelrohr_diff = Diff(list_einzelrohr_typ_all, list_einzelrohr_typ_used)
    list_einzelrohr_diff.sort()

    form = Create_Einzelrohr_Form()

    if request.method == 'POST':
        form = Create_Einzelrohr_Form(request.POST, request.FILES)
        if form.is_valid():
            # --> Calculations WE-Number
            we_val = [0 if not request.POST.get('ha_rohr_we_num') else int(request.POST.get('ha_rohr_we_num'))]
            form.instance.we_number = we_val[0]
            form.instance.customer = rohr_db.customer
            form.instance.project = rohr_db.project
            form.instance.cluster = rohr_db.cluster
            form.instance.technikstandort = rohr_db.technikstandort
            form.instance.technikstandort_id = rohr_db.technikstandort_id
            form.instance.schacht_kvz = rohr_db.schacht_kvz
            form.instance.rohr_typ = rohr_db.type
            form.instance.rohr_name = rohr_db.name
            form.instance.einzelrohr_name = request.POST.get('ha_rohr_remaining')
            # --> Calculations Fiberunit-Size
            fu_val = [0 if not request.POST.get('ha_rohr_we_num') else int(request.POST.get('ha_rohr_we_num'))]
            form.instance.fiberunit_size = calcFiberunitSize(fu_val[0], tst_default_db)
            form.instance.user_created = str(request.user)

            form.save()
            messages.add_message(request, messages.SUCCESS, 'Einzelrohr erfolgreich gespeichert!')
            return redirect("CreateEinzelrohr", pk)
        else:
            messages.add_message(request, messages.WARNING, 'Einzelrohr konnte nicht gespeichert werden!')

    context = {'formset': form, 'rohr_db': rohr_db, 'list_remaining': list_einzelrohr_diff, 'ha_rohre_db_func': ha_rohre_db_func,
               'ha_rohre_db_malfunc': ha_rohre_db_malfunc, 'schacht_kv_db': schacht_kv_db}
    return render(request, 'app_fiberline/create_einzelrohr.html', context)


def create_kabel(request, pk):
    # --> Database-Query
    tst_db = Technikstandort.objects.get(id=pk)

    form = Create_Kabel_Form()

    if request.method == 'POST':
        form = Create_Kabel_Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user_created = request.user
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Kabel erfolgreich erstellt!')
            return redirect("Technikstandort", tst_db.id)
        else:
            messages.add_message(request, messages.WARNING, 'Kabel konnte nicht erstellt werden!')

    context = {'formset': form, 'tst_db': tst_db}
    return render(request, 'app_fiberline/create_kabel.html', context)


def create_wohneinheiten(request, pk):
    # --> Database-Query
    ha_rohr_db = Hausanschlussrohr.objects.get(id=pk)
    schacht_kvz_db = Schacht_Kvz.objects.get(name=ha_rohr_db.schacht_kvz)
    we_db = Wohneinheit.objects.filter(hausanschlussrohr=ha_rohr_db)

    # --> get customers full name
    if not ha_rohr_db.ha_add:
        customer = f"{ha_rohr_db.strasse} {ha_rohr_db.ha_number}"
    else:
        customer = f"{ha_rohr_db.strasse} {ha_rohr_db.ha_number}{ha_rohr_db.ha_add}"

    # --> Calculations
    we_future = ha_rohr_db.we_number
    we_present = we_db.count()
    we_stat = [True if we_present >= we_future else False]
    we_stat = we_stat[0]

    form = Create_Wohneinheit_Form()

    if request.method == 'POST':
        form = Create_Wohneinheit_Form(request.POST, request.FILES)
        if form.is_valid():
            form.instance.hausanschlussrohr = ha_rohr_db
            form.instance.user_created = str(request.user)
            form.save()
            messages.add_message(request, messages.SUCCESS, f"Wohneinheit für Adresse {customer} wurde gespeichert!")
            return redirect("CreateWohneinheiten", pk)
        else:
            messages.add_message(request, messages.WARNING, f"Wohneinheit für Adresse {customer} konnte nicht gespeichert werden!")

    context = {'formset': form, 'ha_rohr_db': ha_rohr_db, 'schacht_kvz_db': schacht_kvz_db, 'we_db': we_db,
               'customer': customer, 'we_stat': we_stat}
    return render(request, 'app_fiberline/create_wohneinheiten.html', context)


def combine_schacht_kvz_kabel(request, pk):
    # --> Database-Querys
    schacht_kvz_db = Schacht_Kvz.objects.get(id=pk)

    form = Combine_Schacht_Kvz_Kabel_Form(instance=schacht_kvz_db)

    if request.method == 'POST':
        form = Combine_Schacht_Kvz_Kabel_Form(request.POST, instance=schacht_kvz_db)
        if form.is_valid():
            form.instance.user_updated = str(request.user)
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Schacht/Kvz & Kabel erfolgreich verbunden!')
            return redirect("SchachtKvz", schacht_kvz_db.id)
        else:
            messages.add_message(request, messages.WARNING, 'Schacht/Kvz & Kabel konnten nicht miteinander verbunden werden!')

    context = {'formset': form, 'schacht_kvz_db': schacht_kvz_db}
    return render(request, 'app_fiberline/combine_schacht_kvz_kabel.html', context)


def update_schacht_kvz(request, pk):
    # --> Database-Querys
    schacht_kvz_db = Schacht_Kvz.objects.get(id=pk)

    form = Update_Schacht_Kvz_Form(instance=schacht_kvz_db)

    if request.method == 'POST':
        form = Update_Schacht_Kvz_Form(request.POST, instance=schacht_kvz_db)
        if form.is_valid():
            form.instance.user_updated = str(request.user)
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Schacht/Kvz wurde erfolgreich aktualisiert!')
            return redirect("Technikstandort", schacht_kvz_db.technikstandort_id)
        else:
            messages.add_message(request, messages.WARNING, 'Schacht/Kvz konnte nicht aktualisiert werden!')

    context = {'formset': form, 'schacht_kvz_db': schacht_kvz_db}
    return render(request, 'app_fiberline/update_schacht_kvz.html', context)


def update_kabel(request, pk):
    # --> Database-Query
    kabel_db = Kabel.objects.get(id=pk)

    form = Update_Kabel_Form(instance=kabel_db)

    if request.method == 'POST':
        form = Update_Kabel_Form(request.POST, instance=kabel_db)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Kabel wurde aktualisiert!')
            return redirect("Technikstandort", kabel_db.technikstandort.id)
        else:
            messages.add_message(request, messages.WARNING, 'Kabel konnte nicht aktualisiert werden!')

    context = {'formset': form, 'kabel_db': kabel_db}
    return render(request, 'app_fiberline/update_kabel.html', context)


def update_technikstandort_default(request, pk):
    # --> Database-Query
    tst_db = Technikstandort.objects.get(id=pk)
    tst_default = TechnikstandortDefault.objects.get(technikstandort_name=tst_db.name)

    form = Update_Technikstandort_Default_Form(instance=tst_default)

    if request.method == 'POST':
        form = Update_Technikstandort_Default_Form(request.POST, instance=tst_default)
        if form.is_valid():
            form.instance.user_updated = str(request.user)
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Grundeinstellungen {} wurden aktualisiert!'.format(tst_db.name))
            return redirect("Technikstandort", tst_db.id)
        else:
            messages.add_message(request, messages.WARNING, 'Grundeinstellungen {} konnten nicht aktualisiert werden!'.format(tst_db.name))

    context = {'formset': form, 'tst_db': tst_db}
    return render(request, 'app_fiberline/update_technikstandort_default.html', context)


def delete_wohneinheit(request, pk):
    # --> Database-Query
    we_db = Wohneinheit.objects.get(id=pk)

    # --> get customers id
    ha_rohr_id = we_db.hausanschlussrohr.id

    # --> get customers full name
    if not we_db.hausanschlussrohr.ha_add:
        customer = f"{we_db.hausanschlussrohr.strasse} {we_db.hausanschlussrohr.ha_number}"
    else:
        customer = f"{we_db.hausanschlussrohr.strasse} {we_db.hausanschlussrohr.ha_number}{we_db.hausanschlussrohr.ha_add}"

    if request.method == 'POST':
        we_db.delete()
        return redirect("CreateWohneinheiten", ha_rohr_id)

    context = {'we_db': we_db, 'customer': customer, 'ha_rohr_id': ha_rohr_id}
    return render(request, 'app_fiberline/delete_wohneinheit.html', context)
