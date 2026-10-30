# Resumen 2do parcial — Análisis y Diseño de Sistemas II

> Versión fácil: la misma información que el resumen completo, pero contada más simple. Los **términos clave quedan igual**, porque son los que pide la cátedra.
> Docente: María Silvina Scarpin. Grupo: Figún, Morales, Haunau. Tecnicatura en Análisis y Desarrollo de Software, Instituto de Profesorado Sedes Sapientiae.

---

## Antes de empezar

### Qué entra

| Tema | Qué estudiar |
|---|---|
| **Temas 6 y 7 — Redes de Petri** | Teoría **+ práctica**: árbol de alcanzabilidad, propiedades, máquina de testigos y método matricial |
| **Tema 8 — Business Intelligence (BI)** | Solo teoría |
| **Tema 9 — Minería de datos y KDD** | Solo teoría |
| **Tema 10 — Big Data** | Solo teoría. **Entra en el final, no en el 2do parcial** |

**Big Data (tema 10) entra en el final.** Queda en el resumen como material para el final.

**No entra**: la práctica de los TP (caso CoffeeTime, TP integrador de fútbol, comercio minorista, abandono de compra, las 7 tareas de modelado del TP6). Tampoco hay ejemplos puntuales, casos de empresas ni datos sueltos de un autor o de un estudio; los ejemplos resueltos de Redes de Petri sí quedan, porque esa práctica entra.

### Cómo leer las marcas

- 📁 = sale del material de la cátedra, de los TP o de los apuntes de clase.
- ⚠️ = no verificado con el material de la cátedra.
- ✅ / ❌ = correcto / incorrecto.
- 👉 = explicación en criollo.

### Trampas que ya están corregidas

1. El apunte de clase dice **"una red viva es cíclica"**. **Está mal**: vivacidad y ciclicidad son cosas distintas.
2. El cuadro **KDD / SEMMA / CRISP-DM** del TP8 tenía un error. Se corrigió con el artículo de la cátedra (Azevedo y Santos). Ver 3.13.
3. Los **videos** de los temas 8 y 10 no se pudieron revisar. La guía de PowerData sí.
4. El libro de BI escribe "Standard Query Language" (SQL) y "Object Data Base Connector" (ODBC). Lo habitual es **Structured Query Language** y **Open Database Connectivity**. Usá estos; si te preguntan, sabé que el libro los escribe distinto.

---

## 0. Datos para memorizar

| Dato | Valor |
|---|---|
| Creador de las Redes de Petri | **Carl Adam Petri** (alemán), tesis de **1962**: *Kommunikation mit Automaten* |
| Holt y Commoner | **1970**, "Events and Conditions": usan las RdP para sistemas concurrentes |
| Estructura de una Red de Petri | **C = (P, T, I, O)**: lugares, transiciones, función de entrada, función de salida |
| Red marcada | **M = (C, μ)** |
| Matriz de incidencia | **C = C⁺ − C⁻** (posterior menos previa). Filas = transiciones, columnas = lugares |
| Ecuación de disparo | **M'(p) = M(p) − Pre(p, t) + Post(t, p)** |
| Red segura | **1-acotada** (binaria): ningún lugar tiene más de 1 marca |
| Ecuación de estado | **M' = M + f(σ)·C** (f(σ) = cuántas veces se dispara cada transición) |
| Transición habilitada (método matricial) | **M ≥ ej·C⁻** |
| ω en el árbol | La red **no es acotada** |
| Subclases de RdP | **4**: grafo de estados (máquina de estados), grafo marcado, red de libre elección, red simple |
| Primero en usar "Business Intelligence" | **Howard Dresner** (Gartner) |
| BI según Gartner | Proceso **interactivo** para **explorar** y **analizar** información **estructurada** de un **área**, normalmente en un *datawarehouse* |
| ROI simple | Valor para el negocio / costo del proyecto |
| ROI completo | **NPV / inversión inicial × 100** |
| Proceso ETL | **60 % a 80 %** del tiempo de un proyecto de BI; **5 subprocesos** |
| *Datawarehouse* según Inmon | Orientado a un área, integrado, indexado en el tiempo, no volátil |
| FASMI (OLAP) | *Fast, Analysis, Shared, Multidimensional, Information* |
| Modelo relacional | **E. F. Codd, 1970** |
| Las dimensiones responden | ¿Qué? ¿Quién? ¿Por qué? ¿Dónde? ¿Cuándo? |
| Término KDD | Desde **1989** |
| Pasos del proceso KDD | **9** |
| Fases del KDD según la lectura | **6** |
| CRISP-DM | **6 fases**; DaimlerChrysler, SPSS y NCR |
| SEMMA | **5 fases**: *Sample, Explore, Modify, Model, Assess*; SAS Institute |
| KDD según Fayyad | **5 etapas**: selección, preprocesamiento, transformación, minería, interpretación/evaluación |
| Big Data (final) | **3 V**: volumen, velocidad, variedad |
| Metodología MAD | Magnética, Ágil, Detallada |
| Megatendencias del Big Data | **4**: Movilidad, Cloud, Social Media, Analytics |
| Hadoop | **HDFS** + **MapReduce**; código abierto desde **2006**, nace de Google |

---

## 1. Redes de Petri (Temas 6 y 7) 📁

> **En una frase:** una Red de Petri es un **dibujo con reglas matemáticas** que muestra cómo funciona un sistema donde **pasan varias cosas a la vez**.

### 1.1 Qué son y para qué sirven

- Las creó **Carl Adam Petri** en su tesis de **1962**, *Kommunikation mit Automaten* ("Comunicación con autómatas"), en Alemania. Trataba de cómo se comunican partes **asíncronas** (que no van al mismo ritmo). El proyecto "Systemics" aportó la notación.
- En **1970**, **Holt y Commoner** ("Events and Conditions") las usan para sistemas con partes **concurrentes**.
- Sirven para modelar cuatro cosas típicas de los sistemas distribuidos:
  - **Concurrencia**: cosas que pasan a la vez.
  - **Sincronización**: esperar a que otro termine.
  - **Exclusión mutua**: de a uno por vez.
  - **Conflictos**: hay que elegir entre dos.
- **Su antecedente son las máquinas de estado** (estado + transición, con entradas y salidas *a/b*). Problema: no sirven bien para **acciones simultáneas**. Si juntás varias, los estados se multiplican y el diagrama no se entiende.
- 👉 Las Redes de Petri (RdP) resuelven eso porque tienen **paralelismo inherente**: la concurrencia ya viene "de fábrica".
- Al analizar la red ves dos cosas: su **estructura** (cómo está armada) y su **comportamiento dinámico** (cómo se mueve). Con eso evaluás el sistema y proponés mejoras.
- **Definición de la cátedra**: representaciones gráficas que modelan sistemas con flujo de información y muestran su estructura y su comportamiento dinámico. Se pueden ver como **generadores de lenguaje o autómatas formales** (teoría de grafos). Sirven para diseñar, especificar y simular *hardware* o *software*.
- **Tres ventajas de modelar con RdP** (presentación "Formalización"):
  1. Se **entienden fácil**: son gráficas y precisas.
  2. Se pueden **analizar con teoría** (árboles de marcados, relación entre estructura y comportamiento).
  3. Se arman *bottom-up* o *top-down*: así diseñás sistemas cuyo comportamiento conocés o podés verificar.
- **Extensiones**: cambios en la estructura (más potencia o comodidad) y **redes de Petri temporizadas** (para medir tiempos y prestaciones).
- **En programación concurrente**: transición = proceso; lugar = condición para que el proceso corra; marca = la condición se cumple.
- Apunte de clase: sirven para ver cómo funciona un sistema, qué procesos tiene y por qué estados pasa. Se usan como **autómatas**. Cualquier proceso se puede dibujar con una RdP.

### 1.2 Elementos y representación gráfica

| Elemento | Dibujo | Qué representa |
|---|---|---|
| **Lugar** o plaza | Círculo | Condición o estado ("cómo está") |
| **Transición** | Barra | Evento o suceso ("qué pasa") |
| **Arco dirigido** | Flecha con peso (sin número = pesa 1) | Une lugar → transición (lugar de entrada) o transición → lugar (lugar de salida). **Nunca** lugar con lugar ni transición con transición |
| **Marca**, **testigo** o *token* | Punto negro dentro del lugar | La condición se cumple. Un lugar con marcas está **activo** |

- La red es un **multígrafo dirigido bipartito**:
  - **Multígrafo**: puede haber varios arcos entre dos nodos.
  - **Dirigido**: las flechas tienen sentido.
  - **Bipartito**: hay dos tipos de nodos (lugares y transiciones) y solo se conectan entre tipos distintos.
- Transición **sensibilizada** (habilitada): todos sus lugares de entrada tienen marca. **Validada**: además ocurre el evento.
- Representación **gráfica** y **matricial**: son dos formas de escribir lo mismo. De una sale la otra, y es única.

### 1.3 Definición formal

- **Estructura**: **C = (P, T, I, O)**
  - **P**: conjunto finito y no vacío de lugares.
  - **T**: conjunto finito y no vacío de transiciones.
  - **I**: **función de entrada** (qué lugares entran a cada transición).
  - **O**: **función de salida** (qué lugares salen de cada transición). La lectura la describe como un mapeo de transiciones en **bolsas de sitios**; O: T × P → N es la **función de incidencia posterior**.
- **Marcado** μ: cuántas marcas tiene cada lugar (números enteros ≥ 0). Se escribe como vector μ = (μ1, …, μn), con n = cantidad de lugares. 👉 **El marcado es el estado de la red.**
- **Red marcada**: **M = (C, μ)** = estructura + marcas. Los marcados posibles son infinitos (pero se pueden numerar).
- **Tipos de red**:
  - **Ordinaria**: sus funciones de incidencia solo toman los valores **0 y 1** (todos los arcos son de **peso unitario**).
  - **Generalizada**: sus funciones de incidencia pueden tomar **cualquier valor entero ≥ 0**.
  - **Pura** o **no reflexiva**: ninguna plaza es a la vez entrada y salida de una misma transición (fórmula en 1.8).
- Notación del apunte: I(t) = lugares de entrada a t; O(t) = lugares de salida de t; I'(p) = transiciones que entran al lugar p; O'(p) = transiciones que salen de p; V(p, t) y V(t, p) = pesos de los arcos.

### 1.4 Ejecución (reglas de disparo)

👉 **Regla de oro:** una transición se dispara si sus entradas tienen marcas suficientes. Al dispararse, **"come" marcas de las entradas y "deja" marcas en las salidas**.

1. **Habilitación**: t está habilitada si cada lugar de entrada tiene al menos tantas marcas como el peso del arco: **M(p) ≥ I(p, t)**. Una **transición fuente** (sin entradas) está siempre habilitada.
2. **Disparo**: se sacan marcas de las entradas (según el peso) y se ponen en las salidas (según el peso). Si hay varias habilitadas, cuál va primero es **arbitrario**.
3. **Nuevo marcado**: **M'(p) = M(p) − Pre(p, t) + Post(t, p)**. 👉 "Lo que había, menos lo que se comió, más lo que dejó". Una **transición sumidero** (sin salidas) borra marcas de la red.

- Las marcas son **indivisibles**: una marca la usa una sola transición. Por eso, disparar una transición puede **deshabilitar** a otra que compartía la misma entrada. Fuera de eso, los disparos son **asíncronos**.
- **Grado de habilitación**: cuántas veces puede dispararse una transición a la vez.
- **Inmediatamente alcanzable**: llegás disparando **una** transición.
- **Alcanzable**: existe una secuencia de disparos **σ** que lleva de Mi a Mk.
- **Conjunto de alcanzabilidad R(M)**: todos los marcados a los que se puede llegar desde M. En las fórmulas de la lectura aparece como **M(R, M0)**.
- **Vocabulario de la lectura**: dice **activada** en vez de habilitada (cada lugar de entrada tiene al menos un elemento) y **descarga** en vez de disparo (elimina un elemento de cada lugar de entrada y agrega uno a cada lugar de salida).

### 1.5 Árbol de alcanzabilidad

