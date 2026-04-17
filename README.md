# � ForgeAdmin – Full-Stack Ready Admin Dashboard

## 📌 Overview

**ForgeAdmin** is a production-ready **Admin Dashboard System** designed for modern e-commerce platforms.
Originally built for the **BackForge Hackathon**, it provides a **complete frontend UI + structured backend API design**, enabling rapid full-stack development.

This project is not just UI — it is a **backend-integrated architecture blueprint** for scalable admin systems.

---

## 🎯 Vision

ForgeAdmin is designed to:

* Accelerate full-stack development
* Provide a clean separation of frontend and backend
* Simulate real-world enterprise admin workflows
* Enable rapid prototyping during hackathons

---

## 🧠 System Architecture

ForgeAdmin follows a **decoupled architecture**:

```
Frontend (HTML/CSS/JS)
    ↓
REST API (FastAPI)
    ↓
MongoDB (Database)
```

### 🔹 Key Principles

* Modular design
* API-first architecture
* Scalable backend structure
* Clean separation of concerns

---

## 🧰 Tech Stack

### Frontend

* HTML5
* Tailwind CSS
* Vanilla JavaScript
* Font Awesome

### Backend

* FastAPI (Python)
* JWT Authentication (Access + Refresh)
* Middleware (Auth, Logging, Error Handling)

### Database

* MongoDB (Dockerized)

---

## 🔐 Authentication System

Secure authentication using JWT:

| Endpoint                  | Description          |
| ------------------------- | -------------------- |
| POST `/api/auth/register` | Register user        |
| POST `/api/auth/login`    | Login user           |
| POST `/api/auth/refresh`  | Refresh access token |
| POST `/api/auth/logout`   | Logout user          |
| GET `/api/auth/me`        | Get current user     |

---

## 📊 Dashboard APIs

| Endpoint                               | Description          |
| -------------------------------------- | -------------------- |
| GET `/api/dashboard/stats`             | Dashboard statistics |
| GET `/api/dashboard/sales-by-category` | Sales insights       |

---

## 📈 Analytics APIs

| Endpoint                      | Description      |
| ----------------------------- | ---------------- |
| GET `/api/analytics/overview` | Overview metrics |
| GET `/api/analytics/traffic`  | Traffic analysis |
| GET `/api/analytics/devices`  | Device usage     |

---

## 📦 Products APIs

| Method | Endpoint                     |
| ------ | ---------------------------- |
| GET    | `/api/products`              |
| POST   | `/api/products`              |
| GET    | `/api/products/{product_id}` |
| PUT    | `/api/products/{product_id}` |
| DELETE | `/api/products/{product_id}` |

---

## 🗂️ Categories APIs

| Method | Endpoint                   |
| ------ | -------------------------- |
| GET    | `/api/categories`          |
| POST   | `/api/categories`          |
| PUT    | `/api/categories/{cat_id}` |
| DELETE | `/api/categories/{cat_id}` |

---

## 🧾 Orders APIs

| Method | Endpoint                        |
| ------ | ------------------------------- |
| GET    | `/api/orders/summary`           |
| GET    | `/api/orders`                   |
| POST   | `/api/orders`                   |
| GET    | `/api/orders/{order_id}`        |
| PUT    | `/api/orders/{order_id}/status` |

---

## 👥 Customers APIs

| Method | Endpoint                       |
| ------ | ------------------------------ |
| GET    | `/api/customers`               |
| POST   | `/api/customers`               |
| GET    | `/api/customers/{customer_id}` |
| PUT    | `/api/customers/{customer_id}` |
| DELETE | `/api/customers/{customer_id}` |

---

## ⭐ Reviews APIs

| Method | Endpoint                   |
| ------ | -------------------------- |
| GET    | `/api/reviews`             |
| POST   | `/api/reviews`             |
| PUT    | `/api/reviews/{review_id}` |
| DELETE | `/api/reviews/{review_id}` |

---

## 🎯 Promotions APIs

| Method | Endpoint                     |
| ------ | ---------------------------- |
| GET    | `/api/promotions`            |
| POST   | `/api/promotions`            |
| PUT    | `/api/promotions/{promo_id}` |
| DELETE | `/api/promotions/{promo_id}` |

---

## 👨‍💼 Staff APIs

| Method | Endpoint                |
| ------ | ----------------------- |
| GET    | `/api/staff`            |
| POST   | `/api/staff`            |
| PUT    | `/api/staff/{staff_id}` |
| DELETE | `/api/staff/{staff_id}` |

---

## ⚙️ Settings APIs

| Method | Endpoint        |
| ------ | --------------- |
| GET    | `/api/settings` |
| PUT    | `/api/settings` |

---

## ❤️ Health Check

| Endpoint | Description      |
| -------- | ---------------- |
| GET `/`  | API Health Check |

---

## 📁 Project Structure

```
/
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── components/
│   └── pages/
│
├── backend/
│   ├── routes/
│   ├── controllers/
│   ├── services/
│   ├── models/
│   ├── schemas/
│   ├── middleware/
│   ├── config/
│   └── main.py
│
├── docker-compose.yml
```

---

## ▶️ Getting Started

### 1. Start MongoDB

```bash
docker compose up -d
```

---

### 2. Start Backend

```bash
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

---

### 3. Start Frontend

```bash
cd frontend
python3 -m http.server 5500
```

---

### 🌐 Access

* Frontend → http://localhost:5500
* Backend → http://localhost:8000/docs
* MongoDB UI → http://localhost:8081

---

## � Security Design

* JWT-based authentication
* Refresh token via HTTP-only cookies
* Role-based system ready
* Middleware-based request validation

---

## ⚠️ Current Limitations

* Frontend still partially static
* No real-time updates
* No WebSocket integration
* Basic role management

---

## 🔮 Future Enhancements

* RBAC (Admin / Staff roles)
* Real-time dashboards (WebSockets)
* Payment gateway integration
* AI-based analytics
* Microservices architecture

---

## 🏆 Hackathon Value

ForgeAdmin demonstrates:

* Real-world system design
* Clean API structuring
* Scalable architecture thinking
* Full-stack integration capability

---

## 🤝 Contribution

Open for:

* Backend improvements
* Feature additions
* UI enhancements

---

## 📜 License

Open for educational and hackathon use.

---

## 💡 Closing Note

> ForgeAdmin is not just a dashboard — it’s a **blueprint for scalable admin systems**.
