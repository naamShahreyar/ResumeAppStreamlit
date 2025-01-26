from langchain_community.vectorstores import Neo4jVector
from Embeddings.embeddings import HuggingFaceEmbeddingModel
from secret import Neo4j_url, Neo4j_username, Neo4j_password, Neo4j_index_name, Neo4j_node_label, Neo4j_text_node_properties, Neo4j_embedding_node_property

# Initialize Index
vector_index = Neo4jVector.from_existing_graph(
    HuggingFaceEmbeddingModel,
    url=Neo4j_url,
    username=Neo4j_username,
    password=Neo4j_password,
    index_name=Neo4j_index_name,
    node_label=Neo4j_node_label,
    text_node_properties=Neo4j_text_node_properties,
    embedding_node_property=Neo4j_embedding_node_property,
)