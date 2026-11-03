# Resumen 2do parcial — Análisis y Diseño de Sistemas II

Docente: María Silvina Scarpin. Grupo: Figún, Morales, Haunau. Tecnicatura en Análisis y Desarrollo de Software, Instituto de Profesorado Sedes Sapientiae.

---

## 1. Redes de Petri (Temas 6 y 7)

> **En una frase:** una Red de Petri es un **modelo gráfico y matemático** que muestra cómo funciona un sistema en el que **pasan varias cosas a la vez**.

### 1.1 Qué son, de dónde vienen y para qué sirven

- **Definición del resumen de cátedra**: las **redes de Petri (RdP)** son representaciones **gráficas** que permiten modelar **sistemas con flujo de información**, mostrando su **estructura** y su **comportamiento dinámico**. Permiten representar **procesos concurrentes** y hacer **modelamiento matemático** del sistema.
- **Definición de la presentación**: además, se pueden ver como **generadores de lenguaje o autómatas formales** (teoría de grafos). Sirven para **diseñar, especificar y simular** sistemas de *hardware* o de *software*.
- **Historia**:
  - **1962**: **Carl Adam Petri** presenta su tesis doctoral *Kommunikation mit Automaten* ("Comunicación con autómatas") en **Alemania**. Es una teoría de comunicación entre componentes **asíncronos** (que no van al mismo ritmo). El proyecto **"Systemics"** aportó la teoría inicial, la notación y la representación.
  - **1970**: **Holt y Commoner** ("Events and Conditions") muestran cómo usarlas para modelar y analizar sistemas con componentes **concurrentes**.
- **Qué modelan**: las cuatro situaciones típicas de los sistemas distribuidos:
  - **Concurrencia**: cosas que pasan a la vez.
  - **Sincronización**: un proceso espera a que otro termine.
  - **Exclusión mutua**: un recurso se usa de a un proceso por vez.
  - **Conflicto**: hay que elegir entre dos acciones posibles.
- **Antecedente: las máquinas de estado** (estados y transiciones, con entradas y salidas *a/b*). Su límite es que no representan bien **acciones simultáneas**: si se combinan varias, la cantidad de estados se multiplica y el diagrama deja de entenderse. Las RdP resuelven eso porque tienen **paralelismo inherente**: la concurrencia forma parte del modelo.
- Al analizar una red se obtiene información de su **estructura** (cómo está armada) y de su **comportamiento dinámico** (cómo evoluciona). Con eso se evalúa el sistema y se proponen mejoras.
- **Tres ventajas de modelar con RdP** (presentación "Formalización"):
  1. El sistema es **más fácil de entender**, porque la representación es gráfica y precisa.
  2. El comportamiento se puede **analizar con la teoría de RdP** (árboles de marcados, relación entre estructura y comportamiento).
  3. Como se construyen *bottom-up* o *top-down*, permiten **diseñar sistemas cuyo comportamiento se conoce o se puede verificar**.
- **Extensiones del modelo original**:
  - **Modificaciones estructurales**: dan más potencia o más comodidad de modelado.
  - **Redes de Petri temporizadas**: agregan tiempo para analizar **cuantitativamente las prestaciones** del sistema.
- **Apunte de clase**: sirven para ver cómo funciona un sistema, qué procesos tiene y por qué estados pasa. Se usan como **autómatas**. Cualquier proceso se puede representar con una RdP.

### 1.2 Elementos y representación gráfica

| Elemento | Se dibuja como | Qué representa | En programación concurrente |
|---|---|---|---|
| **Lugar** o **plaza** | Círculo | Una **condición** o un estado | La condición que se tiene que cumplir para que un proceso se ejecute |
| **Transición** | Barra (segmento recto) | Un **evento** o suceso | Un **proceso** |
| **Arco dirigido** | Flecha, con un **peso** (si no tiene número, pesa 1) | Une un lugar con una transición o una transición con un lugar | Relaciona condiciones y procesos |
| **Marca**, **testigo** o *token* | Punto negro dentro del lugar | Que la condición del lugar **se cumple** | La condición se verifica |

- **Reglas de conexión**: un arco va de **lugar → transición** o de **transición → lugar**. **Nunca** une dos lugares ni dos transiciones.
  - Si hay un arco p → t, p es **lugar de entrada** de t.
  - Si hay un arco t → p, p es **lugar de salida** de t.
  - Puede haber **más de un arco** entre el mismo lugar y la misma transición: eso se resume con el **peso** del arco.
- Por eso la red es un **multígrafo dirigido bipartito**:
  - **Multígrafo**: admite varios arcos entre los mismos dos nodos.
  - **Dirigido**: cada arco tiene sentido.
  - **Bipartito**: hay dos tipos de nodos (lugares y transiciones) y los arcos solo unen nodos de tipos distintos.
- Un lugar que tiene marcas está **activo**. Cada lugar tiene asociada una acción o salida.
- **Transición sensibilizada** (o habilitada): sus lugares de entrada tienen las marcas que necesita (al menos tantas como el peso de cada arco de entrada). **Transición validada**: está sensibilizada **y además ocurre el evento** asociado; en ese momento se dispara.
- **Representación gráfica y matricial**: son dos formas de escribir la misma red. De una se obtiene la otra, y el resultado es único.

### 1.3 Definición formal

**Funciones de incidencia** (presentación "Formalización"):

| Función | Firma | Qué cuenta |
|---|---|---|
| **Incidencia previa** I | I: P × T → ℕ | I(p, t) = cantidad de arcos que van del **lugar p a la transición t** (entradas de t) |
| **Incidencia posterior** O | O: T × P → ℕ | O(t, p) = cantidad de arcos que van de la **transición t al lugar p** (salidas de t) |

El valor I(p, t) u O(t, p) es el **peso** del arco. Un arco sin etiqueta pesa 1.

**Red de Petri** = la cuádrupla **RdP = (P, T, I, O)**, donde:

- **P** es un conjunto **finito y no vacío** de lugares.
- **T** es un conjunto **finito y no vacío** de transiciones.
- **P ∩ T = ∅**: lugares y transiciones son conjuntos **disjuntos** (ningún nodo es las dos cosas).
- **I** es la función de incidencia previa y **O** la de incidencia posterior.

**Marcado**: función **M: P → ℕ** que dice cuántas marcas tiene cada lugar en un momento dado. Con n lugares se escribe como vector **M = (m1, …, mn)**, donde mi = M(pi). **El marcado es el estado de la red.**

**Red marcada**: la red junto con su **marcado inicial M0**: **(RdP, M0)**.

**Tipos de red según la incidencia**:

- **Ordinaria**: las funciones de incidencia solo valen **0 o 1** (todos los arcos pesan 1).
- **Generalizada**: las funciones de incidencia pueden tomar **cualquier entero ≥ 0**.
- **Pura** o **no reflexiva**: **ningún lugar es a la vez entrada y salida de la misma transición** (no hay "autolazos").

**Notación de la lectura (Jorge Castro Monge)**: llama **C = (P, T, I, O)** a la estructura, **μ** al marcado y **M = (C, μ)** a la red marcada. Describe O como un mapeo de transiciones en **bolsas de sitios**. Además usa I(t) = lugares de entrada de t; O(t) = lugares de salida de t; I'(p) = transiciones que entran al lugar p; O'(p) = transiciones que salen de p; V(p, t) y V(t, p) = pesos de los arcos.

> **Ojo con la letra C.** En la lectura, C es la estructura de la red; en la representación matricial (1.8.3), **C es la matriz de incidencia**. En este resumen se usa **RdP** para la estructura y **C** solo para la matriz.

### 1.4 Ejecución y alcanzabilidad

**Regla de disparo simple** (red ordinaria):

1. Una transición está **habilitada** si **todos** sus lugares de entrada tienen marca.
2. Una transición habilitada **puede dispararse**.
3. Al dispararse, **quita una marca de cada lugar de entrada** y **agrega una marca a cada lugar de salida**.

**Regla de disparo general** (con pesos):

1. **Habilitación**: t está habilitada en el marcado Mi si cada lugar de entrada tiene al menos tantas marcas como el peso del arco: **Mi(p) ≥ I(p, t)**.
2. **Disparo**: se quitan I(p, t) marcas de cada lugar de entrada y se agregan O(t, p) marcas a cada lugar de salida.
3. **Nuevo marcado**: **Mj(p) = Mi(p) + O(t, p) − I(p, t)**, para todo lugar p. En palabras: lo que había, más lo que la transición deja, menos lo que consume.

Algunos textos escriben **Pre(p, t)** en lugar de I(p, t) y **Post(t, p)** en lugar de O(t, p). Es la misma fórmula.

**Casos especiales**:

- **Transición fuente**: no tiene lugares de entrada, así que **siempre está habilitada**.
- **Transición sumidero**: no tiene lugares de salida, así que **elimina marcas** de la red.
- **Elección no determinista**: si hay varias transiciones habilitadas, cuál se dispara primero es **arbitrario** (se supone que se decide en un nivel de detalle inferior).
- **Indivisibilidad de las marcas**: una marca la puede quitar **una sola** transición. Por eso, disparar una transición puede **deshabilitar** a otra que compartía el mismo lugar de entrada (de ahí sale el **conflicto**). Fuera de esa restricción, los disparos son **asíncronos**.
- **Grado de habilitación**: cuántas veces se puede disparar una transición de forma concurrente con el marcado actual.

**Alcanzabilidad**:

- Mj es **inmediatamente alcanzable** desde Mi si se obtiene disparando **una** transición habilitada en Mi.
- Mk es **alcanzable** desde Mi si existe una **secuencia de disparos σ** que transforma Mi en Mk. Se escribe **Mi [σ> Mk**.
- **Conjunto de alcanzabilidad R(M0)**: el conjunto de **todos** los marcados alcanzables desde M0. La lectura lo escribe **M(R, M0)**.

**Vocabulario de la lectura**: dice **activada** en vez de habilitada y **descarga** en vez de disparo (la descarga elimina un elemento de cada lugar de entrada y agrega uno a cada lugar de salida).

### 1.5 Estructuras básicas

| Estructura | Qué modela | Cómo se ve en la red |
|---|---|---|
| **Secuencial** | Una acción después de otra | t2 solo puede dispararse después de t1 |
| **Selección** | Elegir qué proceso ejecutar | Un lugar con dos o más transiciones de salida |
| **Atribución** | Llegar al mismo estado desde dos procesos distintos | Dos transiciones que depositan marcas en el mismo lugar |
| **Distribución** | Lanzar procesos en paralelo | Una transición con varios lugares de salida (la red "se abre") |
| **Conjunción** | Juntar procesos paralelos | Una transición con varios lugares de entrada (la red "se cierra") |
| **Sincronización** | Esperar a que todos los procesos estén listos | Es el efecto de la conjunción: la transición se habilita solo cuando **todos** sus lugares de entrada tienen marca |
| **Concurrencia** | Dos acciones a la vez, sin afectarse | Dos transiciones habilitadas al mismo tiempo que no comparten lugares de entrada |
| **Conflicto** | Dos acciones que necesitan lo mismo | Dos transiciones habilitadas que comparten un lugar de entrada: disparar una deshabilita a la otra |

### 1.6 Propiedades

Las propiedades sirven para **detectar fenómenos de interés o errores de funcionamiento** en el sistema que modela la red (bloqueos, necesidad de recursos infinitos, conflictos). Hay dos grupos:

- **Estructurales**: dependen solo de la **estructura** (cómo está dibujada la red) y **no del marcado inicial**.
- **De comportamiento**: **dependen del marcado inicial M0**.

La presentación "Redes_de_petri" trabaja seis: **vivacidad, ciclicidad, limitación, conservación, conflictividad y exclusión mutua**. El resumen de cátedra agrega **acotada** y **completamente controlable**. La lectura destaca dos: **supervivencia** (ausencia de estancamientos) y **seguridad** (capacidad limitada de memoria).

#### Propiedades estructurales

| Propiedad | Definición | En palabras simples |
|---|---|---|
| **Pura** | Ningún lugar es entrada y salida de la misma transición: para toda transición t y todo lugar p, **I(p, t) · O(t, p) = 0** | Ninguna flecha "va y vuelve" entre el mismo lugar y la misma transición |
| **Estructuralmente acotada** | Es acotada con **cualquier** marcado inicial finito | Arranque como arranque, ningún lugar crece sin fin |
| **Estructuralmente viva** | Existe **algún** marcado inicial con el que es viva | Hay al menos una forma de arrancarla sin que se trabe |
| **Estructuralmente conservativa** | Conserva la cantidad (ponderada) de marcas con **cualquier** marcado inicial | Arranque como arranque, los recursos no cambian |
| **Completamente controlable** | **Cualquier marcado es alcanzable desde cualquier otro** | Desde cualquier estado se llega a cualquier estado |

#### Propiedades de comportamiento

**Alcanzabilidad** — ¿se puede llegar a ese estado?

- Es la **base para estudiar todas las propiedades dinámicas**.
- Mn es alcanzable desde M0 si y solo si existe σ tal que **M0 [σ> Mn**.

**Vivacidad** — ¿algo se traba para siempre?

- Sirve para **caracterizar el bloqueo total o parcial** del sistema.
- **Transición viva**: desde **cualquier** marcado alcanzable existe una secuencia de disparos que **la incluye**. En símbolos: para todo M ∈ R(M0) existe σ disparable desde M que contiene a t.
- **Red viva**: **todas** sus transiciones son vivas. Entonces no hay, en el conjunto de alcanzabilidad, ningún marcado con **bloqueo total (*deadlock*)**.
- La diapositiva distingue tres casos:
  - **Viva**: todas las transiciones son vivas.
  - **Parcialmente viva**: la red nunca se bloquea del todo (desde cualquier marcado alcanzable hay al menos una transición disparable), pero **al menos una transición no es viva**. Conserva la **posibilidad de evolución global**.
  - **No viva**: llega a un **marcado muerto** (ninguna transición habilitada): se **bloquea totalmente**. Ejemplo de la lectura: con la secuencia t1, t2, t1, t2 la red no se bloquea, pero con t1, t3, t4 queda **bloqueada**.
- Versión de la lectura: un **marcado vivo** permite, sin importar qué descargas se hicieron antes, descargar cualquier transición con alguna secuencia adicional. Una red así **nunca se estanca**.

**Ciclicidad** o **reversibilidad** — ¿siempre se puede volver al inicio?

- La red tiene comportamiento **globalmente cíclico** si desde **cualquier marcado sucesor** de M0 existe una secuencia que **vuelve a M0**: para todo M ∈ R(M0) existe σ tal que **M [σ> M0**.
- Garantiza que **no hay subconjuntos finales de estados**: grupos de marcados alcanzables entre sí desde los que ya no se puede volver a M0.
- **Vivacidad y ciclicidad son independientes.** Ejemplo de la lectura: una red **pseudoviva** y **no reversible**, porque nunca vuelve a obtener el marcado inicial.

**Acotamiento** o **limitación** — ¿algún lugar se llena sin tope?

- Un lugar p es **k-acotado** si **M(p) ≤ k** para todo M ∈ R(M0). La **cota del lugar** es el **menor** k que cumple eso.
- La red es **k-acotada** (o **k-limitada**) si **todos** sus lugares son k-acotados. Es **acotada** si existe algún k. Ejemplo de la diapositiva: una red **3-limitada**.
- Interés: **garantiza que los marcados alcanzables son finitos** (si cada lugar es una variable de estado, la red tiene un número finito de estados). En la práctica, una red k-limitada **se puede implementar con recursos finitos**.
- Si la red genera más marcas de las que permite su cota, **el modelo está mal**.
- Versión de la lectura: un **marcado acotado** es aquel en el que existe un entero n tal que ningún lugar recibe más de n elementos en ninguna secuencia de descargas.

**Seguridad** — ¿cada lugar tiene a lo sumo una marca?

- Red **segura** = **1-acotada** = **binaria**: cada lugar está marcado o no está marcado.
- Versión de la lectura: un **marcado seguro** es un marcado acotado en el que ningún lugar recibe más de un elemento. Si cada lugar es un registro que guarda una palabra de memoria, un marcado inicial seguro garantiza que **no se excede la capacidad** de los registros.
- Seguridad **no** es lo mismo que vivacidad: una red segura puede bloquearse.

**Conservación** — ¿los recursos se mantienen?

- La cantidad de **recursos disponibles no puede variar** durante la ejecución.
- **Conservación estricta**: la cantidad total de marcas es **la misma en todos los marcados alcanzables**. Es una condición **muy fuerte**.
- Por eso se usa la **conservación respecto de un vector peso w**: la suma ponderada **Σ w(p) · M(p)** es constante en todos los marcados alcanzables. Ejemplo de la diapositiva: w = (1, 1, 1, 2, 2).

**Conflictividad** — ¿hay transiciones que compiten?

- **Conflicto estructural**: un lugar tiene **más de una transición de salida**. Se ve en el dibujo.
- **Conflicto efectivo** para M0: ti y tj lo están si se cumplen **las dos** condiciones:
  1. existe un marcado alcanzable desde M0 que las **sensibiliza simultáneamente**, y
  2. al dispararse una, el marcado que queda **no habilita** a la otra.
- El conflicto efectivo depende del marcado: las dos transiciones están habilitadas a la vez y **compiten por la misma marca**. Todo conflicto efectivo es también estructural, pero no al revés.

**Exclusión mutua** — ¿hay cosas que nunca ocurren juntas?

- Entre **transiciones**: un conjunto Te ⊆ T es mutuamente exclusivo si disparar cualquier ti ∈ Te **deshabilita a todas las demás** tj ∈ Te.
- Entre **lugares**: dos lugares están en exclusión mutua para M0 si **nunca están marcados a la vez** en ningún marcado alcanzable.
- Ejemplo de la diapositiva: los lugares 4 y 5 y las transiciones Π1 y Π2 son mutuamente exclusivos (R = recurso disponible; R1 y R2 = recurso tomado por Π1 o por Π2). El modelo del semáforo está en 1.9.

#### Tabla resumen de propiedades

| Propiedad | Pregunta que responde | Qué detecta |
|---|---|---|
| Vivacidad | ¿Se pueden volver a disparar siempre todas las transiciones? | Bloqueos (*deadlock*) |
| Ciclicidad | ¿Se puede volver siempre al estado inicial? | Sistemas que no se pueden "reiniciar" |
| Limitación (acotada) | ¿Las marcas de cada lugar tienen un tope k? | Necesidad de recursos infinitos |
| Seguridad | ¿Cada lugar tiene como mucho una marca? | Desbordes de capacidad |
| Conservación | ¿Se mantiene la cantidad (ponderada) de marcas? | Recursos que se crean o se pierden |
| Conflictividad | ¿Hay transiciones que compiten por una marca? | Decisiones no deterministas |
| Exclusión mutua | ¿Hay lugares o transiciones que nunca coinciden? | Uso de recursos compartidos |
| Completamente controlable | ¿Todo marcado es alcanzable desde cualquier otro? | Estados inalcanzables |

### 1.7 Subclases

Las RdP se basan en reglas simples pero pueden tener **comportamientos muy complicados**. Por eso se definen **subclases**: redes con reglas más estrictas, **más fáciles de analizar**, que igual sirven para modelar muchos sistemas.

| Subclase | Regla | Puede modelar | No puede modelar |
|---|---|---|---|
| **Grafo de estados** o **máquina de estados** (GE o ME) | Cada **transición** tiene exactamente **una entrada y una salida** | Conflictos y alternativas | Paralelismo, concurrencia y sincronización |
| **Grafo marcado** o **grafo de sincronización** (GM) | Cada **lugar** tiene exactamente **una entrada y una salida** | Paralelismo, concurrencia y sincronización | Conflictos y decisiones que dependen de los datos |
| **Red de libre elección** (RLE) | Si un lugar es entrada de varias transiciones, es la **única** entrada de cada una de ellas | Concurrencia y conflicto, de forma restringida | — |
| **Red simple** (RS) | Cada transición tiene **como máximo un lugar de entrada compartido** con otra transición | Concurrencia y conflicto, con menos restricciones que la RLE | — |

- La **máquina de estados** es **estrictamente conservativa** (cada disparo mueve una marca de un lugar a otro) y muy fácil de analizar, pero tiene **poca potencia de modelado**.
- En la **red de libre elección**, las transiciones en conflicto tienen la misma única entrada, así que **están todas habilitadas o ninguna**: la elección no depende de otros lugares.
- La máquina de estados restringe las **transiciones** (puede elegir, pero no paralelizar); el grafo marcado restringe los **lugares** (puede paralelizar, pero no elegir). Son opuestos.
- **Jerarquía de generalidad**: ME y GM ⊂ RLE ⊂ RS ⊂ RdP generales. (Es un resultado estándar; no aparece escrito en las diapositivas.)

### 1.8 Métodos de análisis

Hay dos familias:

1. Los basados en el **árbol de alcanzabilidad** (incluye la **máquina de testigos**).
2. Los basados en **ecuaciones matriciales** o **de estado**.

#### 1.8.1 Árbol de alcanzabilidad

> **En una frase:** es el **mapa de todos los marcados** a los que puede llegar la red desde M0.

- Cada **nodo** es un marcado alcanzable. Cada **arco** lleva el nombre de la transición que se disparó para pasar de un marcado al otro.
- **Cómo se construye**:
  1. La raíz es M0.
  2. Por cada transición habilitada se crea un hijo con el marcado que resulta de dispararla.
  3. Se repite desde cada marcado nuevo.
  4. Así el árbol sería infinito. Para que sea **finito**, no se expande un nodo cuando es un **marcado frontera** (hoja):

| Condición | Nombre | Qué es |
|---|---|---|
| a) | **Marcado muerto** | No hay **ninguna transición habilitada** |
| b) | **Nodo duplicado** | El marcado **ya apareció antes** en el árbol |
| c) | **Marcado con ω** | Se diferencia de un marcado anterior solo en que tiene **más marcas en algún lugar** y habilita las mismas transiciones. En esos lugares se escribe **ω** (el apunte usa **w**), que significa "puede crecer sin límite" |

