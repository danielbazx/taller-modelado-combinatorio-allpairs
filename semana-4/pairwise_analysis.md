# Taller Autónomo: Modelado Combinatorio y All-Pairs (Pairwise Testing)

**Curso:** Calidad y Pruebas de Software  
**Clase:** 09 - Bloque 2 | Ejecución Autónoma  
**Caso de Estudio:** Configurador Web Global — *SmartDrive Motors*  
**Fecha:** Octubre 2026  
**Rama Git:** `main`  

---

## Portada y Asignación de Roles Tácticos

| Integrante | Rol Táctico Asignado | Responsabilidades Principales |
| :--- | :--- | :--- |
| **Daniel Cadena** | **Analista de Modelado** | Liderazgo en la abstracción de requerimientos del configurador vehicular, estructuración formal de variables discretas y matriz de restricciones lógicas (constraints). |
| **Gonzalo Cárdenas** | **Tester Combinatorio** | Dirección del cálculo matemático de la explosión combinatoria, modelado de cobertura pairwise ($t=2$) y derivación algorítmica de la suite ortogonal reducida. |
| **Gabriel Vasquez** | **Documentador / Git Lead** | Control del time-box de la sesión (Scrum Master), consolidación técnica de la documentación en Markdown, verificación del protocolo pre-commit y gestión de ramas/commits en Git. |

---

## 1. Contexto Operativo y Misión de Ingeniería

*SmartDrive Motors* se prepara para el lanzamiento global de su configurador web de vehículos de última generación. Los clientes finales pueden personalizar múltiples subsistemas críticos: motorización, transmisión, sistema de frenado, mercado geográfico de homologación y modos de asistencia a la conducción.

> **Riesgo Crítico de Negocio:**  
> Un fallo de compatibilidad o colisión lógica entre componentes que llegue a producción paralizará la línea de ensamblaje o generará entregas defectuosas, ocasionando pérdidas millonarias, recalls regulatorios y daño reputacional severo.  
> **Objetivo:** Diseñar una suite de pruebas combinatorias de máxima eficacia que garantice **cero fallos lógicos de compatibilidad**, optimizando drásticamente los recursos y tiempos de ejecución mediante la metodología **All-Pairs (Pairwise Testing)** respaldada por los estándares del NIST.

---

## 2. Paso 1: Matriz de Parámetros y Valores (P&V)

A partir del análisis de requerimientos del configurador de *SmartDrive Motors*, se abstraen los subsistemas configurables en variables discretas bien delimitadas.

### Tabla Formal de Parámetros y Valores (P&V)

| ID | Parámetro (P) | Descripción del Subsistema | Valores Discretos ($V$) | Cantidad ($n$) |
| :---: | :--- | :--- | :--- | :---: |
| **P1** | **Motor** | Tren motriz del vehículo | `Gasolina`, `Híbrido`, `Eléctrico` | 3 |
| **P2** | **Transmisión** | Sistema de caja de velocidades | `Manual`, `Automática`, `Monomarcha` | 3 |
| **P3** | **Frenos** | Tecnología de frenado y deceleración | `Estándar`, `ABS`, `Regenerativo` | 3 |
| **P4** | **Mercado** | Región geográfica y normativa | `América`, `Europa`, `Asia` | 3 |
| **P5** | **Modo** | Perfil electrónico de conducción | `Eco`, `Sport`, `Autónomo` | 3 |

*Total de parámetros discretos:* $N = 5$  
*Cardinalidad por parámetro:* $k_i = 3 \quad \forall i \in \{1, \dots, 5\}$

---

## 3. Paso 2: El Peligro de la Explosión Combinatoria

### 3.1 Demostración Matemática del Espacio Exhaustivo

De acuerdo con el **Principio Fundamental del Conteo (Regla del Producto)**, el número total de combinaciones puras posibles en un sistema de $N$ parámetros independientes con $v_i$ valores discretos viene dado por:

$$\text{Espacio de Estados Exhaustivo} = \prod_{i=1}^{N} v_i = v_1 \times v_2 \times v_3 \times v_4 \times v_5$$

Sustituyendo los valores del configurador de *SmartDrive Motors*:

