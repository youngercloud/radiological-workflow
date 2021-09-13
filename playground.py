"""
IN CASE FHIRCLIENT3.2.0 DOES NOT WORKING
PLEASE INSTALL VERSION FHIRCLIENT4.0.0
pip install -e git+https://github.com/smart-on-fhir/client-py#egg=fhirclient

Run Server: docker run -p 8080:8080 --network="host" -e \
 hapi.fhir.subscription.resthook_enabled=true -e \
  hapi.fhir.cors.allowed_origin=* -e hapi.fhir.cors.allow_credentials=false hapiproject/hapi:latest

For Linux user, you may add sudo before the docker command.

"""
#

import sys
import base64


from fhirclient import server as  fserv
from fhirclient.models.attachment import Attachment
from fhirclient.models.encounter import Encounter
from fhirclient.models.observation import Observation

from fhirclient.models.patient import Patient
from fhirclient.models.practitioner import Practitioner
from fhirclient.models.humanname import HumanName
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.address import Address
from fhirclient.models.identifier import Identifier
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.location import Location
from fhirclient.models.diagnosticreport import DiagnosticReport
from fhirclient.models.appointment import Appointment, AppointmentParticipant
from fhirclient.models.device import Device, DeviceDeviceName
from fhirclient.models.devicerequest import DeviceRequest

def create_par(par_name):
    ident = Identifier()
    par = Practitioner()
    ident.use = "official"
    ident.system = "http://ns.health.qld.gov.au/id/URN"
    par.identifier = [ident]
    hn = HumanName()
    hn.family = par_name[0]
    hn.given = [par_name[1]]
    par.name = [hn]
    return par

if __name__ == "__main__":
    a = Appointment()
    ap = AppointmentParticipant()

    a.participant = ap
    # tt = fserv.FHIRServer(client=None, base_uri="http://localhost:8080/fhir")
    # tt.prepare()
    #
    pat = Patient()
    hn = HumanName()

    ident = Identifier()
    ident.use = "official"
    ident.system = "http://ns.health.qld.gov.au/id/URN"
    ident.value = "LC12123733"
    pat.identifier = [ident]
    hn.family = "Sanchez"
    hn.given = ["Rick"]
    pat.name = [hn]
    pat.gender = "male"
    pat.birthDate = FHIRDate('1948-07-03')
    temp = Address()

    temp.use = "home"
    temp.type = "both"
    temp.text = "42 Botticelli St, Fig Tree Pocket, QLD, 4069"
    temp.city = "Fig Tree Pocket"
    temp.state = "QLD"
    temp.postalCode = "4069"
    temp.country = "Australia"
    pat.address = [temp]

    ap.actor = [pat, create_par("Ha Ha")]
    a.comment = ""
    a.description = ""

    device = Device()
    dn = DeviceDeviceName()
    dn.name = "Siemens X.pree X-Ray"
    device.deviceName = dn
    device.url = "https://example.com"
    device.version = '1'


    d = DeviceRequest()
    d.basedOn = "Chest-X-Ray"
    d.codeReference = device
    a.basedOn = d
    print(a)



