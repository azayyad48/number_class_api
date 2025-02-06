from fastapi import FastAPI, Query, HTTPException
import requests

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
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(n)]
    return sum(d ** len(digits) for d in digits) == n

def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))

def get_fun_fact(n: int, is_armstrong_num: bool) -> str:
    """Returns a specific fun fact for Armstrong numbers, otherwise fetches from Numbers API."""
    if is_armstrong_num:
        digits = [int(d) for d in str(n)]
        length = len(digits)
        breakdown = " + ".join(f"{d}^{length}" for d in digits)
        return f"{n} is an Armstrong number because {breakdown} = {n}."

    try:
        response = requests.get(f"http://numbersapi.com/{n}/math", timeout=5)
        return response.text if response.status_code == 200 else "No fun fact available."
    except requests.RequestException:
        return "Could not fetch fun fact."

# API Endpoint
@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    # Validate input
    if not number.lstrip('-').isdigit():
        raise HTTPException(
            status_code=400,
            detail={"number": number, "error": True}
        )

    num = int(number)

    # Determine properties
    properties = []
    if is_armstrong(num):
        properties.append("armstrong")
    properties.append("odd" if num % 2 != 0 else "even")

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": digit_sum(num),
        "fun_fact": get_fun_fact(num, "armstrong" in properties)
    }