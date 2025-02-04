from fastapi import FastAPI, Query, HTTPException
import requests
import ssl
import certifi
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Utility functions
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    return n > 1 and sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def get_digit_sum(n: int) -> int:
    return sum(int(d) for d in str(n))

def get_fun_fact(n: int) -> str:
    try:
        response = requests.get(f"http://numbersapi.com/{n}/math?json", verify=ssl_context)
        return response.json().get("text", "No fact available")
    except requests.exceptions.RequestException:
        return "Could not fetch fun fact."

@app.get("/api/classify-number")
def classify_number(number: int = Query(..., description="Number to classify")) -> Dict:
    try:
        properties = []
        if is_armstrong(number):
            properties.append("armstrong")
        properties.append("odd" if number % 2 else "even")
        
        response = {
            "number": number,
            "is_prime": is_prime(number),
            "is_perfect": is_perfect(number),
            "properties": properties,
            "digit_sum": get_digit_sum(number),
            "fun_fact": get_fun_fact(number)
        }
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Run the application (for local testing)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
