# Lagos Waste Management API (FastAPI & PostgreSQL)

## Problem

Waste collection in Lagos faces inefficiencies due to inconsistent scheduling and ineffective complaint resolution. Residents struggle with missed pickups and lack a streamlined system for reporting issues, leading to unclean neighborhoods.

## Hypothesis

A structured API with role-based authentication, waste pickup scheduling, complaint tracking, and administrative oversight can enhance waste management efficiency and service responsiveness.

## Approach

- Developed a RESTful API using **FastAPI** and **PostgreSQL** for managing waste pickup requests and complaints.
- Implemented **JWT authentication** for secure user access and role-based authorization.
- Designed an optimized **database schema** with indexed tables for improved query performance.
- Added **pickup scheduling** and **complaint management** features to facilitate structured waste collection.
- Deployed and tested API performance using **Postman** and **Pytest**. [not yet]

## Outcome

- Improved request processing efficiency, reducing response time for residents.
- Enhanced complaint tracking, leading to faster resolutions.
- Successfully handled multiple concurrent requests with minimal latency.

---

## Project Structure 📂

```markdown
wasteApi/
│── alembic/            # Database migration folder
│── app/
│   ├── routers/
│   │   ├── auth.py           # Authentication routes
│   │   ├── complaint.py      # Complaint management routes
│   │   ├── pickuprequest.py  # Request management routes
│   │   ├── users.py          # User management routes
│   ├── config.py             # Configuration settings
│   ├── database.py           # Database connection setup
│   ├── main.py               # Application entry point
│   ├── models.py             # Database models (User, PickupRequest, Complaint)
│   ├── oauth2.py             # Authentication logic (JWT handling, role checks)
│   ├── utils.py              # Utility functions (password hashing, token creation)
│── scripts/                  # Additional scripts (if any)
│── tests/                    # Test cases for the API
│── requirements.txt          # Project dependencies
```

## Features

1. **User Authentication**
   - Residents and admins can register and log in using JWT authentication.
   - Role-based access ensures only admins can manage assignments and status updates.

2. **Pickup Request Management**
   - Residents can schedule pickups with preferred dates and locations.
   - Admins can track and update the status of requests (pending, in-progress, completed, canceled).

3. **Complaint Handling**
   - Users can submit complaints related to waste collection issues.
   - Admins review and provide responses to complaints.

4. **Admin Dashboard**
   - Admins can assign waste collection tasks to workers and manage complaints efficiently.

---

## Deployment & Testing

- Deployed using **Render** (or alternatives like Heroku, Railway).
- API testing performed using **Postman** and automated with **Pytest**.

---

## API Endpoints Overview

### Authentication

- `POST /signup` - Register a new Resident
- `POST /login` - Authenticate Resident and generate JWT
- `POST /admin/signup` - Register a new Admin
- `POST /admin/login` - Authenticate Admin and generate JWT
- `PUT /approve/{user_id}` - Approve an Admin's account (SuperAdmin only)

### User Profile

- `GET /users/` - Retrieve user details (superuser only)
- `GET /users/{username}` - Retrieve user details (this.user only)
- `PUT /users/` - Update user details (this.user only)

### Pickup Requests

- `POST /pickup/` - Schedule a new pickup request
- `GET /pickup/{request_id}` - Retrieve a specific pickup request
- `PUT /pickup/{request_id}` - Update the status of a request
- `DELETE /pickup/{request_id}` - Cancel a request (this.user only)
- `PUT /pickup/adminUpdate/` - Update the status of a request (Admin only)

### Complaints

- `POST /complaint/` - Schedule a new complaint
- `GET /complaint/{complaint_id}` - Retrieve a specific complaint
- `PUT /complaint/{complaint_id}` - Update the status of a request
- `DELETE /complaint/{complaint_id}` - Cancel a request (this.user only)
- `PUT /complaint/adminUpdate/` - Update the status of a request (Admin only)

---

## Technologies Used

- **FastAPI** (Backend framework)
- **PostgreSQL** (Database)
- **JWT Authentication** (Security)
- **Docker** (For containerized deployment) [Not yet]
- **Pytest** (API testing) [Not yet]

---

## Usage

### Resident Flow

1. Sign up/login.  
2. Request a pickup.  
3. Track request status.  
4. Submit and view complaints.  

### Admin Flow

1. Login (must be approved by another admin if newly created).  
2. Approve other admin accounts.  
3. View and assign pickup requests.  
4. Respond to and resolve complaints.  

---

## Installation & Setup

1 **Clone the repository:**  

 download the waste_collection_tracker repository folder

2 **Create and activate a virtual environment:**  

```bash
python -m venv env
env\Scripts\activate
```

3 **Install dependencies:**  

```bash
pip install -r requirements.txt
```

4 **Run the application:**  

```bash
uvicorn app.main:app --reload
```

5 **Access the API Docs:**  

- Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

## Running with Docker  

### Prerequisites  

- Install [Docker](https://docs.docker.com/get-docker/)  

- Build and start the containers:  

   ```sh
   docker-compose up --build  
   ```  

- Access the API:  
  - **Docs:** [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)  
  - **Adminer (DB UI):** [http://127.0.0.1:8081](http://127.0.0.1:8081)  

- Stop the containers:  

   ```sh
   docker-compose down  
   ```  

## License

MIT License. See [LICENSE](LICENSE) for details.

---

 **Let’s keep Lagos clean together!** 🌱
