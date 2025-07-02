Feature: Pet lifecycle management
  # Define la funcionalidad general que se va a probar: gestión del ciclo de vida de una mascota.

  Scenario: Create, verify, update, verify and delete a pet
    # Describe un caso de prueba específico donde se crea, verifica, actualiza, verifica y elimina una mascota.
    Given the pet with id 1234567890 does not exist
      # Asegura que no existe una mascota con ese ID antes de iniciar la prueba (precondición).
      # Si existiera, el sistema debería eliminarla o limpiar ese estado.
    When I create the pet with name "Arnold" and status "available"
      # Acción para crear una mascota con nombre "Arnold" y estado "available" (disponible).
    Then the pet with id 1234567890 should exist with name "Arnold" and status "available"
      # Verifica que la mascota fue creada correctamente con el ID, nombre y estado indicados.
    When I update the pet with name "Mora" and status "pending"
      # Acción para actualizar la mascota existente, cambiando su nombre a "Mora" y estado a "pending" (pendiente).
    Then the pet with id 1234567890 should exist with name "Mora" and status "pending"
      # Verifica que la mascota fue actualizada correctamente con los nuevos datos.
    When I delete the pet
      # Acción para eliminar la mascota del sistema.
    Then the pet with id 1234567890 should not exist
      # Verifica que la mascota ya no existe después de la eliminación.