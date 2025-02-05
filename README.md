# Number_Classification_Api
Creating an API that takes a number and returns interesting mathematical properties about it, along with a fun fact.

## 📌 DevOps Stage 1 - Number Classification API

## **📖 Project Overview**
The **Number Classification API** is a RESTful API that:
- Accepts a number as a query parameter.
- Determines its mathematical properties:
  - Checks if it's **prime**, **perfect**, or **Armstrong**.
  - Classifies it as **even** or **odd**.
  - Computes the **digit sum**.
- Fetches a **fun fact** from [Numbers API](http://numbersapi.com/).
- Returns results in **JSON format**.
- Supports **CORS (Cross-Origin Resource Sharing)**.
- Is deployed on **GitHub** for public access.

---

## **📌 Technologies Used**
- **Programming Language:** Python
- **Framework:** FastAPI
- **Server:** Uvicorn
- **External API:** Numbers API
- **Deployment:** GitHub
- **Package Management:** pip (`requirements.txt`)

---


## 📌 Installation & Running Locally

### 1️⃣ Clone the Repository
```bash
git clone <your-github-repo-url>
cd <your-project-directory>
```
### 2️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```
### 3️⃣ Run the API
```bash
uvicorn main:app --reload
```
### 4️⃣ Test API in Browser or Postman
```bash 
Open: http://127.0.0.1:8000/docs 
```
for interactive testing on your browser.

### 📌 Summary
✅ Fully functional API that classifies numbers and provides fun facts.

✅ Handles CORS for frontend compatibility.

✅ Deployed on GitHub for public access.

✅ Well-documented and follows DevOps best practices.