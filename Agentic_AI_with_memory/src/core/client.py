import stardog
from src.config.settings import SCHEMA_FROM_STARDOG

class StardogClient:
    def __init__(self, endpoint, database, username, password):
        self.endpoint = endpoint
        self.database = database
        self.connection_details = {
            'endpoint': endpoint,
            'username': username,
            'password': password
        }

    def query(self, sparql_query, use_reasoning=True):
        """Execute a SPARQL query against Stardog."""
        try:
            with stardog.Connection(self.database, **self.connection_details) as conn:
                result = conn.select(sparql_query, reasoning=use_reasoning)
                return result
        except Exception as e:
            print(f"Error executing SPARQL query: {e}")
            return None

    def update(self, sparql_update):
        """Execute a SPARQL UPDATE query."""
        try:
            with stardog.Connection(self.database, **self.connection_details) as conn:
                conn.begin()
                conn.update(sparql_update)
                conn.commit()
                return True
        except Exception as e:
            print(f"Error executing SPARQL update: {e}")
            return False

    def get_schema(self):
        """Get the ontology schema from the knowledge graph."""
        schema_details_query = f"""
        SELECT ?s ?p ?o
        FROM {SCHEMA_FROM_STARDOG}
        WHERE {{
            ?s ?p ?o
        }}
        """
        schema_result = self.query(schema_details_query, use_reasoning=False)
        if schema_result and schema_result.get('results', {}).get('bindings'):
            triples = schema_result['results']['bindings']
            classes = set()
            object_properties = {}
            datatype_properties = {}
            ontology_base = SCHEMA_FROM_STARDOG
            
            def short_name(uri):
                return uri[len(ontology_base):] if uri.startswith(ontology_base) else uri

            for triple in triples:
                subject = triple['s']['value']
                predicate = triple['p']['value']
                obj = triple['o']['value']

                if predicate == 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type':
                    if obj == 'http://www.w3.org/2002/07/owl#Class':
                        cls = short_name(subject)
                        if cls != SCHEMA_FROM_STARDOG:
                            classes.add(cls)
                    elif obj == 'http://www.w3.org/2002/07/owl#ObjectProperty':
                        op = short_name(subject)
                        if op not in object_properties:
                            object_properties[op] = {'domain': None, 'range': None}
                    elif obj == 'http://www.w3.org/2002/07/owl#DatatypeProperty':
                        dp = short_name(subject)
                        if dp not in datatype_properties:
                            datatype_properties[dp] = {'domain': None, 'range': None}

                if predicate == 'http://www.w3.org/2000/01/rdf-schema#domain':
                    prop = short_name(subject)
                    val = short_name(obj)
                    if prop in object_properties:
                        object_properties[prop]['domain'] = val
                    elif prop in datatype_properties:
                        datatype_properties[prop]['domain'] = val
                if predicate == 'http://www.w3.org/2000/01/rdf-schema#range':
                    prop = short_name(subject)
                    val = short_name(obj)
                    if prop in object_properties:
                        object_properties[prop]['range'] = val
                    elif prop in datatype_properties:
                        datatype_properties[prop]['range'] = val

            return {
                'classes': sorted(classes),
                'object_properties': object_properties,
                'datatype_properties': datatype_properties,
                'raw_result': schema_result
            }
        return None