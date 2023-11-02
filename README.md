# 
# Hotel Management RestAPI

The Hotel Management REST API is a comprehensive system designed to manage hotel operations efficiently. It offers a range of endpoints with CRUD operations to manage hotel rooms, reservations, customer information, and billing processes.
## Features

- Secure User Authentication: Utilizes email verification and token authentication for user login and logout, ensuring secure access to the system.

- Unit Testing: Comprehensive unit tests have been implemented to ensure reliability and functionality across individual components.

- Dockerized Application: The project has been Dockerized for efficient component isolation and portability.

- Optimized Database Schemas: Designed optimized database schemas for smooth and efficient data management.

- Celery Integration with Redis: Integrated Celery with Redis as the message broker, facilitating communication between Django components and background workers.


## Tech Stack

**Backend:** Python, Django, Rest Framework

**Database:** PostgreSQL

**Other Tools:** Docker, Redis ,Celery


## Installation

Prerequisites

    Python latest version
    Docker 

Clone the repository:
```bash 
git clone git@github.com:asefdevs/HotelManagement.git

```


    
## Usage

Run Docker Compose:

```bash

sudo docker-compose up --build

```


You can access with link:

http://localhost:8000/


## 🔗 Endpoints and Features

## User Account Operations

| Endpoint                                     | HTTP Method | Description                                |
|---------------------------------------------- |-------------|--------------------------------------------|
| /api/account/register/                        | POST        | User registration                          |
| /api/account/verify_email/                   | GET         | Verify user's email                        |
| /api/account/login/                          | POST        | User login                                 |
| /api/account/logout/                         | POST        | User logout                                |
| /api/account/profile/<int:id>/               | GET         | Retrieve user's profile details            |
| /api/account/profile/photo_update/            | POST        | Update user's profile photo                |


## Hotel and Reservation Operations

| Endpoint                                     | HTTP Method | Description                                |
|---------------------------------------------- |-------------|--------------------------------------------|
| /api/hotel/hotels/                           | POST        | Create a new hotel                         |
| /api/hotel/hotels/<int:pk>/                  | GET         | Retrieve details of a specific hotel       |
| /api/hotel/rooms/                            | POST,GET        | Create a new room within a hotel           |
| /api/hotel/rooms/<int:pk>/                   | GET         | Retrieve details of a specific room       |
| /api/hotel/guests/                           | GET         | List all guests                            |
| /api/hotel/reservations/                     | POST        | Create a new reservation                   |
| /api/hotel/reservations/<int:pk>/            | GET         | Retrieve details of a specific reservation|
| /api/hotel/recent_reservations/               | GET         | Retrieve recent reservations               |
| /api/hotel/available_rooms/                  | GET         | Filter and retrieve available rooms        |

## License

[MIT](https://choosealicense.com/licenses/mit/)

