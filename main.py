import json
import numpy as np
import h5py
import subprocess
import os

# ler os dados do saida.txt e pega o payload_raw de bn: 74FE48FFFF6D89FF
# o payload_raw é o que vai ser usado no modelo
# [{"bn": "74FE48FFFF6D89FF", "bt": 1675185787}, {"n": "uplink", "u": "count", "v": 10082}, {"n": "activation_mode", "vs": "OTAA"}, {"n": "datarate", "vs": "SF12BW125"}, {"n": "rssi", "u": "dBW", "v": -79}, {"n": "snr", "u": "dB", "v": 8}, {"n": "payload_raw", "vs": "81623a50080700000097cc00005423e20700004601f406eb0400009101060bcc070000be0086037e0203000000002e5e905c60"}, {"n": "gateway", "vs": "F8033202DF790000"}]
payload_raw = []
with open('saida.txt', 'r') as f:
    lines = f.readlines()
    for line in lines:
        if '"bn": "74FE48FFFF6D89FF"' in line:
            line = line.split('"payload_raw", "vs": "')[1].split('"')[0]
            payload_raw.append(line)
        
# converte o payload_raw para json e salva em um arquivo dentro da pasta output para cada elemento do payload_raw
for elem in payload_raw:
    with open('output/{}.json'.format(elem), 'w') as f:
        result = subprocess.run(["./main-linux", elem], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        f.write(result.stdout)


# pega todos os arquivos json e colocar dentro de uma lista
json_files = []
for file in os.listdir('output'):
    if file.endswith('.json'):
        json_files.append(file)



# pega os dados de cada arquivo json e salva em uma lista
parsed_data = []
for file in json_files:
    with open('output/{}'.format(file), 'r') as f:
        parsed_data.append(json.load(f))

# print(parsed_data)

# para cada arquivo json, pega os dados de cada eixo e salva em uma lista
x_data = []
y_data = []
z_data = []

for data in parsed_data:
    x_data.append(data['Accelerometer']['X-Axis'])
    y_data.append(data['Accelerometer']['Y-Axis'])
    z_data.append(data['Accelerometer']['Z-Axis'])

# x_data = parsed_data['Accelerometer']['X-Axis']
# y_data = parsed_data['Accelerometer']['Y-Axis']
# z_data = parsed_data['Accelerometer']['Z-Axis']

# para cada eixo, pega os dados de cada feature e salva em uma lista
x_matrix = []
y_matrix = []
z_matrix = []

for data in x_data:
    x_matrix.append([data['OAVelocity'], data['Peakmg'], data['RMSmg'], data['Kurtosis'], data['CrestFactor'], data['Skewness'], data['Deviation'], data['Peak-to-Peak Displacement']])
for data in y_data:
    y_matrix.append([data['OAVelocity'], data['Peakmg'], data['RMSmg'], data['Kurtosis'], data['CrestFactor'], data['Skewness'], data['Deviation'], data['Peak-to-Peak Displacement']])
for data in z_data:
    z_matrix.append([data['OAVelocity'], data['Peakmg'], data['RMSmg'], data['Kurtosis'], data['CrestFactor'], data['Skewness'], data['Deviation'], data['Peak-to-Peak Displacement']])

# x_matrix = np.array([x_data['OAVelocity'], x_data['Peakmg'], x_data['RMSmg'], x_data['Kurtosis'], x_data['CrestFactor'], x_data['Skewness'], x_data['Deviation'], x_data['Peak-to-Peak Displacement']])
# y_matrix = np.array([y_data['OAVelocity'], y_data['Peakmg'], y_data['RMSmg'], y_data['Kurtosis'], y_data['CrestFactor'], y_data['Skewness'], y_data['Deviation'], y_data['Peak-to-Peak Displacement']])
# z_matrix = np.array([z_data['OAVelocity'], z_data['Peakmg'], z_data['RMSmg'], z_data['Kurtosis'], z_data['CrestFactor'], z_data['Skewness'], z_data['Deviation'], z_data[ 'Peak-to-Peak Displacement']])



# transforma em um arquivo h5 para ser usado no modelo

# para cada eixo, transforma em um array numpy
x_matrix = np.array(x_matrix)
y_matrix = np.array(y_matrix)
z_matrix = np.array(z_matrix)

# x_matrix = x_matrix.reshape(1, 8)
# y_matrix = y_matrix.reshape(1, 8)
# z_matrix = z_matrix.reshape(1, 8)

print(x_matrix)
print(y_matrix)
print(z_matrix)
print(x_matrix.shape)
print(y_matrix.shape)
print(z_matrix.shape)

# print(x_matrix)
# print(y_matrix)
# print(z_matrix)

# salva em um arquivo h5

with h5py.File('data.h5', 'w') as hf:
    hf.create_dataset('x', data=x_matrix)
    hf.create_dataset('y', data=y_matrix)
    hf.create_dataset('z', data=z_matrix)

