# radiological-workflow
Radiological Workflow Information System using FHIR API

# Setup & Run
1. Start HAPI FHIR Server

Note

In case FHIRCLIENT3.2.0 does not work.
PLEASE INSTALL VERSION FHIRCLIENT4.0.0

```
pip install -e git+https://github.com/smart-on-fhir/client-py#egg=fhirclient
```

Run Server 

```shell
docker run -p 8080:8080 --network="host" -e \
 hapi.fhir.subscription.resthook_enabled=true -e \
  hapi.fhir.cors.allowed_origin=* -e hapi.fhir.cors.allow_credentials=false hapiproject/hapi:latest
```

For Linux user, you may add sudo before the docker command.


2. Run Application

```
python3 manage.py runserver
```