- **Cómo aplicar la condición c**: se compara el marcado nuevo con sus **antecesores en el mismo camino** desde M0. Si un antecesor tiene, en cada lugar, igual o menos marcas, y en algún lugar estrictamente menos, en esos lugares se escribe ω. La diapositiva lo dice así: "solo se diferencia de otro marcado en tener distinto número de testigos en alguna plaza y habilita el mismo conjunto de transiciones".
- Con ω valen **ω + 1 = ω** y **ω − 1 = ω**.
- Con las tres condiciones, **el árbol de alcanzabilidad de cualquier RdP es finito**.
- **Para qué sirve**: da información detallada del comportamiento. Se usa para comprobar que la red **representa bien** el sistema, **verificar** un diseño, **elegir** entre varias propuestas y **predecir** el comportamiento.
- **Desventaja**: puede volverse **grande, complejo e inmanejable**.

**Qué propiedades se leen en el árbol** (detalle en 1.12):

| Si en el árbol… | Entonces la red… |
|---|---|
| Aparece un marcado muerto | **No es viva** (se bloquea) |
| Aparece ω en algún lugar | **No es acotada** |
| El máximo de marcas en un lugar es k | Es **k-acotada** |
| Desde todo marcado se puede volver a M0 | Es **cíclica** |
| La suma (ponderada) de marcas es igual en todos los nodos | Es **conservativa** |

#### 1.8.2 Máquina de testigos

- Es una **modificación del árbol de alcanzabilidad** con una forma **más compacta**.
- El **estado** se escribe con los **nombres de los lugares que tienen marcas**. Un lugar aparece **tantas veces como marcas tenga** (por ejemplo, dos marcas en p2 se escriben p2 p2).
- Es un **grafo dirigido**: cada estado va en un **óvalo**, una sola vez, y los óvalos se unen con arcos que llevan el nombre de la transición.
- **Cuándo conviene**: cuando la red tiene **muchos lugares y pocas marcas**. En el árbol habría que escribir vectores largos llenos de ceros; en la máquina de testigos solo se nombran los lugares marcados.

| | Árbol de alcanzabilidad | Máquina de testigos (MT) |
|---|---|---|
| Cómo se escribe el estado | Vector completo (m1, …, mn) | Nombres de los lugares con marcas |
| Forma | Árbol: los marcados repetidos quedan como hojas "duplicado" | Grafo con ciclos: cada estado aparece una sola vez |
| Conviene en | Redes chicas o con muchas marcas | Redes con muchos lugares y pocas marcas |

#### 1.8.3 Representación matricial (ecuación de estado)

| Matriz | Qué guarda | En palabras simples |
|---|---|---|
| **C⁻** (incidencia previa) | C⁻[j, i] = I(pi, tj): las precondiciones | Lo que cada transición **consume** |
| **C⁺** (incidencia posterior) | C⁺[j, i] = O(tj, pi): las postcondiciones | Lo que cada transición **produce** |
| **C = C⁺ − C⁻** (incidencia) | La diferencia entre las dos | El **efecto neto** de cada transición sobre cada lugar |

- Según la lectura: **filas = transiciones, columnas = lugares**. Con m transiciones y n lugares, C es de m × n.
- Una transición tj se representa con el vector **ej**: 1 en la posición j y 0 en el resto.
  - tj está **habilitada** en M si **M ≥ ej · C⁻** (comparando lugar por lugar).
  - Al dispararla: **M' = M + ej · C**.
- Para una **secuencia** σ = tj1 tj2 … tjk: **M' = M + f(σ) · C**, donde **f(σ) = ej1 + ej2 + … + ejk** es el **vector de disparo**: cuántas veces se dispara cada transición.
- Ejemplo de la cátedra (red del Ejemplo 1 de 1.12): σ = t1, t2, t3 → f(σ) = (1 1 1 0 0) → M' = (0 0 0 1 1).
- **Limitaciones** del método matricial:
  1. La matriz C **no refleja toda la estructura** de la red: si un lugar es entrada y salida de la misma transición, el efecto se cancela y no aparece en C.
  2. El vector de disparo **no dice en qué orden** se disparan las transiciones.
  3. Que la ecuación M' = M + f(σ) · C tenga solución es condición **necesaria pero no suficiente** para que M' sea alcanzable.

### 1.9 Modelos clásicos de concurrencia

- **Exclusión mutua (semáforo)**: varios procesos comparten un recurso y, mientras uno lo usa, los demás no pueden. Hace falta un **mecanismo de espera**. Se usa un lugar que representa la condición **"el recurso está libre"**, con **una marca**. Ese lugar funciona como **semáforo**: el primer proceso que toma la marca usa el recurso y los demás esperan hasta que la devuelve. Sirve para cualquier cantidad de procesos y **no permite fijar prioridades**.
- **Productor y consumidor**: el recurso compartido no se usa, sino que sirve para **comunicar** a los procesos. Un lugar "depósito" (*buffer*) une al productor con el consumidor. Si el depósito no tiene límite, puede crecer sin fin cuando el consumidor se detiene. Con un **buffer de capacidad finita** se agregan dos lugares, "buffers llenos" y "buffers vacíos", que **siempre suman la capacidad total** (por ejemplo, 3).
- **Lectores y escritores**: varios procesos pueden **leer a la vez**, pero **escribir es de a uno** y excluye a los lectores. Se usa un semáforo con **m marcas** (m = cantidad de lectores) y arcos de peso **m**: leer toma 1 marca y escribir toma las m.
- **Cinco filósofos**: cada filósofo necesita los dos tenedores que tiene al lado para comer. Si todos toman primero el mismo lado, nadie come: **estancamiento**. Soluciones habituales para que la red sea viva: que la transición "comer" tome **los dos tenedores a la vez** (una conjunción), o agregar un lugar "sillas" con **4 marcas** que limite cuántos intentan comer al mismo tiempo. (Son las soluciones habituales; la del grupo está en una imagen que no se pudo verificar.)

### 1.10 Ventajas, desventajas y aplicaciones

| Ventajas | Desventajas |
|---|---|
| Son **fáciles de interpretar**: el esquema es gráfico e ilustrativo | Las RdP generales **no pueden modelar ciertas situaciones de prioridad** |
| Permiten tratar **procesos independientes** por separado | El **análisis se complica** cuando el sistema es complejo |
| Modelan con **más exactitud que un diagrama de estados** | Cuanto más alcance tiene el modelo, más **tiempo y espacio** consume |
| Modelan **recursos compartidos** por varios procesos (por ejemplo, una impresora) | Hay **muchas subclases** para problemas específicos: no existe un modelo único |
| Se construyen ***top-down*** o ***bottom-up*** | |
| Modelan **procesos concurrentes** | |

**Aplicaciones**: sistemas en **tiempo real**; **sistemas operativos y compiladores**; *hardware* y *software* de computadoras; **ambientes industriales de producción** (con redes de libre elección); **diagramas de flujo de datos** (DFD); **protocolos de comunicación**; **bases de datos**.

### 1.11 Verificación y ambientes de simulación

- Ejecutar la red es **simular** el sistema. La simulación da una **verificación** del modelo. Una **validación** exige un tratamiento más formal: las técnicas matemáticas de análisis se acercan a una "prueba".
- En modelos grandes no se puede ejecutar a mano: hacen falta herramientas que lo hagan solas (por ejemplo **HPetriSim**, el simulador de los ejercicios).
- **Ambientes gráficos**: dan una visión global rápida, pero definir la red es tedioso y en redes grandes el dibujo se vuelve confuso.
- **Ambientes estructurales** (intérpretes): se pierde lo visual, pero la red escrita como pseudocódigo se parece al código de un programa (lenguajes como ADA o Modula).

### 1.12 Práctica que entra en el parcial: resolver una red paso a paso

Entran el **árbol de alcanzabilidad**, las **características y propiedades**, y **resolver una red con máquina de testigos y método matricial**. Los tres ejemplos están verificados por computadora.

**Receta para el examen**

1. **Leer la red**: lugares, transiciones, arcos con sus pesos y M0. Escribir los lugares de entrada y de salida de cada transición.
2. **Matrices**: C⁻ (entradas), C⁺ (salidas) y **C = C⁺ − C⁻**, con **filas = transiciones** y **columnas = lugares**.
3. **Árbol de alcanzabilidad**: desde M0, por cada transición habilitada calcular el marcado nuevo y numerarlo (M1, M2…). Cortar en los marcados frontera (1.8.1).
4. **Máquina de testigos**: juntar los marcados repetidos y dibujar el grafo. Cada óvalo lleva los lugares marcados, repetidos si tienen más de una marca.
5. **Método matricial**: comprobar una secuencia σ con **M' = M + f(σ) · C**. Como la ecuación no dice el orden, revisar que cada transición esté habilitada en su momento (**M ≥ ej · C⁻**).
6. **Propiedades**: leerlas del árbol y de la máquina de testigos con esta tabla:

| Propiedad | Cómo se ve en el árbol o en la máquina de testigos |
|---|---|
| **Viva** | No hay marcados muertos y, desde cualquier estado, cada transición puede volver a dispararse |
| **Parcialmente viva** | No hay marcados muertos, pero alguna transición deja de poder dispararse |
| **No viva** | Aparece un marcado muerto (bloqueo total) |
| **Acotada (k-acotada)** | No aparece ω; k es el máximo de marcas que llega a tener un lugar |
| **Segura** | k = 1: ningún lugar pasa de una marca |
| **No acotada** | Aparece ω en algún lugar |
| **Cíclica (reversible)** | Desde todos los estados se puede volver a M0 |
| **Conservativa** | La suma de marcas es igual en todos los marcados (o la suma ponderada con un vector peso) |
| **Conflicto** | Estructural: un lugar con dos o más transiciones de salida. Efectivo: en algún marcado las dos están habilitadas y disparar una deshabilita a la otra |
| **Concurrencia** | Dos transiciones habilitadas a la vez que no comparten lugares de entrada |
| **Exclusión mutua de lugares** | Dos lugares que nunca están marcados a la vez |
| **Pura** | Ningún lugar es entrada y salida de la misma transición |

**Ejemplo 1 — red acotada (la de la lectura)**

P = {p1, …, p5}, T = {t1, …, t5}, M0 = (1, 0, 0, 0, 0).
t1: p1 → p2, p3 · t2: p2 → p5 · t3: p3 → p4 · t4: p5 → p2 · t5: p4, p5 → p1.

| | C⁻ (p1 p2 p3 p4 p5) | C⁺ (p1 p2 p3 p4 p5) | C (p1 p2 p3 p4 p5) |
|---|---|---|---|
| t1 | 1 0 0 0 0 | 0 1 1 0 0 | −1 1 1 0 0 |
| t2 | 0 1 0 0 0 | 0 0 0 0 1 | 0 −1 0 0 1 |
| t3 | 0 0 1 0 0 | 0 0 0 1 0 | 0 0 −1 1 0 |
| t4 | 0 0 0 0 1 | 0 1 0 0 0 | 0 1 0 0 −1 |
| t5 | 0 0 0 1 1 | 1 0 0 0 0 | 1 0 0 −1 −1 |

Árbol de alcanzabilidad (los marcados se numeran por nivel: M1; después M2 y M3; después M4):

