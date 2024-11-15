from pymilvus import MilvusClient
from customer_vectorizer import generate_customer_vector

client = MilvusClient("http://localhost:19530") # Replace with ./milvus_demo.db if you'd like to use Milvus Lite instead
