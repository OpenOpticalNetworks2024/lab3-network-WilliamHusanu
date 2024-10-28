import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from core.elements import Network, Signal_information

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'
output_folder = ROOT / 'Results'
file_draw = output_folder / 'Link_Map.png'

# Load the Network from the JSON file, connect nodes and lines in Network.
obj1 = Signal_information(0.001,['ACDB'])
obj = Network(str(file_input))
path = obj.find_paths('A','B')
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
obj.propagate(obj1)
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
obj.draw(str(file_draw))
# Follow all the instructions in README.md file
