# 🛒 Fantasy Store Team Builder

A minimal full-stack web application that helps users assemble the **best value product team** from a fictional fantasy store — within a given budget.

---

## 🚀 Features

- Input a budget and get 5 high-value products from **5 distinct categories**
- Products optimized for a **balance between quality and price**
- Handles low-budget cases gracefully
- Sort returned products by **rating** or **price**
- Dockerized setup — runs with a single command

---

## 📊 Product Selection Logic

The backend selects a team of 5 products by:

- Choosing only products with **rating ≥ 4.0**
- Considering teams with one product per **unique category**
- Scoring each team with a weighted formula:

```text
score = (sum of rating^1.8) * 0.9 + (budget utilization ratio) * 0.1
```


## 🧪 Running Instructions
### 📦 Prerequisites
- Docker installed and running
- Clone the Project
```commandline
git clone https://github.com/your-username/fantasy-store-team-builder.git
```

▶️ Run the App, at the project root, simply run:
```
docker-compose up --build
```
🌐 Access the Application
Frontend: http://localhost:3000

Backend API (Optional): http://localhost:8000/team-builder?budget=300