> **En una frase:** es el **mapa de todos los estados** a los que puede llegar la red desde M0.

- Cada **nodo** es un marcado. Cada **flecha** lleva el nombre de la transición disparada.
- **Cómo se arma**: empezás en M0, disparás cada transición habilitada, anotás el marcado nuevo y repetís.
- Para que el árbol no sea infinito, **dejás de expandir en los nodos frontera**:
  - a) **Marcado muerto**: no hay ninguna transición habilitada.
  - b) **Nodo duplicado**: ese marcado ya apareció antes.
  - c) Un marcado igual a uno anterior **pero con más marcas en algún lugar** (y habilita las mismas transiciones): ahí escribís **w** (infinito). 👉 Significa que la red **no es acotada**.

- **Máquina de testigos** (MT): versión **más corta** del árbol.
  - Cada estado se escribe con los **nombres de los lugares que tienen marcas** (repetido tantas veces como marcas tenga).
  - Los estados van en **óvalos**, unidos por flechas con el nombre de la transición.
  - 👉 Conviene cuando hay **muchos lugares y pocas marcas**: no tenés que escribir todos los lugares.

### 1.6 Representación matricial

👉 Tres matrices, tres ideas:

| Matriz | Qué guarda | En criollo |
|---|---|---|
| **C⁻** (incidencia previa) | C⁻[j, i] = I(pi, tj): las precondiciones | Lo que cada transición **consume** |
| **C⁺** (incidencia posterior) | C⁺[j, i] = O(pi, tj): las postcondiciones | Lo que cada transición **produce** |
| **C = C⁺ − C⁻** (incidencia) | Diferencia entre las dos | El **efecto neto**: cuánto gana o pierde cada lugar |

- Según la lectura: **filas = transiciones, columnas = lugares**.
- Una transición tj se escribe con el vector **ej** (1 en la posición j, 0 en el resto).
  - tj está **habilitada** si **M ≥ ej · C⁻**.
  - Al dispararla: **M' = M + ej · C**.
- Para una **secuencia** σ = tj1 tj2 … tjk: **M' = M + f(σ) · C**, con **f(σ) = ej1 + ej2 + … + ejk** = el **vector de disparo** (cuántas veces se dispara cada transición). Ejemplo de la cátedra: σ = t1, t2, t3 → f(σ) = (1 1 1 0 0) → M' = (0 0 0 1 1).

**Ejemplo resuelto (el de la lectura)** — P = {p1…p5}, T = {t1…t5}, M0 = (1, 0, 0, 0, 0). I(t1) = {p1}, O(t1) = {p2, p3}; I(t2) = {p2}, O(t2) = {p5}; I(t3) = {p3}, O(t3) = {p4}; I(t4) = {p5}, O(t4) = {p2}; I(t5) = {p4, p5}, O(t5) = {p1}.

| | C⁻ (p1 p2 p3 p4 p5) | C⁺ (p1 p2 p3 p4 p5) | C (p1 p2 p3 p4 p5) |
|---|---|---|---|
| t1 | 1 0 0 0 0 | 0 1 1 0 0 | −1 1 1 0 0 |
| t2 | 0 1 0 0 0 | 0 0 0 0 1 | 0 −1 0 0 1 |
| t3 | 0 0 1 0 0 | 0 0 0 1 0 | 0 0 −1 1 0 |
| t4 | 0 0 0 0 1 | 0 1 0 0 0 | 0 1 0 0 −1 |
| t5 | 0 0 0 1 1 | 1 0 0 0 0 | 1 0 0 −1 −1 |

La resolución completa (árbol, máquina de testigos, método matricial y propiedades) está en 1.12, Ejemplo 1.

### 1.7 Estructuras básicas

| Estructura | Qué modela | Cómo se ve |
|---|---|---|
| **Secuencial** | Una cosa después de otra | t2 solo se dispara después de t1 |
| **Selección** | Elegir qué proceso hacer | Un lugar con dos transiciones de salida |
| **Atribución** | Llegar al mismo lugar desde dos procesos distintos | Dos transiciones que llegan al mismo lugar |
| **Distribución** | Arrancar procesos en paralelo | Una transición con varios lugares de salida |
| **Conjunción** | Juntar (sincronizar) procesos paralelos | Una transición con varios lugares de entrada |
| **Sincronización** | Esperar a que todo esté listo | t1 se habilita solo si **todas** sus entradas tienen marca |
| **Concurrencia** | Dos cosas a la vez, sin molestarse | t2 y t3 se disparan a la vez e independientemente |
| **Conflicto** | Dos quieren lo mismo | t1 y t2 habilitadas, pero disparar una deshabilita a la otra |

👉 **Distribución "abre"** (una transición → varias salidas); **conjunción "cierra"** (varias entradas → una transición).

### 1.8 Propiedades

👉 Las propiedades sirven para **detectar fenómenos de interés o errores de funcionamiento** en el sistema que modela la red (bloqueos, recursos infinitos, conflictos…). Hay dos grupos:

- **Estructurales**: dependen de la **estructura topológica** (cómo está dibujada la red) y son **independientes del marcado inicial**.
- **De comportamiento**: **dependen del marcado inicial M0**.

La presentación "Redes_de_petri" trabaja seis: **vivacidad, ciclicidad, limitación, conservación, conflictividad y exclusión mutua**. El resumen agrega **acotada** y **completamente controlable**. La lectura destaca dos: **supervivencia** (ausencia de estancamientos) y **seguridad** (capacidad limitada de la memoria).

Notación: **M(R, M0)** = conjunto de marcados alcanzables desde M0.

#### Propiedades estructurales

| Propiedad | Definición | 👉 En criollo |
|---|---|---|
| **Pura** | Ninguna transición tiene un lugar que sea a la vez de entrada y de salida: **∀tj ∈ T, ∀pi ∈ P: Pre(pi, tj) · Post(tj, pi) = 0** | Ninguna flecha "va y vuelve" entre el mismo lugar y la misma transición |
| **Estructuralmente acotada** | Acotada para **cualquier** marcado inicial finito. Un **lugar** p es **no acotado estructuralmente** si existe un marcado M y una secuencia σ desde M tal que p no está acotado | Arranque como arranque, nada crece sin fin |
| **Estructuralmente viva** | Existe **algún** marcado inicial con el que es viva | Hay al menos una forma de arrancarla sin que se trabe |
| **Estructuralmente conservativa** | La cantidad (ponderada) de marcas se mantiene para **cualquier** marcado inicial | Arranque como arranque, los recursos no cambian |
| **Completamente controlable** | **Cualquier marcado es alcanzable desde cualquier otro** | Desde cualquier estado llego a cualquier estado |

#### Propiedades de comportamiento

**Alcanzabilidad** — 👉 "¿Puedo llegar a ese estado?"

