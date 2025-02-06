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
    if n < 2:  # Fix: 0 should not be classified as perfect
        return False
    return sum(i for i in range(1, n // 2 + 1) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    if n < 0:
        return False  
    digits = [int(d) for d in str(n)]
    length = len(digits)
    return sum(d ** length for d in digits) == n

def digit_sum(n: Union[int, float]) -> int:
    return sum(int(d) for d in str(abs(int(n))))

def get_fun_fact(n: int, properties: list) -> str:
    """ Generate specific fun facts based on number properties. """
    if "armstrong" in properties:
        digits = [int(d) for d in str(n)]
        length = len(digits)
        breakdown = " + ".join(f"{d}^{length}" for d in digits)
        return f"{n} is an Armstrong number because {breakdown} = {n}."

    if "perfect" in properties:
        divisors = [i for i in range(1, n // 2 + 1) if n % i == 0]
        return f"{n} is a Perfect number because {n} = {' + '.join(map(str, divisors))}."

    if "prime" in properties:
        return f"{n} is a Prime number because it has exactly 2 divisors: 1 and {n}."

    if "odd" in properties:
        return f"{n} is an Odd number because it is not divisible by 2."

    if "even" in properties:
        return f"{n} is an Even number because it is divisible by 2."

    # Fallback to numbers API
    try:
        url = f"http://numbersapi.com/{n}/math"
        response = requests.get(url, timeout=5)
        return response.text if response.status_code == 200 else "No fun fact available."
    except requests.RequestException:
        return "Could not fetch fun fact."

# API endpoint
@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        num = int(number)  # Ensure we only accept integers
    except ValueError:
        return {
            "number": number,  # Fix: Return the invalid input in response
            "error": True
        }

    properties = []
    prime_status = is_prime(num)
    perfect_status = is_perfect(num)
    armstrong_status = is_armstrong(num)

    properties.extend(filter(None, [
        "armstrong" if armstrong_status else None,
        "odd" if num % 2 != 0 else "even"
    ]))

    fun_fact = get_fun_fact(num, properties)

    return {
        "number": num,
        "is_prime": prime_status,
        "is_perfect": perfect_status,
        "is_armstrong": armstrong_status,
        "properties": properties,
        "digit_sum": digit_sum(num),
        "fun_fact": fun_fact
    }

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)