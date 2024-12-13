# Airport service Project
<hr>

DRF project for airport service

## Installation

Python 3 must be already installed

```commandline
git clone https://github.com/MaksymProtsak/airport-service.git
cd airport-service
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py runserver  # starts Django Server
```

## Run with docker
<hr>

```commandline
docker-compose build
docker-compose up
```

## Getting access
<hl>

* created user via /api/user/register/
* get access token via /api/user/token/
* refresh access token via /api/user/token/refresh/

## Features

* Authentication functionality for Customer/Admin
* Managing airports, routes, tickets, orders, flights, airplane types, airplanes, crews and flights directly from website interface
* Powerful admin panel form advanced managing
* Documentation is located at api/doc/swagger/

## Demo
Login user succeed 
![Login user succeed](demo_images/login_user_successed.png)

User info page
![User info page](demo_images/api_user_me.png)

Token refresh page
![Token refresh page](demo_images/token_refresh_page.png)

Airport app routes
![Airport app routes](demo_images/airport_app_routes.png)

Crew list
![Crew list](demo_images/crew_list.png)

Airplane type list
![Airplane type list](demo_images/airplane_type_list.png)

Airplane type list
![Airplane type list](demo_images/airplane_type_list.png)

Order list
![Order list](demo_images/order_list.png)

Airplane list
![Airplane list](demo_images/airplane_list.png)

Airport list
![Airport list](demo_images/airport_list.png)

Route list
![Route list](demo_images/route_list.png)

Flight list
![Flight list](demo_images/flight_list.png)