- Es la **base fundamental para estudiar las propiedades dinámicas**.
- Cada disparo cambia la distribución de las marcas; una secuencia de disparos σ = t1, t2, …, tn da una secuencia de marcados.
- Mn es alcanzable desde M0 sii existe σ tal que **M0 [σ> Mn**.

**Vivacidad** — 👉 "Nada se traba para siempre"

- Sirve para **caracterizar el bloqueo total o parcial** del sistema.
- **Transición viva**: desde cualquier marcado alcanzable existe una secuencia de disparos que **la incluye**. La lectura lo escribe: ∀m ∈ M(R, M0) ∃σ: M σ→ M0 t.q. t ⊂ σ.
- **Red viva**: **todas** sus transiciones son vivas. Entonces, en el conjunto de alcanzabilidad **no hay ningún marcado con bloqueo total (*deadlock*)**.
- **Parcialmente viva**: desde cualquier marcado alcanzable hay **al menos una transición disparable** y **otra no viva**. Tiene **posibilidad de evolución global**, aunque algunas transiciones no puedan dispararse.
- **No viva**: se llega a un marcado muerto. Ejemplo de la lectura: con t1, t2, t1, t2 no hay bloqueo, pero con t1, t3, t4 la red queda **bloqueada**.
- Versión de la lectura con "descargas": un **marcado vivo** permite, sin importar las descargas hechas, descargar cualquier transición con alguna secuencia adicional → la red **nunca se estancará**.

**Ciclicidad o reversibilidad** — 👉 "Siempre puedo volver al inicio"

- Comportamiento **globalmente cíclico**: desde **cualquier marcado sucesor** de M0 existe una secuencia de disparos que **vuelve a M0**: **∀M ∈ M(R, M0), ∃σ tal que M σ→ M0**.
- Garantiza que **no existen subconjuntos finales de estados**: grupos de marcados **mutuamente alcanzables entre sí** desde los cuales **M0 no es alcanzable**.
- Ejemplo de la lectura: una red **pseudoviva** y **no reversible**, porque el marcado inicial no se obtiene jamás.

**Acotamiento o limitación** — 👉 "Ningún lugar se llena de más"

- Asegura que el sistema tiene un **número finito de estados** (si cada lugar es una variable de estado y su marcado, el valor de esa variable).
- Un lugar p es **k-acotado** sii M(p) ≤ k para cualquier M ∈ M(R, M0). La **cota del lugar p** es el **menor** k que lo cumple.
- Red **k-acotada** o **k-limitada**: todos sus lugares lo son: **∀p ∈ P y ∀M ∈ M(R, M0), M(p) ≤ k**. Ejemplo de la diapositiva: red **3-limitada**.
- **Garantiza la finitud de los marcados alcanzables**: una red k-limitada **puede implementarse con recursos finitos**.
- Si la red genera más marcas de las que permite su acotación, **el modelado es erróneo**.
- Versión de la lectura con "descargas": un **marcado acotado** es uno en el que existe un entero positivo n tal que ningún lugar recibe más de n elementos en ninguna secuencia de descarga.

**Seguridad** — 👉 "Cada lugar: marca sí o no"

- Red **1-acotada** = **segura** = **binaria**: su marcado es binario (cada lugar está marcado o no).
- En la lectura: un marcado acotado en el que ningún lugar recibe más de un elemento es un **marcado seguro**. Si cada lugar es un registro que guarda una palabra de computadora y el marcado inicial es seguro, **no se excede la capacidad de memoria** de los registros.

**Conservación** — 👉 "Las marcas ni se crean ni se destruyen" (como recursos)

- El **número de recursos disponibles no puede variar** durante la ejecución.
- **Conservación estricta**: el número total de testigos es constante. Es una relación **muy fuerte**.
- Por eso se suele usar **conservación respecto de un vector peso** w: la suma ponderada **Σ wi · mi** es constante. Ejemplo de la diapositiva: w = (1, 1, 1, 2, 2).

**Conflictividad** — 👉 "Hay que elegir una" (decisión no determinista)

- **Conflicto estructural**: un lugar tiene **más de una transición de salida**. Se ve en el dibujo.
- **Conflicto efectivo** para M0: ti y tj lo están si se cumplen las dos condiciones:
  1. existe un marcado alcanzable que las **sensibiliza simultáneamente**, **y**
  2. al disparar una, el marcado que queda **no habilita** a la otra.
- 👉 El efectivo depende del marcado: las dos están habilitadas a la vez y **compiten por el mismo testigo**.

**Exclusión mutua** — 👉 "De a uno por vez"

- Entre **transiciones**: un conjunto Te ⊆ T es mutuamente exclusivo si disparar cualquier ti ∈ Te **deshabilita a todas las demás**.
- Entre **plazas**: dos plazas están en exclusión mutua si **nunca pueden estar marcadas a la vez** en ningún marcado alcanzable.
- Ejemplo de la diapositiva: las plazas 4 y 5 y las transiciones Π1 y Π2 son mutuamente exclusivas (R = recurso disponible; R1 y R2 = recurso tomado por Π1 o por Π2). El modelo del semáforo está en 1.9.

#### Tabla resumen

| Propiedad | Pregunta que responde | Detecta |
|---|---|---|
| Vivacidad | ¿Se pueden disparar siempre todas las transiciones? | Bloqueos (*deadlock*) |
| Ciclicidad | ¿Puede volver al estado inicial? | Sistemas que no se "reinician" |
| Limitación / acotada | ¿Las marcas por plaza tienen un tope k? | Necesidad de recursos infinitos |
| Conservación | ¿Se mantiene la cantidad (ponderada) de marcas? | Creación o pérdida de recursos |
| Conflictividad | ¿Hay transiciones que compiten por una marca? | Decisiones / no determinismo |
| Exclusión mutua | ¿Hay plazas o transiciones que no coexisten? | Uso de recursos compartidos |
| Completamente controlable | ¿Todo marcado es alcanzable desde todo otro? | Estados inalcanzables |

### 1.9 Modelos clásicos de concurrencia

- **Exclusión mutua (semáforo)**: cuando varios procesos comparten un recurso y mientras uno lo usa los demás no pueden, hay que implementar un **mecanismo de espera**. Se usa un lugar (sitio) que representa la condición **"el recurso compartido está libre"**, con **una marca**. Ese lugar actúa como **semáforo**: sincroniza el acceso de los procesos. El primero que lo toma quita la marca y los demás esperan. Sirve para cualquier cantidad de procesos y **no tiene prioridades**.
- **Productor y consumidor**: también hay un recurso compartido, pero no para que lo usen los procesos, sino como **mecanismo de comunicación** entre ellos. Un lugar "depósito" (*buffer*) une a los dos procesos. Sin límite, el depósito puede crecer para siempre si el consumidor se para. Con un **buffer de capacidad finita** se agregan "buffers llenos" y "buffers vacíos"; 👉 **siempre suman la capacidad total** (por ejemplo, 3).
- **Lectores y escritores**: muchos pueden **leer a la vez**; **escribir es de a uno**. Se usa un semáforo con **m marcas** y arcos de peso **m**: leer toma 1 marca, escribir toma las m.
- **Cinco filósofos**: cada uno necesita los dos tenedores de al lado para comer. Si todos agarran primero el mismo tenedor, nadie come: **estancamiento**. Soluciones para que la red sea viva: que "comer" tome **los dos tenedores a la vez** (conjunción), o un lugar "sillas" con **4 marcas** que limite cuántos intentan comer. ⚠️ Son las soluciones habituales; la del grupo está en imagen.

### 1.10 Ventajas, desventajas, aplicaciones, subclases y métodos de análisis

| Ventajas | Desventajas |
|---|---|
| Fáciles de interpretar | **No permiten modelar prioridades** |
| Manejan procesos independientes | El análisis se complica en sistemas complejos |
| Más exactas que un diagrama de estados | Cuanto más grande el modelo, más recursos consume |
| Modelan recursos compartidos (exclusión mutua, por ejemplo una impresora) | Hay muchas **subclases** para problemas específicos |
| Se arman *top-down* o *bottom-up* | |
| Modelan procesos concurrentes | |

**Aplicaciones**: sistemas en **tiempo real**, sistemas operativos y compiladores, *hardware* y *software*, producción industrial (redes de libre elección), diagramas de flujo de datos (DFD), **protocolos de comunicación** y bases de datos.

**Subclases** → versiones con reglas más estrictas, más fáciles de analizar:

| Subclase | Regla | Puede / no puede |
|---|---|---|
| **Grafo de estados** o **máquina de estados** (GE o ME) | Cada **transición**: **1 entrada y 1 salida** | ✅ conflictos y alternativas · ❌ paralelismo, concurrencia, sincronización. Estrictamente conservativa |
| **Grafo marcado** o de sincronización (GM) | Cada **lugar**: **1 entrada y 1 salida** | ✅ paralelismo, concurrencia, sincronización · ❌ conflictos y decisiones |
| **Red de libre elección** (RLE) | Si un lugar es entrada de varias transiciones, es su **única** entrada | Concurrencia y conflicto, pero limitado: las transiciones en conflicto están habilitadas todas o ninguna |
| **Red simple** (RS) | Cada transición tiene como máximo **un lugar de entrada compartido** con otra | — |

👉 El **grafo de estados** se fija en las **transiciones** (elige, pero no paraleliza); el **grafo marcado** se fija en los **lugares** (paraleliza, pero no elige). Son opuestos.

**Métodos de análisis**:

- **Árbol de alcanzabilidad**: da mucho detalle del comportamiento. Sirve para validar el modelo, verificar un diseño, elegir entre propuestas o predecir. **Problema**: puede volverse **enorme e inmanejable**.
- **Ecuaciones matriciales o de estado**: prometen, pero tienen tres problemas:
  1. La matriz C **no muestra toda la estructura** de la red.
  2. El vector de disparo **no dice el orden** de los disparos.
  3. Que M' = M + f(σ)·C tenga solución es condición **necesaria pero no suficiente** para que el marcado sea alcanzable.

**Modelos de redes** (final de la presentación "Redes_de_petri"; son de investigación operativa): arista, nodo, capacidad, fuente y sumidero.
- **Ruta más corta**: el camino de menor distancia entre origen y destino.
- **Árbol de expansión mínima**: conectar todos los nodos al menor costo.
- **Flujo máximo**: pasar lo máximo posible entre origen y destino, respetando capacidades.
- **Flujo de costo mínimo**: cubrir la demanda al menor costo.

### 1.11 Verificación y ambientes de simulación

- Ejecutar la red = **simular**. Eso da una **verificación** del modelo. Una **validación** necesita algo más formal (las técnicas matemáticas se acercan a una "prueba").
- Si el modelo es grande, a mano no se puede: hacen falta herramientas que lo ejecuten solas (por ejemplo **HPetriSim**, el de los ejercicios).
- **Ambientes gráficos**: ves todo rápido, pero definir la red es tedioso y en redes grandes el dibujo se vuelve confuso.
- **Ambientes estructurales** (intérprete): perdés lo visual, pero la red escrita como pseudocódigo se parece al código (lenguajes como ADA o Modula).

### 1.12 Práctica que entra en el parcial: resolver una red paso a paso 📁

Entra: **árbol de alcanzabilidad**, **características y propiedades**, y **resolver una red con máquina de testigos y método matricial**. Los tres ejemplos están verificados por computadora.

**Receta para el examen (6 pasos)**

1. **Leer la red**: lugares, transiciones, arcos (y sus pesos) y M0. Escribir I(t) y O(t) de cada transición.
2. **Matrices**: C⁻ (entradas), C⁺ (salidas) y **C = C⁺ − C⁻**. **Filas = transiciones, columnas = lugares**.
3. **Árbol de alcanzabilidad**: desde M0, por cada transición habilitada calculá el marcado nuevo y numeralo (M1, M2…). Cortá en los **nodos frontera** (ver 1.5). Con ω: ω + 1 = ω y ω − 1 = ω.
4. **Máquina de testigos**: juntá los duplicados y dibujá el **grafo de marcados**. Cada óvalo lleva los lugares marcados (repetidos si tienen más de una marca).
5. **Método matricial**: comprobá una secuencia σ con **M' = M + f(σ)·C**. Como la ecuación no dice el orden, revisá que cada transición esté habilitada en su momento (**M ≥ ej·C⁻**).
6. **Propiedades**: leelas del árbol y del grafo con esta tabla:

| Propiedad | Cómo la ves en el árbol o en la máquina de testigos |
|---|---|
| **Viva** | No hay marcados muertos y, desde cualquier estado, cada transición puede volver a dispararse |
| **Parcialmente viva** | No hay marcados muertos, pero alguna transición deja de poder dispararse |
| **No viva** | Aparece un marcado muerto (bloqueo total) |
| **Acotada (k-acotada)** | No aparece ω; k = el máximo de marcas que llega a tener un lugar |
| **Segura** | k = 1: ningún lugar pasa de una marca |
| **No acotada** | Aparece ω en algún lugar |
| **Cíclica (reversible)** | Desde todos los estados se puede volver a M0 |
| **Conservativa** | La suma de marcas es igual en todos los marcados (o la suma ponderada con un vector peso) |
| **Conflicto** | Estructural: un lugar con 2 o más transiciones de salida. Efectivo: en algún marcado las dos están habilitadas y disparar una deshabilita la otra |
| **Concurrencia** | Dos transiciones habilitadas a la vez que no comparten entradas |
| **Exclusión mutua de lugares** | Dos lugares que nunca están marcados a la vez |
| **Pura** | Ningún lugar es entrada y salida de la misma transición |

**Ejemplo 1 — red acotada (la de la lectura, ver 1.6)**

P = {p1…p5}, M0 = (1, 0, 0, 0, 0). t1: p1 → p2, p3; t2: p2 → p5; t3: p3 → p4; t4: p5 → p2; t5: p4, p5 → p1. Las matrices están en 1.6.

Árbol de alcanzabilidad:

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

Método matricial: σ = t1 t3 t2 t5 → f(σ) = (1 1 1 0 1). f(σ)·C = suma de las filas t1, t2, t3 y t5 de C = (0 0 0 0 0) → **M' = M0**: la secuencia vuelve al inicio. t5 está habilitada en M4: e5·C⁻ = (0 0 0 1 1) ≤ (0 0 0 1 1).

Propiedades:
- **Viva** (sin marcados muertos; desde cualquier estado se vuelve a todos).
- **Segura** (1-acotada), **cíclica**, **pura**.
- **No es estrictamente conservativa** (M0 tiene 1 marca y el resto 2), pero sí respecto del vector peso (2 1 1 1 1).
- **Conflicto** estructural en p5 (t4 y t5) y efectivo en M4.
- **Concurrencia**: t2 y t3 en M1; t3 y t4 en M2.
- **Exclusión mutua de lugares**: p2 y p5, p3 y p4, y p1 con todos los demás.

**Ejemplo 2 — red no acotada (con ω)**

P = {p1, p2, p3}, M0 = (1, 0, 0). t1: p1 → p2; t2: p2 → p1, p3; t3: p3 → (nada, es una transición sumidero).

| | C⁻ (p1 p2 p3) | C⁺ (p1 p2 p3) | C (p1 p2 p3) |
|---|---|---|---|
| t1 | 1 0 0 | 0 1 0 | −1 1 0 |
| t2 | 0 1 0 | 1 0 1 | 1 −1 1 |
| t3 | 0 0 1 | 0 0 0 | 0 0 −1 |

Árbol de alcanzabilidad:

```
M0 (1,0,0)
└─ t1 → M1 (0,1,0)
   └─ t2 → (1,0,1) cubre a M0 (igual en p1 y p2, más en p3) → M2 (1,0,ω)
      ├─ t1 → M3 (0,1,ω)
      │  ├─ t2 → (1,0,ω)  duplicado de M2
      │  └─ t3 → (0,1,ω)  duplicado de M3
      └─ t3 → (1,0,ω)  duplicado de M2
```

Máquina de testigos: p1 —t1→ p2 —t2→ p1 p3ω; p1 p3ω —t1→ p2 p3ω y —t3→ p1 p3ω; p2 p3ω —t2→ p1 p3ω y —t3→ p2 p3ω.

Método matricial: σ = t1 t2 t1 t2 t3 → f(σ) = (2 2 1) → M' = (1 0 0) + 2·(−1 1 0) + 2·(1 −1 1) + (0 0 −1) = **(1 0 1)**. Paso a paso: (0 1 0), (1 0 1), (0 1 1), (1 0 2), (1 0 1).

Propiedades:
- **No acotada** (p3 llega a ω; p1 y p2 son 1-acotados).
- **Viva**.
- **Cíclica**: desde (1, 0, k) disparás t3 k veces y volvés a M0. Ojo: el árbol con ω no alcanza para afirmarlo, hay que razonarlo.
- **No conservativa**, **pura**, **sin conflicto** (ningún lugar tiene dos transiciones de salida).
- **Exclusión mutua de lugares**: p1 y p2 (siempre p1 + p2 = 1).

**Ejemplo 3 — exclusión mutua de dos procesos (semáforo)**

Lugares: a1 y a2 (proceso esperando), b1 y b2 (proceso usando el recurso), s (recurso libre). M0 = (a1, b1, a2, b2, s) = (1, 0, 1, 0, 1). t1: a1, s → b1; t2: b1 → a1, s; t3: a2, s → b2; t4: b2 → a2, s.

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
- **Viva**, **segura**, **cíclica**, **pura**.
- Conservativa respecto del vector peso (1 2 1 2 1).
- **Conflicto** estructural y efectivo en s: en M0, t1 y t3 están habilitadas y disparar una deshabilita la otra.
- **Exclusión mutua**: b1 y b2 nunca están marcados a la vez.

**Errores típicos al resolver**

- ❌ Seguir expandiendo un nodo **duplicado** → ✅ se corta ahí.
- ❌ Poner ω sin compararlo con un **antecesor del mismo camino**, o "restarle" a ω → ✅ ω − 1 = ω.
- ❌ Armar la matriz con **filas = lugares** → ✅ filas = transiciones.
- ❌ Creer que si M' = M + f(σ)·C tiene solución, la secuencia se puede disparar → ✅ es **necesaria pero no suficiente**.
- ❌ En la máquina de testigos, no repetir el nombre de un lugar con **dos marcas** → ✅ se repite.

---

## 2. Business Intelligence (Tema 8) 📁

> **En una frase:** BI es **usar los datos de la empresa para tomar mejores decisiones**, de forma continua.

### 2.1 Definición

- **Business Intelligence** (BI) = "inteligencia de negocio". Objetivo: ayudar a la organización a ser más **competitiva**, de forma **sostenible y continuada**, dándole información para **tomar decisiones**.
- Lo popularizó **Howard Dresner** (consultor de Gartner) como "término paraguas" para métodos que mejoran las decisiones usando **hechos** (lo que ya pasó).
- 👉 Idea central: **datos → información → conocimiento**.

**Definición de Gartner** (la más ajustada): BI es un **proceso interactivo** para **explorar** y **analizar información estructurada** de un **área** (normalmente en un ***datawarehouse***), para descubrir **tendencias o patrones**, sacar ideas y conclusiones. Incluye **comunicar** lo que se descubre y **hacer los cambios**. Las áreas pueden ser clientes, proveedores, productos, servicios y competidores.

| Parte de la definición | 👉 Qué quiere decir |
|---|---|
| Proceso interactivo | Se hace **todo el tiempo**, no una sola vez. Así ves tendencias y cambios |
| Explorar | Primer vistazo: entender qué pasa y encontrar relaciones que no conocías |
| Analizar | Ver cómo se relacionan las variables (si un cliente hace esto, ¿uno parecido hará lo mismo?) |
| Información estructurada y *datawarehouse* | Tablas relacionadas, con registros y atributos, guardadas en un **almacén de datos** |
| Área de análisis | Todo proyecto tiene un objeto (clientes, productos) y un objetivo (bajar costos, subir ventas) |
| Comunicar y efectuar cambios | Lo descubierto tiene que llegar a quien puede cambiar algo |

- **Definición del TDWI** (The Data Warehousing Institute): término paraguas para procesos, herramientas y tecnologías que convierten **datos en información, información en conocimiento** y planes para manejar el negocio. Tiene dos partes:
  - ***Back end*** ("trastienda"): el *datawarehousing*.
  - ***Front end*** ("mostrador"): consultas, informes, análisis y visualización.

### 2.2 De los datos a las decisiones

- Los **datos** de las transacciones (qué se vendió, cuándo, quién, cómo se pagó) se convierten en **información operativa** (ventas del día, ticket medio, ventas por artículo).
- Esa información sirve para **decisiones**:
  - **Operativas**: reponer, asignar turnos.
  - **Estratégicas**: qué hacer cuando bajan las ventas. ¿Viene menos gente o cada cliente gasta menos?
- Con el tiempo aparecen **tendencias** y **relaciones entre productos**, que permiten promociones y mejor ubicación.

### 2.3 Quién lo necesita

- Compras, ventas, negociación con bancos, marketing y personal. 👉 En resumen: **todo el que decide**. Las decisiones pueden ser **operativas o estratégicas**.

### 2.4 Beneficios

| Tipo | 👉 Qué son | Ejemplos |
|---|---|---|
| **Tangibles** (más ingresos) | Se miden en plata | Segmentar clientes, reducir el abandono, análisis de la cesta de la compra, medir campañas, encontrar clientes rentables |
| **Tangibles** (menos costos) | Se miden en plata | Negociar con proveedores, inventarios *just-in-time*, detectar fraude, menos deudas incobrables, "una sola versión de la verdad" |
| **Intangibles** | No se miden fácil | Mejor atención y satisfacción del cliente, información más actual y precisa, más integración, ventaja competitiva |
| **Estratégicos** | Ayudan a decidir el rumbo | A qué clientes, mercados o productos ir; decisiones más rápidas y basadas en hechos |

### 2.5 Componentes básicos

**Los 6 componentes de todo proyecto de BI**:

1. **Problema del negocio** a responder.
2. **Equipo** (o persona) que analiza.
3. **Información interna** de los sistemas de la organización.
4. **Información externa** a la organización (mercado, proveedores, tarifas).
5. Una **base de datos**: el *datawarehouse*.
6. Una **aplicación de BI** para analizar y visualizar.

**Nota técnica 1 — Sistemas de información**:
- Las organizaciones necesitan información para **registrar transacciones**, para **decidir y controlar** y para **nuevos negocios** (vender información).
- Los sistemas sirven para **controlar, coordinar y decidir** en la **planificación, la gestión y las operaciones**.
- Preguntas **estructuradas** (respuesta sí/no o un número: ¿entregamos a tiempo?) vs. **no estructuradas** (¿lanzamos el producto Y en el mercado Z?).
- **ERP** (*Enterprise Resources Planning*): integra módulos con el concepto de **dato único**. Si las aplicaciones no están integradas, se pasan datos con **interfases**.

### 2.6 Retorno de la inversión (ROI)

👉 El ROI responde: **¿lo que gano vale lo que gasto?**

- **ROI simple = valor para el negocio / costo del proyecto**. El costo es fácil de medir; el valor es lo difícil.
- **Los 8 pasos de Bill Whittemore**:
  1. Definir el problema u oportunidad con objetivos **específicos, medibles, alcanzables, adecuados y con plazo**.
  2. Juntar requerimientos.
  3. Construir el proyecto.
  4. Identificar y medir los beneficios.
  5. Fijar el punto de partida de costos e ingresos.
  6. Calcular el **TCO** (*Total Cost of Ownership*, costo total de propiedad): *hardware*, *software*, consultoría, personal, lanzamiento, mantenimiento y formación.
  7. Calcular **ROI = NPV / inversión inicial × 100**.
  8. Seguir y corregir.
- **NPV** (*Net Present Value*, valor actual neto) = suma de los flujos de caja (CF, *Cash Flow*) de cada año, descontados a la tasa r, **menos** la inversión inicial.

### 2.7 Modelización del negocio

- 👉 **"Lo que no se mide, no se puede gestionar"**. Primero definís **qué** medir y **cómo**: el **modelo de negocio** y sus métricas.
- **Modelo de negocio**: una **versión simplificada de la realidad** para **documentar, probar y desarrollar teorías** sobre cómo funciona el negocio y **experimentar** qué pasa si cambiás algo. Tiene que estar **vivo**, como el negocio.
- **Silos de información**: departamentos que no comparten información (por falta de integración o por política). 👉 Lo mejor para un departamento no siempre es lo mejor para la empresa.
- **Cómo se arma**: con metodologías como **contabilidad analítica o de costos, EFQM** (*European Foundation for Quality Management*), **Six Sigma, análisis de procesos, modelos financieros y análisis de ratios**; buscando áreas críticas, factores que influyen en el resultado y la estructura de la organización.

### 2.8 Indicadores clave (KPI)

- **KPI** (*Key Performance Indicators*): números que dicen **si la organización cumple sus objetivos** y cuánto avanza.
- Un KPI tiene que:
  - **Reflejar los objetivos**.
  - Ser **crítico para el éxito**.
  - Ser **cuantificable y comparable**.
  - Permitir **acciones correctivas**.
- Pocos, alineados entre departamentos y definidos con los responsables de cada área.
- Cada KPI tiene **nombre, definición, forma de cálculo y objetivo**.

### 2.9 Modelo de datos

- **Modelo relacional** (E. F. **Codd**, **1970**): tablas y relaciones.
  - **PK** (*Primary Key*, clave primaria): identifica cada registro.
  - **FK** (*Foreign Key*, clave externa): relaciona tablas.
  - Se consulta con **SQL** (*Structured Query Language*; ver la trampa 4 del principio).
  - El **modelo entidad-relación** muestra las tablas y cómo se relacionan.
- Orden: primero el modelo de negocio; después **qué medir (hechos)** y **cómo mirarlo (dimensiones)**.
- Las dimensiones responden **qué, quién, por qué, dónde y cuándo**.

👉 **Hechos = los números que medís. Dimensiones = desde dónde los mirás.**

- **Tabla de hechos** (*fact table*): lo que se mide (por ejemplo, el total del ticket) + las claves de las dimensiones.
- **Tablas de dimensiones**: el contexto para agrupar y filtrar (tiempo, centro, empleado, forma de pago).
- **Dimensiones degeneradas**: no necesitan tabla propia (número de ticket, identificador de caja).
- **Dimensión tiempo**: la fecha se parte en día de la semana, del mes, del año, mes, trimestre, año, vacaciones y fin de semana. Esos datos (y los feriados) **no están** en el sistema transaccional: hay que agregarlos.

| | **Esquema estrella** | **Esquema copo de nieve** (*snowflake*) |
|---|---|---|
| Dimensiones | **Una tabla por dimensión**, desnormalizada | Dimensiones **normalizadas**, partidas en tablas relacionadas (Zona separada de Centro) |
| Relaciones | Solo hechos ↔ dimensiones | También dimensión ↔ dimensión |
| Redundancia | Sí (la zona se repite en cada centro) | No |
| A favor | Más simple y rápido de consultar | Ocupa menos (a veces la diferencia es poca) |
| En contra | Ocupa más | Más complejo |

👉 La **estrella** es "plana" (una tabla por dimensión); el **copo de nieve** se "ramifica" (las dimensiones se parten en más tablas).

- **Constelación de hechos** (o esquema **galaxia**): varias estrellas con distintas tablas de hechos que comparten dimensiones.
- **Granularidad** = nivel de detalle. 👉 **Más granularidad = más detalle** (analizar **líneas** de ticket es más granular que analizar tickets). Cada nivel responde unas preguntas y no otras. **Cada vez que agregás (sumás), perdés información**. Conviene construir al **máximo detalle** si el volumen lo permite.
- **Jerarquías**: año → trimestre → mes → día; familia → subfamilia → artículo; zona → centro; categoría → empleado. Sirven para subir y bajar de nivel.
- **Multidimensionalidad**: analizar por **varias dimensiones a la vez** (ventas de un artículo por centro y por mes).
- Si fabricante y artículo están en la misma dimensión no se pueden cruzar → van en dimensiones distintas.
- 👉 **Cada modelo de datos responde un número limitado de preguntas**, y cada modelo responde preguntas distintas.

### 2.10 Componentes de BI (capítulo 4 del libro)

👉 **El camino de los datos:** **fuentes de información → proceso ETL → *datawarehouse* (con su metadata) → motor OLAP → herramientas de visualización**.
En un proyecto real, el orden de trabajo es otro: primero se definen **objetivos, alcance y modelos de negocio**.

**Fuentes de información**

- **Sistemas operacionales o transaccionales**: aplicaciones a medida, ERP, CRM (relación con clientes), SCM (cadena de suministro).
- **Sistemas departamentales**: previsiones, presupuestos, hojas de cálculo.
- **Fuentes externas**, a veces compradas (estudios de mercado, datos de población).
- La información puede ser estructurada, semiestructurada o **no estructurada** (correos, cartas, informes, videos).

**Calidad de datos**

- 👉 **Si entra basura, sale basura.** Los errores del *datawarehouse* **se contagian a toda la organización** y llevan a malas decisiones; los usuarios **dejan de confiar** en el proyecto.
- Los errores vienen de los **sistemas transaccionales**, del **proceso ETL** o del propio ***datawarehouse***. Conviene **corregirlos en el origen** (que el usuario elija de una lista en vez de escribir libre), no solo en el ETL.
- La calidad es un **problema de negocio, no solo técnico**.
- **7 características** de datos de calidad: **precisión, integridad, coherencia, totalidad, validez, disponibilidad y accesibilidad**.

**Proceso ETL** (*Extract, Transform, Load*: extracción, transformación y carga)

- 👉 Es "la cocina" del BI: se lleva **entre el 60 % y el 80 %** del tiempo del proyecto. Tiene **5 subprocesos**:

| Subproceso | 👉 Qué hace |
|---|---|
| 1. **Extracción** | Saca los datos de las fuentes: datos **en bruto**. A mano (rutinas, por ejemplo en COBOL) o con herramientas ETL (lo más rentable) |
| 2. **Limpieza** | Revisa la calidad, saca duplicados, corrige errores, completa vacíos: datos **limpios** |
| 3. **Transformación** | Ordena y **resume** según los modelos (cambios de formato, códigos, valores calculados y **agregados**). Acá se fija la **granularidad** |
| 4. **Integración** | Verifica que los datos coincidan con las definiciones del *datawarehouse* y los carga (por ejemplo, que los totales de ventas coincidan con el origen) |
| 5. **Actualización** | Define **cada cuánto** se hacen nuevas cargas |

- **Almacén de datos intermedio** (*data staging*): una "sala de espera" entre la extracción y lo demás, mientras se limpian los datos. Junta datos de varias fuentes. **Los usuarios finales nunca entran**.
- **Datos "sucios"**: valores por defecto (código 999), campos vacíos, valores raros o contradictorios, campos con varios usos, claves reutilizadas, identificadores repetidos.
- **Etapas de la limpieza**: **depurar** (*parsing*: separar nombre y apellido), **corregir** (*correcting*), **estandarizar** (*standardizing*), **relacionar** (*matching*: encontrar duplicados) y **consolidar** (*consolidating*: unir registros relacionados).

***Datawarehouse*** (almacén de datos)

- 👉 Es **el lugar único donde están todos los datos listos para analizar**: **consistentes, integrados, históricos y preparados**. Usar planillas en su lugar trae errores, trabajo repetido, "entornos paralelos" y **distintas versiones de la misma realidad**.
- **Hugh J. Watson**: "una colección de información creada para soportar las aplicaciones de toma de decisiones". ***Datawarehousing*** = todo el proceso: extraer, transformar, cargar y dar acceso a los usuarios.
- **Bill Inmon — 4 características**:
  - **Orientado a un área** (un problema de negocio).
  - **Integrado** (medidas, códigos y formatos comunes).
  - **Indexado en el tiempo** (guarda historia).
  - **No volátil** (los usuarios no lo modifican; se actualiza cada tanto).
- **Ralph Kimball**: da acceso a la información, es consistente, se puede separar y combinar por cada medida, incluye herramientas de consulta y es "el lugar donde publicamos la información".
- Guarda los datos para **maximizar flexibilidad, facilidad de acceso y administración**. Se actualiza **mensual, semanal o diariamente**. El concepto *right time* dice que cada situación pide su propio plazo.

**Data Mart y estrategias de construcción**

- **Data Mart**: un "mini *datawarehouse*" para una **comunidad de usuarios** (un departamento, un nivel o un grupo con objetivos comunes) y pocas áreas (por ejemplo, marketing y ventas). **Más chico**: menos datos, menos modelos, menos usuarios. Surgieron porque el *datawarehouse* corporativo era caro, lento e inflexible.
  - **Dependiente**: se alimenta del *datawarehouse* corporativo.
  - **Independiente**: se alimenta directo de las fuentes; puede mantener los **silos de información**.

| | **Inmon** | **Kimball** |
|---|---|---|
| Estrategia | Primero el *datawarehouse* **corporativo**, y de ahí salen los Data Marts (de arriba hacia abajo) | Armar **Data Marts** por área, sin un *datawarehouse* central |
| A favor | Integrado y escalable | Barato y fácil; la más común |
| En contra | Caro, lento, puede fracasar | Riesgo de silos y de dejar los criterios para después |

👉 **Inmon = "primero lo grande"**; **Kimball = "primero lo chico"**. Según Watson, **las dos sirven** si se hacen bien. También existen la **híbrida** y la **federada**.

- **Metadata** o **diccionario de datos**: "información sobre la información" (qué significa cada tabla y atributo, de dónde viene, cómo se transformó). Obliga a que todos usen **las mismas palabras** ("margen bruto" tiene que estar definido).
- **ODS** (*Operational Data Store*): junta datos de varias fuentes para decisiones **operativas** (del día a día). Su información es **volátil**, se actualiza en **tiempo real** y tiene como máximo dos o tres meses. Suele alimentar al *datawarehouse*.

**OLAP** (*On-Line Analytical Processing*, procesamiento analítico en línea)

- La tecnología más usada para analizar el *datawarehouse*: análisis **multidimensional** en distintos **niveles**, desde el resumen total hasta el máximo detalle.
- **FASMI** (resumen de las 12 reglas de Codd según el OLAP Council): ***Fast*** (rápido), ***Analysis*** (lógica de negocio y estadística), ***Shared*** (compartido y seguro), ***Multidimensional*** e ***Information*** (manejar toda la información).
- Se representa con **cubos**: cada celda guarda un **hecho** (por ejemplo, unidades vendidas de un libro a un cliente en un año).

| Operación | 👉 Qué hace |
|---|---|
| **Rotar** (*slicing*) | Girar el cubo: cambiar el orden de las dimensiones (de clientes a libros) |
| **Seleccionar** (*dicing*) | Quedarte con algunas celdas (cliente 2, libros 1 y 2, año 1) |
| **Agregar** (*roll-up*) | Subir al resumen (total de libros) |
| **Bajar al detalle** (*drill-down*) | Bajar por una jerarquía (por materias) |

| Tipo | Cómo accede | Ventaja / desventaja |
|---|---|---|
| **ROLAP** (relacional) | Directo a la base relacional, normalmente sobre un modelo estrella; traduce las consultas a SQL | Sin límite de tamaño y más flexible / más lento |
| **MOLAP** (multidimensional) | A una base multidimensional con datos precalculados | Muy rápido, para soluciones chicas de un departamento / si cambian las dimensiones, hay que recargar el cubo |
| **HOLAP** (híbrido) | Resúmenes en la multidimensional y detalle en la relacional | Junta lo mejor de los dos |
| **DOLAP** (de escritorio) | Cubo en la memoria de la computadora del usuario | El usuario recibe solo lo que le interesa |

- Alternativa al OLAP: herramientas de **lógica asociativa** (por ejemplo QlikView): guardan cada valor una sola vez y consultan sin dimensiones fijas.

**Herramientas de BI**: generadores de informes; consultas e informes para el usuario final; herramientas OLAP; ***dashboards*** (indicadores operativos o tácticos de **un área**) y ***scorecards*** (nivel **estratégico**, indicadores relacionados, **toda la organización**, como el *Balanced Scorecard* de Kaplan y Norton); planificación y simulación; minería de datos; minería de texto; visualización y GIS (sistemas de información geográfica).

**Usuarios** (Eckerson y Howson)

- **Productores** de información (alrededor del **20 %**): estadísticos con minería de datos, autores de informes y usuarios avanzados.
- **Consumidores** (la mayoría): directivos, gestores, clientes y proveedores que usan cuadros de mando e informes, cada vez más por web.
- 👉 Se distinguen **roles, no personas**: el mismo ejecutivo puede usar un informe fijo y un cuadro de mando en tiempo real. Por eso hay que saber qué necesita cada rol antes de elegir la herramienta.

### 2.11 Guías del TP7 — respuestas

| Pregunta | Respuesta modelo |
|---|---|
| ¿Definición más ajustada de BI? | La de Gartner: proceso interactivo para explorar y analizar información estructurada (en un *datawarehouse*) y descubrir tendencias o patrones. Convierte datos en información y conocimiento para decidir con hechos |
| ¿Cuándo aplicar BI? | **Siempre, de forma continua**. Sobre todo con mercados que cambian rápido, cuando algo anda raro en el negocio o cuando quienes preparan la información están desbordados |
| ¿A qué organizaciones va dirigida? | A cualquiera que tome decisiones. Urgente en estructuras complejas, con muchos clientes o con procesos "artesanales" |
| ¿Qué beneficios aporta? | Tangibles, intangibles y estratégicos (ver 2.4) |
| ¿Cómo unificar información de distintos entornos? | Juntarla en un *datawarehouse* (copia, sin tocar los transaccionales), en tablas relacionadas, y cruzarla con herramientas de BI: "una sola versión de la verdad" |
| Concepto y utilidad del modelo de negocio | Versión simplificada de la realidad para documentar y probar teorías. Sirve para ver qué pasa si cambiás algo y para evitar silos |
| ¿Qué es el modelo relacional? | Tablas y relaciones (Codd, 1970) con PK y FK, consultado con SQL |
| Factores del modelado de datos | Partir del modelo de negocio; definir hechos y dimensiones; ver qué datos hay en los transaccionales y cuáles agregar (calendarios, feriados) |
| Estrella frente a copo de nieve | Ver tabla 2.9 |
| Granularidad y multidimensionalidad | Nivel de detalle (decide qué preguntas podés responder) y análisis por varias dimensiones a la vez |

---

## 3. Minería de datos (Tema 9) 📁

> **En una frase:** la minería de datos es **buscar automáticamente patrones escondidos** en muchos datos, para poder **predecir**.

### 3.1 Datos, información y conocimiento

- **Datos**: registros de lo que pasó.
- **Información**: lo que sale cuando le encontrás utilidad a los datos.
- **Conocimiento**: reglas de cómo una cosa afecta a otra. "El conocimiento es poder".
- **Minería de datos** (*Data Mining*, DM): métodos y algoritmos para la **extracción automática** de información resumida que muestra **relaciones escondidas** en grandes volúmenes de datos, con capacidad **predictiva**. Mezcla estadística y **aprendizaje automático** (inteligencia artificial).
- 👉 **Analogía**: una **montaña** (los datos) con **diamantes** escondidos entre las piedras (el conocimiento).
- Trabaja con **datos estáticos** (una foto del pasado que no cambia mientras analizás). **No confundir con monitoreo**: el monitoreo usa datos que cambian en tiempo real y **reconoce** patrones conocidos, no **descubre** nuevos.
- Apunte de clase: la define igual que al KDD (ver 3.2), de forma automática y para ayudar a decidir. Diferencia con BI según la clase: BI es más estático, saca conclusiones de datos estructurados que ya tenés.

### 3.2 Proceso KDD

- **KDD** (*Knowledge Discovery in Databases*, descubrimiento de conocimiento en bases de datos): se usa desde **1989**. Es una **inducción no supervisada** con dos partes: buscar regularidades interesantes y escribir reglas que las expliquen.
- **Definición**: extracción **no trivial** de información **implícita**, **previamente desconocida** y **potencialmente útil** a partir de un conjunto de datos.

**Las cuatro ideas del KDD**:

| Idea | 👉 Qué exige |
|---|---|
| **Lenguaje de alto nivel** | Que **una persona lo entienda**. Por eso las **redes neuronales** quedan afuera del KDD (son una "caja negra"), aunque sirvan como método de minería |
| **Precisión** | Los datos tienen ruido; se mide **qué tan seguro** es el resultado. Si la certeza es baja, no es conocimiento |
| **Interés** | Solo vale lo **nuevo, útil y no obvio** para el usuario |
| **Eficiencia** | Que el tiempo y la memoria crezcan de forma **polinomial** (razonable) con los datos |

- Mezcla aprendizaje automático, estadística, reconocimiento de patrones, inteligencia artificial, bases de datos, visualización, sistemas de apoyo a la decisión y recuperación de información.
- 👉 **KDD vs. minería de datos**: el **KDD es todo el proceso**; la **minería es un solo paso** adentro del KDD (el de descubrir). Es la parte fundamental (la única que encuentra patrones), pero está **subordinada** al KDD.

**Los 9 pasos del KDD** (interactivo e iterativo: podés volver atrás):

| Bloque | Paso | 👉 Qué hacés |
|---|---|---|
| **Preparar** | 1. **Comprensión del dominio** | Entender el negocio y qué quiere el usuario |
| | 2. **Creación del conjunto de datos objetivo** | Elegir variables y ejemplos, muestrear |
| | 3. **Preprocesado** | Sacar ruido, tratar faltantes, normalizar |
| | 4. **Transformación y reducción** | Quedarte con lo útil, menos variables. **Paso crítico**: decide si sale bien o mal |
| **Minar** | 5. **Elección del tipo de sistema** | Clasificación, regresión, agrupamiento o detección de desviaciones |
| | 6. **Elección del algoritmo** | Con qué algoritmo buscar |
| | 7. **Minería de datos** | Buscar el conocimiento. Sale bien si los pasos anteriores salieron bien |
| **Aprovechar** | 8. **Interpretación** | Entender lo encontrado; se puede volver al paso 1 |
| | 9. **Consolidación** | Incorporar o documentar el conocimiento, resolviendo contradicciones |

- **Fayyad** (según el artículo de la cátedra) resume el núcleo en **5 etapas**: **selección, preprocesamiento, transformación, minería de datos e interpretación/evaluación**. Si sumás la comprensión del dominio al principio y la consolidación al final, llegás a los 9 pasos.

Diagrama: **BD → Selección → Datos objetivo → Preprocesado → Datos preprocesados → Transformación → Datos transformados → Minería de datos → Patrones → Interpretación / Evaluación → Conocimiento**.

- **Por qué creció el análisis de datos** (3 razones):
  1. **Computadoras más potentes**.
  2. **Muchísimos más datos** (el ritmo de adquisición de datos crece sin parar).
  3. **Nuevos métodos** de aprendizaje.
- **Aprendizaje automático vs. minería**: el aprendizaje automático usa un conjunto **chico y elegido**; la minería parte de una base **grande** que se armó para **otra cosa**.

### 3.3 Fases del KDD según la lectura (6 estados)

1. **Recolección de datos**: fuentes internas y externas, muchas transaccionales. Conviene una fuente **unificada, accesible y separada** del trabajo transaccional. Depende de la fuente (**OLAP** u **OLTP**, *On-Line Transaction Processing*; *datawarehouse* o copia; **ROLAP** o **MOLAP**) y del usuario:
   - **Picapedreros o granjeros**: sacan informes periódicos y controlan valores.
   - **Exploradores**: buscan patrones nuevos.
   - Información externa: censos, datos de la industria, clima, calendarios, bases compradas.
2. **Selección, limpieza y transformación**: sacar datos erróneos o contradictorios (**limpieza**) e irrelevantes (**criba**), casi siempre con estadística (histogramas, muestreo vertical u horizontal, redefinir atributos).
3. **Minería de datos**: datos en disco, muchísimas variables, evidencia positiva, datos imperfectos.
   - **Minería dirigida**: sabés qué buscás (predecir).
   - **No dirigida**: no sabés qué buscás.
4. **Evaluación y validación**:
   - 1.ª fase: probar la precisión con **ejemplos nuevos e independientes**.
   - 2.ª fase: **prueba piloto** (por ejemplo, un *mailing* a un grupo de clientes).
5. **Interpretación y difusión**: el modelo puede necesitar implementación (fraude con tarjetas en tiempo real), interpretación (zonas geográficas) o difusión (cerveza y congelados se compran juntos → ponerlos en **estantes lejanos** para que el cliente recorra el local).
6. **Actualización y monitorización**: un modelo que hoy sirve deja de servir si cambia el contexto. Hay que revalidarlo con datos nuevos.

### 3.4 Datos atípicos y faltantes

👉 **Atípicos** (*outliers*) = valores muy raros. **Faltantes** (*missing values*) = valores que no están.

| Acción | Atípicos | Faltantes |
|---|---|---|
| **Ignorar** | Con algoritmos robustos (árboles) | Con algoritmos robustos (árboles) |
| **Filtrar la columna** | Extremo; mejor una columna "normal / atípico" | Extremo; mejor una columna sí/no "existía / no existía" |
| **Filtrar la fila** | **Sesga los datos** (suelen ser casos especiales) | **Sesga los datos** |
| **Reemplazar el valor** | Por nulo, máximo, mínimo o media; o predecirlo | Por la media; o predecirlo |
| **Discretizar** | Muy alto, alto, medio, bajo, muy bajo: el atípico cae en un extremo | — |
| **Segmentar** | — | Un modelo por grupo según los datos que haya, y después se combinan |
| **Esperar** | — | Mejorar la calidad y esperar los datos |

- **Por qué faltan datos**:
  - **Relevantes**: que falte dice algo (no dar el teléfono = no quiere que lo molesten).
  - **No existentes**: no puede haberlos (un cliente nuevo no tiene 12 meses de consumo).
  - **Incompletos**: se perdieron al unir fuentes distintas.

### 3.5 Evolución histórica

| Etapa | Pregunta típica | Tecnología | Característica |
|---|---|---|---|
| Recolección (años 60) | Beneficios totales de los últimos 4 años | Computadoras, cintas, discos | Mira al pasado, datos estáticos |
| Acceso a los datos (años 80) | Ventas en Cataluña la última Navidad | Bases relacionales (SQL), ODBC | Mira al pasado, dinámico por registro |
| *Datawarehouse* y apoyo a decisiones (años 90) | Ventas en Andalucía, bajando hasta la tienda | OLAP, bases multidimensionales | Mira al pasado, en varios niveles |
| **Minería de datos** | Tendencia de venta en Castilla el próximo año | Algoritmos avanzados, multiprocesadores | **Mira al futuro (prospectivo), proactivo** |

👉 Las tres primeras preguntan **"¿qué pasó?"**; la minería pregunta **"¿qué va a pasar?"**.

### 3.6 Qué no es minería de datos

**No es estadística**:

| Eje | Minería de datos | Estadística clásica |
|---|---|---|
| Automatización | Arma el modelo **sola** | La maneja un **estadístico** |
| Enfoque | **Exploratorio** (busca) | **Confirmatorio** (prueba hipótesis) |
| Inteligencia artificial | La usa | Teoría de la probabilidad |
| Dimensionalidad | Mejor con **muchas variables** | Le cuesta con muchas variables |
| Supuestos | **Menos exigente** | Los datos deben cumplir requisitos |

Apunte de clase: la estadística toma **muestras** y saca conclusiones de la población; la minería trabaja con **toda la base** (y usa estadística).

**No es OLAP**: OLAP **navega** rápido por los datos (análisis multidimensional) pero **no genera información nueva**. Sus arquitecturas (MOLAP, ROLAP y otras) están en 2.10.

### 3.7 Los tres retos

1. **Falsa interpretación**: es fácil engañarse con estadística (los resultados valen para grupos, no para individuos). Con software de minería es aún más fácil "hacer creíble una falsedad".
2. **Correlación no es causalidad — Florida**: en Florida la gente muere a edad más alta que en el resto de Estados Unidos. ¿Vivir ahí alarga la vida? **No**: es que ahí se van a vivir los jubilados (**efecto de selección**). 👉 La minería **genera hipótesis** desde los datos (es **explorativa, no explicativa**): hay que validarlas con datos nuevos. Además no puede hacer experimentos.
3. **Tiempo, espacio y privacidad**:
   - Variables que cambian durante el período.
   - **Granularidad del tiempo**: con datos mensuales no podés predecir por semana.
   - **Privacidad**: si cruzás las bases del teléfono, el banco y el súper, armás un perfil completo de una persona. La ley no acompañó.


### 3.8 Tareas de la minería de datos

👉 **Predictiva / supervisada** = sabés qué querés predecir. **Descriptiva / no supervisada** = buscás qué hay.

| Tarea | 👉 Qué hace | Tipo |
|---|---|---|
| **Clasificación** | Pone cada dato en una **clase ya definida** | Supervisado / predictivo |
| **Regresión** | Predice un **número** (valor real, continuo) | Supervisado / predictivo |
| **Agrupamiento** (*clustering*) | Arma grupos parecidos sin saber de antemano cuáles | No supervisado / descriptivo |
| **Condensación** (descripción de conceptos) | Describe un grupo en **pocas palabras** | No supervisado / descriptivo |
| **Detección de desviaciones** | Encuentra cambios importantes respecto de lo normal | No supervisado / descriptivo |
| **Modelado de dependencias** | Encuentra qué variables dependen de cuáles | No supervisado / descriptivo |

**Proceso de minería** (4 estados): **preprocesado** → **selección de características** (las variables que más influyen) → **algoritmo de extracción** (el modelo) → **evaluación y validación**.

### 3.9 Predictivo frente a descriptivo

- **Predictivo (supervisado)**: predice una **etiqueta** que ya conocés en los datos viejos. Dos fases: **entrenamiento** (aprende con datos etiquetados) y **prueba** (lo probás con el resto).
- **Descriptivo (no supervisado)**: descubre patrones en los datos actuales.
- **Taxonomía**: interpolación, predicción secuencial, aprendizaje supervisado, aprendizaje no supervisado y abducción. En lo supervisado:
  - **Clasificación**: clases separadas. **Categorización**: pueden superponerse.
  - Clase con dos valores = ***concept learning***. Clase continua = **estimación**.
- **Reglas de asociación** (tipo "el que compra X compra Y"):
  - **Confianza** = casos con antecedente **y** consecuente / casos con el antecedente. 👉 "¿Qué tan seguido se cumple?"
  - **Soporte** = casos (o %) donde se aplica la regla. 👉 "¿Qué tan común es?"
  - Algoritmo tipo **Apriori**, en dos fases: **A**, buscar combinaciones frecuentes (*large itemsets*) con soporte suficiente; **B**, convertirlas en reglas y quedarse con las de confianza suficiente.
  - También hay asociaciones entre jerarquías, **negativas** ("80 % de quienes compran pizza congelada no compra lentejas") y con valores continuos (se pasan a rangos).
- **Combinar hipótesis**:
  - ***Boosting***: el **mismo** algoritmo sobre distintas partes de los datos.
  - ***Voting***: **distintos** algoritmos sobre todos los datos.

### 3.10 Métodos y técnicas

**Métodos**: agrupamiento (segmentación estática o dinámica), asociación, **secuenciamiento** (asociación donde importa el **tiempo**), reconocimiento de patrones, **previsión** (*forecasting*, series temporales), simulación (por ejemplo CAD-CAM), optimización (ganar más o gastar menos con restricciones) y clasificación (*scoring*).

| Supervisados | No supervisados |
|---|---|
| Árboles de decisión | Detección de desviaciones |
| Inducción neuronal | Segmentación |
| Regresión | Agrupamiento (*clustering*) |
| Series temporales | Reglas de asociación |
| | Patrones secuenciales |

**Técnicas**:

- **Estadísticas**:
  - **ANOVA** (análisis de la varianza): ¿los promedios de los grupos son distintos?
  - **Ji cuadrado**: ¿dos variables son independientes?
  - **Componentes principales**: reduce la cantidad de variables.
  - Análisis de **clusters**: arma grupos.
  - **Análisis discriminante**: clasifica en grupos ya definidos.
  - **Regresión lineal** (la más básica; variables continuas) y **logística** (acepta variables discretas).
- **Árboles de decisión**: parten los datos en grupos más chicos.
  - **CART**: parte en **2** (validación cruzada, índice de Gini).
  - **CHAID** (*Chi Squared Automatic Interaction Detector*): parte en **más de 2** (test Ji cuadrado).
- **Reglas de asociación**: "cesta de la compra", reglas SI … ENTONCES.
- **Redes neuronales**: copian la idea del cerebro (estudios desde 1930), con capas de neuronas que aprenden patrones; supervisadas o no. Problema: **no dan una ecuación que explique el modelo** (caja negra).
- **Algoritmos genéticos**: mutación y cruce (como la evolución) para **optimizar**; se usan al principio para **elegir variables**.
- **Lógica difusa**: los grupos tienen bordes suaves, no cortes exactos.
- **Series temporales**: ciclos, tendencias y temporadas para predecir, si no hay cambios de fondo.
- **Redes bayesianas**: aprenden dependencias y causas, combinan conocimiento con datos, evitan el sobreajuste y manejan datos incompletos.
- **Inducción de reglas** y **sistemas expertos** (con motor de inferencia).

### 3.11 Evaluación de la minería

- **Tres medidas clave** de una herramienta: **precisión** (¿acierta?), **explicación** (¿se entiende?) e **integración** (¿se mete en el negocio sin copiar datos?).

| Medida de precisión | 👉 Qué es |
|---|---|
| **Precisión** | % de predicciones correctas |
| **Tasa de error** | Lo contrario de la precisión. Útil con precisiones muy altas: pasar de 99 % a 99,5 % **reduce el error a la mitad** |
| **Tasa de error en rechazo** | Descartás las predicciones dudosas (rechazando el 80 % se puede duplicar la precisión) |
| **Error cuadrático medio** | Para números; castiga más los errores grandes |
| **Elevación** (*lift*) | Cuánto mejora respecto de elegir al azar: 30 % / 10 % = **3** (el modelo es 3 veces mejor que el azar) |
| **Beneficio / ROI** | La mejor medida: cuánto gana el negocio |

- **Explicación**: reglas generadas solas, OLAP integrado, evaluación automática del modelo.
- **Integración**: usar los datos como están, guardar el modelo como metadatos, preparar los predictores, manejar datos sucios, valores perdidos y **escalabilidad**.

### 3.12 Apuntes de clase (14/9)

- **Aplicaciones**: retener clientes, patrones de compra, detectar fraude, manejar riesgo (a quién prestarle), segmentar.
- **Ciclo de un proyecto** (9 pasos): aprender del negocio → recolectar → limpiar y transformar → definir meta y modelo → elegir algoritmos → generar reportes → generar predicciones → aplicar los resultados → actualizar los modelos.
- **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*): proceso confiable y repetible, pensado para gente con pocos conocimientos. **6 fases**: comprensión del negocio, comprensión de los datos, preparación de los datos, modelado, evaluación e implantación.
- **Bodega de datos**: base pensada para consultas, **consolidada, consistente, orientada a un tema, histórica y de solo lectura**. Es el punto de partida de la minería y no cambia mientras minás.
- **Minería vs. análisis de datos**: el análisis no suele ser automático ni con tanto volumen.
- **Minería vs. aprendizaje automático**: el aprendizaje automático es la parte de la inteligencia artificial que hace programas que aprenden; la minería lo usa para predecir.