```
M0 (1,0,0,0,0)
└─ t1 → M1 (0,1,1,0,0)
   ├─ t2 → M2 (0,0,1,0,1)
   │  ├─ t3 → M4 (0,0,0,1,1)
   │  │  ├─ t4 → (0,1,0,1,0)  duplicado de M3
   │  │  └─ t5 → (1,0,0,0,0)  duplicado de M0
   │  └─ t4 → (0,1,1,0,0)  duplicado de M1
   └─ t3 → M3 (0,1,0,1,0)
      └─ t2 → (0,0,0,1,1)  duplicado de M4
```

Máquina de testigos (5 estados, 8 arcos):

| Desde | Transición | Hacia |
|---|---|---|
| p1 | t1 | p2 p3 |
| p2 p3 | t2 | p3 p5 |
| p2 p3 | t3 | p2 p4 |
| p3 p5 | t3 | p4 p5 |
| p3 p5 | t4 | p2 p3 |
| p2 p4 | t2 | p4 p5 |
| p4 p5 | t4 | p2 p4 |
| p4 p5 | t5 | p1 |

Método matricial: σ = t1 t3 t2 t5 → f(σ) = (1 1 1 0 1). f(σ) · C = suma de las filas t1, t2, t3 y t5 de C = (0 0 0 0 0), entonces **M' = M0**: la secuencia vuelve al inicio. Orden: M0 → t1 → M1 → t3 → M3 → t2 → M4 → t5 → M0. Por ejemplo, t5 está habilitada en M4 porque e5 · C⁻ = (0 0 0 1 1) ≤ (0 0 0 1 1).

Propiedades:
- **Viva**: no hay marcados muertos y desde cualquier estado se llega a todos los demás.
- **Segura** (1-acotada), **cíclica** y **pura**.
- **No es estrictamente conservativa** (M0 tiene 1 marca y los demás marcados tienen 2), pero **sí es conservativa respecto del vector peso (2 1 1 1 1)**: la suma ponderada da 2 en todos los marcados.
- **Conflicto** estructural en p5 (t4 y t5) y efectivo en M4.
- **Concurrencia**: t2 y t3 en M1; t3 y t4 en M2.
- **Exclusión mutua de lugares**: p2 y p5; p3 y p4; p1 con todos los demás.

**Ejemplo 2 — red no acotada (con ω)**

P = {p1, p2, p3}, M0 = (1, 0, 0).
t1: p1 → p2 · t2: p2 → p1, p3 · t3: p3 → (ninguno; es una transición sumidero).

| | C⁻ (p1 p2 p3) | C⁺ (p1 p2 p3) | C (p1 p2 p3) |
|---|---|---|---|
| t1 | 1 0 0 | 0 1 0 | −1 1 0 |
| t2 | 0 1 0 | 1 0 1 | 1 −1 1 |
| t3 | 0 0 1 | 0 0 0 | 0 0 −1 |

Árbol de alcanzabilidad:

```
M0 (1,0,0)
└─ t1 → M1 (0,1,0)
   └─ t2 → (1,0,1): es mayor que su antecesor M0 (igual en p1 y p2, más en p3) → M2 (1,0,ω)
      ├─ t1 → M3 (0,1,ω)
      │  ├─ t2 → (1,0,ω)  duplicado de M2
      │  └─ t3 → (0,1,ω)  duplicado de M3
      └─ t3 → (1,0,ω)  duplicado de M2
```

Máquina de testigos: p1 —t1→ p2 —t2→ p1 p3ω; p1 p3ω —t1→ p2 p3ω; p1 p3ω —t3→ p1 p3ω; p2 p3ω —t2→ p1 p3ω; p2 p3ω —t3→ p2 p3ω.

Método matricial: σ = t1 t2 t1 t2 t3 → f(σ) = (2 2 1) → M' = (1 0 0) + 2 · (−1 1 0) + 2 · (1 −1 1) + (0 0 −1) = **(1 0 1)**. Paso a paso: (0 1 0), (1 0 1), (0 1 1), (1 0 2), (1 0 1).

Propiedades:
- **No acotada**: p3 llega a ω (p1 y p2 son 1-acotados).
- **Viva**.
- **Cíclica**: desde (1, 0, k) se dispara t3 k veces y se vuelve a M0; desde (0, 1, k) se dispara t2 y se llega a (1, 0, k + 1). El árbol con ω no alcanza para afirmarlo: hay que razonarlo así.
- **No conservativa**, **pura** y **sin conflicto** (ningún lugar tiene dos transiciones de salida).
- **Exclusión mutua de lugares**: p1 y p2 (siempre p1 + p2 = 1).

**Ejemplo 3 — exclusión mutua de dos procesos (semáforo)**

Lugares: a1 y a2 (proceso esperando), b1 y b2 (proceso usando el recurso), s (recurso libre).
M0 = (a1, b1, a2, b2, s) = (1, 0, 1, 0, 1).
t1: a1, s → b1 · t2: b1 → a1, s · t3: a2, s → b2 · t4: b2 → a2, s.

| | C⁻ (a1 b1 a2 b2 s) | C⁺ (a1 b1 a2 b2 s) | C (a1 b1 a2 b2 s) |
|---|---|---|---|
| t1 | 1 0 0 0 1 | 0 1 0 0 0 | −1 1 0 0 −1 |
| t2 | 0 1 0 0 0 | 1 0 0 0 1 | 1 −1 0 0 1 |
| t3 | 0 0 1 0 1 | 0 0 0 1 0 | 0 0 −1 1 −1 |
| t4 | 0 0 0 1 0 | 0 0 1 0 1 | 0 0 1 −1 1 |

Árbol: M0 (1,0,1,0,1) → t1 → M1 (0,1,1,0,0) → t2 → duplicado de M0; M0 → t3 → M2 (1,0,0,1,0) → t4 → duplicado de M0.

Máquina de testigos: a1 a2 s —t1→ b1 a2 —t2→ a1 a2 s; a1 a2 s —t3→ a1 b2 —t4→ a1 a2 s.

Método matricial: σ = t1 t2 t3 → f(σ) = (1 1 1 0) → M' = M0 + (0 0 −1 1 −1) = **(1 0 0 1 0)** = M2.

Propiedades:
- **Viva**, **segura**, **cíclica** y **pura**.
- **Conservativa respecto del vector peso (1 2 1 2 1)**: la suma ponderada da 3 en todos los marcados.
- **Conflicto** estructural y efectivo en s: en M0, t1 y t3 están habilitadas y disparar una deshabilita a la otra.
- **Exclusión mutua**: b1 y b2 nunca están marcados a la vez.

**Errores típicos al resolver**

- ❌ Seguir expandiendo un nodo **duplicado**. ✅ Se corta ahí.
- ❌ Poner ω comparando con un marcado de **otra rama**, o "restarle" a ω. ✅ Se compara con un **antecesor del mismo camino**, y ω − 1 = ω.
- ❌ Armar la matriz con **filas = lugares**. ✅ Filas = transiciones.
- ❌ Creer que si M' = M + f(σ) · C tiene solución, la secuencia se puede disparar. ✅ Es condición **necesaria pero no suficiente**.
- ❌ En la máquina de testigos, escribir una sola vez un lugar con **dos marcas**. ✅ Se repite el nombre.

### 1.13 Modelos de redes

Es la segunda parte de la presentación "Redes_de_petri". Son modelos de **optimización sobre redes** (investigación operativa). Se aplican en la ciencia de la administración: redes de **transporte**, **logística**, redes **eléctricas** o **de comunicación**, y también en programación y seguimiento de procesos, marketing, recursos humanos y finanzas.

**Conceptos básicos**

| Concepto | Definición |
|---|---|
| **Arista** | Segmento **dirigido** que va de un punto a otro |
| **Nodo** | Punto donde se cruzan dos o más aristas |
| **Capacidad** | Máximo que puede llevar una arista |
| **Fuente** | Punto de partida del flujo total de la red |
| **Sumidero** | Punto de llegada del flujo total de la red |
| **Red** | **Grafo dirigido** formado por una fuente, un sumidero, aristas y nodos |

**Los cuatro modelos**

| Modelo | Sobre qué red | Qué busca |
|---|---|---|
| **Ruta más corta** (RMC) | Red **conexa y no dirigida**, con un nodo **origen** y un nodo **destino**; cada arista tiene una distancia no negativa | La trayectoria de **mínima distancia total** entre origen y destino |
| **Árbol de expansión mínima** (AEM) | Red **conexa y no dirigida**; cada arista tiene una longitud positiva (distancia, costo) | **Conectar todos los nodos** con la **menor longitud total**, sin formar ciclos |
| **Flujo máximo** | Red con **capacidad máxima por unidad de tiempo** en cada arista | El **mayor flujo por unidad de tiempo** entre origen y destino, sin superar ninguna capacidad |
| **Flujo de costo mínimo** | Red con nodos **origen** (oferta), de **transbordo** (intermedios) y **destino** (demanda); cada arista tiene un costo por unidad | **Abastecer la demanda al menor costo total** de transporte |

- **Cómo se resuelve la ruta más corta** (método de la tabla de la diapositiva): en cada iteración se miran los nodos ya resueltos que se conectan con nodos no resueltos; se calcula la distancia total a cada nodo no resuelto más cercano; el de menor distancia total queda resuelto. Se repite hasta resolver el destino.
- **Cómo se resuelve el árbol de expansión mínima**: se elige cualquier nodo y se lo une con el más cercano; después, desde los nodos ya conectados, se agrega siempre la arista más corta hacia un nodo nuevo; se repite hasta conectar todos. Un árbol con n nodos tiene n − 1 aristas.
- **Utilidad del árbol de expansión mínima**: planificar redes de transporte que no se van a transitar mucho, donde lo importante es que haya **algún camino entre todos los pares de nodos** al menor costo.
- **No confundir**: la ruta más corta une **solo el origen con el destino**; el árbol de expansión mínima conecta **todos** los nodos.
- En el flujo máximo, lo que entra a cada nodo intermedio es igual a lo que sale.
- Nombres de los algoritmos (no aparecen en las diapositivas): el método de la ruta más corta es el de **Dijkstra** y el del árbol de expansión mínima es el de **Prim**.

---

## 2. Business Intelligence (Tema 8)

> **En una frase:** BI es **usar los datos de la organización para tomar mejores decisiones**, de forma continua.

### 2.1 Definición

- **Business Intelligence** (BI) significa "inteligencia de negocio". Su objetivo es apoyar a la organización de forma **sostenible y continuada** para mejorar su **competitividad**, dándole la información que necesita para **tomar decisiones**.
- El término lo acuñó y popularizó **Howard Dresner**, consultor de **Gartner**, como "término paraguas" para los conceptos y métodos que mejoran las decisiones usando información sobre lo que ya pasó (**hechos**).
- Idea central: **datos → información → conocimiento**.
- **Definición del resumen de cátedra**: BI es el **proceso interactivo para explorar y analizar información estructurada sobre un área**; abarca **procesos, herramientas y tecnologías** para convertir **datos en información** e **información en conocimiento y planes** que permitan dirigir eficazmente las actividades de la empresa. **Propósito**: dar la información necesaria para que las decisiones sean **más rápidas, precisas y fundamentadas**, y así mejorar la **competitividad** y la **gestión**.

**Definición de Gartner** (la que el libro considera más ajustada): BI es un **proceso interactivo** para **explorar** y **analizar información estructurada** sobre un **área** (normalmente guardada en un ***datawarehouse***), para descubrir **tendencias o patrones**, derivar ideas y extraer conclusiones. Incluye **comunicar** los descubrimientos y **efectuar los cambios**. Las áreas pueden ser clientes, proveedores, productos, servicios y competidores.

| Parte de la definición | Qué quiere decir |
|---|---|
| Proceso interactivo | Es un análisis **continuo en el tiempo**, no algo que se hace una vez. Así se ven tendencias, cambios y variaciones |
| Explorar | Primer acceso a la información: entender qué pasa y encontrar relaciones que no se conocían |
| Analizar | Descubrir cómo se relacionan las variables, las tendencias y los patrones (si un cliente actúa de cierta forma, ¿uno parecido actuará igual?) |
| Información estructurada y *datawarehouse* | Tablas relacionadas, con registros y atributos, guardadas en un **almacén de datos** |
| Área de análisis | Todo proyecto de BI tiene un objeto concreto (clientes, productos) y un objetivo (bajar costos, subir ventas) |
| Comunicar y efectuar cambios | Lo descubierto tiene que llegar a quien puede cambiar algo |

- **Definición del TDWI** (The Data Warehousing Institute): término paraguas que abarca los procesos, las herramientas y las tecnologías para convertir **datos en información, información en conocimiento**, y planes para conducir el negocio. Tiene dos partes:
  - ***Back end*** ("trastienda"): el *datawarehousing*.
  - ***Front end*** ("mostrador"): consultas, informes, análisis y visualización.

### 2.2 De los datos a las decisiones

- Los sistemas de información tienen que ayudar a **decidir**. Quien decide busca información para **reducir la incertidumbre**. No todos buscan la misma información: depende de su experiencia, su formación, lo que tiene disponible y cuánto riesgo está dispuesto a correr.
- Los **datos** de las transacciones (qué se vendió, cuándo, quién, cómo se pagó) se convierten en **información operativa** (ventas del día, ticket medio, ventas por artículo).
- Esa información sirve para tomar **decisiones**:
  - **Operativas**: reponer mercadería, asignar turnos.
  - **Estratégicas**: qué hacer cuando bajan las ventas (¿viene menos gente o cada cliente gasta menos?).
- Con el tiempo aparecen **tendencias** y **relaciones entre productos**, que permiten armar promociones y ubicar mejor los productos.
- BI sirve primero para **ayudar a decidir** y después para **descubrir conocimiento**.

### 2.3 Quién lo necesita

Compras, ventas, la negociación con bancos, marketing y recursos humanos. En resumen: **todo el que toma decisiones**, sean **operativas** o **estratégicas**.

### 2.4 Beneficios

| Tipo | Qué son | Ejemplos |
|---|---|---|
| **Tangibles** | Se miden en dinero: **generación de ingresos**, **reducción de costos** y **reducción de tiempos** | Ingresos: segmentar clientes, reducir el abandono, análisis de la cesta de la compra, medir y ajustar campañas, encontrar clientes rentables. Costos: negociar con proveedores, inventarios *just-in-time*, detectar fraude, menos créditos incobrables, "una sola versión de la verdad" |
| **Intangibles** | **Mejor toma de decisiones** y **mejor posición competitiva**: si la información está disponible, más personas la usan para decidir | Mejor atención y satisfacción del cliente, información más actual y precisa, mejor acceso a los datos, más integración, ventaja competitiva |
| **Estratégicos** | Ayudan a **formular la estrategia**: a qué clientes, mercados o productos dirigirse | Analizar estrategias de precios, identificar clientes con potencial, decisiones más rápidas y basadas en hechos |

### 2.5 Componentes

**Los 6 componentes de todo proyecto de BI** (capítulo 1 del libro):

1. Un **problema del negocio** a responder.
2. Un **equipo** (o una persona) que hace el análisis.
3. **Información interna**, de los sistemas de la organización.
4. **Información externa** a la organización (mercado, proveedores, tarifas).
5. Una **base de datos**: el *datawarehouse*.
6. Una **aplicación de BI** para trabajar, analizar y visualizar la información.

**Componentes del entorno de BI** (visión técnica del resumen de cátedra y del video de la cátedra): el camino que recorren los datos.

**Fuentes de datos operacionales → ETL → *data staging* → *datawarehouse* → Data Marts → plataforma de BI → herramientas de análisis → usuarios**

| Componente | Qué es | Detalle |
|---|---|---|
| **Fuentes de datos operacionales** | Los sistemas donde se registran los datos del día a día: archivos estructurados, bases de datos, ERP, CRM y sistemas **heredados** (*legacy*) | 2.11 |
| **ETL** | El proceso que **recupera los datos de las fuentes y alimenta el *datawarehouse*** | 2.12 |
| ***Data staging*** | Área intermedia donde se limpian y acumulan los datos antes de cargarlos | 2.12 |
| ***Datawarehouse*** | Base de datos **centralizada** que integra la información estratégica de toda la organización | 2.13 |
| **Data Marts** | Estructuras pensadas para una **comunidad de usuarios** concreta. El video los llama "bodegas de datos" | 2.13 |
| **Plataforma de BI** | El entorno tecnológico que permite a los usuarios **interactuar con los datos** | — |
| **Herramientas de análisis** | Informes, OLAP, tableros, minería de datos, alertas, modelos predictivos | 2.14 y 2.15 |
| **Usuarios** | Productores y consumidores de información | 2.16 |

En un proyecto real, el orden de trabajo no es este: primero se definen los **objetivos, el alcance y los modelos de negocio**.

### 2.6 Sistemas de información (Nota técnica 1)

