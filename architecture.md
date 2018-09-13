# Architecture Overview

The solution is essentially a Micro service in the form of a RESTFul API. The code is 
divided in 3 main layers:

- Data Access Layer
- Business Logic Layer
- Presentation Layer (Controllers/Resources)

As part of Data Access Layer we have a DB factory, its main purpose is to decouple the 
solution from any DB Engine and make it extensible. This DB factory will be in charge of 
instantiating a DB connection depending on the application configuration. 

The Business logic layer main purpose is to apply all the rules and validations related 
to the business. In this case applying the taxes and generating the receipt when checking out the order.
This will allow us to incorporate new business rules without having to change the Data Access Layer 
or the Presentation layer

The Presentation Layer is how we let clients consume our app, in this case is in the form of 
a RESTful API exposing endpoints to the provided resources. By exposing the solution through a 
RESTful API we enable other clients to use our system through it and apply other rules that might apply for them.
i.e: A client UI that consumes the API and applies some rules to display information in an interactive way to 
the users.

This micro-service approach allows us to containerize the API and use a container orchestrator like Kubernetes 
to quickly deploy and scale the application as the user base grows.