### 3.13 Preguntas teóricas del TP8 (respuestas del grupo)

| Consigna | Respuesta clave |
|---|---|
| 1. Los 9 pasos con insumo y producto; qué pasa si falla el preprocesado | Cada paso usa lo que produjo el anterior. Si falla el **preprocesado**, el **modelo clasificador** aprende el ruido como si fuera un patrón, los faltantes mal tratados sesgan la muestra y los atípicos distorsionan. La evaluación puede parecer buena si los datos de prueba tienen el mismo defecto. **El modelo no sirve** |
| 2. Minería fundamental pero subordinada al KDD | "Minería sin KDD es una operación algorítmica **ciega**" (no sabe qué buscar, con qué calidad ni si lo encontrado vale). "KDD sin minería es un proceso **inconcluso**" (datos limpios, pero sin patrones) |
| 3. Minería vs. estadística; Florida | Ver 3.6 y 3.7 |
| 4. Minería vs. OLAP vs. monitoreo | Minería **genera** información nueva sobre datos **estáticos** (descubre, es proactiva). OLAP **navega** sobre datos **históricos resumidos** cuando el usuario consulta (*drill-down*, *roll-up*, *slice & dice*). Monitoreo **verifica** datos en **tiempo real** y reacciona (alertas) |
| 5. Mapa de tareas | Supervisado: clasificación y regresión. No supervisado: agrupamiento, dependencias, desviaciones y condensación |
| 6. Redes neuronales y lenguaje de alto nivel | Predicen bien, pero el conocimiento queda en miles de **números (pesos)**: es una **caja negra** que no se puede explicar. Choca con la exigencia de conocimiento **entendible** del KDD |
| 7. Faltantes y atípicos con sesgo | Ver 3.4: filtrar filas **sesga**; usar la media **reduce la varianza**; discretizar **pierde precisión**; segmentar puede **sobreajustar** |
| 8. Ensayo | Más potencia de *hardware* + más detalle de tiempo + privacidad: cuanto más detalle y más fuentes cruzadas, más preciso el perfil de cada persona. Marco legal: Ley 25.326 de Protección de Datos Personales (Argentina) y GDPR (Reglamento General de Protección de Datos, Unión Europea) |
| 9. KDD, CRISP-DM y SEMMA | Ver tablas abajo |