- **Sistema de información de una organización**: la parte de la organización que se dedica formalmente a **capturar, almacenar y transmitir información relevante** a todos sus miembros, para que puedan hacer sus tareas, y a **intercambiar información** con otras personas u organizaciones.
- Las organizaciones necesitan información para tres cosas:
  - **Soportar las transacciones**: coordinar y registrar las operaciones (pedido, entrega, factura, cobro).
  - **Tomar decisiones y controlar**: por ejemplo, comparar las ventas con lo presupuestado.
  - **Crear nuevos negocios**: ofrecer o vender información a clientes o proveedores.
- Los sistemas sirven para **controlar, coordinar y tomar decisiones** en los niveles de **planificación, gestión y operaciones**. Cada área (comercial, administración, producción, logística, marketing, recursos humanos) usa información distinta.
- **Integración de aplicaciones**:
  - En una organización conviven varias aplicaciones. Si no están integradas, la información se pasa de una a otra con **interfases** (por ejemplo, de facturación a contabilidad).
  - Un **ERP** (*Enterprise Resources Planning*, planificación de recursos empresariales) integra los módulos con el concepto de **dato único**: una sola base de datos para toda la información.

| | Preguntas estructuradas | Preguntas no estructuradas |
|---|---|---|
| Dónde aparecen | En los niveles **inferiores** de la organización | En los niveles **superiores** |
| Respuesta | Sí o no, o un valor | Difícil de cuantificar: requiere creatividad y criterio; no se modela fácilmente |
| Ejemplo | ¿Entregamos el pedido del cliente X en plazo? | ¿Nos conviene lanzar el producto Y en el mercado Z? |

### 2.7 Retorno de la inversión (ROI, Nota técnica 2)

El ROI responde: **¿lo que se gana justifica lo que se gasta?**

- **ROI simple = valor para el negocio / costo del proyecto**. El costo es fácil de medir; el valor es lo difícil.
- **Los 8 pasos de Bill Whittemore**:
  1. Definir el problema u oportunidad, con objetivos **específicos, medibles, alcanzables, adecuados y con plazo**.
  2. Recoger los requerimientos.
  3. Construir el proyecto.
  4. Identificar y cuantificar los beneficios.
  5. Fijar el punto de partida de costos e ingresos.
  6. Calcular el **TCO** (*Total Cost of Ownership*, costo total de propiedad): *hardware*, *software*, consultoría, personal, lanzamiento, mantenimiento y formación.
  7. Calcular el **ROI = NPV / inversión inicial × 100**.
  8. Hacer seguimiento y corregir.
- **NPV** (*Net Present Value*, valor actual neto): la suma de los flujos de caja (CF, *Cash Flow*) de cada año, descontados a la tasa r, menos la inversión inicial: **NPV = −inversión inicial + Σ CFt / (1 + r)^t**.

### 2.8 Modelo de negocio

- **"Lo que no se mide, no se puede gestionar."** Por eso el primer paso es definir **qué** se va a medir y **cómo**: el **modelo de negocio** y sus métricas.
- **Definición del resumen de cátedra**: el modelo de negocio es una **simplificación de la realidad** que sirve para **comprender qué está pasando** en un área del negocio. Permite **experimentar cómo afectarán los cambios** al resultado y **analizar dónde se genera el resultado**.
- **Definición del libro**: permite **documentar, probar y desarrollar teorías** sobre cómo funciona el negocio. Tiene que estar **vivo**, igual que el negocio.
- **Cómo se arma**:
  1. Definir qué se quiere medir y cómo.
  2. Documentar, probar y desarrollar teorías sobre cómo funciona el negocio.
  3. Usar metodologías de análisis: **contabilidad analítica o de costos**, **EFQM** (*European Foundation for Quality Management*), **Six Sigma**, **análisis de procesos**, **modelos financieros** y **análisis de ratios**. En organizaciones complejas hay que considerar también la **estructura organizativa**.
- **Silos de información**: departamentos entre los que no circula la información necesaria para gestionar o analizar. Se deben a la **falta de integración** de los sistemas o a **razones políticas** internas. Lo mejor para un departamento no siempre es lo mejor para la organización.

### 2.9 Indicadores clave (KPI)

- **KPI** (*Key Performance Indicators*, indicadores clave de desempeño): sirven para **evaluar si la organización alcanza sus objetivos** y **medir su progreso hacia las metas**.
- Según el resumen de cátedra, se definen **después** de que la organización analizó su **misión**, identificó a sus **grupos de poder** y definió sus **objetivos**.
- **Un KPI tiene que**:
  1. **Reflejar los objetivos** del negocio.
  2. Ser **crítico para el éxito**.
  3. Ser **cuantificable y comparable**.
  4. **Permitir acciones correctivas**.
- **Buenas prácticas**: pocos KPI; alineados entre departamentos y con los objetivos de la organización; definidos junto con los responsables de cada área.
- Cada KPI tiene **nombre, definición, forma de cálculo y valor objetivo**.
- Dos empresas del mismo sector pueden tener KPI distintos, según su modelo de negocio y sus objetivos.

### 2.10 Modelo de datos

- **Modelo relacional** (E. F. **Codd**, **1970**): organiza los datos en **tablas** relacionadas.
  - **PK** (*Primary Key*, clave primaria): identifica cada registro de una tabla.
  - **FK** (*Foreign Key*, clave externa): relaciona una tabla con otra.
  - Se consulta con **SQL** (*Structured Query Language*). El libro de BI escribe "Standard Query Language"; el desarrollo habitual es *Structured Query Language*.
  - El **modelo entidad-relación** muestra las tablas y cómo se relacionan.
- **Orden de trabajo**: primero el modelo de negocio; después, **qué se mide (hechos)** y **desde qué perspectivas se analiza (dimensiones)**.
- **Hechos** = los valores que se miden. **Dimensiones** = las perspectivas desde las que se miran. Las dimensiones responden **qué, quién, por qué, dónde y cuándo**.
- **Tabla de hechos** (*fact table*): guarda lo que se mide (por ejemplo, el importe de cada ticket) y las claves de las dimensiones.
- **Tablas de dimensiones**: el contexto para agrupar y filtrar (tiempo, centro, empleado, forma de pago).
- **Dimensiones degeneradas**: no necesitan tabla propia (por ejemplo, el número de ticket o el identificador de caja).
- **Dimensión tiempo**: la fecha se descompone en día de la semana, del mes y del año, mes, trimestre, año, vacaciones y fin de semana. Esos datos (y los feriados) **no están** en el sistema transaccional: hay que agregarlos.

| | **Esquema estrella** | **Esquema copo de nieve** (*snowflake*) |
|---|---|---|
| Dimensiones | **Una tabla por dimensión**, desnormalizada | Dimensiones **normalizadas**, divididas en varias tablas relacionadas (por ejemplo, Zona separada de Centro) |
| Relaciones | Solo entre la tabla de hechos y cada dimensión | También entre dimensiones |
| Redundancia | Sí (la zona se repite en cada centro) | No |
| A favor | Más simple y más rápido de consultar | Ocupa menos espacio (a veces la diferencia es chica) |
| En contra | Ocupa más espacio | Es más complejo |

- **Constelación de hechos** (o esquema **galaxia**): varias tablas de hechos que comparten dimensiones.
- **Granularidad**: el **nivel de detalle** con que se guardan y analizan los datos. **Determina qué preguntas se pueden responder y cuáles no**, así que se decide con cuidado.
  - **Más granularidad = más detalle**: analizar **líneas** de ticket es más granular que analizar tickets.
  - **Cada vez que se agregan (suman) datos, se pierde información.**
  - Conviene construir el modelo con el **máximo detalle** que permita el volumen de datos.
- **Jerarquías**: año → trimestre → mes → día; familia → subfamilia → artículo; zona → centro. Permiten agregar (subir de nivel) y desagregar (bajar).
- **Multidimensionalidad**: analizar la información **por varias dimensiones a la vez** (por ejemplo, ventas de un artículo por centro y por mes). Permite mirar desde distintas perspectivas y períodos y descubrir relaciones y tendencias.
- Si dos atributos que se quieren cruzar (por ejemplo, fabricante y artículo) están en la misma dimensión, no se pueden cruzar: tienen que ir en dimensiones distintas.
- **Cada modelo de datos responde un número limitado de preguntas**, y modelos distintos responden preguntas distintas.

### 2.11 Fuentes de información y calidad de datos

**Fuentes de información**

- **Sistemas operacionales o transaccionales**: aplicaciones a medida, ERP, CRM (gestión de la relación con clientes), SCM (gestión de la cadena de suministro).
- **Sistemas departamentales**: previsiones, presupuestos, hojas de cálculo.
- **Fuentes externas**, a veces compradas: estudios de mercado, datos de población.
- La información puede ser **estructurada**, **semiestructurada** o **no estructurada** (correos, cartas, informes, videos).

**Calidad de datos**

- Si los datos del *datawarehouse* tienen errores, esos errores **llegan a toda la organización** y llevan a malas decisiones; además, los usuarios **dejan de confiar** en el proyecto.
- Los errores pueden venir de los **sistemas transaccionales**, del **proceso ETL** o del propio ***datawarehouse***. Conviene **corregirlos en el origen** (por ejemplo, que el usuario elija de una lista en vez de escribir libremente), no solo en el ETL.
- La calidad de datos es un **problema del negocio**, no solo de tecnología.
- **7 características** de los datos de calidad: **precisión, integridad, coherencia, totalidad, validez, disponibilidad y accesibilidad**.

### 2.12 Proceso ETL

- **ETL** (*Extract, Transform, Load*: extracción, transformación y carga) **recupera los datos de las fuentes y alimenta el *datawarehouse***.
- Consume **entre el 60 % y el 80 %** del tiempo de un proyecto de BI. Por eso es **costoso** y requiere recursos, estrategia, habilidades especializadas y tecnología.
- Tiene **5 subprocesos**:

| Subproceso | Qué hace |
|---|---|
| 1. **Extracción** | Obtiene los datos de las fuentes: datos **en bruto**. Se hace con rutinas propias (por ejemplo, en COBOL) o con herramientas ETL (la opción más rentable) |
| 2. **Limpieza** | Revisa la calidad, elimina duplicados, corrige errores y completa vacíos: datos **limpios** |
| 3. **Transformación** | Estructura y **resume** los datos según los modelos de análisis (cambios de formato, códigos, valores calculados y **agregados**). Acá se fija la **granularidad** |
| 4. **Integración** | Comprueba que los datos sean coherentes con las definiciones del *datawarehouse* y los carga (por ejemplo, que los totales de ventas coincidan con el origen) |
| 5. **Actualización** | Define **cada cuánto** se hacen las nuevas cargas |

- ***Data staging*** (almacén de datos intermedio): área de paso entre la extracción y las etapas siguientes, donde se limpian y se juntan los datos de varias fuentes. **Los usuarios finales nunca acceden.** No es un sexto subproceso: es el **lugar** donde ocurre la limpieza.
- **Datos "sucios"**: valores por defecto (por ejemplo, código 999), campos vacíos, valores crípticos o contradictorios, campos con varios usos, claves reutilizadas, identificadores que no son únicos.
- **Etapas de la limpieza**:
  1. **Depurar** (*parsing*): separar los datos en sus partes (por ejemplo, nombre y apellido).
  2. **Corregir** (*correcting*).
  3. **Estandarizar** (*standardizing*).
  4. **Relacionar** (*matching*): encontrar duplicados.
  5. **Consolidar** (*consolidating*): unir los registros que corresponden a lo mismo.

### 2.13 *Datawarehouse*, Data Mart y ODS

***Datawarehouse*** (almacén de datos)

- **Definición del resumen de cátedra**: base de datos **centralizada** que **integra la información estratégica** de toda la organización. Responde a la necesidad de tener información **consistente, integrada, histórica y preparada para ser analizada**. Toma datos de los sistemas **transaccionales, departamentales y externos** y los reúne en un entorno integrado.
- Usar hojas de cálculo en su lugar trae errores, trabajo repetido, "entornos paralelos" y **distintas versiones de la misma realidad**.
- **Hugh J. Watson**: "una colección de información creada para soportar las aplicaciones de toma de decisiones". ***Datawarehousing*** es el proceso completo: extraer, transformar y cargar los datos, y dar acceso a los usuarios.
- **Bill Inmon — 4 características**:
  - **Orientado a un área** (a un problema de negocio).
  - **Integrado** (medidas, códigos y formatos comunes).
  - **Indexado en el tiempo** (guarda la historia).
  - **No volátil** (los usuarios no lo modifican; se actualiza periódicamente).
- **Ralph Kimball**: da acceso a la información, es consistente, se puede separar y combinar por cada medida, incluye las herramientas de consulta y es "el lugar donde publicamos la información".
- Guarda los datos para **maximizar la flexibilidad, la facilidad de acceso y la administración**. Se actualiza en forma mensual, semanal o diaria. El concepto ***right time*** dice que cada situación de negocio necesita su propio plazo de actualización.

**Data Mart**

- **Definición**: estructura pensada para responder rápido a las necesidades de una **comunidad de usuarios** (un departamento, un nivel de la organización o un grupo con objetivos comunes), sobre **pocas áreas** (por ejemplo, marketing y ventas). Es **más chico** que el *datawarehouse*: menos datos, menos modelos y menos usuarios.
- Surgieron porque el *datawarehouse* corporativo era caro, lento de construir e inflexible.
- **Dependiente**: se alimenta del *datawarehouse* corporativo.
- **Independiente**: se alimenta directamente de las fuentes; puede mantener los **silos de información**.

**Estrategias de construcción**

| | **Inmon** | **Kimball** |
|---|---|---|
| Estrategia | Primero el *datawarehouse* **corporativo**, y de él salen los Data Marts (*top-down*) | Primero los **Data Marts** por área, sin un *datawarehouse* central (*bottom-up*) |
| A favor | Integrado y escalable | Barato y fácil de implementar; es la más usada |
| En contra | Caro, lento y con riesgo de fracaso | Riesgo de silos y de postergar la definición de criterios comunes |

Según Watson, **las dos son válidas** si se hacen bien. También existen las estrategias **híbrida** y **federada**.

**Metadata y ODS**

- **Metadata** o **diccionario de datos**: "información sobre la información": qué significa cada tabla y cada atributo, de dónde viene y cómo se transformó. Obliga a que toda la organización use **la misma terminología** (por ejemplo, "margen bruto" tiene que tener una sola definición).
- **ODS** (*Operational Data Store*, almacén de datos operacional): reúne datos de varias fuentes para decisiones **operativas** (del día a día). Su información es **volátil**, se actualiza en **tiempo real** y cubre como máximo dos o tres meses. Suele alimentar al *datawarehouse*, que en cambio es no volátil e histórico.

> **Ojo con "bodega de datos".** El video de la cátedra llama "bodegas de datos" a los Data Marts; el apunte de clase de minería usa "bodega de datos" para el *datawarehouse* (ver 3.18). Si aparece en el examen, aclarar a cuál se refiere.

### 2.14 OLAP

- **OLAP** (*On-Line Analytical Processing*, procesamiento analítico en línea) es la tecnología **más usada** para analizar la información de un *datawarehouse*. Permite el **análisis multidimensional**: explorar los datos desde distintas perspectivas y **agregarlos en distintos niveles de detalle**, desde el resumen total hasta el máximo detalle.
- **FASMI**: resumen de las 12 reglas de Codd hecho por el OLAP Council. Es la sigla de *Fast Analysis of Shared Multidimensional Information* (análisis rápido de información multidimensional compartida):
  - ***Fast***: rápido.
  - ***Analysis***: maneja la lógica del negocio y el análisis estadístico.
  - ***Shared***: compartido y seguro.
  - ***Multidimensional***.
  - ***Information***: maneja toda la información necesaria.
- Su representación gráfica es el **cubo**: cada celda guarda un **hecho** (por ejemplo, las unidades vendidas de un libro a un cliente en un año).

| Operación (términos de la cátedra) | Qué hace |
|---|---|
| **Rotar** (*slicing*) | Gira el cubo: cambia el orden de las dimensiones (por ejemplo, de clientes a libros) |
| **Seleccionar** (*dicing*) | Se queda con algunas celdas (por ejemplo, cliente 2, libros 1 y 2, año 1) |
| **Agregar** (*roll-up*) | Sube en la jerarquía hacia el resumen (por ejemplo, total de libros) |
| **Bajar al detalle** (*drill-down*) | Baja en la jerarquía (por ejemplo, de total de libros a libros por materia) |

> **Ojo con la terminología.** El libro llama *slicing* a rotar y *dicing* a seleccionar. En la bibliografía habitual, rotar es *pivot*, *slice* es fijar una dimensión en un valor y *dice* es elegir un subcubo. En el examen, responder con los términos de la cátedra y, si se quiere, aclarar los habituales.

