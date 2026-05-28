import ollama

customer_data = """
Customer Churn Risk: HIGH

Key Risk Factors:
- Low product usage
- High support burden
- Low satisfaction score

Generate retention recommendations.
"""

response = ollama.chat(
    model="phi3",
    messages=[
        {
            "role": "user",
            "content": customer_data
        }
    ]
)

print(
    response["message"]["content"]
)