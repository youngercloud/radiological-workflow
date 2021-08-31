"""
IN CASE FHIRCLIENT3.2.0 DOES NOT WORKING
PLEASE INSTALL VERSION FHIRCLIENT4.0.0
pip install -e git+https://github.com/smart-on-fhir/client-py#egg=fhirclient

Run Server: docker run -p 8080:8080 --network="host" -e
 hapi.fhir.subscription.resthook_enabled=true -e
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
from fhirclient.models.humanname import HumanName
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.address import Address
from fhirclient.models.identifier import Identifier
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.location import Location


if __name__ == "__main__":

    tt = fserv.FHIRServer(client=None, base_uri="http://localhost:8080/fhir")
    tt.prepare()

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

    # img = base64.b64encode(open(sys.argv[1], 'rb').read())
    # pat.photo = []
    # temp = Attachment()
    # temp.contentType = "image/jpeg"
    # temp.data = img.decode('utf-8')
    # pat.photo.append(temp)
    # pat.update()

    pat.address = [temp]
    print(pat.create(tt))