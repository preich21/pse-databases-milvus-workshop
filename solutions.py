from pymilvus import MilvusClient
from customer_vectorizer import generate_customer_vector

client = MilvusClient("http://localhost:19530") # Replace with ./milvus_demo.db if you'd like to use Milvus Lite instead


#########################################################################
# Aufgabe 1
#########################################################################
res = client.get(
    collection_name="customers",
    ids=[3],
    output_fields=["name"],
)
print("1: ", res)


#########################################################################
# Aufgabe 2
#########################################################################
res = client.query(
    collection_name="customers",
    filter="name == 'Bob Jackson'",
    output_fields=["name", "interests"],
)
print("2: ", res)


#########################################################################
# Aufgabe 3
#########################################################################
res = client.query(
    collection_name="customers",
    filter="interests LIKE '%coding%'",
    output_fields=["name", "age", "interests"],
)
print("3: ", res)


#########################################################################
# Aufgabe 4
#########################################################################
res = client.query(
    collection_name="customers",
    filter="interests LIKE '%skiing%'",
    output_fields=["count(*)"],
)
print("4: ", res)


#########################################################################
# Aufgabe 5
#########################################################################
data = client.query(
    collection_name="customers",
    filter="name == 'Sam Lopez'",
    limit=1,
    output_fields=["*"],
)
data[0]["interests"] = "photography"
res = client.upsert(
    collection_name="customers",
    data=data,
)
print("5: ", res)


#########################################################################
# Aufgabe 6
#########################################################################
data = [
    {
        "id": 201,
        "name": "Agathe Bauer",
        "age": 34,
        "interests": "singing, dancing",
        "vector": generate_customer_vector("Agathe Bauer", 34, ["singing", "dancing"])
    }
]
res = client.insert(
    collection_name="customers",
    data=data,
)
print("6: ", res)


#########################################################################
# Aufgabe 7
#########################################################################
res = client.delete(
    collection_name="customers",
    filter="name == 'Kara Lee'"
)
print("7: ", res)


#########################################################################
# Aufgabe 8
#########################################################################
limit = client.query(
    collection_name="customers",
    output_fields=["count(*)"],
)[0]["count(*)"]
res = client.query(
    collection_name="customers",
    limit=limit,
    output_fields=["age"],
)
ageSum = 0
for i, re in enumerate(res):
    ageSum += re["age"]
print("8: ", ageSum / len(res))


#########################################################################
# Aufgabe 9
#########################################################################
res = client.search(
    collection_name="customers",
    data=[generate_customer_vector("Alice Miller", 62, ['yoga', 'skiing', 'cooking', 'gaming'])],
    limit=3,
    output_fields=["name", "age", "interests"],
)
print("9: ", res)


#########################################################################
# Aufgabe 10
#########################################################################
vector = client.query(
    collection_name="customers",
    filter="name == 'Charlie Martinez'",
    limit=1,
    output_fields=["vector"],
)[0]["vector"]
res = client.search(
    collection_name="customers",
    data=[vector],
    filter="interests LIKE '%gardening%'",
    limit=3,
    output_fields=["name", "age", "interests"],
)
print("10: ", res)


#########################################################################
# Aufgabe 11
#########################################################################
customer = client.query(
    collection_name="customers",
    filter="name == 'Nina Thomas'",
    limit=1,
    output_fields=["name", "age", "interests"],
)[0]
vector = generate_customer_vector("Mina Thomas", customer["age"], customer["interests"].split(", "))
res = client.search(
    collection_name="customers",
    data=[vector],
    limit=3,
    output_fields=["name", "age", "interests"],
)
print("11: ", res)
