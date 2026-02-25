import threading
import time
import random
import logging

# Configuración de logs para ver la trazabilidad de los hilos
logging.basicConfig(level=logging.INFO, format='[%(threadName)s] %(message)s')

# Recursos: Las Islas Canarias (Cada una es un Lock)
islas = {
    "Tenerife": threading.Lock(),
    "Gran Canaria": threading.Lock(),
    "Lanzarote": threading.Lock(),
    "Fuerteventura": threading.Lock(),
    "La Palma": threading.Lock(),
    "La Gomera": threading.Lock(),
    "El Hierro": threading.Lock()
}

def teletransportar(nombre_viajero, origen, destino):
    logging.info(f"ESTADO: IDLE - {nombre_viajero} quiere ir de {origen} a {destino}.")
    
    # Transición de Estado: REQUESTING
    logging.info(f"ESTADO: REQUESTING - Intentando acceder a {destino}...")
    
    # Intentamos adquirir el bloqueo de la isla destino
    # Si 'blocking=False', simulamos el fallo/condición de carrera si no está libre
    exito = islas[destino].acquire(blocking=False)
    
    if exito:
        try:
            # Transición de Estado: TELEPORTING (Sección Crítica)
            logging.info(f"ESTADO: TELEPORTING - {nombre_viajero} está en el túnel hacia {destino}.")
            time.sleep(random.uniform(1, 2)) # Simulando el tiempo de viaje
            
            # Transición de Estado: COMPLETED
            logging.info(f"ESTADO: COMPLETED - {nombre_viajero} ha llegado a {destino} con éxito. ¡A la playa!")
        finally:
            # Liberamos el destino para el siguiente
            islas[destino].release()
    else:
        # Transición de Estado: FUSION (Error de concurrencia)
        # Aquí manejamos el fallo concatenando strings como pide el ejercicio
        mutante = f"ERROR_FUSION_{nombre_viajero}_CON_DESCONOCIDO_EN_{destino}"
        logging.error(f"ESTADO: FAILED - ¡DESASTRE! {nombre_viajero} ha colisionado. Resultado: {mutante}")

# --- Simulación de múltiples viajeros simultáneos ---
viajeros = [
    ("Yeray", "Tenerife", "Lanzarote"),
    ("Ayoze", "Gran Canaria", "Lanzarote"), # Conflicto potencial con Yeray
    ("Chano", "La Palma", "El Hierro"),
    ("Paco_El_Murciano", "Murcia", "Tenerife") # ¡Cuidado con este!
]

hilos = []
for nombre, orig, dest in viajeros:
    h = threading.Thread(target=teletransportar, args=(nombre, orig, dest), name=nombre)
    hilos.append(h)
    h.start()

for h in hilos:
    h.join()

print("\n--- Sistema de Teletransporte Finalizado ---")