$$3^5 = 3 \times 3 \times 3 \times 3 \times 3 = 243 \text{ configuraciones totales}$$

### 3.2 Análisis de Viabilidad Operativa y Financiera

Si el equipo de QA decide ejecutar una estrategia de prueba exhaustiva (brute-force testing):
* **Tiempo promedio por prueba:** $15 \text{ minutos}$ (incluye aprovisionamiento de configuración en el simulador/banco de pruebas, ejecución de pruebas de integración de la ECU y verificación del checklist de telemetría).

$$\text{Tiempo Total de Ejecución} = 243 \text{ pruebas} \times 15 \text{ min/prueba} = 3,645 \text{ minutos}$$

$$\text{Horas de Ingeniería} = \frac{3,645 \text{ min}}{60 \text{ min/h}} = 60.75 \text{ horas netas}$$

Asumiendo una jornada laboral estándar de desarrollo de software de $8 \text{ horas/día}$:

$$\text{Días Laborables Requeridos} = \frac{60.75 \text{ horas}}{8 \text{ horas/día}} \approx 7.59 \text{ días laborables completos}$$

```
+-----------------------------------------------------------------------------------------+
|                                DEBATE DE EQUIPO Y CONCLUSIÓN                            |
+-----------------------------------------------------------------------------------------+
| Conclusión: Probar exhaustivamente las 243 combinaciones es financieramente inviable y  |
| operacionalmente ineficiente, pues consumiría casi dos semanas de trabajo dedicadas a   |
| un solo tester por cada versión o ciclo de release, disparando los costos de testing,   |
| retrasando el time-to-market y provocando fatiga cognitiva humana que aumenta la tasa   |
| de errores no detectados.                                                               |
+-----------------------------------------------------------------------------------------+
```

---

## 4. Fundamentación Teórica: La Solución NIST y el Embudo Pairwise ($t=2$)

Los estudios empíricos desarrollados por el **NIST (National Institute of Standards and Technology)** en software crítico industrial demuestran que:
* Entre el **70% y el 90%** de los defectos de software son provocados por la interacción de **a lo sumo dos parámetros simultáneos** (fallos de orden $t=1$ y $t=2$).
* Los defectos derivados de interacciones de orden superior ($t \ge 3$) son extremadamente infrecuentes y habitualmente se manifiestan de manera predecible si los pares subyacentes han sido evaluados.

### Cálculo de Pares Teóricos Únicos a Cubrir

El número de pares de parámetros a evaluar en un sistema de 5 variables es la combinación de 5 tomados de 2 en 2:

$$\binom{N}{2} = \binom{5}{2} = \frac{5 \times 4}{2} = 10 \text{ pares de parámetros}$$

Dado que cada parámetro tiene 3 valores discretos, cada par de parámetros posee $3 \times 3 = 9$ interacciones posibles. Por lo tanto, el universo de pares que se debe garantizar es:

$$\text{Total de Pares Únicos} = 10 \times 9 = 90 \text{ pares}$$

Al aplicar el **filtro ortogonal All-Pairs**, el espacio de prueba se comprime de **243 combinaciones exhaustivas a tan solo 15 casos de prueba**, logrando el **100% de cobertura de pares ($t=2$)** con una **reducción del 93.8%** en el esfuerzo de ejecución.

---

## 5. Paso 3: Derivación de la Suite All-Pairs (Pura / Sin Restricciones)

Utilizando algoritmos heurísticos ortogonales (implementados formalmente a través de la librería `allpairspy` en `src/generate_allpairs.py`), se derivó la siguiente suite mínima óptima de **15 casos de prueba**:

### Suite Reducida All-Pairs ($t=2$)