| Tipo | Cómo accede a los datos | Ventaja | Desventaja |
|---|---|---|---|
| **ROLAP** (relacional) | Directo a la base relacional, normalmente sobre un esquema estrella; traduce las consultas a SQL | Sin límite de tamaño; más flexible | Más lento |
| **MOLAP** (multidimensional) | A una base multidimensional con los datos precalculados | Muy rápido; útil para soluciones chicas de un departamento | Si cambian las dimensiones, hay que recargar el cubo |
| **HOLAP** (híbrido) | Los datos agregados en la base multidimensional y el detalle en la relacional | Combina las ventajas de los dos | — |
| **DOLAP** (de escritorio) | Cubo cargado en la memoria de la computadora del usuario | El usuario recibe solo lo que le interesa | — |

- Alternativa al OLAP: herramientas de **lógica asociativa** (por ejemplo, QlikView), que guardan cada valor una sola vez y permiten consultar sin dimensiones definidas de antemano.

### 2.15 Herramientas de BI y visualización

**Herramientas fundamentales** (resumen de cátedra y video "¿Qué es el Business Intelligence?"):

| Herramienta | Para qué sirve |
|---|---|
| **Consultas e informes** | Acceder a información estructurada de forma **predeterminada** |
| **Cubos OLAP** | Visualización y análisis **multidimensional**: explorar desde distintas perspectivas y agregar en distintos niveles |
| **Minería de datos** | Descubrir **patrones ocultos, correlaciones y tendencias** en grandes volúmenes de datos |
| **Tableros de control** | Representar visualmente los **KPI** y los **objetivos estratégicos** |
| **Alertas** (excepciones) **y notificaciones** | Avisar **automáticamente** cuando un indicador se desvía de lo esperado |
| **Modelado y predicción** | **Anticipar** comportamientos futuros para decidir de forma **proactiva** |

El video también muestra para qué sirve BI: **mejorar la productividad**, crear **nuevos modelos de negocio** y que la organización **se conozca mejor a sí misma**.

**Clasificación del libro** (Eckerson y Howson, TDWI 2005):

1. **Generadores de informes**: los usan **desarrolladores profesionales** para crear informes estándar para grupos, departamentos o toda la organización.
2. **Herramientas de consultas e informes para el usuario final**: el usuario crea sus propios informes **sin programar**.
3. **Herramientas OLAP**: análisis multidimensional desde distintas perspectivas y períodos.
4. **Herramientas de *dashboard* y *scorecard***: muestran **de un vistazo** la información crítica de rendimiento, con íconos gráficos y la posibilidad de ver más detalle.
5. **Herramientas de planificación, modelización y consolidación**: crean planes de negocio y simulaciones (presupuestos, previsiones) y dan a los *dashboards* y *scorecards* los **objetivos y umbrales** de las métricas.
6. **Herramientas de minería de datos**: estadísticos o analistas crean **modelos estadísticos** para descubrir e interpretar patrones desconocidos (segmentación, venta cruzada, clasificación, previsiones, optimización).
7. Hoy se suman la **minería de texto** (información no estructurada) y la **visualización avanzada**.

***Dashboard* frente a *scorecard*** (los dos son "cuadros de mando"):

| | ***Dashboard*** | ***Scorecard*** |
|---|---|---|
| Nivel | **Operativo** o **táctico** | **Estratégico** |
| Indicadores | De áreas que **no tienen por qué estar relacionadas** | **Relacionados** entre sí |
| Alcance | Puede cubrir **solo una parte** de la organización | Suele cubrir **toda** la organización |
| Referente | — | El ***Balanced Scorecard*** de Robert Kaplan y David Norton (1992) |

**Visualización**: los resultados se muestran de forma numérica y gráfica, con hojas de cálculo, herramientas específicas o un navegador web. Dos tipos de sistemas específicos:

- **GIS** (*Geographic Information Systems*, sistemas de información geográfica): muestran los resultados **sobre un mapa**.
- **GDSS** (*Group Decision Support Systems*, sistemas de apoyo a la decisión en grupo): permiten que **un grupo** acceda a la información y decida en conjunto.

### 2.16 Usuarios de BI

- Conocer a los usuarios es **crítico para elegir la herramienta**: hay que saber **qué información consultan** y **qué funciones necesitan según su rol**. La clasificación es de W. W. Eckerson y C. Howson (TDWI).
- **Productores** de información (alrededor del **20 %**): estadísticos que usan minería de datos, autores de informes y usuarios avanzados.
- **Consumidores** (la mayoría): directivos, gestores, clientes y proveedores que usan cuadros de mando e informes, cada vez más por web.
- Se distinguen **roles, no personas**: el mismo directivo puede usar un informe fijo y un cuadro de mando en tiempo real.

### 2.17 Guías del TP7 — respuestas

| Pregunta | Respuesta modelo |
|---|---|
| ¿Cuál es la definición más ajustada de BI? | La de Gartner: proceso interactivo para explorar y analizar información estructurada de un área (normalmente en un *datawarehouse*) y descubrir tendencias o patrones. Convierte datos en información y conocimiento para decidir con hechos |
| ¿Cuándo conviene aplicar BI? | **De forma continua**, no una sola vez. Sobre todo cuando el mercado cambia rápido, cuando aparece algo raro en el negocio o cuando quienes preparan la información están desbordados |
| ¿A qué organizaciones va dirigida? | A cualquiera que tome decisiones. Es urgente en estructuras complejas, con muchos clientes o con procesos de información "artesanales" |
| ¿Qué beneficios aporta? | Tangibles, intangibles y estratégicos (2.4) |
| ¿Cómo se unifica información de distintos entornos? | Reuniéndola en un *datawarehouse* (una copia, sin afectar a los sistemas transaccionales), en tablas relacionadas, y cruzándola con herramientas de BI: "una sola versión de la verdad" |
| ¿Qué es y para qué sirve el modelo de negocio? | Una simplificación de la realidad para entender qué pasa en un área, documentar y probar teorías, ver qué pasa si se cambia algo y analizar dónde se genera el resultado. Ayuda a evitar los silos |
| ¿Qué es el modelo relacional? | Tablas y relaciones (Codd, 1970), con PK y FK, consultadas con SQL |
| ¿Qué factores influyen en el modelado de datos? | Partir del modelo de negocio; definir hechos y dimensiones; ver qué datos hay en los sistemas transaccionales y cuáles hay que agregar (calendarios, feriados) |
| ¿En qué se diferencian estrella y copo de nieve? | Ver la tabla de 2.10 |
| ¿Qué son la granularidad y la multidimensionalidad? | Granularidad: el nivel de detalle, que decide qué preguntas se pueden responder. Multidimensionalidad: analizar por varias dimensiones a la vez |

---

## 3. Minería de datos (Tema 9)

> **En una frase:** la minería de datos es **buscar de forma automática patrones escondidos** en grandes cantidades de datos, para **apoyar las decisiones** y **predecir**.

### 3.1 Qué es la minería de datos

- **Datos**: registros de observaciones o hechos. **Información**: lo que se obtiene al encontrarles utilidad a los datos. **Conocimiento**: reglas sobre cómo una cosa afecta a otra. "El conocimiento es poder."
- **Definición del resumen de cátedra**: la minería de datos es el **proceso de extracción de información y patrones de comportamiento que permanecen ocultos** en grandes cantidades de información. Descubre **relaciones, tendencias, desviaciones, comportamientos atípicos, patrones y trayectorias ocultas**, con el fin de **apoyar la toma de decisiones con más conocimiento**.
- **Definición de la lectura** (Beatriz Beltrán Martínez): métodos y algoritmos para la **extracción automática** de información resumida que caracteriza **relaciones escondidas** en grandes volúmenes de datos, idealmente con capacidad **predictiva**. Reúne técnicas **estadísticas** y de **aprendizaje automático** (inteligencia artificial).
- Otra definición de la lectura: **proceso analítico** para explorar grandes cantidades de datos con el objetivo de **detectar patrones consistentes o relaciones** entre variables y **aplicarlos a nuevos conjuntos de datos**.
- **Apunte de clase**: es la extracción de información o patrones **no triviales, implícitos, previamente desconocidos y potencialmente útiles**, por medios automáticos, para ayudar a decidir. Según la clase, BI es más estático: saca conclusiones de los datos estructurados que ya se tienen.
- **Origen del nombre**: una **montaña** (los datos de la empresa) con **diamantes** escondidos entre las piedras (el conocimiento valioso) que se encuentran haciendo "minería".
- Trabaja con **datos estáticos**: datos ya recolectados, que no cambian mientras se analizan.
- **No confundir con el monitoreo de datos**: el monitoreo trabaja con datos que cambian en **tiempo real** y **reconoce** patrones ya conocidos; la minería **descubre** patrones nuevos.

### 3.2 Evolución histórica

| Etapa | Pregunta típica | Tecnología | Característica |
|---|---|---|---|
| Recolección de datos (años 60) | Beneficios totales de los últimos 4 años | Computadoras, cintas, discos | **Retrospectiva** (mira al pasado), datos estáticos |
| Acceso a los datos (años 80) | Ventas en Cataluña la última Navidad | Bases relacionales (SQL), ODBC | Retrospectiva, datos dinámicos a nivel de registro |
| *Datawarehouse* y apoyo a las decisiones (años 90) | Ventas en Andalucía, bajando hasta el nivel de tienda | OLAP, bases multidimensionales, *datawarehouse* | Retrospectiva, datos dinámicos en varios niveles |
| **Minería de datos** | Tendencia de venta en Castilla el año próximo | Algoritmos avanzados, multiprocesadores, bases masivas | **Prospectiva** (mira al futuro) y **proactiva** |

Las tres primeras etapas responden **"¿qué pasó?"**; la minería responde **"¿qué va a pasar?"**. La minería está en el nivel más alto de esta evolución. Fue el *datawarehouse*, a fines de los años 80, el que resolvió la integración de los datos e impulsó la minería.

### 3.3 Proceso KDD

- **KDD** (*Knowledge Discovery in Databases*, descubrimiento de conocimiento en bases de datos): el término se usa desde **1989**.
- **Definición del resumen de cátedra**: el KDD es el **proceso amplio de encontrar conocimiento en los datos**, con énfasis en la aplicación de "alto nivel" de los métodos de minería. Es **interactivo e iterativo**, con muchos pasos y decisiones del usuario. Debe estar **precedido** por la comprensión del dominio, el conocimiento previo y los objetivos del usuario, y **continuado** por la **consolidación** del conocimiento.
- **Definición de descubrimiento de conocimiento**: extracción **no trivial** de información **implícita**, **previamente desconocida** y **potencialmente útil** a partir de un conjunto de datos.
- **Definición formal de la lectura**: dado un conjunto de **hechos H**, un **lenguaje L** y una **medida de certidumbre C**, una **regularidad** (*pattern*) es una sentencia S en L que describe relaciones dentro de un subconjunto de H con certidumbre C, y que es **más simple que enumerar todos esos hechos**. Una regularidad **interesante y bastante cierta** según los criterios del usuario es **conocimiento**. Cuando se extrae de una base de datos, el proceso es KDD.
- **El descubrimiento** es una **inducción no supervisada** de conocimiento, con dos procesos: **buscar regularidades interesantes** en los datos y **formular leyes** que las describan.

**Las cuatro ideas que distinguen al KDD**:

| Idea | Qué exige |
|---|---|
| **Lenguaje de alto nivel** | Que el conocimiento sea **entendible para una persona**. Por eso las representaciones de bajo nivel, como las de las **redes neuronales**, quedan fuera del KDD, aunque sean un método válido de minería |
| **Precisión** | Los datos tienen ruido; casi ningún conocimiento se cumple en todos los datos. Se mide el **grado de certidumbre**: si es bajo, el patrón no llega a ser conocimiento |
| **Interés** | Solo es conocimiento lo **nuevo, potencialmente útil y no trivial** según el usuario |
| **Eficiencia** | Algoritmos cuyo tiempo y memoria crezcan de forma **polinomial** con el tamaño de los datos |

- El KDD reúne varias disciplinas: aprendizaje automático, estadística, reconocimiento de patrones, inteligencia artificial, bases de datos, visualización, sistemas de apoyo a la decisión y recuperación de información.
- **KDD frente a minería de datos**: el **KDD es el proceso completo**; la **minería es una de sus etapas** (la que extrae los patrones). Es la parte fundamental, porque es la única que encuentra patrones, pero está **subordinada** al KDD. En la literatura muchas veces se usan como sinónimos, y eso confunde.
- **Por qué creció el análisis de datos** (tres razones):
  1. **Computadoras más potentes** y almacenamiento más barato.
  2. **Mucho más ritmo de adquisición de datos**: la información guardada en el mundo se duplica cada 20 meses.
  3. **Nuevos métodos** de aprendizaje y de representación del conocimiento.
- **Aprendizaje automático frente a minería**: el aprendizaje automático usa un conjunto de datos **chico y elegido** con cuidado; la minería parte de una base **grande**, cuyos datos se generaron **para otros fines**.

### 3.4 Etapas del KDD según cada fuente

La cantidad de etapas **depende de la fuente**. En el examen conviene **aclarar qué versión se usa**.

**Versión del resumen de cátedra** (dice "cinco etapas", pero enumera siete):

1. **Recolección de datos**: obtener la información que se quiere investigar.
2. **Selección**: crear el **conjunto de datos objetivo** o concentrarse en un subconjunto de variables o de muestras.
3. **Preprocesamiento o limpieza**: limpiar los datos objetivo para que sean **consistentes**.
4. **Transformación**: **reducir la dimensionalidad** (la cantidad de variables) u otros métodos de transformación.
5. **Minería de datos**: buscar **patrones de interés** con una forma de representación determinada.
6. **Interpretación y evaluación** de los patrones encontrados.
7. **Actualización y monitorización**: actualizar el modelo para que **siga siendo válido** y revalidarlo periódicamente con datos nuevos.

**Versión de Fayyad** (según el artículo de Azevedo y Santos) — **5 etapas**:

**selección → preprocesamiento → transformación → minería de datos → interpretación/evaluación**

**BD → (selección) → datos objetivo → (preprocesamiento) → datos preprocesados → (transformación) → datos transformados → (minería) → patrones → (interpretación/evaluación) → conocimiento**

**Versión de la lectura — 9 pasos** (proceso interactivo e iterativo):

| Bloque | Paso | Qué se hace |
|---|---|---|
| Preparar | 1. **Comprensión del dominio** | Entender el negocio, el conocimiento previo y qué quiere el usuario |
| | 2. **Creación del conjunto de datos objetivo** | Elegir variables y ejemplos; muestrear |
| | 3. **Preprocesado** | Eliminar ruido, tratar valores ausentes, normalizar |
| | 4. **Transformación y reducción** | Buscar características útiles y reducir variables. Es el **paso crítico**: suele decidir el éxito o el fracaso |
| Minar | 5. **Elección del tipo de sistema** | Clasificación, regresión, agrupamiento, detección de desviaciones |
| | 6. **Elección del algoritmo** | Con qué algoritmo buscar |
| | 7. **Minería de datos** | Buscar el conocimiento; su éxito depende de los pasos anteriores |
| Aprovechar | 8. **Interpretación** | Interpretar lo encontrado, con posibilidad de volver a cualquier paso anterior |
| | 9. **Consolidación** | Incorporar el conocimiento al sistema o documentarlo, resolviendo contradicciones con lo que ya se sabía |

**Versión de la lectura — 6 fases** (detalle en 3.5): recolección; selección, limpieza y transformación; minería; evaluación y validación; interpretación y difusión; actualización y monitorización.

**Equivalencias entre versiones**

| Fayyad (5) | Resumen de cátedra (7) | Lectura, 6 fases | Lectura, 9 pasos |
|---|---|---|---|
| (antes del KDD) | — | — | 1. Comprensión del dominio |
| — | 1. Recolección | 1. Recolección | — |
| Selección | 2. Selección | 2. Selección, limpieza y transformación | 2. Datos objetivo |
| Preprocesamiento | 3. Preprocesamiento | (incluido en la 2) | 3. Preprocesado |
| Transformación | 4. Transformación | (incluido en la 2) | 4. Transformación y reducción |
| Minería de datos | 5. Minería de datos | 3. Minería de datos | 5. Tipo de sistema · 6. Algoritmo · 7. Minería |
| Interpretación/evaluación | 6. Interpretación y evaluación | 4. Evaluación y validación · 5. Interpretación y difusión | 8. Interpretación |
| (después del KDD: consolidación) | 7. Actualización y monitorización | 6. Actualización y monitorización | 9. Consolidación |

