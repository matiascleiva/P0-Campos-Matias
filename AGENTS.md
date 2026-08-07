# AGENTS.md — Instrucciones para OpenCode

## Propósito del proyecto

Implementar `mimatmul`, una función propia de multiplicación de matrices en
Python puro, y compararla con `numpy.matmul` en un benchmark simple. P0E1
configura el ambiente; P0E2 completa benchmark, datos, gráfico y
documentación.

## Reglas de trabajo

- Mantener el código sencillo y legible. No añadir complejidad innecesaria.
- No inventar mediciones ni datos. Todo resultado debe provenir de
  ejecuciones reales en la máquina del estudiante.
- No ejecutar comandos destructivos de Git (p. ej. `push --force`,
  `reset --hard` que borre trabajo, `branch -D` sin confirmar).
- No subir credenciales, tokens ni archivos de configuración con secretos.
- Ejecutar las pruebas después de modificar código:

  ```bash
  .venv\Scripts\python.exe -m pytest
  ```

  (o `source .venv/bin/activate && python -m pytest` en Linux/macOS).

- Usar el ambiente virtual `.venv`; nunca instalar dependencias de forma
  global.
- Al agregar dependencias, actualizar `requirements.txt`.
