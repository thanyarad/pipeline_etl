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

    def get_formatted_schema(self):
        """Get a formatted schema summary with classes and relationships."""
        schema = self.get_schema()
        if schema:
            classes_with_properties = {}
            relationships = {}
            for cls in schema['classes']:
                classes_with_properties[cls] = {}
            for prop_name, prop_info in schema['datatype_properties'].items():
                domain = prop_info.get('domain')
                range_type = prop_info.get('range', 'string')
                if range_type and 'XMLSchema#' in range_type:
                    range_type = range_type.split('#')[-1]
                elif range_type and range_type.startswith('http://'):
                    range_type = range_type.split('/')[-1].split('#')[-1]
                if domain and domain in classes_with_properties:
                    classes_with_properties[domain][prop_name] = range_type
            for relationship, rel_info in schema['object_properties'].items():
                domain = rel_info.get('domain')
                range_obj = rel_info.get('range')
                relationships[relationship] = {'domain': domain, 'range': range_obj}
            schema_dict = {'classes': classes_with_properties, 'relation': relationships}
            schema_str = str(schema_dict).replace("{", "{{").replace("}", "}}")
            return schema_str
        return None