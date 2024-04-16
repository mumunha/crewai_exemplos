import sys
#!/usr/bin/env python
from agencia_clipping.crew import AgenciaNoticiasCrew
input_cmd = sys.argv[1]

def run():
    # Replace with your inputs, it will automatically interpolate any tasks and agents information
    inputs = {
        'topic': input_cmd
    }
    AgenciaNoticiasCrew().crew().kickoff(inputs=inputs)