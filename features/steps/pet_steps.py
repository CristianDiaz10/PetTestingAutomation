import requests  # Importa la librería para hacer peticiones HTTP
import time      # Importa la librería para manejo de esperas
from behave import given, when, then  # Importa decoradores para definir pasos en BDD

BASE_URL = "https://petstore.swagger.io/v2"  # URL base de la API
pet_id = 1234567890  # ID fijo para la mascota que usaremos en las pruebas

# Clase cliente para encapsular llamadas a la API
class PetAPIClient:
    def __init__(self):
        self.base_url = BASE_URL  # Guarda la URL base

    def create_pet(self, pet_data):
        # Hace POST para crear una mascota con los datos enviados
        return requests.post(f"{self.base_url}/pet", json=pet_data, headers={"Content-Type": "application/json"})

    def get_pet_by_id(self, pet_id):
        # Hace GET para obtener una mascota por su ID
        return requests.get(f"{self.base_url}/pet/{pet_id}", headers={"accept": "application/json"})

    def update_pet(self, pet_data):
        # Hace PUT para actualizar la mascota con nuevos datos
        return requests.put(f"{self.base_url}/pet", json=pet_data, headers={"Content-Type": "application/json"})

    def delete_pet(self, pet_id):
        # Hace DELETE para eliminar la mascota por ID
        return requests.delete(f"{self.base_url}/pet/{pet_id}", headers={"accept": "application/json"})

client = PetAPIClient()  # Instancia del cliente para usar en los pasos

# Paso Given: asegurar que la mascota con ID no existe (la elimina si está)
@given('the pet with id {pet_id:d} does not exist')
def step_impl(context, pet_id):
    response = client.get_pet_by_id(pet_id)  # Consulta si la mascota existe
    if response.status_code == 200:          # Si existe
        client.delete_pet(pet_id)             # La elimina
        time.sleep(10)                         # Espera 10 segundo para asegurar eliminación

# Paso When: crear la mascota con nombre y estado especificados
@when('I create the pet with name "{name}" and status "{status}"')
def step_impl(context, name, status):
    # Construye el JSON para crear la mascota
    pet_data = {
        "id": pet_id,
        "category": {"id": 10, "name": "Basset"},
        "name": name,
        "photoUrls": ["string"],
        "tags": [{"id": 10, "name": "Basset"}],
        "status": status
    }
    context.response = client.create_pet(pet_data)  # Llama a la API para crear la mascota
    assert context.response.status_code == 200 # Verifica que la creación fue exitosa
    time.sleep(10)

# Paso Then: verificar que la mascota existe con el nombre y estado indicados
@then('the pet with id {pet_id:d} should exist with name "{name}" and status "{status}"')
def step_impl(context, pet_id, name, status):
    max_retries = 5                      # Número máximo de intentos para verificar
    for attempt in range(max_retries):  # Bucle para reintentos
        response = client.get_pet_by_id(pet_id)  # Consulta la mascota por ID
        print(f"INTENTO {attempt+1}: STATUS: {response.status_code}")  # Imprime el intento y status
        print("BODY:", response.text)                               # Imprime el cuerpo de la respuesta

        if response.status_code == 200:  # Si la mascota fue encontrada
            data = response.json()       # Convierte respuesta JSON a dict
            print("DEBUG respuesta JSON:", data)  # Imprime datos para debug
            # Comprueba que nombre y estado coincidan con lo esperado
            if data.get("name") == name and data.get("status") == status:
                print("✅ Pet encontrada con los datos correctos")  # Mensaje de éxito
                return  # Sale del paso porque fue exitoso
        time.sleep(10)  # Espera 10 segundos antes de intentar nuevamente

    # Si agotó los intentos sin éxito, falla el test con mensaje
    assert False, f"La mascota con id {pet_id} no se encontró con name='{name}' y status='{status}' tras {max_retries} intentos"

# Paso When: actualizar la mascota con nuevo nombre y estado
@when('I update the pet with name "{name}" and status "{status}"')
def step_impl(context, name, status):
    # Construye el JSON con nuevos datos para la mascota
    pet_data = {
        "id": pet_id,
        "category": {"id": 10, "name": "Pitbull"},
        "name": name,
        "photoUrls": ["string"],
        "tags": [{"id": 10, "name": "Pitbull"}],
        "status": status
    }
    context.update_response = client.update_pet(pet_data)  # Llama a la API para actualizar
    assert context.update_response.status_code == 200     # Verifica que la actualización fue exitosa
    time.sleep(10)  # Espera 10 segundos para que la API procese el cambio

# Paso When: eliminar la mascota
@when('I delete the pet')
def step_impl(context):
    response = client.delete_pet(pet_id)       # Llama a la API para borrar la mascota
    assert response.status_code in [200, 204]  # Verifica que el borrado fue exitoso (200 o 204)
    time.sleep(10)

# Paso Then: verificar que la mascota ya no exista
@then('the pet with id {pet_id:d} should not exist')
def step_impl(context, pet_id):
    max_retries = 5                      # Número máximo de intentos para verificar borrado
    for attempt in range(max_retries):  # Bucle con reintentos
        response = client.get_pet_by_id(pet_id)  # Consulta la mascota por ID
        print(f"INTENTO {attempt+1}: STATUS: {response.status_code}")  # Imprime intento y status
        print("BODY:", response.text)                               # Imprime cuerpo de la respuesta
        if response.status_code == 404:  # Si la mascota no existe (correcto)
            print("✅ Pet no encontrada (borrada correctamente)")  # Mensaje de éxito
            return  # Sale porque se confirmó el borrado
        time.sleep(10)  # Espera 100 segundos antes de reintentar

    # Si tras varios intentos la mascota sigue existiendo, falla la prueba con mensaje informativo
    assert response.status_code == 404, (
        f"La mascota con id {pet_id} sigue existiendo después de DELETE, "
        f"estatus actual: {response.status_code}. Esto es una limitación del entorno Swagger Petstore demo."
    )