| Eje | KDD | CRISP-DM | SEMMA |
|---|---|---|---|
| Origen | **Académico** (1989, Fayyad) | **Consorcio de empresas**: DaimlerChrysler, SPSS y NCR; ligado a SPSS Clementine | **SAS Institute**; ligado a SAS Enterprise Miner |
| Fases | 9 (5 en el núcleo de Fayyad) | 6, en orden **no rígido** | 5: *Sample, Explore, Modify, Model, Assess*; el muestreo es **opcional** |
| Iteración | Muy iterativo, vuelve desde cualquier fase | Ciclo con mucha retroalimentación | Más en línea recta, con ajustes técnicos |
| Orientación al negocio | Arranca por el dominio; foco en la validez científica | **La más orientada al negocio** | Técnica; supone que los objetivos ya están definidos |
| ¿Incluye negocio y despliegue? | Sí (antes y después del núcleo) | Sí, explícitamente | **No explícitamente**; según Azevedo y Santos está implícito, porque no podés muestrear sin entender el negocio |

**Equivalencia de fases según el artículo de la cátedra** (Azevedo y Santos, "KDD, SEMMA and CRISP-DM: a parallel overview"):

| KDD | SEMMA | CRISP-DM |
|---|---|---|
| Antes del KDD (comprensión del dominio) | — | Comprensión del negocio |
| Selección | *Sample* | Comprensión de los datos |
| Preprocesamiento | *Explore* | Comprensión de los datos |
| Transformación | *Modify* | Preparación de los datos |
| Minería de datos | *Model* | Modelado |
| Interpretación / evaluación | *Assess* | Evaluación |
| Después del KDD (consolidación) | — | Despliegue |

