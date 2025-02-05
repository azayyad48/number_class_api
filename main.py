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
    if n < 2:
        return False
    return sum(i for i in range(1, n) if n % i == 0) == n

def is_armstrong(n: int) -> bool:
    digits = [int(d) for d in str(abs(n))]  # Handle negative numbers
    length = len(digits)
    return sum(d ** length for d in digits) == abs(n)

def digit_sum(n: int) -> int:
    return sum(int(d) for d in str(abs(n)))  # Handle negative numbers

def get_fun_fact(n: int) -> str:
    url = f"http://numbersapi.com/{n}/math"
    response = requests.get(url)
    return response.text if response.status_code == 200 else "No fun fact available."

# API endpoint
@app.get("/api/classify-number")
async def classify_number(number: str = Query(..., description="The number to classify")):
    try:
        # Check if the input is a valid integer (positive, negative, or zero)
        num = int(number)
    except ValueError:
        # If not, check if it's a floating-point number
        try:
            float(number)
            # If it's a float, return 400 Bad Request
            raise HTTPException(status_code=400, detail={"number": number, "error": True})
        except ValueError:
            # If it's not a number at all, return 400 Bad Request
            raise HTTPException(status_code=400, detail={"number": number, "error": True})

    # For valid integers, proceed with classification
    properties = []
    if is_prime(num):
        properties.append("prime")
    if is_perfect(num):
        properties.append("perfect")
    if is_armstrong(num):
        properties.append("armstrong")
    if num % 2 != 0:
        properties.append("odd")
    else:
        properties.append("even")

    fun_fact = get_fun_fact(num)

    return {
        "number": num,
        "is_prime": is_prime(num),
        "is_perfect": is_perfect(num),
        "properties": properties,
        "digit_sum": digit_sum(num),
        "fun_fact": fun_fact
    }

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)