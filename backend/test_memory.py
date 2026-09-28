from hindsight_client import Hindsight

client = Hindsight(base_url="http://localhost:8888")

# Store a previous incident
client.retain(
    bank_id="incident-response",
    content="""
    Incident: Payment API returned 500 errors.
    Root cause: Database connection pool was exhausted.
    Resolution: Increased the database connection pool size and restarted the service.
    Outcome: Payment API returned to normal.
    """,
    context="production incident"
)

print("Memory stored successfully!")

# Search the memory
results = client.recall(
    bank_id="incident-response",
    query="What happened when the Payment API returned 500 errors?"
)

print("\nRecalled memories:")

for result in results.results:
    print("-", result.text)