- **Conclusión del artículo**: SEMMA y CRISP-DM son **formas de aplicar el proceso KDD**. CRISP-DM parece más completo, pero SEMMA también incluye (sin decirlo) el negocio y la consolidación.
- **Ojo:** el TP8 del grupo puso "preparación de los datos" junto al preprocesado. Según el artículo, el preprocesado va con **comprensión de los datos** y la transformación con **preparación de los datos**.

---

## 4. Big Data (Tema 10, entra en el final) 📁

> **En una frase:** Big Data es **la forma de manejar datos tan grandes, rápidos y variados** que los sistemas de siempre no pueden con ellos.

### 4.1 Mapa conceptual

- **Definición**: ecosistema o paradigma para **capturar, almacenar y analizar** datos de **gran volumen, velocidad y variedad**, que superan a los sistemas tradicionales. Es la base sobre la que se construyen el análisis y la estrategia (apunte de clase).
- **Las 3 V**:
  - **Volumen**: muchísimos datos.
  - **Velocidad**: llegan muy rápido.
  - **Variedad**: de todo tipo (texto, fotos, sensores, redes).
- 👉 La guía de PowerData avisa: **"Big" no es lo importante**. El volumen es solo una parte. Las empresas quieren saber no solo qué pasa, sino **qué va a pasar**, y lo más cerca posible del **tiempo real**.
- **Por qué importa**: cambia la industria, el negocio y la sociedad, y da **ventaja competitiva**. Hoy puede valer más encontrar al **cliente que más influye** sobre otros que al que más compra.
- **Nace de 3 necesidades nuevas del mercado**:
  1. **Personalización máxima** del cliente.
  2. Pasar **de la transacción a la interacción**.
  3. **Nuevos dispositivos** (celulares, domótica, autos con sensores).
