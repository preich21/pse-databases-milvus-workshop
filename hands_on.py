from time import sleep
from pymilvus import MilvusClient, DataType
from customer_vectorizer import generate_customer_vector

client = MilvusClient("http://localhost:19530")

#########################################################
# Collections
#########################################################

client.create_collection(
    collection_name="workshop",
    dimension=5
)

res = client.list_collections()
print(res)

res = client.get_load_state(collection_name="workshop")
print(res)

client.release_collection(collection_name="workshop")
res = client.get_load_state(collection_name="workshop")
print(res)

client.load_collection(collection_name="workshop")
res = client.get_load_state(collection_name="workshop")
print(res)

client.drop_collection(collection_name="workshop")
res = client.list_collections()
print(res)

schema = client.create_schema(
    auto_id=True,
    enable_dynamic_field=True
)
schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=5)

index_params = client.prepare_index_params()
index_params.add_index(
    field_name="id",
    index_type="STL_SORT"
)
index_params.add_index(
    field_name="vector",
    index_type="IVF_FLAT",
    metric_type="L2",
    params={"nlist": 5}
)

client.create_collection(
    collection_name="workshop",
    schema=schema,
    index_params=index_params
)

res = client.list_collections()
print(res)

#########################################################
# Partitions
#########################################################

client.create_partition(
    collection_name="workshop",
    partition_name="partition1"
)

res = client.list_partitions(collection_name="workshop")
print(res)

res = client.has_partition(collection_name="workshop", partition_name="partition1")
print(res)
res = client.has_partition(collection_name="workshop", partition_name="non_existent_partition")
print(res)

#########################################################
# Data
#########################################################

data = [
    {"vector": [1, 4, -5, 3, 2]}
]
res = client.insert(
    collection_name="workshop",
    partition_name="partition1",
    data=data
)
print(res)

sleep(1)

inserted_id = res['ids'][0]
print(inserted_id)
res = client.get(
    collection_name="workshop",
    partition_name="partition1",
    ids=[inserted_id],
    output_fields=["*"]
)
print(res)

res = client.upsert(
    collection_name="workshop",
    partition_name="partition1",
    data= [{"id": inserted_id, "vector": [1, 23, -5, 3, 2]}]
)
print(res)

sleep(1)

res = client.query(
    collection_name="workshop",
    limit=10,
)
print(res)

updated_id = res[0]["id"]
res = client.delete(
    collection_name="workshop",
    ids=[updated_id]
)
print(res)

sleep(1)
res = client.query(
    collection_name="workshop",
    limit=10
)
print(res)

#########################################################
# Exercise introduction - Data & Aggregate
#########################################################

res = client.query(
    collection_name="customers",
    filter="35 < age < 45",
    limit=10,
)
print(res)

res = client.search(
    collection_name="customers",
    data=[generate_customer_vector("Peter Hertkorn", 42, ["databases"])],
    limit=1,
    output_fields=["name", "age", "interests"]
)
print(res)

res = client.query(
    collection_name="customers",
    filter="35 < age < 45",
    output_fields=["count(*)"]
)
print(res)