| Test Case | Motor | Transmisión | Frenos | Mercado | Modo |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **TC-01** | Gasolina | Manual | Estándar | América | Eco |
| **TC-02** | Híbrido | Automática | ABS | Europa | Eco |
| **TC-03** | Eléctrico | Monomarcha | Regenerativo | Asia | Eco |
| **TC-04** | Eléctrico | Automática | Estándar | Asia | Sport |
| **TC-05** | Híbrido | Manual | Regenerativo | Europa | Sport |
| **TC-06** | Gasolina | Monomarcha | ABS | América | Sport |
| **TC-07** | Gasolina | Automática | Regenerativo | América | Autónomo |
| **TC-08** | Híbrido | Monomarcha | Estándar | Europa | Autónomo |
| **TC-09** | Eléctrico | Manual | ABS | Asia | Autónomo |
| **TC-10** | Eléctrico | Manual | ABS | Europa | Autónomo |
| **TC-11** | Híbrido | Manual | ABS | América | Autónomo |
| **TC-12** | Gasolina | Manual | ABS | Europa | Autónomo |
| **TC-13** | Gasolina | Manual | ABS | Asia | Autónomo |
| **TC-14** | Híbrido | Manual | ABS | Asia | Autónomo |
| **TC-15** | Eléctrico | Manual | ABS | América | Autónomo |

### 5.1 Comprobación de Ortogonalidad y Cobertura

Se verificaron las **10 parejas de columnas** posibles mediante el script automatizado. Para ilustrar la ortogonalidad, tomamos dos columnas al azar:

#### Comprobación 1: `Motor` vs `Transmisión` ($3 \times 3 = 9$ combinaciones)
1. `(Gasolina, Manual)` $\rightarrow$ Presente en TC-01, TC-12, TC-13.
2. `(Gasolina, Automática)` $\rightarrow$ Presente en TC-07.
3. `(Gasolina, Monomarcha)` $\rightarrow$ Presente en TC-06.
4. `(Híbrido, Manual)` $\rightarrow$ Presente en TC-05, TC-11, TC-14.
5. `(Híbrido, Automática)` $\rightarrow$ Presente en TC-02.
6. `(Híbrido, Monomarcha)` $\rightarrow$ Presente en TC-08.
7. `(Eléctrico, Manual)` $\rightarrow$ Presente en TC-09, TC-10, TC-15.
8. `(Eléctrico, Automática)` $\rightarrow$ Presente en TC-04.
9. `(Eléctrico, Monomarcha)` $\rightarrow$ Presente en TC-03.
*Resultado:* **9 de 9 pares cubiertos (100%)**.

#### Comprobación 2: `Frenos` vs `Modo` ($3 \times 3 = 9$ combinaciones)
1. `(Estándar, Eco)` $\rightarrow$ Presente en TC-01.
2. `(ABS, Eco)` $\rightarrow$ Presente en TC-02.
3. `(Regenerativo, Eco)` $\rightarrow$ Presente en TC-03.
4. `(Estándar, Sport)` $\rightarrow$ Presente en TC-04.
5. `(ABS, Sport)` $\rightarrow$ Presente en TC-06.
6. `(Regenerativo, Sport)` $\rightarrow$ Presente en TC-05.
7. `(Estándar, Autónomo)` $\rightarrow$ Presente en TC-08.
8. `(ABS, Autónomo)` $\rightarrow$ Presente en TC-09, TC-10, TC-11, TC-12, TC-13, TC-14, TC-15.
9. `(Regenerativo, Autónomo)` $\rightarrow$ Presente en TC-07.
*Resultado:* **9 de 9 pares cubiertos (100%)**.

---

## 6. Paso 4: Alerta de Sistema e Identificación de Constraints (Restricciones Lógicas)

> **Alerta de Ingeniería:**  
> Las matemáticas generan combinaciones ortogonales puras, pero los vehículos físicos obedecen a restricciones mecánicas, electrónicas y normativas reales. Por ejemplo, intentar emparejar un motor de gasolina convencional con un freno regenerativo sin hibridación destruirá la coherencia del sistema y detendría la línea de ensamblaje.

Para modelar la realidad operativa del configurador, definimos las siguientes reglas de negocio en **lógica formal** y **seudocódigo**:

### Regla 1: Restricción del Tren Motriz Eléctrico
* **Lógica Formal:**  
  $$\text{Motor} = \text{Eléctrico} \implies (\text{Transmisión} = \text{Monomarcha}) \land (\text{Frenos} = \text{Regenerativo})$$
