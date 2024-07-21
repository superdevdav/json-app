import click
import json
from pathlib import Path
from pydantic import create_model, BaseModel
from typing import Dict, Any


def parse_json_schema(schema: Dict[str, Any], model_name: str = "Model") -> BaseModel:
    fields = {}
    for key, value in schema.items():
        if key == 'kind' and len(value) <= 32:
            if len(value) <= 32:
                model_name = value.capitalize()
                fields[key] = (str(value), ...)
            else:
                raise Exception('incorrect kind value')
        
        elif key == 'name':
            if len(value) <= 128:
                fields[key] = (str, ...)
            else:
                raise Exception('incorrect name value')
        
        elif key == 'description':
            if len(value) <= 4096:
                fields[key] = (str, ...)
            else:
                raise Exception('incorrect description value')
        
        elif key == 'version':
            version_split = value.split('.')
            if version_split[0][0] == 'v' and '0' <= version_split[0][1] <= '9' and '0' <= version_split[1] <= '9' and '0' <= version_split[2] <= '9' and len(value) == 6:
                fields[key] = (str, ...)
            else:
                raise Exception('incorrect version value')
        
        elif type(value) == dict:
            nested_model = parse_json_schema(value, f"{key.capitalize()}")
            fields[key] = (nested_model, ...)
        
        else:
            fields[key] = (Any, ...)

    return create_model(model_name, **fields)


def generate_nested_classes(schema: Dict[str, Any]) -> str:
    code = ""
    for key, value in schema.items():
        if type(value) == dict:
            model_nested = parse_json_schema(value, key.capitalize())
            code += generate_classes(model_nested)
    return code


def generate_classes(model: Dict[str, Any]) -> str:
    model_name = model.__name__ 
    code = f"class {model_name}(BaseModel):\n"
    for field, field_type in model.__annotations__.items():
        if field in ('specification', 'settings'):
            code += f"  {field}: dict\n"
        elif field == 'kind':
            code += f"  {field}: str = '{field_type.capitalize()}'\n"
        else:
            type_name = getattr(field_type, '__name__', repr(field_type))
            code += f"  {field}: {type_name}\n"

    return code


def generate_pydantic_code(schema: Dict[str, Any], model_name: str) -> str:
    model = parse_json_schema(schema, model_name)
    code = f"from pydantic import BaseModel\n\n"
    code += generate_nested_classes(schema)
    code += "\n"
    code += generate_classes(model)
    return code


@click.command()
@click.option(
    "--json-schema",
    type=click.Path(exists=True),
    required=True,
    help="Path to JSON schema file.",
)
@click.option(
    "--out-dir",
    type=click.Path(file_okay=False, dir_okay=True),
    required=True,
    help="Directory to save the generated Pydantic models.",
)
def gen_models(json_schema, out_dir):
    json_schema_path = Path(json_schema).expanduser()
    out_dir_path = Path(out_dir).expanduser()

    out_dir_path.mkdir(parents=True, exist_ok=True)

    with open(json_schema_path, "r") as file:
        schema = json.load(file)

    model = parse_json_schema(schema)
    model_name = model.__name__
    try:
        pydantic_model_code = generate_pydantic_code(schema, model_name)

        path_out = out_dir_path / f"{model_name}.py"

        with open(path_out, "w") as file:
            file.write(pydantic_model_code)

        click.echo("Pydantic model saved successfully")
    except Exception as e:
        print(f'Exception: {e}')


if __name__ == "__main__":
    gen_models()
