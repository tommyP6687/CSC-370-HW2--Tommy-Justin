"""Read and collect data from the three csv files
"""

def read_data(file_name):
    """Read each line in the dataset & append to corresponding lists

    Args:
        file_name (str): name of file containing dataset

    Returns:
        tuple: (x, x1, x2, x3, y) lists; unused lists remain empty
    """
    # lists to store values
    x = []
    x1 = []
    x2 = []
    x3 = []
    y = []
    
    # open file in read-mode
    with open(file_name, 'r') as file:
        
        # iterate through each line
        for line in file:
            
            # strip leading & trailing whitespace & split each value into a list
            info = line.strip().split(",")
            
            # dataset 1 & 3 (optional)
            if len(info) == 2:
                # ignore first line
                if info[0] == 'x':
                    continue
                # otherwise, add each value (x, f(x)) to corresponding lists
                x.append(float(info[0]))
                y.append(float(info[1]))
                
            # dataset 2
            else: 
                # ignore first line 
                if info[0] == 'x1':
                    continue
                # otherwise, add each value (x1, x2, x3, f(x1, x2, x3)) to corresponding lists
                x1.append(float(info[0]))
                x2.append(float(info[1]))
                x3.append(float(info[2]))
                y.append(float(info[3]))
        
    return x, x1, x2, x3, y