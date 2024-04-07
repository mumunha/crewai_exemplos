import sys
import os
#!/usr/bin/env python
from agencia_noticias.crew import AgenciaNoticiasCrew

# set current path as variable path_root
path_root = os.path.dirname(os.path.abspath(__file__))

# load input_cmd from file email.txt
with open(path_root+'/email.txt', encoding='utf-8') as f:
    input_cmd = f.read().strip()

# input_cmd = "Bom dia! Gostaria de propor uma parceria!"
def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': input_cmd,
    }
    print(inputs)
    AgenciaNoticiasCrew().crew().kickoff(inputs=inputs)