* **Seudocódigo:**
```pseudo
RULE R1_Electrico_Architecture
    IF Motor == "Eléctrico" THEN
        ASSERT Transmisión == "Monomarcha" 
            ERROR "Un vehículo eléctrico 100% no admite cajas manuales o automáticas multietapa convencionales"
        ASSERT Frenos == "Regenerativo" 
            ERROR "El tren motriz eléctrico exige sistema de recuperación de energía cinética (frenado regenerativo)"
    END IF
END RULE
```

### Regla 2: Exclusión de Regeneración en Motor de Gasolina Pura
* **Lógica Formal:**  
  $$\text{Motor} = \text{Gasolina} \implies \text{Frenos} \neq \text{Regenerativo}$$
* **Seudocódigo:**
```pseudo
RULE R2_Gasolina_No_Regenerativo
    IF Motor == "Gasolina" THEN
        ASSERT Frenos != "Regenerativo" 
            ERROR "Incompatibilidad técnica: Los motores de combustión pura carecen de batería de tracción o inversor para almacenar energía regenerada"
    END IF
END RULE
```

### Regla 3: Incompatibilidad Mecánica de Motor Gasolina con Transmisión Monomarcha
* **Lógica Formal:**  
  $$\text{Motor} = \text{Gasolina} \implies \text{Transmisión} \neq \text{Monomarcha}$$
* **Seudocódigo:**
```pseudo
RULE R3_Gasolina_Requires_Gears
    IF Motor == "Gasolina" THEN
        ASSERT Transmisión != "Monomarcha"
            ERROR "Un motor de combustión interna requiere relaciones de marcha variables (Manual o Automática) para operar dentro de su curva de torque"
    END IF
END RULE
```

### Regla 4: Conducción Autónoma Segura (Control Drive-by-Wire)
* **Lógica Formal:**  
  $$\text{Modo} = \text{Autónomo} \implies (\text{Transmisión} \neq \text{Manual}) \land (\text{Frenos} \neq \text{Estándar})$$
* **Seudocódigo:**
```pseudo
RULE R4_Autonomous_Drive_Requirements
    IF Modo == "Autónomo" THEN
        ASSERT Transmisión != "Manual"
            ERROR "La conducción autónoma no es compatible con transmisión manual al carecer de actuador robotizado de embrague"
        ASSERT Frenos != "Estándar"
            ERROR "El piloto autónomo requiere actuadores electrónicos de frenado antibloqueo inteligente (ABS o Regenerativo) para el frenado autónomo de emergencia"
    END IF
END RULE
```

### Suite de Pruebas All-Pairs con Constraints Aplicados

Al alimentar el motor de derivación All-Pairs con estas reglas de exclusión lógicas, se eliminan los casos físicamente imposibles, generando una suite de producción de **9 casos de prueba válidos y ejecutables**:

| Test Case | Motor | Transmisión | Frenos | Mercado | Modo | Justificación de Viabilidad |
| :---: | :--- | :--- | :--- | :--- | :--- | :--- |
| **TC-C01** | Gasolina | Manual | Estándar | América | Eco | Configuración de entrada básica a combustión |
| **TC-C02** | Híbrido | Automática | ABS | Europa | Eco | Configuración híbrida estándar para ciudad |
| **TC-C03** | Eléctrico | Monomarcha | Regenerativo | Asia | Eco | Vehículo eléctrico urbano de alta eficiencia |
| **TC-C04** | Eléctrico | Monomarcha | Regenerativo | Europa | Sport | Configuración eléctrica de alto rendimiento |
| **TC-C05** | Híbrido | Manual | Regenerativo | América | Sport | Configuración híbrida deportiva con caja manual |
| **TC-C06** | Gasolina | Automática | ABS | Asia | Sport | Vehículo convencional de carretera con caja automática |
| **TC-C07** | Eléctrico | Monomarcha | Regenerativo | América | Autónomo | Flota autónoma eléctrica para transporte homologado |
| **TC-C08** | Eléctrico | Monomarcha | Regenerativo | Asia | Autónomo | Homologación autónoma para mercado asiático |
| **TC-C09** | Eléctrico | Monomarcha | Regenerativo | Europa | Autónomo | Cumplimiento regulatorio autónomo para mercado europeo |

