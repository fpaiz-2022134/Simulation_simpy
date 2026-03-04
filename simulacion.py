"""
@author: Franco Paiz 25780, Juan Carlos Espinal 251576, 04/03/2026

simulacion.py
Contiene la lógica de simulación: modelo del proceso, generador de llegadas
y la función principal para correr un escenario.
"""

import simpy
import random
import statistics

RANDOM_SEED = 42
# unidades de tiempo por tick del CPU
CPU_SPEED = 1  

def proceso(env, ram, cpu, instrucciones_por_tick, tiempos):
    """Ciclo de vida de un proceso: new -> ready -> running -> (waiting) -> terminated."""
    llegada = env.now
    memoria = random.randint(1, 10)
    instrucciones = random.randint(1, 10)

    # Estado new: solicitar memoria RAM
    yield ram.get(memoria)

    # Estados ready / running: competir por CPU hasta terminar instrucciones
    while instrucciones > 0:
        with cpu.request() as req:
            yield req
            ejecutar = min(instrucciones, instrucciones_por_tick)
            yield env.timeout(CPU_SPEED)
            instrucciones -= ejecutar

        if instrucciones <= 0:
             # terminated
            break 

        decision = random.randint(1, 21)
        if decision == 1:
            # Estado waiting: operación de I/O, luego regresa a ready
            yield env.timeout(random.randint(1, 5))
        # Cualquier otro valor: regresa a ready directamente

    # Libera memoria al terminar
    ram.put(memoria)
    tiempos.append(env.now - llegada)


def generador(env, num_procesos, ram, cpu, instrucciones_por_tick, interval, tiempos):
    """Genera procesos con distribución exponencial de llegadas."""
    for _ in range(num_procesos):
        env.process(proceso(env, ram, cpu, instrucciones_por_tick, tiempos))
        yield env.timeout(random.expovariate(1.0 / interval))


def correr_simulacion(num_procesos, interval=10, ram_capacity=100,
                      cpu_capacity=1, instrucciones_por_tick=3):
    """
    Ejecuta un escenario de simulación completo.

    Parámetros:
        num_procesos        -- cantidad de procesos a simular
        interval            -- intervalo promedio de llegada (distribución exponencial)
        ram_capacity        -- capacidad total de memoria RAM
        cpu_capacity        -- número de CPUs disponibles
        instrucciones_por_tick -- instrucciones que ejecuta el CPU por tick

    Retorna:
        (promedio, desviacion_estandar) de los tiempos en el sistema
    """
    random.seed(RANDOM_SEED)
    env = simpy.Environment()
    ram = simpy.Container(env, init=ram_capacity, capacity=ram_capacity)
    cpu = simpy.Resource(env, capacity=cpu_capacity)
    tiempos = []

    env.process(generador(env, num_procesos, ram, cpu,
                          instrucciones_por_tick, interval, tiempos))
    env.run()

    promedio = statistics.mean(tiempos)
    desv = statistics.stdev(tiempos) if len(tiempos) > 1 else 0.0
    return promedio, desv
