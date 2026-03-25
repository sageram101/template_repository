# Command to create a Conda environment
import os
def create_conda_environment(env_name):
    conda_cmd = f"conda create --name {env_name} python=3.8 --y"
    os.system(conda_cmd)
    print(f"Conda environment '{env_name}' created.")

create_conda_environment('my_env')
