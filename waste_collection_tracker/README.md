# Lagos Waste Collection API Documentation

Residents in Lagos face inconsistent waste collection and poor complaint resolution. This project aims to solve that by creating a digital portal that bridges the gap between citizens and the waste services.  

**Steps:**  

1. **Identify the Problem:**  
   Residents struggle with missed pickups and have no easy way to report issues.  

2. **Solution Idea:**  
   Develop a platform where residents can:  
   - Schedule pickups at their convenience  
   - Submit complaints seamlessly  
   - Track service completion [in real-time]  

3. **Building the System:**  
   - **Residents** sign up, request services, and receive updates.  
   - **Waste Management Teams** receive organized requests, improving efficiency.  
   - **Admins** monitor activities and respond to complaints promptly.  

4. **Impact:**  
   The portal boosts responsiveness, reduces littering, and promotes cleaner neighborhoods in Lagos.  

**Steps to Build the Lagos Waste Collection Portal:**

1. **Define Features:**
   - Schedule waste pickups  
   - Submit complaints  
   - Track service completion
   - Only role admin can update the status  

2. **Choose Tech Stack:**  
   - **Backend:**Python (FastAPI)  
   - **Database:** PostgreSQL
   - **Authentication:** JWT for user login  

3. **Plan Database Models:**  
   - **User:** id, name, email, password, location, role, created_at, updated_at  
   - **PickupRequest:** id, user_id, scheduled_date, status, location, created_at, updated_at  
   - **Complaint:** id, user_id, description, status,admin_response, created_at, updated_at

4. **Set Up Backend:**  
   - Create routes: `/schedule-pickup`, `/submit-complaint`, `/track-status`  
   - Implement CRUD operations  
   - Add authentication & authorization  

5. **Deploy:**  
   - Use platforms like Render, Railway, or Heroku for quick deployment  

6. **Bonus:**  
   - Add admin dashboard for service management  
   - Implement geolocation for route optimization  

**Database Model for the Lagos Waste Collection Portal:**  

1. **Users Table**  
   - `id` (PK): UUID  
   - `name`: VARCHAR  
   - `email`: VARCHAR (unique)  
   - `password_hash`: TEXT  
   - `location`: TEXT  
   - `role`: ENUM ('resident', 'admin')  
   - `created_at`: TIMESTAMP  
   - `updated_at`: TIMESTAMP  

2. **PickupRequests Table**  
   - `id` (PK): UUID  
   - `user_id` (FK): UUID → Users(id)  
   - `scheduled_date`: DATE  
   - `status`: ENUM ('pending', 'in_progress', 'completed', 'cancelled')  
   - `location`: str
   - `created_at`: TIMESTAMP  
   - `updated_at`: TIMESTAMP  

3. **Complaints Table**  
   - `id` (PK): UUID  
   - `user_id` (FK): UUID → Users(id)  
   - `description`: TEXT  
   - `status`: ENUM ('pending', 'reviewed', 'resolved')  
   - `response`: TEXT (optional admin response)  
   - `created_at`: TIMESTAMP  
   - `updated_at`: TIMESTAMP  

 **Plan to build the authentication aspect:**  

1. **User model** with secure password storage.  
2. **Signup & Login** routes.  
3. **JWT token generation** for sessions.  
4. **Dependency** to protect routes.  
