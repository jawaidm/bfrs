from bfrs.models import (Bushfire, AreaBurnt, Damage, Injury)
from django.db import IntegrityError, transaction
from django.http import HttpResponse
import json

import unicodecsv
from django.utils.encoding import smart_str
from datetime import datetime
from django.core import serializers
from xlwt import Workbook
from itertools import count


def breadcrumbs_li(links):
    """Returns HTML: an unordered list of URLs (no surrounding <ul> tags).
    ``links`` should be a iterable of tuples (URL, text).
    """
    crumbs = ''
    li_str = '<li><a href="{}">{}</a></li>'
    li_str_last = '<li class="active"><span>{}</span></li>'
    # Iterate over the list, except for the last item.
    if len(links) > 1:
        for i in links[:-1]:
            crumbs += li_str.format(i[0], i[1])
    # Add the last item.
    crumbs += li_str_last.format(links[-1][1])
    return crumbs

def serialize_bushfire(auth_type, obj):
    "Serializes a Bushfire object"
    if auth_type == 'initial':
            obj.initial_snapshot = serializers.serialize('json', [obj])
    if auth_type == 'final':
            obj.final_snapshot = serializers.serialize('json', [obj])
    obj.save()

def deserialize_bushfire(auth_type, obj):
    "Returns a deserialized Bushfire object"
    if auth_type == 'initial':
            return serializers.deserialize("json", obj.initial_snapshot).next().object
    if auth_type == 'final':
            return serializers.deserialize("json", obj.final_snapshot).next().object


def calc_coords(obj):
    coord_type = obj.coord_type
    if coord_type == Bushfire.COORD_TYPE_MGAZONE:
        obj.lat_decimal = float(obj.mga_zone)/2.0
        obj.lat_degrees = float(obj.mga_zone)/2.0
        obj.lat_minutes = float(obj.mga_zone)/2.0

        obj.lon_decimal = float(obj.mga_zone)/2.0
        obj.lon_degrees = float(obj.mga_zone)/2.0
        obj.lon_minutes = float(obj.mga_zone)/2.0

    elif coord_type == Bushfire.COORD_TYPE_LATLONG:
        obj.mga_zone = float(obj.lat_decimal) * 2.0
        obj.mga_easting = float(obj.lat_decimal) * 2.0
        obj.mga_northing = float(obj.lat_decimal) * 2.0


def update_areas_burnt_fs(bushfire, area_burnt_formset):
    new_fs_object = []
    for form in area_burnt_formset:
        if form.is_valid():
            tenure = form.cleaned_data.get('tenure')
            area = form.cleaned_data.get('area')
            remove = form.cleaned_data.get('DELETE')

            if not remove and (tenure and area):
                new_fs_object.append(AreaBurnt(bushfire=bushfire, tenure=tenure, area=area))

    try:
        with transaction.atomic():
            AreaBurnt.objects.filter(bushfire=bushfire).delete()
            AreaBurnt.objects.bulk_create(new_fs_object)
    except IntegrityError:
        return 0

    return 1

def update_injury_fs(bushfire, injury_formset):
    new_fs_object = []
    for form in injury_formset:
        if form.is_valid():
            injury_type = form.cleaned_data.get('injury_type')
            number = form.cleaned_data.get('number')
            remove = form.cleaned_data.get('DELETE')

            if not remove and (injury_type and number):
                new_fs_object.append(Injury(bushfire=bushfire, injury_type=injury_type, number=number))

    try:
        with transaction.atomic():
            Injury.objects.filter(bushfire=bushfire).delete()
            Injury.objects.bulk_create(new_fs_object)
    except IntegrityError:
        return 0

    return 1

def update_damage_fs(bushfire, damage_formset):
    new_fs_object = []
    for form in damage_formset:
        if form.is_valid():
            damage_type = form.cleaned_data.get('damage_type')
            number = form.cleaned_data.get('number')
            remove = form.cleaned_data.get('DELETE')

            if not remove and (damage_type and number):
                new_fs_object.append(Damage(bushfire=bushfire, damage_type=damage_type, number=number))

    try:
        with transaction.atomic():
            Damage.objects.filter(bushfire=bushfire).delete()
            Damage.objects.bulk_create(new_fs_object)
    except IntegrityError:
        return 0

    return 1

