import json
import pandas as pd

schema_file = "/Users/laurahughes/GitHub/niaid-data-portal/schema/NIAIDDataset.json"

schema = json.load(open(schema_file))

# From the graph...
props = [{"namespace": prop["schema:domainIncludes"][0]["@id"].split(":")[1], "field": prop["rdfs:label"], "type_obj": prop["schema:rangeIncludes"], "description": prop["rdfs:comment"], "required": prop["marginality"] == "required", "cardinality": prop["owl:cardinality"]} for prop in schema["@graph"] if prop["@type"] == "rdf:Property"]
df = pd.DataFrame(props)


def getType(type_obj):
    if(isinstance(type_obj, list)):
        id = type_obj[0]["@id"]
    else:
        id = type_obj["@id"]
    return(id.split(":")[1])

def getVariable(row, df = df, namespace = "NiaidDataset"):
    if(row.namespace == namespace):
        return(row.field)
    else:
        filtered = df[df.type == row.namespace]
        if(len(filtered) == 1):
            filtered.reset_index(inplace=True)
            return(f'{filtered.loc[0, "field"]}.{row.field}')
        else:
            print("Too many stubs found! Yell at Laura for not providing a more useful error message")


df["type"] = df.type_obj.apply(getType)
df["variable"] = df.apply(getVariable, axis=1)
df = df[["namespace", "field", "variable", "description", "type", "required", "cardinality"]]
df.to_csv("NIAID_dataset_template.csv")
