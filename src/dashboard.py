def run_completa():
    bonus_count = 0
    inicio_run = time.time()

    # Verificar menu
    log("Verificando menu...")
    for _ in range(5):
        estado = detectar_pantalla()
        if estado == 'menu':
            break
        time.sleep(2)
    else:
        log("No detecto menu, volviendo atras...")
        subprocess.run(["adb", "shell", "input", "keyevent", "4"],
                       capture_output=True)
        time.sleep(3)
        registrar_run(False, time.time() - inicio_run, bonus_count)
        return False

    log("Tocando JR Normal...")
    tap(*COORDS['jr_normal'])
    time.sleep(3)

    log("Esperando pantalla monstruos...")
    for _ in range(10):
        estado = detectar_pantalla()
        if estado == 'monstruos':
            log("Confirmando monstruos...")
            tap(*COORDS['confirmar'])
            time.sleep(3)
            break
        time.sleep(1)

    log("Run iniciada...")
    inicio = time.time()
    tiempo_max = 25 * 60

    while time.time() - inicio < tiempo_max:
        estado = detectar_pantalla()

        if estado == 'continua':
            log("Run completada! Tocando Continua...")
            tap(*COORDS['continua'])
            time.sleep(3)
            registrar_run(True, time.time() - inicio_run, bonus_count)
            return True

        elif estado == 'bonus':
            bonus_count += 1
            log(f"Bonus #{bonus_count} detectado! Tocando Recompensa Gratis...")
            tap(*COORDS['recompensa'])
            log("Esperando anuncio...")
            for _ in range(60):
                time.sleep(1)
                estado_inner = detectar_pantalla()
                if estado_inner == 'recibiste':
                    break

        elif estado == 'recibiste':
            log("Recibiste! Tocando Aceptar...")
            tap(*COORDS['aceptar'])
            time.sleep(2)

        elif estado == 'menu':
            log("Volvio al menu inesperadamente")
            registrar_run(False, time.time() - inicio_run, bonus_count)
            return False

        elif estado == 'jugando':
            time.sleep(3)

        else:
            time.sleep(2)

    log("Run excedio 25 minutos")
    registrar_run(False, time.time() - inicio_run, bonus_count)
    return False