def export_final_csv(request, queryset):
    #import csv
    filename = 'export_final-' + datetime.now().strftime('%Y-%m-%dT%H%M%S') + '.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = unicodecsv.writer(response, quoting=unicodecsv.QUOTE_ALL)

    writer.writerow([
        "ID",
		"Region",
		"District",
		"Name",
		"Year",
		"Incident No",
		"DFES Incident No",
		"Job Code",
		"Fire Level",
		"Media Alert Req",
		"Investigation Req",
		"Fire Position",
		#"Origin Point",
		#"Fire Boundary",
		"Fire Not Found",
		"Assistance Req",
		"Communications",
		"Other Info",
		"Cause",
		"Other Cause",
		"Field Officer",
		"Duty Officer",
		"Init Authorised By",
		"Init Authorised Date",
		"Authorised By",
		"Authorised Date",
		"Reviewed By",
		"Reviewed Date",
		"Dispatch P&W",
		"Dispatch Aerial",
		"Fire Detected",
		"Fire Controlled",
		"Fire Contained",
		"Fire Safe",
		"Fuel Type",
		#"Initial Snapshot",
		"First Attack",
		"Other First Attack",
		"Initial Control",
		"Other Initial Control",
		"Final Control",
		"Other Final Control",
		"Arson Squad Notified",
		"Offence No",
		"Area",
		"Estimated Time to Control",
		"Authorised By",
		"Authorised Date",
		"Report Status",
    ]
	)
    for obj in queryset:
		writer.writerow([
			smart_str( obj.id),
			smart_str( obj.region.name),
			smart_str( obj.district.name),
			smart_str( obj.name),
			smart_str( obj.year),
			smart_str( obj.incident_no),
			smart_str( obj.dfes_incident_no),
			smart_str( obj.job_code),
			smart_str( obj.get_fire_level_display()),
			smart_str( obj.media_alert_req),
			smart_str( obj.investigation_req),
			smart_str( obj.fire_position),
			#row.write(col_no(), smart_str( obj.origin_point)),
			#row.write(col_no(), smart_str( obj.fire_boundary),
			smart_str( obj.fire_not_found),
			smart_str( obj.assistance_req),
			smart_str( obj.communications),
			smart_str( obj.other_info),
			smart_str( obj.cause),
			smart_str( obj.other_cause),
			smart_str( obj.field_officer.get_full_name() if obj.field_officer else None ),
			smart_str( obj.duty_officer.get_full_name() if obj.duty_officer else None ),
			smart_str( obj.init_authorised_by.get_full_name() if obj.init_authorised_by else None ),
			smart_str( obj.init_authorised_date.strftime('%Y-%m-%d %H:%M:%S') if obj.init_authorised_date else None),
			smart_str( obj.authorised_by.get_full_name() if obj.authorised_by else None ),
			smart_str( obj.authorised_date.strftime('%Y-%m-%d %H:%M:%S') if obj.authorised_date else None),
			smart_str( obj.reviewed_by.get_full_name() if obj.reviewed_by else None ),
			smart_str( obj.reviewed_date.strftime('%Y-%m-%d %H:%M:%S') if obj.reviewed_date else None),
			smart_str( obj.dispatch_pw_date.strftime('%Y-%m-%d %H:%M:%S') if obj.dispatch_pw_date else None),
			smart_str( obj.dispatch_aerial_date.strftime('%Y-%m-%d %H:%M:%S') if obj.dispatch_aerial_date else None),
			smart_str( obj.fire_detected_date.strftime('%Y-%m-%d %H:%M:%S') if obj.fire_detected_date else None),
			smart_str( obj.fire_controlled_date.strftime('%Y-%m-%d %H:%M:%S') if obj.fire_controlled_date else None),
			smart_str( obj.fire_contained_date.strftime('%Y-%m-%d %H:%M:%S') if obj.fire_contained_date else None),
			smart_str( obj.fire_safe_date.strftime('%Y-%m-%d %H:%M:%S') if obj.fire_safe_date else None),
			smart_str( obj.fuel_type),
			#row.write(col_no(), smart_str( obj.initial_snapshot),
			smart_str( obj.first_attack),
			smart_str( obj.other_first_attack),
			smart_str( obj.initial_control),
			smart_str( obj.other_initial_control),
			smart_str( obj.final_control),
			smart_str( obj.other_final_control),
			smart_str( obj.arson_squad_notified),
			smart_str( obj.offence_no),
			smart_str( obj.area),
			smart_str( obj.time_to_control),
			smart_str( obj.authorised_by.get_full_name() if obj.authorised_by else None ),
			smart_str( obj.authorised_date.strftime('%Y-%m-%d %H:%M:%S') if obj.authorised_date else None ),
			smart_str( obj.get_report_status_display()),
        ])
    return response
