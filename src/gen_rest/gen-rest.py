import click
import os
from pathlib import Path
from generate_controller_code import generate_controller_code

def get_files_in_directory(path):
      files = []
      for file in os.listdir(path):
          file_path = os.path.join(path, file)
          if file_path[-3:] == '.py':
            files.append(file_path)
      return files

@click.command()
@click.option("--models", type=click.Path(exists=True), required=True, help="Path to pydantic model file.")
@click.option("--rest-routes", type=click.Path(file_okay=False, dir_okay=True), required=True, help="Directory to save the generated REST controllers.")
def gen_rest(models, rest_routes):
    models_path = Path(models).expanduser()
    rest_routes_path = Path(rest_routes).expanduser()
    rest_routes_path.mkdir(parents=True, exist_ok=True)

    models_files = get_files_in_directory(models_path)
    
    for file_path in models_files:    
        file_name = file_path.split('\\')[-1]
        model_name = file_name.split('.')[0]
        rest_code = generate_controller_code(model_name)
        path_out = rest_routes + '/' + f"{model_name}_controller.py"
        
        try:
            with open(path_out, "w") as file:
                file.write(rest_code)
                click.echo(f"REST controller created successfully for model: {model_name.capitalize()}")
        except Exception as e:
            click.echo(f'Error in creating REST controller for model: {model_name.capitalize()}')

if __name__ == '__main__':
    gen_rest()