- **Necesita Big Analytics**:
  - Análisis **predictivo** y **clusterización** (agrupar) de clientes.
  - Trabaja con **datos en crudo, al nivel más bajo de detalle**, con modelos más ágiles.
  - Lo manejan el **Data Scientist** y el **Data Analyst** (aparece el perfil de **Data Science**).
  - Viene del **BI tradicional y el Data Warehouse**, que tenían **modelos rígidos, poco ágiles y sin tiempo real**: cargaban los modelos tan lento que cuando terminaban ya no servían.
  - Se apoya en el **Analytic Data Warehouse (ADW)**. 👉 El ADW **no reemplaza** al *data warehouse*: cada uno cubre algo distinto y **conviven** en un **modelo híbrido DWH + ADW**.
- **Metodología MAD**:
  - **Magnética**: atrae todo tipo de datos.
  - **Ágil**: los carga y se adapta rápido.
  - **Detallada**: análisis estadístico fino.
- **Origen de Hadoop**: **Google** no podía indexar la web tan rápido como hacía falta. Aplicó **"divide y vencerás"**: muchas computadoras chicas, cada una procesa un pedazo, pero funcionan como una sola. En **2006** la comunidad de **código abierto** crea Hadoop; después **Yahoo** lo impulsa y lo adoptan empresas como **Facebook**. Permite, por ejemplo, una regresión lineal sobre millones de registros históricos con un **ROI muy rápido**.
- **Hadoop tiene dos partes**:
  - **HDFS** (*Hadoop Distributed File System*): **guarda** los archivos repartidos en muchas máquinas.
  - **MapReduce**: **procesa** en paralelo.
  - Es **código abierto** y usa ***commodity hardware*** (equipos comunes y baratos).
- **4 megatendencias**:
  - **Movilidad**: acceso a los datos desde cualquier lugar y desde dispositivos que no son de la empresa (más difícil de controlar).
  - **Cloud**: no comprás la infraestructura; baja la inversión inicial y podés **prever el costo de crecer**.
  - **Social Media**: gustos y preferencias para captar y fidelizar clientes.
  - **Analytics**: analizar cualquier tipo de dato, sin patrones de búsqueda fijos.
- **Tiempo real**:
  - ***Data Stream***: analiza **datos en movimiento** (mientras llegan).
  - **CEP** (*Complex Event Processing*): **detecta eventos ya definidos** (por ejemplo, operaciones sospechosas con tarjetas).
  - Ejemplos de CEP de la guía: un banco que mira en tiempo real lo que pasa con las **tarjetas de crédito** en cajeros y comercios; **sensores de maquinaria** que avisan antes de que se rompa algo.
- **Cómo implementarlo**:
  1. Primero **conocer y medir el valor** que le da al negocio (ver límites, expectativas y restricciones).
  2. **Las metas eligen la tecnología** (no al revés): para eventos en tiempo real, **CEP**; para análisis predictivo, bases **MPP** (*Massively Parallel Processing*, procesamiento masivamente paralelo) sobre todo el histórico.
  3. Perfiles que conozcan el negocio (Data Scientist, Data Analyst).
  4. Herramientas según el tipo de análisis.
- **Privacidad**: en Google "no todo es gratis": el precio es tu privacidad. Las empresas tienen que equilibrar los datos que analizan con lo que sus clientes **toleran**.
- 👉 **Resumen**: Big Data **genera** innovación y ventaja competitiva, pero **plantea** el desafío de **seguridad y privacidad**.

### 4.2 BI, minería de datos y Big Data

