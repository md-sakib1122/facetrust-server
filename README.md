# FaceTrust - AI-based Smart Attendance System

FaceTrust is a **real-time face recognition attendance system** built using **FastAPI**, **React.js**, and **MongoDB**. It automates employee attendance by detecting and verifying faces through live camera feeds, supporting multi-company environments with role-based access control.

---

## 🌟 Features

- **Real-Time Face Recognition:** Captures live webcam frames and verifies faces using **InsightFace (ArcFace)** embeddings.
- **Multi-Company Support:** Filters embeddings by `company_id` to ensure company-specific verification.
- **Role-Based Authentication:** JWT-based login with **secure HttpOnly cookies**.
- **Employee Management:** Add, edit, and manage employee embeddings per company.
- **Attendance Reporting:** Generates reports of employee attendance automatically.
- **Asynchronous Backend:** FastAPI handles multiple concurrent requests efficiently.
- **Frontend Dashboard:** Interactive React.js dashboard with protected routes and real-time status updates.

---

## 🛠 Tech Stack

- **Backend:** FastAPI, Python, ONNX, OpenCV, InsightFace, async MongoDB (Motor)
- **Frontend:** React.js, JavaScript, Tailwind CSS, Canvas API
- **Database:** MongoDB
- **Authentication:** JWT tokens with HttpOnly cookies
- **Deployment Tools:** Uvicorn, Vercel (frontend), optional Docker for backend

---


---

## ⚡ Installation

### Backend
```bash
# Clone the repository
git clone https://github.com/Nazmuzzaman/facetrust-server.git
cd facetrust-server

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Set environment variables
cp .env.example .env
# Update .env with SECRET_KEY, MONGO_URI, ALGORITHM, etc.

# Run the server
uvicorn app.main:app --reload