---

## 7. Paso 5: Protocolo Pre-Commit (Autoevaluación de Calidad)

El equipo ha verificado exhaustivamente el cumplimiento de los cuatro pilares del taller previo al commit:

- [x] **¿La Matriz P&V define los 5 parámetros y sus variables discretas?**  
  *Sí.* Se han definido con rigor técnico: `Motor (3)`, `Transmisión (3)`, `Frenos (3)`, `Mercado (3)` y `Modo (3)`.
- [x] **¿Se calculó y justificó el límite de la explosión combinatoria ($3^5$)?**  
  *Sí.* Se demostró matemáticamente el espacio de 243 estados y se acreditó que requeriría 60.75 horas hombre (7.6 días laborables), demostrando su inviabilidad financiera.
- [x] **¿La suite All-Pairs fue generada y listada correctamente?**  
  *Sí.* Se generó la suite de 15 pruebas cubriendo el 100% de los 90 pares posibles, validada estadísticamente en sus 10 combinaciones inter-columnares.
- [x] **¿Las reglas formales de exclusión (Constraints) reflejan el caso de negocio?**  
  *Sí.* Se formalizaron 4 reglas en lógica matemática y seudocódigo que impiden colisiones físicas en planta de ensamblaje y garantizan la viabilidad operativa.

---

## 8. Paso 6: Cierre Cognitivo (Preguntas de Transferencia)

### Pregunta 1 (Transferencia)
> *¿Qué riesgo financiero y operativo corremos si ignoramos los constraints lógicos y enviamos la matriz matemática pura directamente al equipo de automatización (QA)?*

**Respuesta Técnica:**  
Enviar la matriz matemática no filtrada introduce una distorsión operativa inmediata: se instruye a los scripts de automatización a instanciar combinaciones que el backend o la planta de manufactura rechazarán por diseño (como acoplar un motor a gasolina con frenado regenerativo o un piloto autónomo con caja manual). Operativamente, esto satura el tablero de incidentes con falsos positivos (*falsos bugs*), desperdiciando costosas horas de ingeniería de desarrollo y QA en investigar anomalías que no son defectos de software, sino violaciones de dominio físico. Financieramente, este ruido degrada la confianza en el pipeline de Integración Continua (CI/CD), ralentiza el despliegue del configurador y puede provocar que, ante la presión de los plazos de entrega, se silencien alertas de error legítimas, permitiendo que configuraciones erróneas lleguen a la fábrica y generen pérdidas millonarias en líneas de montaje detenidas o pedidos de clientes no fabricables.

### Pregunta 2 (Elaboración)
> *¿Por qué la técnica All-Pairs es matemáticamente y empíricamente superior a que un tester diseñe 20 casos de prueba basándose únicamente en su intuición?*

**Respuesta Técnica:**  
La intuición humana está sujeta a sesgos cognitivos documentados (principalmente el *sesgo de confirmación* y la concentración en los *caminos felices* o combinaciones que el tester considera "típicas"), lo cual deja sistemáticamente desatendidas combinaciones cruzadas periféricas donde estadísticamente anidan los defectos más severos. Mientras que 20 casos diseñados intuitivamente pueden repetir redundantemente los mismos pares habituales y omitir más del 40% de las interacciones cruzadas posibles, la técnica All-Pairs ofrece una garantía matemática formal: asegura que **el 100% de los pares de interacción ($t=2$) están representados** con el menor número posible de filas mediante matrices ortogonales. Empíricamente, la literatura y los estudios de referencia del NIST demuestran que entre el 70% y el 90% de las fallas en sistemas complejos son detonadas por la interacción de un máximo de 2 parámetros; por ende, All-Pairs maximiza la densidad de detección de defectos por hora invertida, convirtiendo la prueba en un proceso científico, auditable, determinista y repetible.

---

## 9. Instrucciones de Ejecución y Reproducibilidad

El repositorio contiene el script ejecutable para reproducir la generación y validación de cobertura:

```bash
# Ejecutar generador y validador de cobertura All-Pairs
python src/generate_allpairs.py
```
