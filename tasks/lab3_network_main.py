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

# Load the Network from the JSON file, connect nodes and lines in Network.
obj1 = Signal_information(0.001,['ABCD'])
obj = Network(str(file_input))
obj.connect()
path = obj.find_paths('A','B')
obj.draw()

# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file
