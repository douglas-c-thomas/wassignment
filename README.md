# WAssignment
Assignment, with a W in the front yard

Once you clone the repository locally, these steps should get you up and running:

### Supply your Google Application Credentials
In the Codebase, replace the contents of the [google-application-credential.json](https://github.com/douglas-c-thomas/wassignment/blob/master/src/google-application-credentials.json) with your credentials.  I can provide mine offline if need be.

### Start the server
Console 1:
```
~/Projects/Workiva/wassignment > docker-compose up --build
```

Console 2:
```
~/Projects/Workiva/wassignment > docker-compose exec app bash
root@76364d5cbc52:/code# python manage.py test
```

I believe the database should be set up correctly in the docker build, but if it gives you guff, you might try this:
```
root@76364d5cbc52:/code# python manage.py makemigrations
root@76364d5cbc52:/code# python manage.py migrate
root@76364d5cbc52:/code# python manage.py test
```

I tried to get some basic coverage with my [tests](https://github.com/douglas-c-thomas/wassignment/tree/master/src/tests) (model, unit, integration) but didn't go crazy.

### Points of interest
- The API URLs are captured [here](https://github.com/douglas-c-thomas/wassignment/blob/master/src/bls_dataset/urls.py).
- The API requests are handled in the [views](https://github.com/douglas-c-thomas/wassignment/blob/master/src/bls_dataset/views.py).
- The data [serializer](https://github.com/douglas-c-thomas/wassignment/blob/master/src/bls_dataset/serializers.py#L20) for the Query POST delegates to a data handler to process the Big Query request.  In this case, a [UnemploymentCPSDatasetHandler](https://github.com/douglas-c-thomas/wassignment/blob/master/src/dataset_handlers/unemployment_cps_dataset_handler.py#L9) is created via a psuedo-factory method and processes the requests against the [bls.unemployment_cps](https://bigquery.cloud.google.com/results/data-studio-175515:US.bquijob_1da9ab00_16a97c44bd2?pli=1) dataset.
- I do give a nod to security by [requiring a Bearer token in the header](https://github.com/douglas-c-thomas/wassignment/blob/master/src/bls_dataset/permissions.py#L4).  IRL, the API_KEY would be kept in a Kubernetes secrets file, or the architecture would support Apps with a Client ID / Client Secret pair for proper OAuth.
- To show some level of request validation, I specified that [limiting query results to 666](https://github.com/douglas-c-thomas/wassignment/blob/master/src/bls_dataset/serializers.py#L34) was not permissible.  This, of course, could be used to guard against throttling, but since I expect that large limits will be used to test resiliancy, I didn't set an upper boundary.

### The APIs themselves
I tested these thoroughly myself in Postman as well, but the following endpoints are supported

#### Query POST
- http://0.0.0.0:8000/bls-dataset/queries
- The endpoint takes in query parameters, uses them to lob a request against Big Query, parses the results and persists them locally.

#### Query INDEX
- http://0.0.0.0:8000/bls-dataset/queries
- The endpoint returns all queries executed and persisted thus far, as well as their associative result sets.

#### Query GET (uuid)
- http://0.0.0.0:8000/bls-dataset/queries/<uuid>
- The endpoint returns a specific previoiusly executed query and its result set.
  
#### Query GET (name)
- http://0.0.0.0:8000/bls-dataset/queries?name=<name>
- The endpoint returns a set of previoiusly executed queries that match by name, along with their associative result sets.
  
The API endpoints and filtering possibilities are endless, but this should cover the basics.

### Data Payloads
#### Header
```
{
    'Accept': 'application/json',
    'Content-Type': 'application/json',
    'Authorization': 'Bearer MAGIC_KEY'
}
```
#### Sample Request Body
```
{
    "dataset": "unemployment_cps",
    "name": "CPS-Limit Test 1",
    "query": {
        "year": 1984
    },
    "limit": 42
}
```