| Aspecto | BI | Minería de datos | Big Data |
|---|---|---|---|
| Qué es | Procesos y herramientas que convierten datos en información para decidir | Descubrir patrones, relaciones y tendencias ocultas | Paradigma para capturar, almacenar y analizar datos masivos |
| Pregunta central | ¿Qué pasó y cómo vamos? | ¿Qué patrones hay en los datos? | ¿Qué va a pasar y qué descubrimos con todos los datos? |
| Tiempo | Pasado y presente | Pasado, para descubrir y predecir | Presente y futuro, en tiempo real |
| Tipo de datos | Estructurados, internos | Estructurados y semiestructurados, ya preparados | Estructurados, semiestructurados y **no estructurados** (redes, sensores, logs) |
| Volumen | Moderado (lo que aguanta un *datawarehouse*) | De moderado a grande | **Masivo**, infraestructura distribuida |
| Técnicas | Consultas, reportes, tableros, OLAP, KPI | Clasificación, agrupamiento, asociación, regresión, anomalías | Big Analytics, MapReduce, Data Stream, CEP |
| Tecnología | *Datawarehouse*, ETL, *reporting* | Algoritmos estadísticos y de aprendizaje automático | Hadoop, ADW, *cloud*, bases MPP |
| Perfil | Gerentes y analistas de negocio | Analistas de datos, estadísticos | Data Scientist, Data Analyst |
| Resultado | Informes y tableros | Modelos y patrones | Conocimiento nuevo y servicios personalizados casi en tiempo real |
| Limitación | Poco ágil, sin tiempo real | Depende de la calidad de los datos | Infraestructura nueva, perfiles caros, privacidad |

**Matriz de la clase** ("Ingeniería de datos"):

| | Big Data | Minería de datos | BI |
|---|---|---|---|
| Fin principal | Almacenar y procesar a escala masiva | **Descubrir patrones** | **Optimizar decisiones** de la empresa |
| Tipo de datos | **Crudos** y variados | **Consolidados** | **Estructurados y depurados** |
| Perfil | **Ingeniero de datos** | **Científico de datos** | **Analista de BI** o consultor |
| Foco temporal | **Presente continuo** | **Futuro predictivo** | **Pasado y presente** descriptivo |

- 👉 **Cadena de la clase**: **Big Data** junta los datos → la **minería** encuentra patrones → **BI** los convierte en decisiones.
- **No compiten**: conviven en un **modelo híbrido**. BI mira hacia atrás; Big Data apunta hacia adelante; la minería se usa tanto sobre un *datawarehouse* como sobre Big Data.
- El TP dice que la minería mira al "pasado" y la clase dice "futuro predictivo". Si te preguntan: la minería **analiza datos pasados para predecir el futuro**.

---

## 5. Repaso final

### 5.1 Cómo se conectan los temas

- **Redes de Petri** → modelan **cómo se comporta** un sistema concurrente (procesos, estados, recursos). Es **diseño**.
- **BI, minería y Big Data** → trabajan con los **datos** que generan esos sistemas, para **decidir**: Big Data junta y procesa → la minería descubre patrones → BI los convierte en indicadores y decisiones.
- **Puntos de contacto**:
  - El *datawarehouse* (BI) es el punto de partida de la minería.
  - OLAP aparece en BI y en minería (que **no** es OLAP).
  - La **granularidad** aparece en el modelo de datos de BI y en el tercer reto de la minería.
  - La **privacidad** aparece en minería y en Big Data.

### 5.2 Errores frecuentes en el examen

- ❌ "Una red viva siempre es cíclica." ✅ Son cosas **distintas**: una red puede ser viva y nunca volver a M0.
- ❌ "Red segura = red que no se traba." ✅ Segura = **1-acotada**. Que no se trabe es **vivacidad**.
- ❌ "C = C⁻ − C⁺." ✅ **C = C⁺ − C⁻**.
- ❌ "Un arco puede unir dos lugares." ✅ Siempre une **lugar con transición** (grafo bipartito).
- ❌ "BI es un análisis que se hace una vez." ✅ Es un **proceso continuo** (interactivo).
- ❌ "El esquema estrella está normalizado." ✅ La estrella está **desnormalizada**; el **copo de nieve** está normalizado.
- ❌ "Más granularidad = menos detalle." ✅ **Más granularidad = más detalle** (líneas de ticket > tickets).
- ❌ "Un Data Mart es más grande que un *datawarehouse*." ✅ Es **más chico** y para un grupo de usuarios.
- ❌ "KDD y minería de datos son lo mismo." ✅ La minería es **un paso** del KDD.
- ❌ "OLAP descubre patrones nuevos." ✅ OLAP **navega**; la minería **descubre**.
- ❌ "Si dos cosas están correlacionadas, una causa la otra." ✅ **Correlación no es causalidad** (Florida).
- ❌ "Sacar las filas con faltantes no tiene costo." ✅ **Sesga** los datos.
- ❌ "La regresión es descriptiva." ✅ Es **predictiva / supervisada** (predice un número).
- ❌ "Las redes neuronales cumplen con el lenguaje de alto nivel del KDD." ✅ Son una **caja negra**: no lo cumplen, aunque sirvan como método.
- ❌ "Big Data reemplaza al *datawarehouse*." ✅ **Conviven** (modelo híbrido DWH + ADW).
- ❌ "SEMMA incluye la comprensión del negocio." ✅ SEMMA **la da por hecha**; CRISP-DM es la más orientada al negocio.

### 5.3 Preguntas integradoras con respuesta modelo

1. **¿Por qué la minería de datos depende del *datawarehouse* de BI?**
   Porque la minería necesita datos **consolidados, limpios e históricos**, separados de los sistemas transaccionales. Eso es justo lo que da el **datawarehouse** cargado con **ETL**. La lectura dice que el análisis es mucho más fácil si la fuente es unificada, accesible y separada del trabajo transaccional. Por eso el *datawarehouse* es "el punto de partida" de la minería.

2. **Compará OLAP, minería de datos y Big Data.**
   **OLAP** navega por datos históricos resumidos en varias dimensiones, **sin generar información nueva**. La **minería** descubre **sola** patrones nuevos y predice. **Big Data** es el **contexto** de datos enormes, rápidos y variados (hasta no estructurados) que necesita infraestructura distribuida (**Hadoop**) y análisis en tiempo real (**CEP**, **Data Stream**).

3. **¿Qué tienen en común la granularidad de un modelo estrella y el tercer reto de la minería?**
   En los dos casos, el **nivel de detalle** decide qué preguntas podés responder. En BI, si analizás tickets no podés analizar productos; en minería, con datos mensuales no podés predecir por semana. **Cada vez que resumís, perdés información**.

### 5.4 Autopreguntas

- ¿Qué es un nodo frontera y cuáles son los tres tipos?
- Dada una red, ¿podés armar C⁻, C⁺ y C sin mirar, con filas = transiciones?
- ¿Cuándo se escribe ω en el árbol y qué propiedad indica?
- ¿Cómo pasás del árbol de alcanzabilidad a la máquina de testigos?
- ¿Por qué M' = M + f(σ)·C no alcanza para asegurar que una secuencia se puede disparar?
- ¿Cómo ves en el grafo de marcados que una red es cíclica?
- ¿Qué diferencia hay entre una red viva, parcialmente viva y no viva?
- ¿Cuáles son los 6 componentes de un proyecto de BI?
- ¿Qué es una dimensión degenerada? Dame dos ejemplos.
- ¿Por qué el fabricante va en una dimensión distinta del artículo?
- ¿Cuáles son los 9 pasos del KDD y cuál es el crítico?
- ¿Qué hace un "picapedrero" y qué hace un "explorador"?
- ¿Qué es la elevación (*lift*) y cómo se calcula?
- ¿Qué es la metodología MAD y qué significa cada letra?
- ¿Qué diferencia hay entre Data Stream y CEP?

---

## Glosario de siglas y abreviaturas

**Redes de Petri**

| Sigla | Desarrollo | Original |
|---|---|---|
| RdP | Red de Petri | — |
| M0 | Marcado inicial | — |
| C⁻ | Matriz de incidencia previa | — |
| C⁺ | Matriz de incidencia posterior | — |
| MT | Máquina de testigos | — |
| GE | Grafo de estados | — |
| ME | Máquina de estados | — |
| GM | Grafo marcado | — |
| RLE | Red de libre elección | — |
| RS | Red simple | — |
| DFD | Diagrama de flujo de datos | — |

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
| MOLAP | OLAP multidimensional | *Multidimensional OLAP* |
| ROLAP | OLAP relacional | *Relational OLAP* |
| HOLAP | OLAP híbrido | *Hybrid OLAP* |
| DOLAP | OLAP de escritorio | *Desktop OLAP* |
| FASMI | Rápido, análisis, compartido, multidimensional, información | *Fast, Analysis, Shared, Multidimensional, Information* |
| ODS | Almacén de datos operacional | *Operational Data Store* |
| CRM | Gestión de la relación con clientes | *Customer Relationship Management* |
| SCM | Gestión de la cadena de suministro | *Supply Chain Management* |
| GIS | Sistemas de información geográfica | *Geographic Information Systems* |
| DWH | Almacén de datos | *Data Warehouse* |
| ERP | Planificación de recursos empresariales | *Enterprise Resources Planning* |
| PK | Clave primaria | *Primary Key* |
| FK | Clave externa | *Foreign Key* |
| SQL | Lenguaje de consulta estructurado | *Structured Query Language* |
| ODBC | Conectividad abierta de bases de datos | *Open Database Connectivity* |
| DAX | Expresiones de análisis de datos | *Data Analysis Expressions* |
| IDC | International Data Corporation, consultora | — |
| TDWI | The Data Warehousing Institute | — |
| EFQM | Fundación Europea para la Gestión de la Calidad | *European Foundation for Quality Management* |

**Minería de datos**

| Sigla | Desarrollo | Original |
|---|---|---|
| DM | Minería de datos | *Data Mining* |
| KDD | Descubrimiento de conocimiento en bases de datos | *Knowledge Discovery in Databases* |
| CRISP-DM | Proceso estándar intersectorial para minería de datos | *Cross-Industry Standard Process for Data Mining* |
| SEMMA | Muestrear, Explorar, Modificar, Modelar, Evaluar | *Sample, Explore, Modify, Model, Assess* |
| ML | Aprendizaje automático | *Machine Learning* |
| IA | Inteligencia artificial | — |
| ANOVA | Análisis de la varianza | *Analysis of Variance* |
| CART | Árboles de clasificación y regresión | *Classification And Regression Trees* |
| CHAID | Detector automático de interacciones por Ji cuadrado | *Chi Squared Automatic Interaction Detector* |
| k-NN | k vecinos más cercanos | *k Nearest Neighbors* |
| IQR | Rango intercuartílico | *Interquartile Range* |
| PII | Información de identificación personal | *Personally Identifiable Information* |
| GDPR | Reglamento General de Protección de Datos, de la Unión Europea | *General Data Protection Regulation* |
| CAD-CAM | Diseño y fabricación asistidos por computadora | *Computer-Aided Design / Manufacturing* |

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
| N° | Número |

---

## De dónde sale este resumen

- **Material de la cátedra** 📁 (carpeta *Análisis y Diseño de Sistemas II - 2026*): presentaciones "Redes_de_petri" y "Formalización Redes de Petri"; capítulos "Introducción al BI", "BI_modelos", "Componentes de BI" y "experiencias BI_detalle" del libro *Business Intelligence: competir con información*; lectura de minería de Beatriz Beltrán Martínez; artículo "KDD-CRISP-SEMMA" (Azevedo y Santos); guía "PowerData - Del bit… al Big Data". El documento "Data Mining: el arte de anticipar" (Palma y otros) no se volcó porque no aparece en los TP.
- **Material del grupo**: TP6 a TP9, guías de BI, apuntes de clase ("Redes Petri - Análisis y Diseño II", "Apuntes 14/9", "Ingeniería de datos") y el mapa conceptual de Big Data.
- **Verificado por computadora**: matrices, árboles, máquinas de testigos, secuencias y propiedades de los tres ejemplos de Redes de Petri.
- **Sacado por alcance**: TP6 de modelado, CoffeeTime, TP de fútbol, comercio minorista y abandono de compra.
- **Depuración (30/10)**: Big Data pasa al final. Se sacaron los ejemplos y casos puntuales (supermercado, paquetería, Wal-Mart, ROI del libro, K-means de empleados, Play Tennis, experiencias de BI) y los datos sueltos de estudios o encuestas (IDC, TDWI, Watson, Gartner 2005, hospitales). Se conservaron los ejemplos resueltos de Redes de Petri.
- **No disponible**: contenido de los videos de los temas 8 y 10.
