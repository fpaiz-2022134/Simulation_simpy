"""

@author: Franco Paiz 25780, Juan Carlos Espinal 251576, 04/03/2026
main.py
Punto de entrada: corre los escenarios de las tareas 1-4, imprime
las tablas de resultados y genera las gráficas.
"""

import matplotlib.pyplot as plt
from simulacion import correr_simulacion

# ─── Configuración de escenarios ──────────────────────────────────────────────

CANTIDADES  = [25, 50, 100, 150, 200]
INTERVALOS  = [10, 5, 1]

ESTRATEGIAS = {
    'Base (RAM=100, 1 CPU, 3 instr)': dict(ram_capacity=100, cpu_capacity=1, instrucciones_por_tick=3),
    'RAM=200':                         dict(ram_capacity=200, cpu_capacity=1, instrucciones_por_tick=3),
    'CPU rápido (6 instr)':           dict(ram_capacity=100, cpu_capacity=1, instrucciones_por_tick=6),
    '2 CPUs':                          dict(ram_capacity=100, cpu_capacity=2, instrucciones_por_tick=3),
}

# ─── Helpers de presentación ──────────────────────────────────────────────────

def imprimir_tabla_intervalos(res_intervalos):
    print("=" * 60)
    print("Tareas 1 y 2 — Variación de intervalo de llegada")
    print("=" * 60)
    for interval in INTERVALOS:
        print(f"\nIntervalo = {interval}")
        print(f"{'Procesos':>10}  {'Promedio':>10}  {'Desv. Est.':>10}")
        for n in CANTIDADES:
            m, s = res_intervalos[interval][n]
            print(f"{n:>10}  {m:>10.2f}  {s:>10.2f}")


def imprimir_tabla_estrategias(res_estrategias):
    print("\n" + "=" * 60)
    print("Tareas 3 y 4 — Estrategias de optimización")
    print("=" * 60)
    for label, datos in res_estrategias.items():
        print(f"\n{label}")
        print(f"{'Procesos':>10}  {'int=10':>10}  {'int=5':>10}  {'int=1':>10}")
        for n in CANTIDADES:
            row = datos[n]
            print(f"{n:>10}  {row[10]:>10.2f}  {row[5]:>10.2f}  {row[1]:>10.2f}")


def imprimir_resumen(res_estrategias):
    print("\n" + "=" * 60)
    print("Resumen final — 200 procesos, intervalo=10")
    print("=" * 60)
    for label, datos in res_estrategias.items():
        m = datos[200][10]
        print(f"  {label:<35}  promedio={m:.2f}")
    print("""
Conclusión:
  Aumentar la velocidad del CPU (6 instrucciones/tick) es la estrategia
  más efectiva. Reduce cuántas veces cada proceso compite por el procesador,
  mejorando el tiempo en todos los escenarios de carga. Aumentar la RAM ayuda
  cuando muchos procesos esperan memoria, pero pierde impacto cuando el cuello
  de botella es el CPU. Usar 2 CPUs mejora el rendimiento pero de forma menos
  consistente que doblar la velocidad de ejecución por tick.
    """)

# ─── Recolección de resultados ────────────────────────────────────────────────

def recolectar_intervalos():
    """Corre tareas 1 y 2: distintos intervalos de llegada, configuración base."""
    res = {}
    for interval in INTERVALOS:
        res[interval] = {}
        for n in CANTIDADES:
            res[interval][n] = correr_simulacion(n, interval=interval)
    return res


def recolectar_estrategias():
    """Corre tareas 3 y 4: estrategias de optimización cruzadas con intervalos."""
    res = {}
    for label, params in ESTRATEGIAS.items():
        res[label] = {}
        for n in CANTIDADES:
            res[label][n] = {}
            for interval in INTERVALOS:
                m, _ = correr_simulacion(n, interval=interval, **params)
                res[label][n][interval] = m
    return res

# ─── Gráficas ─────────────────────────────────────────────────────────────────

COLORES_INT  = ['steelblue', 'tomato', 'seagreen']
MARKERS_INT  = ['o', 's', '^']
COLORES_EST  = ['steelblue', 'tomato', 'seagreen', 'darkorchid']
MARKERS_EST  = ['o', 's', '^', 'D']


def grafica_intervalos(res_intervalos, guardar_como='grafica_intervalos.png'):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    fig.suptitle('Variación de intervalo de llegada', fontsize=13)

    for i, interval in enumerate(INTERVALOS):
        datos = res_intervalos[interval]
        promedios = [datos[n][0] for n in CANTIDADES]
        desvs     = [datos[n][1] for n in CANTIDADES]
        kw = dict(marker=MARKERS_INT[i], color=COLORES_INT[i],
                  label=f'Intervalo={interval}', linewidth=1.8)
        axes[0].plot(CANTIDADES, promedios, **kw)
        axes[1].plot(CANTIDADES, desvs,     **kw)

    for ax, titulo in zip(axes, ['Tiempo promedio', 'Desviación estándar']):
        ax.set_xlabel('Número de procesos')
        ax.set_ylabel('Tiempo')
        ax.set_title(titulo)
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(guardar_como, dpi=150)
    plt.show()
    print(f"Gráfica guardada: {guardar_como}")


def grafica_estrategias(res_estrategias, guardar_como='grafica_estrategias.png'):
    fig, axes = plt.subplots(1, 3, figsize=(17, 5))
    fig.suptitle('Estrategias de optimización por intervalo de llegada', fontsize=13)

    for ax_idx, interval in enumerate(INTERVALOS):
        ax = axes[ax_idx]
        for i, label in enumerate(ESTRATEGIAS):
            promedios = [res_estrategias[label][n][interval] for n in CANTIDADES]
            ax.plot(CANTIDADES, promedios, marker=MARKERS_EST[i], color=COLORES_EST[i],
                    label=label, linewidth=1.8)
        ax.set_title(f'Intervalo = {interval}')
        ax.set_xlabel('Número de procesos')
        ax.set_ylabel('Tiempo promedio')
        ax.legend(fontsize=7.5)
        ax.grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig(guardar_como, dpi=150)
    plt.show()
    print(f"Gráfica guardada: {guardar_como}")

# ─── Main ─────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # Recolectar datos
    res_intervalos  = recolectar_intervalos()
    res_estrategias = recolectar_estrategias()

    # Imprimir tablas
    imprimir_tabla_intervalos(res_intervalos)
    imprimir_tabla_estrategias(res_estrategias)
    imprimir_resumen(res_estrategias)

    # Generar gráficas
    grafica_intervalos(res_intervalos)
    grafica_estrategias(res_estrategias)
