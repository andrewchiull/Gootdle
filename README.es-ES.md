

# Google-HPS-2023-Team8
Un proyecto creado por el Equipo 8 del Programa de Sprint de Producto de Hardware (HPS) de Google 2023.

- [Pruebas del Sistema](#system-testing)
    - [Requisitos Previos](#prerequisite)
        - [Arduino](#arduino)
        - [Raspberry Pi](#raspberry-pi)

## Pruebas del Sistema

### Requisitos Previos

#### Arduino

1. Use el IDE de Arduino para cargar `./src/arduino/main/main.ino`.
2. Sensor de fuerza: `PIN A1-A5`.
3. Tira de LEDs: `PIN 6`.


#### Raspberry Pi

1. Abra la Terminal/PowerShell.
2. `cd` (cambiar directorio) al directorio del proyecto.
    ```sh
    cd [your_path]/Google-HPS-2023-Team8
    ```
3. Use `ls` (listar) para verificar que se encuentra en el lugar correcto. (Para más información, use `ls -al`) La terminal debería mostrar algo como esto:
    ```sh
    (...)
    -rw-r--r--    1 andrewchiu  staff  1068 Jul 21 04:28 LICENSE
    -rw-r--r--    1 andrewchiu  staff   660 Aug 20 08:53 README.md
    (...)
    ```
4. Actualice el proyecto mediante `git`.
    1. Verifique el estado de git mediante
        ```sh
        git status
        ```
    2. La terminal debería mostrar algo como esto:
        ```sh
        (...)
        nothing to commit, working tree clean
        ```

        > Si indica `no changes added to commit (use "git add" and/or "git commit -a")`, primero confirme o descarte los cambios.
    3. realice `pull` desde el remoto
        ```sh
        git pull
        ```
        > Si aparecen algunas advertencias o errores, comuníquese con Andrew.

5. Use Python para ejecutar las pruebas.
    ```sh
    python3 ./tests/[test_name].py
    ```
