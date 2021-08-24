import datetime
from fhirclient.models import patient as p, address as a, period as pe, fhirdate as fd, humanname as hn


a = a.Address()
a.city = "Brisbane"
a.country = "Australia"
a.line = ["1 Mystery Rd"]
period = pe.Period()
period.start = fd.FHIRDate()
period.start.date = datetime.datetime(2020, 5, 10)
period.end = fd.FHIRDate()
period.end.date = datetime.datetime(2020, 5, 19)
a.period = period

name = hn.HumanName()
name.given = ['Peter']
name.family = 'Parker'


patient = p.Patient()
patient.address = [a]
patient.name = [name]
print(patient.as_json())


