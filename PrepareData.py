import numpy as np,csv,time,h5py 

def SaveH5(filename, data_array):
    try:
        with h5py.File(filename, 'w') as file:
            dataset = file.create_dataset("data", data=data_array)
        print(f"Array stored in {filename} successfully.")
    except Exception as e:
        print(f"Error: {e}")
        
INDICATOR = "YOUR_INDICATOR" # CHANGE THE INDICATOR ACCORDINGLY

# ENTER YOUR INDICATOR HERE

Closing = []
High = []
Low = []
Open = []
with open("YOUR_FOLDER_PATH",'r') as f:
    csv_r = csv.DictReader(f)
    rows = list(csv_r)
    for i in range(len(rows) -1,-1,-1):
            Closing.append(float(rows[i]['close']))
            High.append(float(rows[i]['high']))
            Low.append(float(rows[i]['low']))
            Open.append(float(rows[i]['open']))
Unix = [i for i,_ in enumerate(Closing)]

periods = []
for k in range(1,31):
    periods.append(k*1440)
    
data = {
    "High":np.array(High),
    "Low":np.array(Low),
    "Close":np.array(Closing),
    "Open":np.array(Open)
}

st = time.time()
DATA = []
for period in periods:
    #TODO: Function Implementation According to convention
print("Time taken : ",time.time() - st)

for d in range(len(DATA)):
    SaveH5(f"IndicatorData/{INDICATOR}/{INDICATOR}_{d}.h5",DATA[d]) 