Para una respuesta completa: escribir las 7 del resumen de cátedra y aclarar que Fayyad define 5 (sin recolección ni actualización), precedidas por la comprensión del dominio y seguidas por la consolidación.

### 3.5 Las 6 fases del KDD en detalle (lectura)

1. **Recolección de datos**: de fuentes internas y externas, muchas transaccionales. Conviene una fuente **unificada, accesible y separada** del trabajo transaccional. Depende de la fuente (**OLAP** u **OLTP**, *On-Line Transaction Processing*; *datawarehouse* o copia; **ROLAP** o **MOLAP**) y del tipo de usuario:
   - **Picapedreros o granjeros**: sacan informes periódicos y controlan valores.
   - **Exploradores**: buscan patrones nuevos.
   - Información externa posible: censos, datos de la industria, clima, calendarios, bases compradas.
2. **Selección, limpieza y transformación**: eliminar datos erróneos o contradictorios (**limpieza**) y datos irrelevantes (**criba**), casi siempre con métodos estadísticos (histogramas, muestreo vertical u horizontal, redefinición de atributos).
3. **Minería de datos**: se trabaja con datos en disco, muchísimas variables, evidencia positiva y datos imperfectos.
   - **Minería dirigida**: se sabe qué se busca (por ejemplo, predecir algo).
   - **Minería no dirigida**: no se sabe qué se busca.
4. **Evaluación y validación**:
   - Primera fase: medir la precisión con **ejemplos nuevos e independientes** de los usados para construir el modelo.
   - Segunda fase: una **prueba piloto** (por ejemplo, un envío de publicidad a un grupo de clientes).
5. **Interpretación y difusión**: según el caso, el modelo se **implementa** (detección de fraude con tarjetas en tiempo real), se **interpreta** (zonas geográficas) o se **difunde** (si cerveza y congelados se compran juntos, se ubican en estantes alejados para que el cliente recorra el local).
6. **Actualización y monitorización**: un modelo válido deja de serlo si cambia el contexto; hay que revalidarlo con datos nuevos.

### 3.6 KDD, SEMMA y CRISP-DM

- **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*): lo creó un **consorcio de empresas** (DaimlerChrysler, SPSS y NCR). Busca un proceso **confiable y repetible**, que pueda seguir gente con pocos conocimientos de minería. Tiene **6 fases**, en un orden **no rígido**: **comprensión del negocio**, **comprensión de los datos**, **preparación de los datos**, **modelado**, **evaluación** e **implantación** (despliegue).
- **SEMMA** (*Sample, Explore, Modify, Model, Assess*: muestrear, explorar, modificar, modelar, evaluar): lo creó el **SAS Institute**. Tiene **5 fases**; el muestreo es **opcional**.

| Eje | KDD | CRISP-DM | SEMMA |
|---|---|---|---|
| Origen | **Académico** (Fayyad) | **Consorcio de empresas**; ligado al *software* SPSS Clementine | **SAS Institute**; ligado a SAS Enterprise Miner |
| Fases | 5 en el núcleo de Fayyad (9 pasos en la lectura) | 6, en orden no rígido | 5 |
| Iteración | Muy iterativo: se puede volver desde cualquier fase | Ciclo con mucha retroalimentación | Más secuencial, con ajustes técnicos |
| Orientación al negocio | Empieza por el dominio; foco en la validez del conocimiento | **La más orientada al negocio** | Técnica: supone que los objetivos ya están definidos |
| ¿Incluye negocio y despliegue? | Sí (antes y después del núcleo) | Sí, de forma explícita | **No de forma explícita**; según Azevedo y Santos están implícitos, porque no se puede muestrear sin entender el negocio |

**Equivalencia de fases según el artículo de la cátedra** (Azevedo y Santos, "KDD, SEMMA and CRISP-DM: a parallel overview"):

| KDD | SEMMA | CRISP-DM |
|---|---|---|
| Antes del KDD (comprensión del dominio) | — | Comprensión del negocio |
| Selección | *Sample* | Comprensión de los datos |
| Preprocesamiento | *Explore* | Comprensión de los datos |
| Transformación | *Modify* | Preparación de los datos |
| Minería de datos | *Model* | Modelado |
| Interpretación/evaluación | *Assess* | Evaluación |
| Después del KDD (consolidación) | — | Despliegue |

- **Conclusión del artículo**: SEMMA y CRISP-DM son **implementaciones del proceso KDD**. CRISP-DM parece más completo, pero SEMMA también incluye, de forma implícita, el negocio y la consolidación.
- **Corrección al TP8**: el cuadro del grupo puso "preparación de los datos" junto al preprocesamiento. Según el artículo, el preprocesamiento corresponde a **comprensión de los datos** y la transformación a **preparación de los datos**.

### 3.7 Datos atípicos y faltantes

**Atípicos** (*outliers*) = valores muy alejados del resto. **Faltantes** (*missing values*) = valores que no están.

| Acción | Con atípicos | Con faltantes |
|---|---|---|
| **Ignorar** | Usando algoritmos robustos (por ejemplo, árboles) | Usando algoritmos robustos (por ejemplo, árboles) |
| **Filtrar la columna** | Solución extrema; mejor reemplazarla por una columna "normal / atípico" | Solución extrema; mejor una columna "existía / no existía" |
| **Filtrar la fila** | **Sesga los datos** (los atípicos suelen ser casos especiales) | **Sesga los datos** |
| **Reemplazar el valor** | Por nulo, máximo, mínimo o media; o predecirlo | Por la media; o predecirlo |
| **Discretizar** | Pasar a rangos (muy alto, alto, medio, bajo, muy bajo): el atípico cae en un extremo | — |
| **Segmentar** | — | Un modelo por grupo según los datos disponibles, y después se combinan |
| **Esperar** | — | Mejorar la calidad de la carga y esperar a tener los datos |

**Por qué faltan datos**:

- **Relevantes**: que falte el dato dice algo (no dar el teléfono puede significar que no quiere ser molestado).
- **No existentes**: no puede haber dato (un cliente nuevo no tiene 12 meses de consumo).
- **Incompletos**: se perdieron al unir fuentes distintas.

### 3.8 Qué no es minería de datos y cuáles son sus retos

**No es estadística**:

| Eje | Minería de datos | Estadística clásica |
|---|---|---|
| Automatización | Construye el modelo **automáticamente** | La maneja un **estadístico profesional** |
| Enfoque | **Exploratorio**: busca | **Confirmatorio**: prueba hipótesis planteadas antes |
| Inteligencia artificial | La usa | Se basa en la teoría de la probabilidad |
| Cantidad de variables | Funciona bien con **muchas variables** | Le cuesta encontrar hipótesis con muchas variables |
| Supuestos | **Menos exigente** | Los datos tienen que cumplir ciertos requisitos |

Apunte de clase: la estadística toma **muestras** y saca conclusiones sobre la población; la minería trabaja con **toda la base** (y usa estadística).

**No es OLAP**: OLAP **navega** rápido por los datos (análisis multidimensional), pero **no genera información nueva**. Sus arquitecturas (ROLAP, MOLAP y otras) están en 2.14.

**Los tres retos**:

1. **Falsa interpretación**: es fácil engañarse con la estadística (sus resultados valen para grupos, no para individuos). Con *software* de minería es todavía más fácil "hacer creíble una falsedad".
2. **Correlación no es causalidad (el caso de Florida)**: en Florida la edad promedio al morir es la más alta de Estados Unidos. Eso no significa que vivir ahí alargue la vida: ahí se mudan muchos jubilados (**efecto de selección**). La minería **genera hipótesis** a partir de los datos (es **exploratoria, no explicativa**), y esas hipótesis hay que validarlas con datos nuevos. Además, no puede hacer experimentos.
3. **Tiempo, espacio y privacidad**:
   - Hay variables que cambian durante el período analizado.
   - **Granularidad del tiempo**: con datos mensuales no se puede predecir por semana.
   - **Privacidad**: si se cruzan las bases del teléfono, del banco y del supermercado, se arma un perfil completo de una persona. El marco legal no avanzó al mismo ritmo.

### 3.9 Tareas de la minería de datos

La minería ajusta **modelos** o encuentra **patrones** en los datos (es un ajuste estadístico: admite ruido o error). Sus dos metas son la **predicción** (estimar datos desconocidos) y la **descripción** (encontrar patrones).

| Tarea | Qué hace | Tipo |
|---|---|---|
| **Clasificación** | Asigna cada dato a una de varias **clases definidas de antemano** | Supervisada / predictiva |
| **Regresión** | Asigna a cada dato un **valor real** (continuo) | Supervisada / predictiva |
| **Agrupamiento** (*clustering*) o identificación de clases | Encuentra grupos o categorías que describen los datos, sin saber de antemano cuáles son | No supervisada / descriptiva |
| **Condensación** (descripción de conceptos) | Encuentra una **descripción compacta** de un subconjunto de datos | No supervisada / descriptiva |
| **Detección de desviaciones** (casos extremos, anomalías) | Encuentra los **cambios más significativos** respecto de valores pasados o normales | No supervisada / descriptiva |
| **Modelado de dependencias** | Encuentra las **dependencias significativas** entre variables, a nivel **estructural** (qué depende de qué) y **cuantitativo** (con qué fuerza) | No supervisada / descriptiva |

### 3.10 Proceso de minería de datos (4 estados)

1. **Procesado de los datos**: los datos casi nunca vienen en el formato ideal. Se filtran valores incorrectos o desconocidos, se muestrea y se reduce la cantidad de valores posibles.
2. **Selección de características**: se reduce el tamaño de los datos quedándose con las **variables que más influyen**, sin perder calidad.
3. **Algoritmo de extracción de conocimiento**: una técnica de minería obtiene un **modelo de conocimiento** (patrones o asociaciones).
4. **Interpretación, evaluación y validación**: se comprueba que las conclusiones sean válidas; se comparan modelos; si ninguno sirve, se vuelve a los pasos anteriores.

### 3.11 Modelos predictivos y descriptivos

| | **Predictivos** (algoritmos **supervisados**) | **Descriptivos** (algoritmos **no supervisados**) |
|---|---|---|
| Qué responden | Preguntas sobre **datos futuros**: predicen el valor de un atributo (**etiqueta**) a partir de otros conocidos | **Tendencias y patrones** en los datos actuales |
| Cómo aprenden | De datos con etiqueta conocida, en dos fases: **entrenamiento** (con un subconjunto etiquetado) y **prueba** (con el resto) | Sin etiqueta; se usan cuando todavía no se puede plantear una predicción |
| Técnicas según el resumen de cátedra | Clasificación (o *scoring*), regresión, previsión, predicción secuencial e interpolación | Agrupamiento, asociación, secuenciamiento, detección de desviaciones, condensación, modelado de dependencias y reconocimiento de patrones |

### 3.12 Taxonomía de las técnicas (lectura)

**Verificación frente a descubrimiento**:

- **Minería dirigida a la verificación**: el usuario **plantea una hipótesis** y la comprueba con los datos (con SQL, herramientas de consulta u OLAP).
- **Minería dirigida al descubrimiento**: se encuentra información **sin plantear antes una hipótesis**. Es mucho más eficiente en bases grandes y complejas. El descubrimiento se divide en **descripción** (visualización, agrupamiento, asociación, condensación) y **predicción** (clasificación y regresión).

**Formas de un problema de aprendizaje inductivo**:

| Forma | Qué es |
|---|---|
| **Interpolación** | Encontrar una **función continua** sobre varias dimensiones |
| **Predicción secuencial** | Las observaciones están **ordenadas** y se quiere predecir el **siguiente valor** |
| **Aprendizaje supervisado** | Cada observación tiene su **clase**, y se aprende un **clasificador** |
| **Aprendizaje no supervisado** | Las observaciones **no tienen clase**; se buscan regularidades: grupos, asociaciones, casos anómalos |
| **Abducción** o **aprendizaje analítico** | El conocimiento previo es muy importante; se busca **explicar la evidencia** a partir de ese conocimiento |

**Variantes del aprendizaje supervisado**:

- **Clasificación**: las clases son **disjuntas** (cada dato pertenece a una sola). **Categorización**: las clases **pueden superponerse**.
- Según el tipo de clase:
  - Clase **discreta** → **clasificación** (por ejemplo, el grupo sanguíneo a partir del de los padres).
  - Clase con **solo dos valores** (verdadero o falso) → ***concept learning*** (por ejemplo, si un compuesto químico es cancerígeno).
  - Clase **continua** o discreta ordenada → **estimación** (por ejemplo, la cantidad de hijos de una familia).

### 3.13 Técnicas descriptivas (no supervisadas)

- **Correlación**: mide cuánto varían juntas dos variables numéricas: **Cor(x, y) = Cov(x, y) / (σx · σy)**. Los **estudios factoriales** dicen si un factor es relevante y si su efecto es positivo o negativo.
- **Asociación**: dos atributos discretos tienden a aparecer juntos (por ejemplo, tabaquismo y alcoholismo). Si de n casos los dos coinciden en rc, su fuerza es **rc / n**.
- **Dependencia de valor** o **regla de asociación** (si antecedente, entonces consecuente): de n casos, el antecedente se cumple en ra y, de esos, el consecuente en rc.
  - **Confianza** = **rc / ra**: probabilidad del consecuente dado el antecedente. Mide la **fuerza** de la regla ("¿qué tan seguido se cumple cuando se da el antecedente?").
  - **Soporte** = **rc** o **rc / n**: cantidad o porcentaje de casos en los que se aplica la regla ("¿qué tan común es?").
- **Algoritmo de dos fases** (tipo **Apriori**):
  - **Fase A**: buscar los conjuntos de atributos frecuentes (*large itemsets*), es decir, los que tienen **soporte** suficiente.
  - **Fase B**: dividir cada conjunto en antecedente y consecuente, calcular la **confianza** y quedarse con las reglas que superan el mínimo.
- **Otros tipos de asociaciones**: entre **jerarquías** (por ejemplo, familias de productos); **negativas** ("el 80 % de quienes compran pizza congelada no compra lentejas"); con valores **continuos** (primero se pasan a rangos).
- **Patrones secuenciales**: asociaciones en las que el **tiempo** importa (algoritmos AprioriAll, AprioriSome, DynamicSome). Los usuarios suelen pedir restricciones de tiempo mínimo o máximo entre eventos.
- **Dependencias funcionales**: A ∧ B ∧ C ⇒ D significa que, para los mismos valores de A, B y C, D tiene un único valor (D es función de A, B y C). Buscarlas tiene un costo **exponencial**.
- **Agrupamiento** (*clustering*): algoritmos **k-means**, redes de **Kohonen**, **EM**, **Cobweb** y **AutoClass**.

### 3.14 Técnicas predictivas (supervisadas)

- **Regresión**:
  - **Lineal global**: busca una sola recta (o hiperplano) **f(x) = w0 + w1·x1 + … + wn·xn** para todos los datos, minimizando la suma de los errores al cuadrado.
  - **Lineal ponderada localmente**: aproxima la función alrededor de cada punto usando los **k puntos más cercanos**, dando más peso a los más próximos. Con k grande se vuelve más global; con k chico, más local.
  - **No lineal**: por ejemplo, la estimación **logarítmica** (se aplica logaritmo, se hace regresión lineal y se vuelve con la exponencial).
  - **Adaptativa**: predice los valores futuros de una serie (se usa, por ejemplo, para comprimir sonido y video).
- **k-NN** (*k Nearest Neighbors*, k vecinos más cercanos): para clasificar un caso nuevo se miran los **k casos más parecidos**. Si todos son de la misma clase, el caso nuevo es de esa clase; si no, se elige por la distancia media a cada clase o por la clase con más vecinos. El valor de k se elige por prueba y error.
- **Perceptrón**: calcula una **función lineal** de las entradas y ajusta los pesos según el error de cada predicción. La **tasa de aprendizaje** (alrededor de 0,05) regula cuánto cambia cada vez: si es más grande, aprende más rápido pero puede quedar atrapado en mínimos locales.
- **Perceptrón multicapa** (redes neuronales artificiales): el perceptrón de una capa no aprende funciones no lineales, así que se agregan **capas internas** con una función de activación continua (la **sigmoide**). Se entrena con ***backpropagation***.
- **RBF** (*Radial Basis Function*, función de base radial): primero agrupa los datos con k-means, después expresa cada ejemplo como su distancia a los centros de los grupos y finalmente aplica un perceptrón.
- **Combinación de hipótesis**:
  - ***Boosting***: el **mismo** algoritmo sobre **distintas partes** de los datos.
  - ***Voting***: **distintos** algoritmos sobre **todos** los datos.

### 3.15 Métodos y técnicas de minería de datos

**Criterios para clasificar los sistemas de minería**:

- Por el **objetivo**: clasificación, regresión, agrupamiento, compactación, modelado de dependencias, detección de desviaciones.
- Por el **paradigma**: **conexionistas** (redes neuronales), **evolucionistas** (algoritmos genéticos) y **simbólicos**.
- Por el **lenguaje de representación**: lógica de proposiciones, lógica de predicados de primer orden, representaciones estructuradas, ejemplos o representaciones no simbólicas (redes neuronales).

**Los 8 métodos**:

| Método | Qué hace |
|---|---|
| **Agrupamiento** o segmentación | Encuentra grupos de elementos parecidos entre sí y distintos de los de otros grupos. Puede ser **estático** (valores en un momento) o **dinámico** (comportamiento a lo largo del tiempo) |
| **Asociación** | Encuentra relaciones entre sucesos que parecen independientes: cómo la ocurrencia de uno induce a otros |
| **Secuenciamiento** | Como la asociación, pero el **tiempo** es la variable clave: cómo una acción desencadena otras a lo largo del tiempo |
| **Reconocimiento de patrones** | Asocia una señal de entrada con la más parecida de las ya catalogadas |
| **Previsión** (*forecasting*) | Estima el comportamiento futuro más probable según la evolución pasada y presente (series temporales) |
| **Simulación** | Genera muchos escenarios para analizar si una decisión o un prototipo es adecuado (por ejemplo, en CAD-CAM) |
| **Optimización** | Maximiza o minimiza una función de varias variables con restricciones (más beneficio, menos costo) |
| **Clasificación** (*scoring*) | Asigna un elemento a una clase según sus atributos; si asigna un valor numérico, se llama predicción o evaluación |

Para una solución completa suele hacer falta **combinar varios métodos**.

| Técnicas supervisadas | Técnicas no supervisadas |
|---|---|
| Árboles de decisión | Detección de desviaciones |
| Inducción neuronal | Segmentación |
| Regresión | Agrupamiento (*clustering*) |
| Series temporales | Reglas de asociación |
| | Patrones secuenciales |

**Técnicas**:

- **Estadísticas**:
  - **ANOVA** (análisis de la varianza): ¿los promedios de varios grupos son distintos?
  - **Ji cuadrado**: ¿dos variables son independientes?
  - **Componentes principales**: reduce la cantidad de variables.
  - **Análisis de *clusters***: arma grupos.
  - **Análisis discriminante**: clasifica en grupos ya definidos.
  - **Regresión lineal** (la más básica; para variables continuas) y **regresión logística** (admite variables discretas).
- **Árboles de decisión**: dividen los datos en grupos cada vez más chicos según el valor de los atributos.
  - **CART**: cada nodo se divide en **2** ramas (usa validación cruzada y el índice de Gini).
  - **CHAID** (*Chi Squared Automatic Interaction Detector*): cada nodo se divide en **más de 2** ramas (usa la prueba de Ji cuadrado).
- **Reglas de asociación**: análisis de la "cesta de la compra"; reglas del tipo SI … ENTONCES.
- **Redes neuronales**: inspiradas en el cerebro, con capas de neuronas que aprenden patrones; pueden ser supervisadas o no. Su problema es que **no dan una ecuación que explique el modelo**: son una **caja negra**.
- **Algoritmos genéticos**: usan mutación y cruce, como la evolución, para **optimizar**; suelen usarse al principio para **elegir las variables**.
- **Lógica difusa**: los grupos tienen bordes graduales, no cortes exactos.
- **Series temporales**: usan ciclos, tendencias y estacionalidades para predecir, siempre que no haya cambios de fondo.
- **Redes bayesianas**: aprenden dependencias y relaciones de causa, combinan conocimiento previo con datos, evitan el sobreajuste y manejan datos incompletos.
- **Inducción de reglas** y **sistemas expertos** (con un motor de inferencia).

### 3.16 Evaluación de la minería de datos

- Lo mínimo que se le pide a un modelo es que **beneficie al negocio** de forma visible: más ingresos, menos costos o mejor ROI.
- **Tres medidas clave** para evaluar una herramienta de minería: **precisión** (¿acierta?), **explicación** (¿se entiende cómo funciona?) e **integración** (¿se incorpora al proceso de negocio sin copiar los datos?). Si cumple las tres, los modelos rinden bien y duran.

| Medida de precisión | Qué es |
|---|---|
| **Precisión** | Porcentaje de predicciones correctas |
| **Tasa de error** | El complemento de la precisión. Es útil cuando la precisión es muy alta: pasar de 99 % a 99,5 % de precisión **reduce el error a la mitad** |
| **Tasa de error en rechazo** | Se descartan las predicciones menos confiables; rechazando el 80 % se puede duplicar la precisión |
| **Error cuadrático medio** | Para variables continuas: promedio de (predicción − valor real)². Pesa más los errores grandes |
| **Elevación** (*lift*) | Cuánto aumenta el modelo la proporción de respuestas respecto de elegir al azar: **proporción de respuestas con el modelo / proporción sin el modelo**. Ejemplo: si al azar responde el 10 % y en el grupo elegido por el modelo responde el 30 %, la elevación es 30 / 10 = **3** |
| **Beneficio / ROI** | La mejor medida: cuánto gana el negocio con el modelo |

- **Cómo se mide la explicación**: generación automática de reglas que expliquen el modelo; resultados disponibles dentro del entorno OLAP; evaluación automática del modelo (con un conjunto de prueba o con validación cruzada).
- **Cómo se mide la integración**: usar los datos tal como están (sin extractos propios); guardar el modelo como metadatos; preprocesar los predictores automáticamente; aceptar distintos tipos de datos; manejar datos sucios y valores perdidos; y tener **escalabilidad** (funcionar con bases grandes y chicas).

### 3.17 Apuntes de clase (14/9)

- **Aplicaciones**: retener clientes, encontrar patrones de compra, detectar fraude, manejar el riesgo (a quién prestarle) y segmentar.
- **Ciclo de un proyecto de minería** (9 pasos): aprender sobre el negocio → recolectar los datos → limpiarlos y transformarlos → definir la meta y el modelo → elegir los algoritmos → generar reportes → generar predicciones → aplicar los resultados → actualizar los modelos.
- **Minería frente a análisis de datos**: el análisis de datos no suele ser automático ni manejar tanto volumen.
- **Minería frente a aprendizaje automático**: el aprendizaje automático es el área de la inteligencia artificial que crea programas que aprenden; la minería lo usa para predecir.

### 3.18 Bodega de datos y relación con BI (apunte de clase)

- **Bodega de datos**: base de datos pensada para consultas, **consolidada, consistente, orientada a un tema, histórica y de solo lectura**. Es el punto de partida de la minería y no cambia mientras se mina. Es lo que en BI se llama *datawarehouse* (ver 2.13).

### 3.19 Preguntas teóricas del TP8 (respuestas del grupo)

| Consigna | Respuesta clave |
|---|---|
| 1. Los 9 pasos con su insumo y su producto; qué pasa si falla el preprocesado | Cada paso usa lo que produjo el anterior. Si falla el **preprocesado**, el modelo aprende el ruido como si fuera un patrón, los faltantes mal tratados sesgan la muestra y los atípicos distorsionan el resultado. La evaluación puede parecer buena si los datos de prueba tienen el mismo defecto. El modelo no sirve |
| 2. La minería es fundamental pero está subordinada al KDD | "Minería sin KDD es una operación algorítmica **ciega**": no sabe qué buscar, con qué calidad de datos ni si lo encontrado es válido. "KDD sin minería es un proceso **inconcluso**": quedan datos limpios, pero sin patrones |
| 3. Minería frente a estadística; el caso de Florida | Ver 3.8 |
| 4. Minería, OLAP y monitoreo | La minería **genera** información nueva sobre datos **estáticos** (descubre; es proactiva). OLAP **navega** sobre datos históricos resumidos cuando el usuario consulta (*drill-down*, *roll-up*, *slice & dice*). El monitoreo **verifica** datos en **tiempo real** y reacciona con alertas |
| 5. Mapa de tareas | Supervisadas: clasificación y regresión. No supervisadas: agrupamiento, modelado de dependencias, detección de desviaciones y condensación |
| 6. Redes neuronales y lenguaje de alto nivel | Predicen bien, pero el conocimiento queda guardado en miles de **pesos numéricos**: son una **caja negra** que no se puede explicar. Eso choca con la exigencia del KDD de que el conocimiento sea entendible |
| 7. Faltantes y atípicos, y el sesgo de cada solución | Ver 3.7: filtrar filas **sesga** los datos; reemplazar por la media **reduce la varianza**; discretizar **pierde precisión**; segmentar puede **sobreajustar** |
| 8. Ensayo sobre escalabilidad, tiempo y privacidad | Más potencia de *hardware*, más detalle temporal y más fuentes cruzadas permiten perfiles cada vez más precisos de cada persona. Marco legal: Ley 25.326 de Protección de Datos Personales (Argentina) y GDPR (Reglamento General de Protección de Datos, Unión Europea) |
| 9. KDD, CRISP-DM y SEMMA | Ver 3.6 |

---

## 4. Big Data (Tema 10, entra en el final)

> **En una frase:** Big Data es **la forma de manejar datos tan grandes, rápidos y variados** que los sistemas tradicionales no pueden procesarlos.

### 4.1 Conceptos

- **Definición** (apunte de clase): ecosistema o paradigma para **capturar, almacenar y analizar** datos de **gran volumen, velocidad y variedad**, que superan lo que manejan los sistemas tradicionales. Es la base sobre la que se construyen el análisis y la estrategia.
- **Las 3 V**:
  - **Volumen**: muchísimos datos.
  - **Velocidad**: llegan muy rápido.
  - **Variedad**: de todo tipo (texto, imágenes, sensores, redes sociales).
- La guía de PowerData aclara que **lo importante no es el tamaño**: el volumen es solo una parte. Las empresas quieren saber no solo qué pasa, sino **qué va a pasar**, y lo más cerca posible del **tiempo real**.
- **Por qué importa**: transforma la industria, el negocio y la sociedad, y da **ventaja competitiva**. Hoy puede ser más valioso encontrar al **cliente que más influye** sobre otros que al que más compra.
- **Nace de tres necesidades nuevas del mercado**:
  1. La **personalización máxima** del trato con el cliente.
  2. El paso **de la transacción a la interacción**.
  3. Los **nuevos dispositivos** (celulares, domótica, autos con sensores).

### 4.2 Big Analytics y metodología MAD

- **Big Analytics**:
  - Hace análisis **predictivo** y **clusterización** (agrupamiento) de clientes.
  - Trabaja con **datos en crudo**, al **mayor nivel de detalle**, con modelos más ágiles.
  - Lo manejan el **Data Scientist** y el **Data Analyst** (aparece el perfil de **Data Science**).
  - Viene del **BI tradicional y el *data warehouse***, cuyos límites eran los **modelos rígidos, poco ágiles y sin tiempo real**: cargar los modelos llevaba tanto tiempo que, al terminar, ya no servían.
  - Se apoya en el **Analytic Data Warehouse** (ADW). El ADW **no reemplaza** al *data warehouse*: cada uno cubre necesidades distintas y **conviven** en un **modelo híbrido DWH + ADW**.
- **Metodología MAD**:
  - **Magnética**: atrae todo tipo de datos.
  - **Ágil**: los incorpora y se adapta rápido.
  - **Detallada**: permite un análisis estadístico fino.

### 4.3 Hadoop

- **Origen**: **Google** no podía indexar la web tan rápido como hacía falta y aplicó **"divide y vencerás"**: muchas computadoras chicas, cada una procesa una parte, pero funcionan como una sola. En **2006** la comunidad de **código abierto** desarrolla Hadoop; después lo impulsa **Yahoo** y lo adoptan empresas como **Facebook**.
- **Tiene dos partes**:
  - **HDFS** (*Hadoop Distributed File System*, sistema de archivos distribuido de Hadoop): **guarda** los archivos repartidos en muchas máquinas.
  - **MapReduce**: **procesa** los datos en paralelo.
- Es **código abierto** y usa ***commodity hardware*** (equipos comunes y baratos).
- Permite, por ejemplo, hacer una regresión lineal sobre millones de registros históricos con un **ROI muy rápido**.

### 4.4 Megatendencias y tiempo real

- **4 megatendencias**:
  - **Movilidad**: acceso a los datos desde cualquier lugar y desde dispositivos que no son de la empresa (más difícil de controlar).
  - **Cloud**: no hace falta comprar la infraestructura; baja la inversión inicial y se puede **prever el costo de crecer**.
  - **Social Media**: gustos y preferencias de las personas para captar y fidelizar clientes.
  - **Analytics**: analizar cualquier tipo de dato, sin patrones de búsqueda fijos.
- **Tiempo real**:
  - ***Data Stream***: analiza **datos en movimiento**, mientras llegan.
  - **CEP** (*Complex Event Processing*, procesamiento de eventos complejos): **detecta eventos definidos de antemano**. Ejemplos de la guía: un banco que vigila en tiempo real lo que pasa con las **tarjetas de crédito** en cajeros y comercios; **sensores de maquinaria** que avisan antes de que se produzca una falla.

### 4.5 Implementación y privacidad

- **Cómo implementarlo**:
  1. Primero **conocer y medir el valor** que puede dar al negocio (revisar límites, expectativas y restricciones).
  2. **Las metas eligen la tecnología**, no al revés: para eventos en tiempo real, **CEP**; para análisis predictivo sobre todo el histórico, bases **MPP** (*Massively Parallel Processing*, procesamiento masivamente paralelo).
  3. Contar con perfiles que conozcan el negocio (Data Scientist, Data Analyst).
  4. Elegir herramientas según el tipo de análisis.
- **Privacidad**: en Google "no todo es gratis": el precio es la privacidad. Las empresas tienen que equilibrar los datos que analizan con lo que sus clientes **toleran**.
- **En síntesis**: Big Data **genera** innovación y ventaja competitiva, pero **plantea** el desafío de la **seguridad y la privacidad**.

### 4.6 BI, minería de datos y Big Data

| Aspecto | BI | Minería de datos | Big Data |
|---|---|---|---|
| Qué es | Procesos y herramientas que convierten datos en información para decidir | Descubrimiento de patrones, relaciones y tendencias ocultas | Paradigma para capturar, almacenar y analizar datos masivos |
| Pregunta central | ¿Qué pasó y cómo vamos? | ¿Qué patrones hay en los datos? | ¿Qué va a pasar y qué se descubre con todos los datos? |
| Enfoque temporal | Pasado y presente | Datos pasados, para descubrir y predecir | Presente y futuro, en tiempo real |
| Tipo de datos | Estructurados, internos | Estructurados y semiestructurados, ya preparados | Estructurados, semiestructurados y **no estructurados** (redes, sensores, registros de sistemas) |
| Volumen | Moderado (lo que soporta un *datawarehouse*) | De moderado a grande | **Masivo**, con infraestructura distribuida |
| Técnicas | Consultas, reportes, tableros, OLAP, KPI | Clasificación, agrupamiento, asociación, regresión, detección de anomalías | Big Analytics, MapReduce, Data Stream, CEP |
| Tecnología | *Datawarehouse*, ETL, *reporting* | Algoritmos estadísticos y de aprendizaje automático | Hadoop, ADW, *cloud*, bases MPP |
| Perfil | Gerentes y analistas de negocio | Analistas de datos, estadísticos | Data Scientist, Data Analyst |
| Resultado | Informes y tableros | Modelos y patrones | Conocimiento nuevo y servicios personalizados casi en tiempo real |
| Limitación | Poco ágil, sin tiempo real | Depende de la calidad de los datos | Infraestructura nueva, perfiles caros, riesgos de privacidad |

**Matriz de la clase** ("Ingeniería de datos"):

| | Big Data | Minería de datos | BI |
|---|---|---|---|
| Fin principal | Almacenar y procesar datos a escala masiva | **Descubrir patrones** | **Optimizar las decisiones** de la empresa |
| Tipo de datos | **Crudos** y variados | **Consolidados** | **Estructurados y depurados** |
| Perfil | **Ingeniero de datos** | **Científico de datos** | **Analista de BI** o consultor |
| Foco temporal | **Presente continuo** | **Futuro predictivo** | **Pasado y presente**, descriptivo |

- **Cadena de la clase**: **Big Data** reúne y procesa los datos → la **minería** encuentra patrones → **BI** los convierte en indicadores y decisiones.
- **No compiten**: conviven en un **modelo híbrido**. BI mira hacia atrás; Big Data apunta hacia adelante; la minería se aplica tanto sobre un *datawarehouse* como sobre Big Data.
- El TP dice que la minería mira al "pasado" y la clase dice "futuro predictivo". Las dos cosas son ciertas: la minería **analiza datos pasados para predecir el futuro**.

