import os
import django
import serial
import sys

# 1. Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iot_app.settings')
django.setup()

# 2. Importar tu modelo (ajusta 'weather_station' al nombre real de tu app)
from weather_station.models import Lectura 

# Configuración Serial
puerto = '/dev/ttyUSB0'

try:
    ser = serial.Serial(puerto, 9600, timeout=1)
    print("✅ Conectado y usando el ORM de Django")
    
    while True:
        if ser.in_waiting > 0:
            linea = ser.readline().decode('utf-8').strip()
            partes = linea.split(',')
            
            if len(partes) == 3:
                # 3. Guardar usando el ORM (esto usa lo que definiste en settings.py)
                nueva_lectura = Lectura(
                    dht_temp=float(partes[0]),
                    dht_hum=float(partes[1]),
                    lm35_temp=float(partes[2])
                )
                # Especificamos que guarde en la conexión 'supabase' de tu settings.py
                nueva_lectura.save(using='supabase')
                
                print(f"📡 Guardado en Supabase vía ORM: {partes}")
                
except KeyboardInterrupt:
    print("\nDetenido.")
finally:
    if 'ser' in locals(): ser.close()