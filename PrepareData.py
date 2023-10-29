import numpy as np,csv,time,h5py 
import matplotlib.pyplot as plt

def SaveH5(filename, data_array):
    try:
        with h5py.File(filename, 'w') as file:
            dataset = file.create_dataset("data", data=data_array)
        print(f"Array stored in {filename} successfully.")
    except Exception as e:
        print(f"Error: {e}")
        
INDICATOR = "ATR" # CHANGE THE INDICATOR ACCORDINGLY

def Average_True_Range_TREND(data, period):
    atr = [0]  # ATR for the first data point is 0
    for i in range(1, len(data)):
            high = data['High'][i]
            low = data['Low'][i]
            previous_close = data['Close'][i - 1]
            
            tr = max(high - low, abs(high - previous_close), abs(low - previous_close))
            atr_value = (atr[-1] * (period - 1) + tr) / period
            atr.append(atr_value)
    
    return atr

Closing = []
High = []
Low = []
Open = []
with open("Bitstamp_ETHUSD_2023_minute.csv",'r') as f:
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
    DATA.append(Average_True_Range_TREND(data,period)) # CHANGE THE ARGUMENTS ACCORDINGLY
print("Time passed is : ",time.time() - st)

print("Length : ",len(DATA))
plt.figure()
plt.plot(DATA[5])
plt.show()

for d in range(len(DATA)):
    SaveH5(f"IndicatorData/{INDICATOR}/{INDICATOR}_{d}.h5",DATA[d]) 