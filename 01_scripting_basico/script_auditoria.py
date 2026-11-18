import requests #hacer peticiones 
import json #devuelve el formato json 
from requests.auth import HTTPBasicAuth #mandar un usuario y contraseña 

# Deshabilitar advertencias de certificados SSL autofirmados
requests.packages.urllib3.disable_warnings()

# 1. Parámetros de la API RESTCONF


url = "https://sandbox-iosxe-latest-1.cisco.com/restconf/data/ietf-interfaces:interfaces"   # opción sandbox direccion a la que voy a acudir 
headers = { #soluciones extras a la pregunta que yo haga 
    "Accept": "application/yang-data+json", #quiere su respuesta en JSON 
    "Content-Type": "application/yang-data+json" # en que formato lo mando yo 
}
auth = HTTPBasicAuth("developer", "C1sco12345!")   # guarda el usuario y la contraseña y se la muestra al router 

# ruta del archivo de salida, junto al script 
archivo = "inventario_interfaces.json" #archivo donde se guardaran los datos 

try: #intentar hacer esto 
    # 2. Petición GET HTTP
    print(f"consultando la APi") #muestra el texto para ver que el programa arranco 
    response = requests.get( #conexion en get como si le pidiera algo al router y este guarda su respuesta en response
        url, #a donde pregunto 
        headers=headers, 
        auth=auth, #usuario y contraseña 
        verify=False,  # certificado de seguridad 
        timeout=10     #  espera 
    )

    # 3. Validación del código de respuesta
    if response.status_code == 200: #todo bien 
        data = response.json() #la respuesta llega en formato texto lo guarda en data 
        interfaces = data["ietf-interfaces:interfaces"]["interface"] #lista de todas las interfaces y las guarda en interfaces 
        
        print(f"{'Nombre':<20} {'Tipo':<30} {'Habilitada':<10}") #imprime los titulos el ancho de la tabla para que quede alineada 
        print("-" * 60) #linea de 60 giones para la separacion 
        for iface in interfaces: #ciclo para que cada interfaz realice lo siguiente cuando ya este lista 
            name = iface.get("name", "N/A") #nombre de la interfaz y sino existe es n/a
            if_type = iface.get("type", "N/A") #lo mismo para el tipo
            enabled = iface.get("enabled", False) #si esta prendida y sino es false 
            print(f"{name:<20} {if_type:<30} {str(enabled):<10}") #fila con los saltos 

        # NUEVO: quedarse solo con las interfaces activas que tienen IP
        activas = [] #crea una lista vacia 
        for iface in interfaces: #otra vez la crea pero para cada interfaz lista 
            direcciones = iface.get("ietf-ip:ipv4", {}).get("address", []) #busca las direcciones ip de esa interfaz 
            if iface.get("enabled", False) and direcciones: #si esta encendida y tiene direcciones 
                activas.append({ #agrega a la lista 
                    "nombre": iface["name"], #el nombre de la interfaz 
                    "ip": direcciones[0]["ip"], # la primera de la lista 
                    "mascara": direcciones[0]["netmask"] #mascara de red 
                })

       
except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")
