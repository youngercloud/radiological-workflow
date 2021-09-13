import json

from django.http import HttpResponse
from django.shortcuts import render
from django import views
from fhirclient import server as  fserv
from fhirclient.models.identifier import Identifier
from fhirclient.models.device import Device, DeviceDeviceName
from fhirclient.models.devicerequest import DeviceRequest
from fhirclient.models.patient import Patient
from fhirclient.models.practitioner import Practitioner
from fhirclient.models.humanname import HumanName
from fhirclient.models.appointment import Appointment, AppointmentParticipant
# Create your views here.

tt = fserv.FHIRServer(client=None, base_uri="http://localhost:8080/fhir")
tt.prepare()

## Create All demo devices
device = Device()
dn = DeviceDeviceName()
dn.name = "Siemens X.pree X-Ray"
device.deviceName = dn
device.url = "https://example.com"
device.version = '1'


d = DeviceRequest()
d.basedOn = "Chest-X-Ray"
d.codeReference = device
# a.basedOn = d
# print(a)

def index(request):
    return render(request, 'index.html')


def order(request):
    return render(request, 'orders.html')


def booking(request):
    return render(request, 'booking.html')


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
                print(request.body)
                pat_name = request.body["pat_name"].split(" ")
                par_name = request.body["par_name"].split(" ")
                pat = self.create_pat(pat_name)
                par = self.create_par(par_name)
                pat.create(tt)
                par.create(tt)
                self.create_appoientment()
        return HttpResponse("Success")