---

## 5. Repaso final

### 5.1 Datos para memorizar

| Dato | Valor |
|---|---|
| Creador de las Redes de Petri | **Carl Adam Petri** (Alemania), tesis de **1962**: *Kommunikation mit Automaten* |
| Holt y Commoner | **1970**, "Events and Conditions": aplican las RdP a sistemas concurrentes |
| Definición formal | **RdP = (P, T, I, O)**, con P y T finitos, no vacíos y disjuntos |
| Red marcada | **(RdP, M0)**; la lectura escribe M = (C, μ) |
| Ecuación de disparo | **Mj(p) = Mi(p) + O(t, p) − I(p, t)** |
| Matriz de incidencia | **C = C⁺ − C⁻**; filas = transiciones, columnas = lugares |
| Transición habilitada (método matricial) | **M ≥ ej · C⁻** |
| Ecuación de estado | **M' = M + f(σ) · C** (f(σ) = cuántas veces se dispara cada transición) |
| Red segura | **1-acotada** (binaria) |
| ω en el árbol | La red **no es acotada** |
| Marcados frontera | Muerto, duplicado o con ω |
| Subclases de RdP | **4**: máquina de estados, grafo marcado, red de libre elección, red simple |
| Modelos de redes | **4**: ruta más corta, árbol de expansión mínima, flujo máximo, flujo de costo mínimo |
| Término "Business Intelligence" | Lo acuñó y popularizó **Howard Dresner** (Gartner) |
| BI según Gartner | Proceso **interactivo** para **explorar** y **analizar** información **estructurada** de un **área**, normalmente en un *datawarehouse* |
| Componentes de un proyecto de BI | **6**: problema, equipo, información interna, información externa, *datawarehouse*, aplicación de BI |
| Herramientas fundamentales de BI | **6**: consultas e informes, cubos OLAP, minería de datos, tableros de control, alertas y notificaciones, modelado y predicción |
| ROI simple | Valor para el negocio / costo del proyecto |
| ROI completo | **NPV / inversión inicial × 100** |
| Requisitos de un KPI | **4**: reflejar objetivos, ser crítico, cuantificable y comparable, permitir acciones correctivas |
| Proceso ETL | **60 % a 80 %** del tiempo de un proyecto de BI; **5 subprocesos** |
| Datos de calidad | **7 características**: precisión, integridad, coherencia, totalidad, validez, disponibilidad, accesibilidad |
| *Datawarehouse* según Inmon | Orientado a un área, integrado, indexado en el tiempo, no volátil |
| FASMI (OLAP) | *Fast Analysis of Shared Multidimensional Information* |
| Modelo relacional | **E. F. Codd, 1970** |
| Las dimensiones responden | ¿Qué? ¿Quién? ¿Por qué? ¿Dónde? ¿Cuándo? |
| Término KDD | Desde **1989** |
| Etapas del KDD | Resumen de cátedra: **7**; Fayyad: **5**; lectura: **6 fases** y **9 pasos** |
| Paso crítico del KDD (lectura) | Transformación y reducción |
| Tareas de la minería | **6**: clasificación, regresión, agrupamiento, condensación, detección de desviaciones, modelado de dependencias |
| CRISP-DM | **6 fases**; DaimlerChrysler, SPSS y NCR |
| SEMMA | **5 fases**: *Sample, Explore, Modify, Model, Assess*; SAS Institute |
| Medidas clave para evaluar una herramienta de minería | **3**: precisión, explicación, integración |
| Big Data (final) | **3 V**: volumen, velocidad, variedad |
| Metodología MAD | Magnética, Ágil, Detallada |
| Megatendencias del Big Data | **4**: Movilidad, Cloud, Social Media, Analytics |
| Hadoop | **HDFS** + **MapReduce**; código abierto desde **2006**; nace de una idea de Google |

### 5.2 Cómo se conectan los temas

- **Redes de Petri**: modelan **cómo se comporta** un sistema concurrente (procesos, estados, recursos). Es **diseño**.
- **BI, minería y Big Data**: trabajan con los **datos** que generan esos sistemas, para **decidir**. Big Data reúne y procesa → la minería descubre patrones → BI los convierte en indicadores y decisiones.
- **Puntos de contacto**:
  - El *datawarehouse* de BI es el punto de partida de la minería.
  - La minería de datos es también una de las herramientas de BI.
  - OLAP aparece en BI y en minería (pero la minería **no** es OLAP).
  - La **granularidad** aparece en el modelo de datos de BI y en el tercer reto de la minería.
  - La **privacidad** aparece en minería y en Big Data.

### 5.3 Errores frecuentes en el examen

- ❌ "Una red viva siempre es cíclica." ✅ Son propiedades **independientes**: una red puede ser viva y no volver nunca a M0.
- ❌ "Red segura = red que no se traba." ✅ Segura = **1-acotada**. Que no se trabe es **vivacidad**.
- ❌ "C = C⁻ − C⁺." ✅ **C = C⁺ − C⁻**.
- ❌ "Un arco puede unir dos lugares." ✅ Siempre une un **lugar con una transición** (grafo bipartito).
- ❌ "La máquina de estados modela concurrencia." ✅ La máquina de estados modela **conflictos**; el **grafo marcado** modela concurrencia.
- ❌ "El árbol de expansión mínima une el origen con el destino." ✅ Eso es la **ruta más corta**; el árbol de expansión mínima conecta **todos** los nodos.
- ❌ "BI es un análisis que se hace una vez." ✅ Es un **proceso continuo** (interactivo).
- ❌ "El esquema estrella está normalizado." ✅ La estrella está **desnormalizada**; el **copo de nieve** está normalizado.
- ❌ "Más granularidad = menos detalle." ✅ **Más granularidad = más detalle** (líneas de ticket > tickets).
- ❌ "El ETL tiene 6 subprocesos, y el *data staging* es uno." ✅ Tiene **5**; el *data staging* es el **área intermedia** donde se limpian los datos.
- ❌ "Un Data Mart es más grande que un *datawarehouse*." ✅ Es **más chico** y para una comunidad de usuarios.
- ❌ "En OLAP, *slicing* es fijar una dimensión." ✅ En la cátedra, **rotar = *slicing*** y **seleccionar = *dicing***.
- ❌ "KDD y minería de datos son lo mismo." ✅ La minería es **una etapa** del KDD.
- ❌ "El KDD tiene 5 etapas." ✅ **Depende de la fuente**: 7 en el resumen de cátedra, 5 en Fayyad, 6 fases y 9 pasos en la lectura. Aclarar cuál se usa.
- ❌ "OLAP descubre patrones nuevos." ✅ OLAP **navega**; la minería **descubre**.
- ❌ "Si dos variables están correlacionadas, una causa la otra." ✅ **Correlación no es causalidad** (Florida).
- ❌ "Sacar las filas con faltantes no tiene costo." ✅ **Sesga** los datos.
- ❌ "La regresión es una tarea descriptiva." ✅ Es **predictiva / supervisada** (predice un valor real).
- ❌ "Las redes neuronales cumplen con el lenguaje de alto nivel del KDD." ✅ Son una **caja negra**: no lo cumplen, aunque sirvan como método de minería.
- ❌ "Big Data reemplaza al *datawarehouse*." ✅ **Conviven** (modelo híbrido DWH + ADW).
- ❌ "SEMMA incluye la comprensión del negocio." ✅ SEMMA **la da por resuelta**; CRISP-DM es la más orientada al negocio.

### 5.4 Preguntas integradoras con respuesta modelo

1. **¿Por qué la minería de datos depende del *datawarehouse* de BI?**
   Porque la minería necesita datos **consolidados, limpios e históricos**, separados de los sistemas transaccionales, y eso es lo que da el *datawarehouse* cargado con **ETL**. La lectura indica que el análisis es mucho más sencillo si la fuente es unificada, accesible y separada del trabajo transaccional. Por eso el *datawarehouse* es el punto de partida de la minería.

2. **Compará OLAP, minería de datos y Big Data.**
   **OLAP** navega por datos históricos resumidos en varias dimensiones, **sin generar información nueva**. La **minería** descubre de forma **automática** patrones nuevos y predice. **Big Data** es el **contexto** de datos enormes, rápidos y variados (incluso no estructurados), que necesita infraestructura distribuida (**Hadoop**) y análisis en tiempo real (**CEP**, **Data Stream**).

3. **¿Qué tienen en común la granularidad de un modelo estrella y el tercer reto de la minería?**
   En los dos casos, el **nivel de detalle** decide qué preguntas se pueden responder. En BI, si se guardan solo tickets, no se pueden analizar productos; en minería, con datos mensuales no se puede predecir por semana. **Cada vez que se resume, se pierde información.**

### 5.5 Autopreguntas

- ¿Qué es un marcado frontera y cuáles son los tres tipos?
- ¿Cuándo se escribe ω en el árbol, con qué marcado se compara y qué propiedad indica?
- Dada una red, ¿podés armar C⁻, C⁺ y C sin mirar, con filas = transiciones?
- ¿Cómo se pasa del árbol de alcanzabilidad a la máquina de testigos?
- ¿Por qué M' = M + f(σ) · C no alcanza para asegurar que una secuencia se puede disparar?
- ¿Cómo se ve en el grafo de marcados que una red es cíclica?
- ¿Qué diferencia hay entre una red viva, parcialmente viva y no viva?
- ¿Qué diferencia hay entre conflicto estructural y conflicto efectivo?
- ¿Qué puede modelar una máquina de estados y qué un grafo marcado?
- ¿Qué busca cada uno de los cuatro modelos de redes?
- ¿Cuáles son los 6 componentes de un proyecto de BI y cuáles los componentes del entorno de BI?
- ¿Cuáles son las 6 herramientas fundamentales de BI?
- ¿Qué es una dimensión degenerada? Dame dos ejemplos.
- ¿Por qué el fabricante va en una dimensión distinta de la del artículo?
- ¿En qué se diferencian un *dashboard* y un *scorecard*?
- ¿Cuáles son las etapas del KDD según el resumen de cátedra y según Fayyad?
- ¿Cuál es el paso crítico del KDD según la lectura y por qué?
- ¿Qué hace un "picapedrero" y qué hace un "explorador"?
- ¿Qué diferencia hay entre minería dirigida a la verificación y dirigida al descubrimiento?
- ¿Cómo se calculan el soporte y la confianza de una regla?
- ¿Qué es la elevación (*lift*) y cómo se calcula?
- ¿Qué es la metodología MAD y qué significa cada letra?
- ¿Qué diferencia hay entre Data Stream y CEP?

---

## Glosario de siglas

**Redes de Petri**

| Sigla | Desarrollo |
|---|---|
| RdP | Red de Petri |
| M0 | Marcado inicial |
| C⁻ | Matriz de incidencia previa |
| C⁺ | Matriz de incidencia posterior |
| MT | Máquina de testigos |
| GE | Grafo de estados |
| ME | Máquina de estados |
| GM | Grafo marcado |
| RLE | Red de libre elección |
| RS | Red simple |
| DFD | Diagrama de flujo de datos |
| RMC | Ruta más corta |
| AEM | Árbol de expansión mínima |

**Business Intelligence**

| Sigla | Desarrollo | Original |
|---|---|---|
| BI | Inteligencia de negocio | *Business Intelligence* |
| KPI | Indicador clave de desempeño | *Key Performance Indicator* |
| ROI | Retorno de la inversión | *Return on Investment* |
| NPV | Valor actual neto | *Net Present Value* |
| TCO | Costo total de propiedad | *Total Cost of Ownership* |
| CF | Flujo de caja | *Cash Flow* |
| ETL | Extracción, transformación y carga | *Extract, Transform, Load* |
| OLAP | Procesamiento analítico en línea | *On-Line Analytical Processing* |
| OLTP | Procesamiento de transacciones en línea | *On-Line Transaction Processing* |
| ROLAP | OLAP relacional | *Relational OLAP* |
| MOLAP | OLAP multidimensional | *Multidimensional OLAP* |
| HOLAP | OLAP híbrido | *Hybrid OLAP* |
| DOLAP | OLAP de escritorio | *Desktop OLAP* |
| FASMI | Análisis rápido de información multidimensional compartida | *Fast Analysis of Shared Multidimensional Information* |
| ODS | Almacén de datos operacional | *Operational Data Store* |
| DWH | Almacén de datos | *Data Warehouse* |
| ERP | Planificación de recursos empresariales | *Enterprise Resources Planning* |
| CRM | Gestión de la relación con clientes | *Customer Relationship Management* |
| SCM | Gestión de la cadena de suministro | *Supply Chain Management* |
| GIS | Sistemas de información geográfica | *Geographic Information Systems* |
| GDSS | Sistemas de apoyo a la decisión en grupo | *Group Decision Support Systems* |
| PK | Clave primaria | *Primary Key* |
| FK | Clave externa | *Foreign Key* |
| SQL | Lenguaje de consulta estructurado (el libro escribe "Standard Query Language") | *Structured Query Language* |
| ODBC | Conectividad abierta de bases de datos (el libro escribe "Object Data Base Connector") | *Open Database Connectivity* |
| EFQM | Fundación Europea para la Gestión de la Calidad | *European Foundation for Quality Management* |
| TDWI | The Data Warehousing Institute | — |

**Minería de datos**

| Sigla | Desarrollo | Original |
|---|---|---|
| DM | Minería de datos | *Data Mining* |
| KDD | Descubrimiento de conocimiento en bases de datos | *Knowledge Discovery in Databases* |
| CRISP-DM | Proceso estándar intersectorial para minería de datos | *Cross-Industry Standard Process for Data Mining* |
| SEMMA | Muestrear, explorar, modificar, modelar, evaluar | *Sample, Explore, Modify, Model, Assess* |
| ANOVA | Análisis de la varianza | *Analysis of Variance* |
| CART | Árboles de clasificación y regresión | *Classification And Regression Trees* |
| CHAID | Detector automático de interacciones por Ji cuadrado | *Chi Squared Automatic Interaction Detector* |
| k-NN | k vecinos más cercanos | *k Nearest Neighbors* |
| RBF | Función de base radial | *Radial Basis Function* |
| GDPR | Reglamento General de Protección de Datos (Unión Europea) | *General Data Protection Regulation* |
| CAD-CAM | Diseño y fabricación asistidos por computadora | *Computer-Aided Design / Computer-Aided Manufacturing* |

**Big Data**

| Sigla | Desarrollo | Original |
|---|---|---|
| ADW | Almacén de datos analítico | *Analytic Data Warehouse* |
| MAD | Magnética, Ágil, Detallada | — |
| HDFS | Sistema de archivos distribuido de Hadoop | *Hadoop Distributed File System* |
| CEP | Procesamiento de eventos complejos | *Complex Event Processing* |
| MPP | Procesamiento masivamente paralelo | *Massively Parallel Processing* |

**Otras**

| Sigla | Desarrollo |
|---|---|
| TP | Trabajo Práctico |

---

## De dónde sale este resumen

- **Material de la cátedra** (carpeta *Análisis y Diseño de Sistemas II - 2026*): resumen de cátedra del 2do cuatrimestre; presentaciones "Redes_de_petri" (incluye los modelos de redes) y "Formalización Redes de Petri"; lectura de Redes de Petri de Jorge Castro Monge; capítulos "Introducción al BI" (con las notas técnicas 1 y 2), "BI_modelos" y "Componentes de BI" del libro *Business Intelligence: competir con información*; video "¿Qué es el Business Intelligence?"; lectura de minería de datos de Beatriz Beltrán Martínez; artículo "KDD, SEMMA and CRISP-DM: a parallel overview" (Azevedo y Santos); guía "PowerData - Del bit… al Big Data".
- **Notas de estudio en Obsidian**: de ahí salen los fragmentos del resumen de cátedra y el contenido del video de BI. El video se reconstruyó con los fotogramas y los textos en pantalla, porque el audio no se pudo transcribir.
- **Material del grupo**: TP6 a TP9, guías de BI, apuntes de clase ("Redes Petri - Análisis y Diseño II", "Apuntes 14/9", "Ingeniería de datos") y el mapa conceptual de Big Data.
- **Verificado por computadora**: matrices, árboles, máquinas de testigos, secuencias y propiedades de los tres ejemplos de Redes de Petri.
- **Fuera del resumen por alcance**: la práctica de los TP (modelado del TP6, CoffeeTime, TP de fútbol, comercio minorista, abandono de compra), los ejemplos y casos puntuales (empresas, encuestas, estudios, casos de BI y del libro *Data Mining: el arte de anticipar*) y los ejercicios resueltos de modelos de redes. Se conservan los ejemplos resueltos de Redes de Petri, porque esa práctica entra.
- **No disponible**: el contenido del video del tema 10 (Big Data).
