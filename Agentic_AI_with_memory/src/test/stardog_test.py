import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.core.client import StardogClient
from src.config.settings import (
    STARDOG_ENDPOINT, 
    STARDOG_DATABASE, 
    STARDOG_USERNAME, 
    STARDOG_PASSWORD
)

def main():
    
    print("Testing Stardog Client...")
    
    # Check config
    if not all([STARDOG_ENDPOINT, STARDOG_DATABASE, STARDOG_USERNAME, STARDOG_PASSWORD]):
        print("❌ Missing Stardog configuration in .env file")
        return
    
    try:
        # Create client
        client = StardogClient(STARDOG_ENDPOINT, STARDOG_DATABASE, STARDOG_USERNAME, STARDOG_PASSWORD)
        print("✅ Client created successfully")
        
        # Test 1: Get Schema
        print("\n1. Getting schema...")
        schema = client.get_schema()
        if schema:
            print(f"✅ Schema retrieved: {len(schema['classes'])} classes found")
            print(f"Classes: {schema['classes']}")
            print(f"\nObject Properties: {schema['object_properties']}")
            print(f"\nDatatype Properties: {schema['datatype_properties']}")
        else:
            print("❌ Failed to get schema")
        
        # # Test 2: Simple Query
        # print("\n2. Testing simple query...")
        # query = """
        # PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        # PREFIX ins: <https://a.in/sales/CRUD_Ontology#>
        
        # SELECT ?name
        # FROM <https://a.in/sales/CRUD_data>
        # WHERE {
        #   ?s rdf:type ins:Student ;
        #      ins:name ?name .
        # }
        # LIMIT 5
        # """
        
        # result = client.query(query)
        # if result and 'results' in result:
        #     bindings = result['results']['bindings']
        #     print(f"✅ Query executed: {len(bindings)} results")
        #     for binding in bindings:
        #         print(f"   - {binding['name']['value']}")
        # else:
        #     print("❌ Query failed")
            
        print("\n✅ Test completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main() 