export_final_csv.short_description = u"Export CSV (Final)"


def export_excel(request, queryset):

    filename = 'export_final-' + datetime.now().strftime('%Y-%m-%dT%H%M%S') + '.xls'
    #response = HttpResponse(content_type='text/csv')
    response = HttpResponse(content_type='application/vnd.ms-excel; charset=utf-16')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    writer = unicodecsv.writer(response, quoting=unicodecsv.QUOTE_ALL)


    book = Workbook()
    sheet1 = book.add_sheet('Data')
    book.add_sheet('Sheet 2')

    col_no = lambda c=count(): next(c)
    row_no = lambda c=count(): next(c)
    sheet1 = book.get_sheet(0)
    hdr = sheet1.row(row_no())

    hdr.write(col_no(), "ID")
    hdr.write(col_no(), "Region")
    hdr.write(col_no(), "District")
    hdr.write(col_no(), "Name")
    hdr.write(col_no(), "Year")
    hdr.write(col_no(), "Incident Number")
    hdr.write(col_no(), "DFES Incident No")
    hdr.write(col_no(), "Job Code")
    hdr.write(col_no(), "Fire Level")
    hdr.write(col_no(), "Media Alert Req")
    hdr.write(col_no(), "Investigation Req")
    hdr.write(col_no(), "Fire Position")
    #"Origin Point",
    #"Fire Boundary",
    hdr.write(col_no(), "Fire Not Found")
    hdr.write(col_no(), "Assistance Req")
    hdr.write(col_no(), "Communications")
    hdr.write(col_no(), "Other Info")
    hdr.write(col_no(), "Cause")
    hdr.write(col_no(), "Other Cause")
    hdr.write(col_no(), "Field Officer")
    hdr.write(col_no(), "Duty Officer")
    hdr.write(col_no(), "Init Authorised By")
    hdr.write(col_no(), "Init Authorised Date")
    hdr.write(col_no(), "Authorised By")
    hdr.write(col_no(), "Authorised Date")
    hdr.write(col_no(), "Reviewed By")
    hdr.write(col_no(), "Reviewed Date")
    hdr.write(col_no(), "Dispatch P&W")
    hdr.write(col_no(), "Dispatch Aerial")
    hdr.write(col_no(), "Fire Detected")
    hdr.write(col_no(), "Fire Controlled")
    hdr.write(col_no(), "Fire Contained")
    hdr.write(col_no(), "Fire Safe")
    hdr.write(col_no(), "Fuel Type")
    #"Initial Snpshot",
    hdr.write(col_no(), "First Attack")
    hdr.write(col_no(), "Other First Attack")
    hdr.write(col_no(), "Initial Control")
    hdr.write(col_no(), "Other Initial Control")
    hdr.write(col_no(), "Final Control")
    hdr.write(col_no(), "Other Final Control")
    hdr.write(col_no(), "Arson Squad Notified")
    hdr.write(col_no(), "Offence No")
    hdr.write(col_no(), "Area")
    hdr.write(col_no(), "Estimated Time to Control")
    hdr.write(col_no(), "Authorised By")
    hdr.write(col_no(), "Authorised Date")
    hdr.write(col_no(), "Report Status")

    row_no = lambda c=count(1): next(c)
    for obj in queryset:
        row = sheet1.row(row_no())
        col_no = lambda c=count(): next(c)

        row.write(col_no(), obj.id )
        row.write(col_no(), smart_str( obj.region.name) )
        row.write(col_no(), smart_str( obj.district.name) )
        row.write(col_no(), smart_str( obj.name) )
        row.write(col_no(), smart_str( obj.year) )
        row.write(col_no(), obj.incident_no )
        row.write(col_no(), obj.dfes_incident_no )
        row.write(col_no(), obj.job_code )
        row.write(col_no(), smart_str( obj.get_fire_level_display() ))
        row.write(col_no(), smart_str( obj.media_alert_req) )
        row.write(col_no(), smart_str( obj.investigation_req) )
        row.write(col_no(), smart_str( obj.fire_position) )
        #row.write(col_no(), smart_str( obj.origin_point) )
        #row.write(col_no(), smart_str( obj.fire_boundary) )
        row.write(col_no(), smart_str( obj.fire_not_found) )
        row.write(col_no(), smart_str( obj.assistance_req) )
        row.write(col_no(), smart_str( obj.communications) )
        row.write(col_no(), smart_str( obj.other_info) )
        row.write(col_no(), smart_str( obj.cause) )
        row.write(col_no(), smart_str( obj.other_cause) )
        row.write(col_no(), smart_str( obj.field_officer.get_full_name() if obj.field_officer else None ) )
        row.write(col_no(), smart_str( obj.duty_officer.get_full_name() if obj.duty_officer else None ) )
        row.write(col_no(), smart_str( obj.init_authorised_by.get_full_name() if obj.init_authorised_by else None ) )
        row.write(col_no(), smart_str( obj.init_authorised_date.strftime('%Y-%m-%d %H:%M:%S') if obj.init_authorised_date else None) )
        row.write(col_no(), smart_str( obj.authorised_by.get_full_name() if obj.authorised_by else None ) )
        row.write(col_no(), smart_str( obj.authorised_date.strftime('%Y-%m-%d %H:%M:%S') if obj.authorised_date else None) )
        row.write(col_no(), smart_str( obj.reviewed_by.get_full_name() if obj.reviewed_by else None ) )
        row.write(col_no(), smart_str( obj.reviewed_date.strftime('%Y-%m-%d %H:%M:%S') if obj.reviewed_date else None) )
        row.write(col_no(), smart_str( obj.dispatch_pw_date.strftime('%Y-%m-%d %H:%M:%S') if obj.dispatch_pw_date else None) )
        row.write(col_no(), smart_str( obj.dispatch_aerial_date.strftime('%Y-%m-%d %H:%M:%S') if obj.dispatch_aerial_date else None) )
        row.write(col_no(), smart_str( obj.fire_detected_date.strftime('%Y-%m-%d %H:%M:%S') if obj.fire_detected_date else None) )
        row.write(col_no(), smart_str( obj.fire_controlled_date.strftime('%Y-%m-%d %H:%M:%S') if obj.fire_controlled_date else None) )
        row.write(col_no(), smart_str( obj.fire_contained_date.strftime('%Y-%m-%d %H:%M:%S') if obj.fire_contained_date else None) )
        row.write(col_no(), smart_str( obj.fire_safe_date.strftime('%Y-%m-%d %H:%M:%S') if obj.fire_safe_date else None) )
        row.write(col_no(), smart_str( obj.fuel_type) )
        #row.write(col_no(), smart_str( obj.initial_snapshot) )
        row.write(col_no(), smart_str( obj.first_attack) )
        row.write(col_no(), smart_str( obj.other_first_attack) )
        row.write(col_no(), smart_str( obj.initial_control) )
        row.write(col_no(), smart_str( obj.other_initial_control) )
        row.write(col_no(), smart_str( obj.final_control) )
        row.write(col_no(), smart_str( obj.other_final_control) )
        row.write(col_no(), smart_str( obj.arson_squad_notified) )
        row.write(col_no(), obj.offence_no )
        row.write(col_no(), obj.area )
        row.write(col_no(), smart_str( obj.time_to_control) )
        row.write(col_no(), smart_str( obj.authorised_by.get_full_name() if obj.authorised_by else None ) )
        row.write(col_no(), smart_str( obj.authorised_date.strftime('%Y-%m-%d %H:%M:%S') if obj.authorised_date else None ) )
        row.write(col_no(), smart_str( obj.get_report_status_display()) )

    book.save(response)

    return response
export_final_csv.short_description = u"Export Excel"


#def activity_names():
#	return [i['name'] for i in ActivityType.objects.all().order_by('id').values()]
#
#def activity_map(obj):
#	bools = []
#	for activity_name in activity_names():
#		if len(obj.activities.all().filter(activity__name__contains=activity_name)) > 0:
#			dt = obj.activities.get(activity__name__contains=activity_name).date.strftime('%Y-%m-%d %H:%M:%S')
#			bools.append([activity_name, row.write(col_no(), smart_str( dt)])
#		else:
#			bools.append([activity_name, row.write(col_no(), smart_str( None)])
#	return bools

