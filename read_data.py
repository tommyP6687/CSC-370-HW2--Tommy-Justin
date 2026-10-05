"""Read and collect data from the three csv files
"""

def read_data(file_name):
    """Read each line in the dataset
    """
    with open(file_name, 'r') as file:
        for line in file:
            info = line.strip().split()