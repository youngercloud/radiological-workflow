import json
from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django import views
from fhirclient import server as fserv
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.identifier import Identifier
from fhirclient.models.device import Device, DeviceDeviceName, DeviceVersion
from fhirclient.models.devicerequest import DeviceRequest
from fhirclient.models.patient import Patient
from fhirclient.models.practitioner import Practitioner
from fhirclient.models.humanname import HumanName
from fhirclient.models.appointment import Appointment, AppointmentParticipant
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.servicerequest import ServiceRequest
from fhirclient.models.annotation import Annotation

# Create your views here.

tt = fserv.FHIRServer(client=None, base_uri="http://localhost:8080/fhir")
tt.prepare()

## Create All demo devices
device = Device()
dn = DeviceDeviceName()
dn.name = "Siemens X.pree X-Ray"
dn.type = "user-friendly-name"
device.deviceName = [dn]
device.url = "https://example.com"
dv = DeviceVersion()
dv.value = '1'
device.version = [dv]
device_json = device.create(tt)


def index(request):
    return render(request, 'index.html')


def order(request):
    return render(request, 'orders.html')


def get_orders():
    res = []
    search = Appointment.where({'status': 'waitlist'})
    procedures = search.perform_resources(tt)
    for procedure in procedures:
        data = procedure.as_json()
        p_name = Patient.read(data['participant'][0]['actor']['reference'].split('/')[1], tt)
        pat_fn = p_name.as_json()['name'][0]['family']
        pat_gn = p_name.as_json()['name'][0]['given'][0]

        pr_name = Practitioner.read(data['participant'][1]['actor']['reference'].split('/')[1], tt)
        par_fn = pr_name.as_json()['name'][0]['family']
        par_gn = pr_name.as_json()['name'][0]['given'][0]

        wk_flow = ServiceRequest.read(data['basedOn'][0]['reference'].split('/')[1], tt)
        wk_flow_name = wk_flow.as_json()['note'][0]['text']

        res.append({
            'id': data['id'],
            'status': data["status"],
            'pName': pat_gn + " " + pat_fn,
            'wName': wk_flow_name,
            'wVersion': data['meta']['versionId'],
            'wprName': par_gn + " " + par_fn
        })
    return res


def booking(request):
    data = get_orders()
    return render(request, 'booking.html', {'rows': data})


def checkin(request):
    return render(request, 'checkIn.html')


def report(request):
    return render(request, 'report.html')


class OrderView(views.View):

    def create_pat(self, pat_name):
        ident = Identifier()
        pat = Patient()
        ident.use = "official"
        ident.system = "http://ns.health.qld.gov.au/id/URN"
        pat.identifier = [ident]
        hn = HumanName()
        hn.family = pat_name[0]
        hn.given = [pat_name[1]]
        pat.name = [hn]
        return pat

    def create_par(self, par_name):
        ident = Identifier()
        par = Practitioner()
        ident.use = "official"
        ident.system = "http://ns.health.qld.gov.au/id/URN"
        par.identifier = [ident]
        hn = HumanName()
        hn.family = par_name[0]
        hn.given = [par_name[1]]
        par.name = [hn]
        par.create(tt)
        return par

    def appointment(self, doctor, patient, comment, description):
        a = Appointment()
        ap = AppointmentParticipant()
        ap.actor = [doctor, patient]
        a.comment = comment
        a.description = description
        a.participant = ap

    def post(self, request):
        if request.is_ajax():
            if request.method == 'POST':
                data = json.loads(request.body)
                pat_name = data["pat_name"].strip().split(" ")
                par_name = data["par_name"].strip().split(" ")
                pat = self.create_pat(pat_name)
                par = self.create_par(par_name)
                pat_json = pat.create(tt)
                par_json = par.create(tt)
                self.create_appointment(pat_json, par_json, data["wk_name"].strip(),
                                        data["comment"].strip(), data["encounter"].strip())
                return JsonResponse({'msg': 'success'})

        return JsonResponse({'msg': 'failed'})

    def create_appointment(self, patient, practitioner, service, comment, desc):
        a = Appointment()
        ap = AppointmentParticipant()
        pr = AppointmentParticipant()
        ap.actor = FHIRReference()
        ap.actor.reference = "Patient/" + patient["id"]
        ap.status = "accepted"
        pr.actor = FHIRReference()
        pr.actor.reference = "Practitioner/" + practitioner["id"]
        pr.status = "accepted"
        a.comment = comment
        a.description = desc

        sr = ServiceRequest()
        sr.intent = "proposal"
        sr.note = [Annotation()]
        sr.note[0].text = service
        sr.status = "active"
        srfr = FHIRReference()
        srfr.reference = "Patient/" + patient["id"]
        sr.subject = srfr
        sr_json = sr.create(tt)

        fdr = FHIRReference()
        fdr.reference = "ServiceRequest/" + sr_json["id"]

        a.participant = [ap, pr]
        a.basedOn = [fdr]
        a.status = "waitlist"
        a.create(tt)


class BookingView(views.View):

    def post(self, request):
        if request.is_ajax():
            if request.method == 'POST':
                data = json.loads(request.body)
                search = Appointment.where({'status': 'waitlist'})
                procedures = search.perform_resources(tt)
                for procedure in procedures:
                    p_json = procedure.as_json()
                    if data['patId'] == p_json['id']:
                        procedure.status = 'booked'
                        date = data['startDate'].split('-')
                        time = data['startTime'].split(':')
                        t = datetime(int(date[0]), int(date[1]), int(date[2]), int(time[0]), int(time[1]))
                        procedure.start = FHIRDate()
                        procedure.start.date = t
                        if procedure.comment is None:
                            procedure.comment = f" Booked scan at {str(t)}, use scanner {data['machine']}"
                        else:
                            procedure.comment += f"Booked scan at {str(t)}, use scanner {data['machine']}"
                        procedure.update(tt)
                        return JsonResponse({'msg': 'success'})
        return JsonResponse({'msg': 'failed'})
