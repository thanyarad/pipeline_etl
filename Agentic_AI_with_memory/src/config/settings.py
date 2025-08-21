import os
from dotenv import load_dotenv

load_dotenv()

# Stardog configuration
STARDOG_ENDPOINT = os.getenv("STARDOG_ENDPOINT")
STARDOG_DATABASE = os.getenv("STARDOG_DATABASE")
STARDOG_USERNAME = os.getenv("STARDOG_USERNAME")
STARDOG_PASSWORD = os.getenv("STARDOG_PASSWORD")

# Ontology prefixes for product

PREFIXES = """
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX so: <https://schema.org/>
PREFIX stardog: <tag:stardog:api:>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX : <http://api.stardog.com/>
PREFIX Prod_Ont: <https://ph.org/prod/ontology#>
PREFIX Prod_data: <https://ph.org/prod/data#>
PREFIX Product_catalog: <https://product.org/product_catalog/ontology#>
"""

# Ontology schema for product

SCHEMA_FROM_STARDOG = "<https://product.org/product_catalog/ontology>"
EXECUTE_FROM_STARDOG = "<https://product.org/product_catalog/apparel>"


# PREFIXES = """
# PREFIX ins: <https://a.in/sales/CRUD_Ontology#> 
# PREFIX owl: <http://www.w3.org/2002/07/owl#> 
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
# PREFIX so: <https://schema.org/> 
# PREFIX stardog: <tag:stardog:api:> 
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
# PREFIX : <http://api.stardog.com/> 
# PREFIX ins_data: <https://a.in/sales/CRUD_data#>
# """

# SCHEMA_FROM_STARDOG = "<https://a.in/sales/CRUD_Ontology>"
# EXECUTE_FROM_STARDOG = "<https://a.in/sales/CRUD_data>"

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = "https://api.openai.com/v1"
OPENAI_MODEL = os.getenv("OPENAI_MODEL")

# Google configuration
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
# GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")

# Default LLM provider to use
DEFAULT_LLM_PROVIDER = os.getenv("DEFAULT_LLM_PROVIDER", "openai")