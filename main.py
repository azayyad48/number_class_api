from fastapi import FastAPI, Query, HTTPException
import requests 
from typing import Union

app = FastAPI()

# Helper functions
def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def is_perfect(n: int) -> bool:
    if n < 2:
        return False
    return sum(i for i in range(1, n // 2 + 1) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    if n < 0:
        return False  # Armstrong numbers are non-negative
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d ** length for d in digits) == n

def digit_sum(n: Union[int, float]) -> int:
    return sum(int(d) for d in str(abs(int(n))))

def get_fun_fact(n: Union[int, float]) -> str:
    try:
        url = f"http://numbersapi.com/{int(n)}/math"
        response = requests.get(url, timeout=5)
        return response.text if response.status_code == 200 else "No fun fact available."
    except requests.RequestException:
        return "Could not fetch fun fact."

# API endpoint
@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        num = float(number)
        is_integer = num.is_integer()
        num = int(num) if is_integer else num
    except ValueError:
        return {
            "number": number,
            "error": True,
            "message": f"Invalid input: '{number}' is not a valid number."
        }

    properties = []
    prime_status, perfect_status, armstrong_status = None, None, None

    if is_integer:
        num_int = int(num)
        prime_status = is_prime(num_int)
        perfect_status = is_perfect(num_int)
        armstrong_status = is_armstrong(num_int)
        properties.extend(filter(None, [
            "prime" if prime_status else None,
            "perfect" if perfect_status else None,
            "armstrong" if armstrong_status else None,
            "odd" if num_int % 2 != 0 else "even"
        ]))
    else:
        properties.append("floating-point")

    fun_fact = get_fun_fact(num)

    return {
        "number": num,
        "is_prime": prime_status if is_integer else None,
        "is_perfect": perfect_status if is_integer else None,
        "is_armstrong": armstrong_status if is_integer else None,
        "properties": properties,
        "digit_sum": digit_sum(num),
        "fun_fact": fun_fact
    }


# Run the app
if __name__ == "__main__":
     import uvicorn
     uvicorn.run(app, host="127.0.0.1", port=8000)
