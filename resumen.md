# Resumen 2do parcial — Análisis y Diseño de Sistemas II

> Armado a partir de los Trabajos Prácticos (TP) 6 a 9 del grupo (Figún, Morales, Haunau), del material de la cátedra (carpeta compartida *Análisis y Diseño de Sistemas II - 2026*: presentaciones de Redes de Petri, capítulos del libro *Business Intelligence: competir con información*, experiencias de BI, lectura de Minería de Datos, artículo KDD-SEMMA-CRISP-DM y guía *Del bit… al Big Data* de PowerData) y de los apuntes de clase. Docente: María Silvina Scarpin. Tecnicatura en Análisis y Desarrollo de Software, Instituto de Profesorado Sedes Sapientiae.

**Temas del examen**

| Bloque | Qué entra | Fuente principal |
|---|---|---|
| Temas 6 y 7 | Teoría completa y práctica de árbol de alcanzabilidad, propiedades, máquina de testigos y método matricial. Redes de Petri: definición, historia, representación gráfica y matricial, ejecución, árbol de alcanzabilidad y máquina de testigos, estructuras básicas, propiedades, subclases, métodos de análisis, modelos clásicos | TP6; presentaciones de la cátedra "Redes_de_petri" y "Formalización Redes de Petri"; lectura de Jorge Castro Monge; apunte de clase |
| Tema 8 | *Business Intelligence* (BI): definición, beneficios, componentes (fuentes, calidad de datos, ETL, *datawarehouse*, Data Mart, OLAP, herramientas, usuarios), retorno de la inversión, modelo de negocio, indicadores clave, modelo de datos, experiencias. Solo teoría | TP7; capítulos 1 a 4 del libro *Business Intelligence: competir con información* ("Introducción al BI", "BI_modelos", "Componentes de BI"); "experiencias BI_detalle" |
| Tema 9 | Minería de datos y proceso KDD (descubrimiento de conocimiento en bases de datos): fases, limpieza, tareas, técnicas, evaluación, metodologías KDD, CRISP-DM y SEMMA. Solo teoría | TP8; lectura "Minería de Datos" (Beatriz Beltrán Martínez, Benemérita Universidad Autónoma de Puebla); artículo "KDD, SEMMA and CRISP-DM: a parallel overview" (Azevedo y Santos); apuntes del 14/9 |
| Tema 10 (entra en el final, no en el parcial) | Big Data: las 3 V, nuevas necesidades, Big Analytics, metodología MAD, Hadoop, megatendencias, tiempo real, implementación, comparación con BI y minería. Solo teoría | TP9; guía *Del bit… al Big Data* (PowerData); apunte de clase "Ingeniería de datos" |

**Aclaraciones de la docente (vigentes)**

- **De todos los temas entra solo la teoría.**
- **Big Data (tema 10) entra en el final**, no en el 2do parcial. Queda en el resumen como material para el final.
- **Excepción, Redes de Petri**: además de la teoría entran el **árbol de alcanzabilidad**, las **características y propiedades**, y **resolver una red con máquina de testigos y método matricial** (ver 1.12).
- **No entra**: la práctica de los TP (caso CoffeeTime, TP integrador de fútbol, aplicación en comercio minorista, caso de abandono de compra, modelado de las 7 tareas y demás ejercicios de modelado del TP6). Se sacaron de los tres entregables.

**Cómo leer las marcas**

- 📁 = sale de tus archivos (material de la cátedra, TP del grupo o apuntes de clase).
- ⚠️ = no verificado: no hay fuente primaria en la carpeta, sale solo de un TP o apunte del grupo que no se pudo cotejar con el material de la cátedra, o es una propuesta armada para este resumen.
- ✅ / ❌ = correcto / incorrecto en las listas de errores frecuentes.

**Siglas y abreviaturas**

Toda sigla se desarrolla la primera vez que aparece en cada sección. TP = Trabajo Práctico. RdP = Red de Petri. El glosario completo está al final.

**Avisos antes de estudiar**

1. **Alcance.** Para el **2do parcial**: solo teoría de los temas 6 a 9 (Redes de Petri, BI y Minería de datos), más la práctica de Redes de Petri indicada arriba. **Big Data (tema 10) entra en el final.** El resumen ya está recortado a eso: no incluye ejemplos puntuales, casos de empresas ni datos sueltos de un autor o de un estudio.
2. **Numeración.** La cátedra numera así: Temas 6 y 7 = Redes de Petri, Tema 8 = BI, Tema 9 = Minería de datos, Tema 10 = Big Data. El resumen usa esa numeración; Big Data queda como material para el final.
3. **Redes de Petri, apunte de clase con errores.** El apunte dice "una red viva es cíclica": no es correcto, vivacidad y ciclicidad son propiedades independientes y ninguna presentación de la cátedra lo dice. Las definiciones de conflicto estructural y efectivo se toman de la presentación "Redes_de_petri" (ver 1.8 y "Errores frecuentes").
4. **Mapeo KDD, SEMMA y CRISP-DM.** El cuadro del TP8 del grupo difiere un poco del artículo de la cátedra (Azevedo y Santos). Se corrigió según el artículo (ver 3.13).
5. **Videos.** Los videos de los temas 8 y 10 no se pudieron revisar (solo se procesó texto). La guía de PowerData sí está cotejada.
6. **Siglas que el libro escribe distinto.** La lectura de BI dice "Standard Query Language" para SQL y "Object Data Base Connector" para ODBC; los desarrollos habituales son **Structured Query Language** y **Open Database Connectivity**. Usá los habituales y, si te lo preguntan, sabé que el libro los escribe distinto.

---

## 0. Datos para memorizar

| Dato | Valor |
|---|---|
| Creador de las Redes de Petri | Carl Adam Petri (alemán), tesis doctoral de 1962 *Kommunikation mit Automaten* |
| Holt y Commoner | 1970, "Events and Conditions": aplican las RdP a sistemas concurrentes |
| Estructura de una Red de Petri | C = (P, T, I, O): lugares, transiciones, función de entrada, función de salida |
| Red marcada | M = (C, μ) |
| Matriz de incidencia | C = C⁺ − C⁻ (posterior menos previa); filas = transiciones, columnas = lugares |
| Ecuación de disparo | M'(p) = M(p) − Pre(p, t) + Post(t, p) |
| Red segura | 1-acotada (binaria): ningún lugar tiene más de una marca |
| Ecuación de estado | M' = M + f(σ)·C, con f(σ) el vector de disparo (cuántas veces se dispara cada transición) |
| Transición habilitada (método matricial) | M ≥ ej·C⁻ |
| ω en el árbol de alcanzabilidad | La red no es acotada |
| Subclases de RdP | 4: grafo de estados o máquina de estados, grafo marcado, red de libre elección, red simple |
| Primero en usar "Business Intelligence" | Howard Dresner (consultor de Gartner) |
| BI según Gartner | Proceso **interactivo** para **explorar** y **analizar** información **estructurada** de un **área**, normalmente en un *datawarehouse* |
| ROI (fórmula simple) | Valor para el negocio / costo del proyecto |
| ROI (fórmula completa) | NPV / inversión inicial × 100 |
| Proceso ETL | Consume entre el 60 % y el 80 % del tiempo de un proyecto de BI; 5 subprocesos |
| Características de un *datawarehouse* (Inmon) | Orientado a un área, integrado, indexado en el tiempo, no volátil |
| Concepto FASMI de OLAP | *Fast, Analysis, Shared, Multidimensional, Information* |
| Modelo relacional | E. F. Codd, 1970 |
| Las dimensiones responden | ¿Qué? ¿Quién? ¿Por qué? ¿Dónde? ¿Cuándo? |
| Término KDD | Empieza a usarse en 1989 |
| Pasos del proceso KDD | 9 |
| Fases (estados) del KDD según la lectura | 6 |
| CRISP-DM | 6 fases; consorcio DaimlerChrysler, SPSS y NCR |
| SEMMA | 5 fases: *Sample, Explore, Modify, Model, Assess*; SAS Institute |
| KDD según Fayyad | 5 etapas núcleo: selección, preprocesamiento, transformación, minería, interpretación/evaluación |
| Big Data | 3 V: volumen, velocidad, variedad |
| Metodología MAD | Magnética, Ágil, Detallada |
| Megatendencias del Big Data | 4: Movilidad, Cloud, Social Media, Analytics |
| Hadoop | HDFS (archivos distribuidos) + MapReduce (procesamiento paralelo); código abierto desde 2006, nace de Google |

---

## 1. Redes de Petri (Temas 6 y 7) 📁

### 1.1 Qué son y para qué sirven

- Teoría matemática de **Carl Adam Petri**: herramienta **gráfica y matemática** de modelado para describir formalmente sistemas con **concurrencia, sincronización, exclusión mutua y conflictos**, típicos de los sistemas distribuidos.
- **Antecedente: las máquinas de estado** (estado + transición, con entradas y salidas *a/b*). Su gran límite: modelar **acciones simultáneas**. Unir varias máquinas de estado hace explotar la cantidad de estados y vuelve ilegible el diagrama.
- Las Redes de Petri (RdP) representan la concurrencia de forma natural porque tienen **paralelismo inherente**.
- Al analizar la red se obtiene información sobre la **estructura** y el **comportamiento dinámico** del sistema, para evaluarlo y sugerir mejoras.
- **Definición de la presentación de la cátedra**: representaciones gráficas que modelan sistemas con flujo de información, mostrando su estructura y comportamiento dinámico. Pueden verse como **generadores de lenguaje o autómatas formales** asociados a la teoría de grafos; sirven para diseñar, especificar y simular sistemas de *hardware* o *software*.
- **Historia**: surgen en **1962** con la tesis doctoral de Carl Adam Petri, *Kommunikation mit Automaten* ("Comunicación con autómatas"), en Alemania: una teoría de comunicación entre componentes **asíncronos**. El proyecto "Systemics" aportó la notación. En **1970**, **Holt y Commoner** ("Events and Conditions") muestran cómo aplicarlas a sistemas con componentes concurrentes.
- **Tres ventajas de modelar con RdP** (presentación "Formalización"): el sistema es más fácil de entender por la naturaleza gráfica y precisa; el comportamiento se puede analizar con la teoría (árboles de marcados, relación entre estructura y comportamiento); y como se sintetizan *bottom-up* o *top-down*, se pueden diseñar sistemas de comportamiento conocido o verificable.
- **Extensiones**: modificaciones estructurales (más potencia o comodidad de modelado) y **redes de Petri temporizadas** (análisis cuantitativo de prestaciones).
- **En programación concurrente**: transiciones = procesos; lugares = condiciones para que un proceso se ejecute; marcas = la condición se verifica.
- Apunte de clase: se usan para modelar un sistema, ver cómo funciona, identificar sus procesos y los estados por los que pasa; se usan como **autómatas**. Cualquier proceso puede reflejarse con una RdP.

### 1.2 Elementos y representación gráfica

| Elemento | Dibujo | Qué representa al modelar |
|---|---|---|
| Lugar o plaza | Círculo | Condición o estado |
| Transición | Barra | Evento o suceso |
| Arco dirigido | Flecha con peso (si no tiene número, pesa 1) | Une lugar → transición (lugar de entrada) o transición → lugar (lugar de salida). Nunca lugar con lugar ni transición con transición |
| Marca o *token* | Punto negro dentro del lugar | Que la condición se cumple. Un lugar con marcas está **activo** |

- La red es un **multígrafo dirigido bipartito**: admite arcos múltiples, los arcos tienen dirección y los nodos se dividen en dos conjuntos (lugares y transiciones) que solo se conectan entre sí.
- Una transición está **sensibilizada** (habilitada) cuando todos sus lugares de origen están marcados; está **validada** cuando además ocurre el evento asociado.
- Representación **gráfica** y **matricial** son equivalentes: dada una se obtiene la otra, y es única.

### 1.3 Definición formal

- **Estructura**: C = (P, T, I, O), donde P es un conjunto finito y no vacío de lugares, T un conjunto finito y no vacío de transiciones, I la **función de entrada** (lugares de entrada de cada transición) y O la **función de salida** (lugares de salida).
- **Marcado** μ: función de P en los enteros no negativos; también se escribe como vector μ = (μ1, …, μn) con n = cantidad de lugares. El marcado es el **estado** de la red.
- **Red marcada**: M = (C, μ). Hay infinitos marcados posibles (el conjunto es infinito pero numerable).
- **Tipos de red**:
  - **Ordinaria**: todos los arcos pesan 1.
  - **Generalizada**: los arcos pueden tener cualquier peso entero mayor o igual que cero.
  - **Pura** (no reflexiva): ningún lugar es a la vez entrada y salida de la misma transición.
- Notación del apunte: I(t) lugares de entrada a t; O(t) lugares de salida de t; I'(p) transiciones que entran al lugar p; O'(p) transiciones que salen de p; V(p, t) y V(t, p) valores (pesos) de los arcos.

### 1.4 Ejecución (reglas de disparo)

1. **Habilitación**: t está habilitada si cada lugar de entrada tiene al menos tantas marcas como el peso del arco hacia t: M(p) ≥ I(p, t). Una **transición fuente** (sin lugares de entrada) está siempre habilitada.
2. **Disparo**: se quitan de cada lugar de entrada tantas marcas como el peso del arco, y se agregan a cada lugar de salida tantas como el peso del arco de salida. Cuál de las habilitadas se dispara primero es **arbitrario**.
3. **Nuevo marcado**: **M'(p) = M(p) − Pre(p, t) + Post(t, p)**. Una **transición sumidero** (sin lugares de salida) elimina marcas de la red.

- Las marcas son **indivisibles**: una marca la quita una sola transición. Por eso disparar una transición puede **deshabilitar** a otra que compartía el lugar de entrada. Fuera de eso, los disparos son **asíncronos**.
- **Grado de habilitación**: cuántas veces puede dispararse una transición de forma concurrente.
- **Inmediatamente alcanzable**: se llega disparando una sola transición. **Alcanzable**: existe una secuencia de disparos σ que lleva de Mi a Mk. **Conjunto de alcanzabilidad** R(M): todos los marcados alcanzables desde M.

### 1.5 Árbol de alcanzabilidad

- Representa **todos los marcados alcanzables** desde M0. Cada nodo es un marcado; cada arco lleva el nombre de la transición disparada.
- Se parte de M0, se generan los marcados que se obtienen disparando cada transición habilitada, y se repite. Para que el árbol sea **finito** se deja de expandir en los **nodos frontera**:
  - a) **Marcado muerto**: no hay ninguna transición habilitada.
  - b) **Nodo duplicado**: el marcado ya apareció en el árbol.
  - c) Marcado que solo difiere de otro por tener **más marcas en algún lugar** y habilita las mismas transiciones: se escribe **w** (infinito) en ese lugar. Indica que la red **no es acotada**.
- **Máquina de testigos** (MT): versión más compacta del árbol. Cada estado se escribe con los **nombres de los lugares que tienen marcas** (un nombre repetido tantas veces como marcas tenga); los estados van en **óvalos** unidos por arcos con el nombre de la transición. Conviene cuando hay **muchos lugares y pocas marcas**, porque no hay que enumerar todos los lugares.

### 1.6 Representación matricial

- **C⁻ (matriz de incidencia previa)**: C⁻[j, i] = I(pi, tj), las precondiciones (función de entrada).
- **C⁺ (matriz de incidencia posterior)**: C⁺[j, i] = O(pi, tj), las postcondiciones (función de salida).
- **C = C⁺ − C⁻ (matriz de incidencia)**. Según la lectura: **filas = transiciones, columnas = lugares**.
- Forma matricial (presentación "Formalización"): una transición tj se representa con el vector **ej** (1 en la posición j, 0 en el resto). tj está habilitada si **M ≥ ej · C⁻**, y al dispararla **M' = M + ej · C**.
- Para una **secuencia** σ = tj1 tj2 … tjk: **M' = M + f(σ) · C**, donde **f(σ) = ej1 + ej2 + … + ejk** es el **vector de disparo** (cuántas veces se dispara cada transición). Ejemplo de la cátedra: σ = t1, t2, t3 → f(σ) = (1 1 1 0 0) → M' = (0 0 0 1 1).

**Ejemplo resuelto (el de la lectura)** — P = {p1…p5}, T = {t1…t5}, M0 = (1, 0, 0, 0, 0). I(t1) = {p1}, O(t1) = {p2, p3}; I(t2) = {p2}, O(t2) = {p5}; I(t3) = {p3}, O(t3) = {p4}; I(t4) = {p5}, O(t4) = {p2}; I(t5) = {p4, p5}, O(t5) = {p1}.

| | C⁻ (p1 p2 p3 p4 p5) | C⁺ (p1 p2 p3 p4 p5) | C (p1 p2 p3 p4 p5) |
|---|---|---|---|
| t1 | 1 0 0 0 0 | 0 1 1 0 0 | −1 1 1 0 0 |
| t2 | 0 1 0 0 0 | 0 0 0 0 1 | 0 −1 0 0 1 |
| t3 | 0 0 1 0 0 | 0 0 0 1 0 | 0 0 −1 1 0 |
| t4 | 0 0 0 0 1 | 0 1 0 0 0 | 0 1 0 0 −1 |
| t5 | 0 0 0 1 1 | 1 0 0 0 0 | 1 0 0 −1 −1 |

Marcados alcanzables (verificados): (1,0,0,0,0) → t1 → (0,1,1,0,0) → t2 → (0,0,1,0,1) o t3 → (0,1,0,1,0); de ahí se llega a (0,0,0,1,1), donde t5 devuelve a M0 y t4 vuelve a (0,1,0,1,0). Son **5 marcados**, ninguno muerto, ningún lugar pasa de 1 marca: la red es **viva, segura y cíclica**. t2 y t3 son **concurrentes**; en (0,0,0,1,1) t4 y t5 están en **conflicto** (comparten p5).

### 1.7 Estructuras básicas

| Estructura | Qué modela |
|---|---|
| **Secuencial** | t2 solo se dispara después de t1 |
| **Selección** | Se elige qué proceso ejecutar (un lugar con dos transiciones de salida) |
| **Atribución** | Un proceso se ejecuta de forma independiente desde dos procesos distintos (dos transiciones que llegan al mismo lugar) |
| **Distribución** | Lanza procesos paralelos o concurrentes (una transición con varios lugares de salida) |
| **Conjunción** | Sincroniza procesos paralelos (una transición con varios lugares de entrada) |
| **Sincronización** | t1 se habilita solo si **todos** sus lugares de entrada tienen marca |
| **Concurrencia** | t2 y t3 pueden dispararse a la vez e independientemente |
| **Conflicto** | t1 y t2 están habilitadas, pero disparar una deshabilita a la otra |

### 1.8 Propiedades

**Estructurales** (dependen solo de la topología, no del marcado inicial):

- **Pura**: ningún lugar es entrada y salida de la misma transición.
- **Estructuralmente acotada**: acotada para **cualquier** marcado inicial finito.
- **Estructuralmente viva**: existe **algún** marcado inicial para el que es viva.
- **Completamente controlable**: cualquier marcado es alcanzable desde cualquier otro.
- **Estructuralmente conservativa**: el número (ponderado) de marcas se mantiene para cualquier marcado inicial.

**De comportamiento** (dependen del marcado inicial M0):

| Propiedad | Definición | Qué garantiza |
|---|---|---|
| **Alcanzabilidad** | Mn es alcanzable desde M0 si existe σ que lleva de M0 a Mn | Es la base para estudiar las demás |
| **Vivacidad** | Una transición es viva si, desde cualquier marcado alcanzable, se puede volver a disparar alguna vez. La red es **viva** si todas sus transiciones lo son | Ausencia de **bloqueo total (*deadlock*)** |
| **Parcialmente viva** | Desde cualquier marcado alcanzable hay al menos una transición disparable, pero hay alguna transición no viva | La red evoluciona, aunque algo se bloquee |
| **No viva** | Se llega a un marcado muerto | Hay bloqueo total |
| **Acotamiento** | Un lugar es **k-acotado** si nunca tiene más de k marcas; la red es k-acotada si todos sus lugares lo son | Número **finito** de estados; si la red genera más marcas que las permitidas, el modelo está mal |
| **Seguridad** | Red **1-acotada** = **segura** = **binaria**: cada lugar está marcado o no | No se excede la capacidad (por ejemplo, de un registro de memoria) |
| **Ciclicidad o reversibilidad** | Desde cualquier marcado alcanzable se puede volver a M0 | No hay subconjuntos finales de estados de los que no se vuelve |
| **Conservación** | La cantidad total de marcas se mantiene constante | Recursos que no se crean ni se destruyen |
| **Conflicto** | Dos transiciones habilitadas comparten un lugar de entrada y disparar una deshabilita la otra | Hay una decisión no determinista |
| **Exclusión mutua** | Dos procesos no pueden usar el recurso a la vez | Acceso ordenado a un recurso compartido |

- Lectura (forma resumida): la **supervivencia** es la ausencia de estancamientos; la **seguridad** se relaciona con la capacidad limitada de memoria.
- Ejemplo de la lectura: una red que no se bloquea con t1, t2, t1, t2 pero queda **bloqueada** con t1, t3, t4 → **no viva**. Otra red es **pseudoviva** y **no reversible** porque nunca vuelve a M0.
- **Conflictividad** (presentación "Redes_de_petri"): hay **conflicto estructural** cuando **un lugar tiene más de una transición de salida**. Dos transiciones ti y tj están en **conflicto efectivo** para M0 si existe un marcado alcanzable que **habilita a las dos a la vez** y, al disparar una, el marcado que queda **no habilita a la otra**.
- **Exclusión mutua** (misma presentación): un conjunto de transiciones es mutuamente exclusivo si disparar cualquiera **deshabilita a todas las demás**. Dos **lugares** están en exclusión mutua para M0 si **nunca pueden estar marcados a la vez** en los marcados alcanzables.
- **Limitación**: garantiza la **finitud** de los marcados alcanzables; una red k-limitada se puede **implementar con recursos finitos**.
- **Conservación**: el número de recursos no varía durante la ejecución. La forma más simple es que el total de testigos sea constante; como es muy exigente, se suele hablar de conservación **respecto de un vector peso**.
- Las propiedades sirven para **detectar fenómenos de interés o errores de funcionamiento** en el sistema modelado. La presentación las agrupa en seis: **vivacidad, ciclicidad, limitación, conservación, conflictividad y exclusión mutua**.

### 1.9 Modelos clásicos de concurrencia

- **Exclusión mutua (semáforo)**: un lugar "recurso libre" con una marca. El primer proceso que lo toma quita la marca y los demás esperan. Sirve para cualquier cantidad de procesos y **no tiene prioridades**.
- **Productor y consumidor**: un lugar "depósito con producto" (*buffer*) comunica a los dos procesos. Sin límite, el depósito puede crecer sin fin si el consumidor se detiene. Para un **buffer de capacidad finita** se agregan dos lugares: "buffers llenos" y "buffers vacíos"; **siempre suman la capacidad total** (por ejemplo, 3).
- **Lectores y escritores**: n lectores conocidos; las lecturas pueden ser concurrentes y la escritura es excluyente. Se usa un semáforo con **m marcas** y arcos de peso **m**: leer toma 1 marca, escribir toma las m.
- **Cinco filósofos**: cada uno tiene un plato y un tenedor a la izquierda; para comer necesita los dos tenedores de al lado. Si todos toman primero el mismo tenedor, nadie come: **estancamiento**. Solución para que la red sea viva: que la transición "comer" tome **los dos tenedores a la vez** (es una conjunción), o limitar con un lugar "sillas" con 4 marcas a cuántos intentan comer al mismo tiempo. ⚠️ Las soluciones son las habituales; la del grupo está en imagen.

### 1.10 Ventajas, desventajas, aplicaciones, subclases y métodos de análisis

| Ventajas | Desventajas |
|---|---|
| Fáciles de interpretar | No permiten modelar **prioridades** |
| Tratan procesos independientes | El análisis se complica con sistemas complejos |
| Modelan con más exactitud que un diagrama de estados | A mayor modelo, mayor consumo de recursos |
| Modelan recursos compartidos (exclusión mutua, por ejemplo una impresora) | |
| Se construyen de arriba hacia abajo (*top-down*) o de abajo hacia arriba (*bottom-up*) | Hay muchas **subclases** del modelo general para problemas específicos |
| Modelan procesos concurrentes | |

**Aplicaciones** (presentación de la cátedra): sistemas en **tiempo real**, sistemas operativos y compiladores, *hardware* y *software*, ambientes industriales de producción (redes de libre elección), diagramas de flujo de datos (DFD), **protocolos de comunicación** y bases de datos.

**Subclases**: clases restringidas, más fáciles de analizar, que siguen modelando muchos sistemas.

| Subclase | Regla | Qué puede y qué no puede modelar |
|---|---|---|
| **Grafo de estados** o **máquina de estados** (GE o ME) | Cada **transición** tiene exactamente **una entrada y una salida** | Conflictos y alternativas; **no** paralelismo, concurrencia ni sincronización. Estrictamente conservativa |
| **Grafo marcado** o de sincronización (GM) | Cada **lugar** tiene exactamente **una entrada y una salida** | Paralelismo, concurrencia y sincronización; **no** conflictos ni decisiones |
| **Red de libre elección** (RLE) | Si un lugar es entrada de varias transiciones, es su **única** entrada | Concurrencia y conflicto, de forma restringida: las transiciones en conflicto están habilitadas todas o ninguna |
| **Red simple** (RS) | Cada transición tiene como máximo **un lugar de entrada compartido** con otra | — |

**Métodos de análisis**:

- **Árbol de alcanzabilidad**: da información detallada del comportamiento; sirve para validar el modelo, verificar un diseño, elegir entre propuestas o predecir. Desventaja: puede volverse **grande e inmanejable**.
- **Ecuaciones matriciales o de estado**: prometedoras pero con problemas: la matriz C **no refleja toda la estructura de la red**; el vector de disparo **no informa el orden** de los disparos; y que la ecuación M' = M + f(σ)·C tenga solución es condición **necesaria pero no suficiente** para que el marcado sea alcanzable.

**Modelos de redes** (al final de la presentación "Redes_de_petri"; son de investigación operativa): conceptos de arista, nodo, capacidad, fuente y sumidero; **ruta más corta** (trayectoria de mínima distancia entre origen y destino), **árbol de expansión mínima** (conectar todos los nodos al menor costo), **flujo máximo** (maximizar el flujo entre origen y destino respetando capacidades) y **flujo de costo mínimo** (abastecer la demanda al menor costo).

### 1.11 Verificación y ambientes de simulación

- Ejecutar la red permite **simular** el comportamiento: se logra una **verificación** del modelo. Una **validación** exige un lenguaje más formal (las técnicas matemáticas de análisis se acercan a una "prueba").
- Cuando el modelo crece, ejecutar a mano no sirve: hacen falta herramientas que lo ejecuten solas (por ejemplo **HPetriSim**, el simulador de los ejercicios).
- **Ambientes gráficos**: visión global rápida, pero definir la red es tedioso y en redes grandes el dibujo se vuelve confuso. **Ambientes estructurales** (intérprete): se pierde lo visual, pero la red escrita como pseudocódigo se acerca al código (lenguajes como ADA o Modula).

### 1.12 Práctica que entra en el parcial: resolver una red paso a paso 📁

La docente aclaró que de Redes de Petri entran **árbol de alcanzabilidad**, **características y propiedades**, y **resolver una red con máquina de testigos y método matricial**. Los tres ejemplos de esta sección están resueltos y verificados por computadora.

**Receta para el examen**

1. **Leer la red**: lugares, transiciones, arcos (con su peso) y marcado inicial M0. Escribir I(t) y O(t) de cada transición.
2. **Matrices**: C⁻ (entradas), C⁺ (salidas) y **C = C⁺ − C⁻**, con **filas = transiciones** y **columnas = lugares**.
3. **Árbol de alcanzabilidad**: desde M0, por cada transición habilitada calcular el marcado nuevo y numerarlo (M1, M2…). Cortar en los **nodos frontera**: muerto, duplicado o con **ω** (infinito; el apunte lo escribe w). Con ω vale ω + 1 = ω y ω − 1 = ω.
4. **Máquina de testigos**: juntar los duplicados y dibujar el **grafo de marcados**; cada estado (óvalo) lleva los nombres de los lugares marcados, repetidos tantas veces como marcas tengan.
5. **Método matricial**: comprobar una secuencia σ con **M' = M + f(σ)·C**. La ecuación no dice el orden: hay que verificar que cada transición esté habilitada en su momento (**M ≥ ej·C⁻**).
6. **Propiedades**: leerlas del árbol y del grafo con la tabla de abajo.

| Propiedad | Cómo se lee en el árbol o en la máquina de testigos |
|---|---|
| **Viva** | No hay marcados muertos y, desde cualquier estado del grafo, se puede volver a disparar cada transición |
| **Parcialmente viva** | No hay marcados muertos, pero alguna transición deja de poder dispararse |
| **No viva** | Aparece un marcado muerto (bloqueo total) |
| **Acotada (k-acotada)** | No aparece ω; k es el máximo de marcas que llega a tener un lugar |
| **Segura** | k = 1: ningún lugar pasa de una marca |
| **No acotada** | Aparece ω en algún lugar |
| **Cíclica (reversible)** | Desde todos los estados del grafo se puede volver a M0 |
| **Conservativa** | La suma de marcas es la misma en todos los marcados (o la suma ponderada con un vector peso) |
| **Conflicto** | Estructural: un lugar con dos o más transiciones de salida. Efectivo: en algún marcado las dos están habilitadas y disparar una deshabilita la otra |
| **Concurrencia** | Dos transiciones habilitadas a la vez que no comparten lugares de entrada |
| **Exclusión mutua de lugares** | Dos lugares que nunca están marcados a la vez en ningún marcado alcanzable |
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

Método matricial: σ = t1 t3 t2 t5 → f(σ) = (1 1 1 0 1). f(σ)·C = suma de las filas t1, t2, t3 y t5 de C = (0 0 0 0 0), entonces **M' = M0**: la secuencia vuelve al inicio. Habilitación de t5 en M4: e5·C⁻ = (0 0 0 1 1) ≤ (0 0 0 1 1).

Propiedades: **viva** (sin marcados muertos y el grafo vuelve siempre a todos los estados), **segura** (1-acotada), **cíclica**, **pura**. **No es estrictamente conservativa** (M0 tiene 1 marca y el resto 2), pero sí respecto del vector peso (2 1 1 1 1). **Conflicto** estructural en p5 (t4 y t5) y efectivo en M4. **Concurrencia**: t2 y t3 en M1; t3 y t4 en M2. **Exclusión mutua de lugares**: p2 y p5, p3 y p4, y p1 con todos los demás.

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

Propiedades: **no acotada** (p3 llega a ω; p1 y p2 son 1-acotados), **viva**, **cíclica** (desde (1, 0, k) se dispara t3 k veces y se vuelve a M0; el árbol con ω no alcanza para afirmarlo, hay que razonarlo), **no conservativa**, **pura**, **sin conflicto** (ningún lugar tiene dos transiciones de salida). **Exclusión mutua de lugares**: p1 y p2 (siempre p1 + p2 = 1).

**Ejemplo 3 — exclusión mutua de dos procesos (semáforo)**

Lugares: a1 y a2 (proceso esperando), b1 y b2 (proceso usando el recurso), s (recurso libre). M0 = (a1, b1, a2, b2, s) = (1, 0, 1, 0, 1). t1: a1, s → b1; t2: b1 → a1, s; t3: a2, s → b2; t4: b2 → a2, s.

| | C⁻ (a1 b1 a2 b2 s) | C⁺ (a1 b1 a2 b2 s) | C (a1 b1 a2 b2 s) |
|---|---|---|---|
| t1 | 1 0 0 0 1 | 0 1 0 0 0 | −1 1 0 0 −1 |
| t2 | 0 1 0 0 0 | 1 0 0 0 1 | 1 −1 0 0 1 |
| t3 | 0 0 1 0 1 | 0 0 0 1 0 | 0 0 −1 1 −1 |
| t4 | 0 0 0 1 0 | 0 0 1 0 1 | 0 0 1 −1 1 |

Árbol: M0 (1,0,1,0,1) → t1 → M1 (0,1,1,0,0) → t2 → duplicado de M0; M0 → t3 → M2 (1,0,0,1,0) → t4 → duplicado de M0. Máquina de testigos: a1 a2 s —t1→ b1 a2 —t2→ a1 a2 s; a1 a2 s —t3→ a1 b2 —t4→ a1 a2 s.

Método matricial: σ = t1 t2 t3 → f(σ) = (1 1 1 0) → M' = M0 + (0 0 −1 1 −1) = **(1 0 0 1 0)** = M2.

Propiedades: **viva**, **segura**, **cíclica**, **pura**; conservativa respecto del vector peso (1 2 1 2 1). **Conflicto** estructural y efectivo en s: en M0, t1 y t3 están habilitadas y disparar una deshabilita la otra. **Exclusión mutua**: b1 y b2 nunca están marcados a la vez.

**Errores típicos al resolver**

- Seguir expandiendo un nodo **duplicado**: se corta ahí.
- Poner ω sin comparar con un **antecesor** del mismo camino, o "restarle" marcas a ω.
- Armar la matriz con **filas = lugares**: según la lectura, filas = transiciones.
- Creer que si M' = M + f(σ)·C tiene solución, la secuencia se puede disparar: es condición **necesaria pero no suficiente**.
- En la máquina de testigos, olvidar repetir el nombre de un lugar que tiene **dos marcas**.

---

## 2. Business Intelligence (Tema 8) 📁

### 2.1 Definición

- **Business Intelligence** (BI), "inteligencia de negocio": su objetivo básico es apoyar de forma **sostenible y continuada** a las organizaciones para mejorar su **competitividad**, facilitando la información para **tomar decisiones**.
- El término lo popularizó **Howard Dresner** (consultor de Gartner) como término paraguas para conceptos y métodos que mejoran la toma de decisiones usando información sobre lo que pasó (**hechos**).
- Idea central: convertir **datos → información → conocimiento**.
- **Definición de Gartner** (la que se toma como la más ajustada): BI es un **proceso interactivo** para **explorar** y **analizar información estructurada** sobre un **área** (normalmente almacenada en un ***datawarehouse***), para descubrir **tendencias o patrones**, derivar ideas y extraer conclusiones. Incluye **comunicar** los descubrimientos y **efectuar los cambios**. Las áreas incluyen clientes, proveedores, productos, servicios y competidores.

| Parte de la definición | Qué significa |
|---|---|
| Proceso interactivo | Análisis **continuado en el tiempo**, no puntual: permite ver tendencias, cambios y variabilidad |
| Explorar | Primer acceso a la información para entender qué pasa y descubrir relaciones desconocidas |
| Analizar | Descubrir relaciones entre variables, tendencias y patrones (si un cliente actúa así, ¿otro parecido actuará igual?) |
| Información estructurada y *datawarehouse* | Tablas relacionadas, con registros y atributos, en un **almacén de datos** |
| Área de análisis | Todo proyecto de BI tiene un objeto concreto (clientes, productos) y un objetivo (bajar costos, subir ventas) |
| Comunicar y efectuar cambios | Lo descubierto tiene que llegar a quien hace los cambios |

- **Definición del The Data Warehousing Institute (TDWI)**: término paraguas que abarca procesos, herramientas y tecnologías para convertir datos en información, información en conocimiento y planes para conducir los negocios. Incluye el ***back end*** (la "trastienda": *datawarehousing*) y el ***front end*** (el "mostrador": consultas, informes, análisis y visualización).

### 2.2 De los datos a las decisiones

- Los **datos** de las transacciones (qué se vendió, cuándo, quién, cómo se pagó) se convierten en **información operativa** (ventas del día, ticket medio, ventas por artículo), y esa información sirve para **decisiones**: **operativas** (reponer, asignar turnos) o **estratégicas** (qué hacer cuando bajan las ventas: ¿bajó la afluencia o lo que gasta cada cliente?).
- Con el tiempo aparecen **tendencias** y **relaciones entre productos**, que permiten promociones y mejor ubicación.

### 2.3 Quién lo necesita

- Compras (qué se vende y tendencias), ventas (ubicación según rotación), negociación con entidades financieras (flujos de efectivo y tarjetas), marketing (efectividad de promociones) y personal (turnos según afluencia). En síntesis: **todo el que toma decisiones**; las decisiones pueden ser **operativas o estratégicas**.

### 2.4 Beneficios

| Tipo | Ejemplos |
|---|---|
| **Tangibles** (generación de ingresos) | Segmentación de clientes, reducir el abandono, análisis de la cesta de la compra, medir campañas y ajustarlas, identificar clientes rentables |
| **Tangibles** (reducción de costos) | Negociar con proveedores, inventarios *just-in-time*, detectar fraude, reducir créditos incobrables, "una sola versión de la verdad" |
| **Intangibles** | Mejor atención y satisfacción del cliente, información más actualizada y precisa, mayor integración, ventaja competitiva |
| **Estratégicos** | Ayudan a formular la estrategia: a qué clientes, mercados o productos dirigirse; decisiones más rápidas, informadas y basadas en hechos |

### 2.5 Componentes básicos

Componentes de todo proyecto de BI:

1. **Problemática empresarial** a responder.
2. **Equipo** (o persona) que hace el análisis.
3. **Información interna** de los sistemas de la organización.
4. **Información externa** a la organización (mercado, proveedores, tarifas).
5. Una **base de datos**: el *datawarehouse*.
6. Una **aplicación de BI** para trabajar, analizar y visualizar.

**Nota técnica 1 — Sistemas de información**: las organizaciones necesitan información para **soportar transacciones**, para **tomar decisiones y controlar** y para **nuevos negocios** (vender información). Los sistemas sirven para **controlar, coordinar y tomar decisiones** en la **planificación, la gestión y las operaciones**. Preguntas **estructuradas** (respuesta sí/no o un valor: ¿entregamos a tiempo?) frente a **no estructuradas** (¿lanzamos el producto Y en el mercado Z?). Un **ERP** (*Enterprise Resources Planning*, planificación de recursos empresariales) integra módulos con el concepto de **dato único**; si las aplicaciones no están integradas, se pasan datos con **interfases**.

### 2.6 Retorno de la inversión (ROI)

- **ROI simple = valor para el negocio / costo del proyecto**. El costo es fácil de medir; el valor es lo difícil.
- **Pasos de Bill Whittemore**: 1) definir el problema u oportunidad y objetivos **específicos, medibles, alcanzables, adecuados y con plazo**; 2) recoger requerimientos; 3) construir el proyecto; 4) identificar y cuantificar beneficios; 5) establecer el punto de partida de costos e ingresos; 6) calcular el **TCO** (*Total Cost of Ownership*, costo total de propiedad: *hardware*, *software*, consultoría, personal, lanzamiento, mantenimiento y formación); 7) calcular el **ROI = NPV / inversión inicial × 100**; 8) hacer seguimiento y corregir.
- **NPV** (*Net Present Value*, valor actual neto) = suma de los flujos de caja (CF, *Cash Flow*) de cada año descontados a la tasa r, menos la inversión inicial.

### 2.7 Modelización del negocio

- "Aquello que no se mide, no se puede gestionar". Primero se define **qué** medir y **cómo**: el **modelo de negocio** y sus métricas.
- **Modelo de negocio**: simplificación de la realidad que permite **documentar, probar y desarrollar teorías** sobre cómo funciona el negocio y **experimentar** cómo afectan los cambios al resultado. Debe estar **vivo** como el negocio.
- **Silos de información**: departamentos entre los que no fluye la información (por falta de integración o por razones políticas). Lo mejor para un departamento no siempre es lo mejor para la organización.
- **Cómo se crea**: con metodologías como **contabilidad analítica o de costos, EFQM** (*European Foundation for Quality Management*), **Six Sigma, análisis de procesos, modelos financieros, análisis de ratios**; identificando áreas críticas, factores que influyen en el resultado y la estructura organizativa.

### 2.8 Indicadores clave (KPI)

- **KPI** (*Key Performance Indicators*, indicadores clave de desempeño): sirven para **evaluar si la organización alcanza sus objetivos** y medir su progreso.
- Deben: **reflejar los objetivos**, ser **críticos para el éxito**, ser **cuantificables y comparables** y **permitir acciones correctivas**. Pocos, alineados entre departamentos, definidos con los responsables de cada área.
- Cada KPI tiene **nombre, definición, forma de cálculo y objetivo**.

### 2.9 Modelo de datos

- **Modelo relacional** (E. F. **Codd**, **1970**): tablas y relaciones. **PK** (*Primary Key*, clave primaria) identifica cada registro; **FK** (*Foreign Key*, clave externa) relaciona tablas. Se consulta con **SQL** (*Structured Query Language*; ver aviso 6). El **modelo entidad-relación** muestra las tablas y sus relaciones.
- Primero se define el modelo de negocio; después, qué se quiere **medir (hechos)** y **cómo (dimensiones)**. Las dimensiones responden **qué, quién, por qué, dónde y cuándo**.
- **Tabla de hechos** (*fact table*): lo que se mide (por ejemplo, el total del ticket) más las claves de las dimensiones. **Tablas de dimensiones**: el contexto para agrupar y filtrar (tiempo, centro, empleado, forma de pago). **Dimensiones degeneradas**: no necesitan tabla propia (número de ticket, identificador de caja).
- **Dimensión tiempo**: la fecha se descompone en día de la semana, del mes, del año, mes, trimestre, año, vacaciones y fin de semana. Esos datos (y los feriados) **no están** en el sistema transaccional: hay que agregarlos.

| | **Esquema estrella** | **Esquema copo de nieve** (*snowflake*) |
|---|---|---|
| Dimensiones | **Una tabla por dimensión**, desnormalizada | Dimensiones **normalizadas**, con tablas relacionadas entre sí (Zona separada de Centro) |
| Relaciones | Solo hechos ↔ dimensiones | También dimensión ↔ dimensión |
| Redundancia | Sí (la descripción de zona se repite por centro) | No |
| A favor | Más simple y rápido de consultar | Menos espacio (a veces la diferencia es poca) |
| En contra | Ocupa más | Más complejo |

- **Constelación de hechos** (o esquema **galaxia**): varias estrellas con distintas tablas de hechos que comparten dimensiones.
- **Granularidad**: nivel de detalle. Analizar **líneas** de ticket tiene **mayor** granularidad que analizar tickets. Cada nivel responde unas preguntas y no otras; **cada vez que se agrega, se pierde información**. Conviene construir al **máximo detalle** si el volumen lo permite.
- **Jerarquías**: año → trimestre → mes → día; familia → subfamilia → artículo; zona → centro; categoría → empleado. Permiten agregar y desagregar.
- **Multidimensionalidad**: analizar por **varias dimensiones a la vez** (ventas de un artículo por centro y por mes).
- Si fabricante y artículo están en la misma dimensión no se pueden cruzar: van en dimensiones distintas.
- **Metadata o diccionario de datos**: describe atributos, origen, definiciones y transformaciones para que todos usen la **misma terminología**.
- **Cada modelo de datos responde un número limitado de preguntas**, y cada modelo responde preguntas distintas.

### 2.10 Componentes de BI (capítulo 4 del libro)

Los componentes son: **fuentes de información → proceso ETL → *datawarehouse* (con su metadata) → motor OLAP → herramientas de visualización**. En un proyecto real el orden es otro: primero se definen los **objetivos, el alcance y los modelos de negocio**.

**Fuentes de información**

- **Sistemas operacionales o transaccionales**: aplicaciones a medida, ERP, CRM (gestión de la relación con clientes), SCM (gestión de la cadena de suministro).
- **Sistemas departamentales**: previsiones, presupuestos, hojas de cálculo.
- **Fuentes externas**, a veces compradas (estudios de mercado, datos de población).
- La información puede ser estructurada, semiestructurada o **no estructurada** (correos, cartas, informes, videos).

**Calidad de datos**

- Si hay errores en el *datawarehouse* se **propagan por toda la organización** y llevan a decisiones erróneas; los usuarios **desprestigian** el proyecto.
- Los errores vienen de los **sistemas transaccionales**, del **proceso ETL** o del propio ***datawarehouse***. Conviene **corregirlos en el origen** (que el usuario elija valores en vez de escribirlos libremente), no solo en el ETL.
- La calidad es un **problema de negocio, no solo de tecnología**.
- **7 características** de datos de calidad: **precisión, integridad, coherencia, totalidad, validez, disponibilidad y accesibilidad**.

**Proceso ETL** (*Extract, Transform, Load*, extracción, transformación y carga)

- Consume entre el **60 % y el 80 %** del tiempo de un proyecto de BI. Tiene **5 subprocesos**:

| Subproceso | Qué hace |
|---|---|
| 1. **Extracción** | Recupera los datos físicamente de las fuentes: datos **en bruto**. Manual (rutinas, por ejemplo en COBOL) o con herramientas ETL (la opción más rentable) |
| 2. **Limpieza** | Comprueba la calidad, elimina duplicados, corrige errores y completa vacíos: datos **limpios** |
| 3. **Transformación** | Estructura y **sumariza** según los modelos de análisis (cambios de formato, códigos, valores derivados y **agregados**); acá se ajusta la **granularidad** |
| 4. **Integración** | Valida que los datos sean consistentes con las definiciones del *datawarehouse* y los carga (por ejemplo, que los totales de ventas coincidan con el origen) |
| 5. **Actualización** | Define la **periodicidad** de las nuevas cargas |

- **Almacén de datos intermedio** (*data staging*): paso entre la extracción y las etapas posteriores mientras se limpian los datos; acumula datos de varias fuentes. **Los usuarios finales nunca acceden**.
- **Datos "sucios"**: valores por defecto (código 999), ausencia de valor, valores crípticos o contradictorios, campos con varios usos, claves reutilizadas, identificadores no únicos.
- **Etapas de la limpieza**: **depurar** (*parsing*: separar nombre y apellido), **corregir** (*correcting*), **estandarizar** (*standardizing*), **relacionar** (*matching*: encontrar duplicados) y **consolidar** (*consolidating*: unir registros relacionados).

***Datawarehouse*** (almacén de datos)

- Responde a la necesidad de información **consistente, integrada, histórica y preparada** para analizar. Usar hojas de cálculo en su lugar genera errores, trabajo repetido, "entornos paralelos" y **distintas versiones de la misma realidad**.
- **Hugh J. Watson**: "una colección de información creada para soportar las aplicaciones de toma de decisiones". ***Datawarehousing***: el proceso completo de extraer, transformar y cargar, más el acceso de los usuarios.
- **Bill Inmon** (4 características): **orientado a un área** (un problema de negocio), **integrado** (medidas, códigos y formatos comunes), **indexado en el tiempo** (guarda historia) y **no volátil** (no lo mantienen los usuarios; se actualiza periódicamente).
- **Ralph Kimball**: da acceso a la información, es consistente, se puede separar y combinar por cada medida, incluye las herramientas de consulta y es "el lugar donde publicamos la información".
- Guarda los datos para **maximizar flexibilidad, facilidad de acceso y administración**. Se actualiza en forma **mensual, semanal o diaria**; el concepto *right time* dice que cada situación de negocio requiere su propio plazo.

**Data Mart y estrategias de construcción**

- **Data Mart**: para una **comunidad de usuarios** (un departamento, un nivel o un grupo con objetivos comunes) y pocas áreas (por ejemplo, marketing y ventas). **Más chico** que el *datawarehouse*: menos datos, menos modelos y menos usuarios. Surgieron porque el *datawarehouse* corporativo era caro, lento e inflexible.
- **Dependiente**: se alimenta del *datawarehouse* corporativo. **Independiente**: se alimenta directo de las fuentes; puede perpetuar los **silos de información**.

| | **Inmon** | **Kimball** |
|---|---|---|
| Estrategia | *Datawarehouse* **corporativo** primero y de él salen los Data Marts (de arriba hacia abajo) | Construir **Data Marts** por área, sin un *datawarehouse* central |
| A favor | Integrado y escalable | Barato y fácil de implementar; la más común |
| En contra | Caro, lento, propenso al fracaso | Riesgo de silos y de posponer la definición de criterios |

Según Watson, **las dos son válidas** bien desarrolladas. También existen la **híbrida** y la **federada**.

- **Metadata**: repositorio central de "información de la información" (significado de cada tabla y atributo, origen, transformaciones). Obliga a que toda la organización use **la misma terminología** ("margen bruto" debe estar definido).
- **ODS** (*Operational Data Store*): consolida datos de varias fuentes para decisiones **operativas**; su información es **volátil**, se actualiza en **tiempo real** y tiene como máximo dos o tres meses. Suele alimentar al *datawarehouse*.

**OLAP** (*On-Line Analytical Processing*, procesamiento analítico en línea)

- Es la tecnología más extendida para analizar el *datawarehouse*: análisis **multidimensional** en distintos **niveles de agregación**, desde el máximo resumen hasta el máximo detalle.
- **FASMI** (resumen de las 12 reglas de Codd según el OLAP Council): ***Fast*** (rápido), ***Analysis*** (lógica de negocio y estadística), ***Shared*** (compartido y seguro), ***Multidimensional*** e ***Information*** (manejar toda la información).
- Se representa con **cubos**: cada celda guarda un **hecho** (por ejemplo, unidades vendidas de un libro a un cliente en un año).

| Operación | Qué hace |
|---|---|
| **Rotar** (*slicing*) | Cambia el orden de las dimensiones (de clientes a libros) |
| **Seleccionar** (*dicing*) | Toma solo algunas celdas (cliente 2, libros 1 y 2, año 1) |
| **Agregar** (*roll-up*) | Sube al máximo nivel de agregación (total de libros) |
| **Bajar al detalle** (*drill-down*) | Baja por una jerarquía (por materias) |

| Tipo | Cómo accede | Ventaja / desventaja |
|---|---|---|
| **ROLAP** (relacional) | Directo a la base relacional, normalmente sobre un modelo estrella | Sin límite de tamaño / más lento |
| **MOLAP** (multidimensional) | A una base multidimensional | Muy rápido / si cambian las dimensiones hay que recargar el cubo |
| **HOLAP** (híbrido) | Datos agregados en la multidimensional y detalle en la relacional | Combina las ventajas de ambos |
| **DOLAP** (de escritorio) | Cubo cargado en la memoria de la computadora del usuario | El usuario recibe solo lo que le interesa |

- Alternativa al OLAP: herramientas de **lógica asociativa** (por ejemplo QlikView), que guardan cada valor una sola vez y consultan sin dimensiones predefinidas.

**Herramientas de BI**: generadores de informes; herramientas de consultas e informes para el usuario final; herramientas OLAP; ***dashboards*** (indicadores operativos o tácticos de un área) y ***scorecards*** (nivel estratégico, indicadores relacionados, toda la organización, como el *Balanced Scorecard* de Kaplan y Norton); planificación y simulación; minería de datos; minería de texto; visualización y GIS (sistemas de información geográfica).

**Usuarios** (Eckerson y Howson)

- **Productores** de información (alrededor del **20 %**): estadísticos con minería de datos, autores de informes y usuarios avanzados.
- **Consumidores** (la mayoría): directivos, gestores, clientes y proveedores que usan cuadros de mando, informes interactivos y estandarizados, cada vez más vía web.
- Se diferencian **roles, no individuos**: el mismo ejecutivo puede usar un informe estático y un cuadro de mando en tiempo real. Por eso hay que conocer qué necesita cada rol antes de elegir la herramienta.

### 2.11 Guías del TP7 — respuestas

| Pregunta | Respuesta modelo |
|---|---|
| ¿Definición más ajustada de BI? | La de Gartner: proceso interactivo para explorar y analizar información estructurada (en un *datawarehouse*) y descubrir tendencias o patrones; convierte datos en información y conocimiento para decidir basándose en hechos |
| ¿Momento adecuado para aplicar BI? | **De forma continua**, no puntual. Especialmente con mercados que cambian rápido, ante anomalías del negocio o cuando quienes generan información están desbordados |
| ¿A qué organizaciones va dirigida? | A cualquiera que tome decisiones; urgente en estructuras complejas, con muchos clientes o que dependen de procesos "artesanales" |
| ¿Qué beneficios aporta? | Tangibles, intangibles y estratégicos (ver 2.4) |
| ¿Cómo unificar información de distintos entornos? | Reunirla en un *datawarehouse* (copia, sin afectar a los transaccionales), en tablas relacionadas, y cruzarla con herramientas de BI: "una sola versión de la verdad" |
| Concepto y utilidad del modelo de negocio | Simplificación de la realidad para documentar y probar teorías; sirve para experimentar el efecto de los cambios y evitar silos |
| ¿Qué es el modelo relacional? | Tablas y relaciones (Codd, 1970) con PK y FK, consultado con SQL |
| Factores del modelado de datos | Partir del modelo de negocio; definir hechos y dimensiones; ver qué datos hay en los transaccionales y cuáles agregar (calendarios, feriados) |
| Estrella frente a copo de nieve | Ver tabla 2.9 |
| Granularidad y multidimensionalidad | Nivel de detalle (decide qué preguntas se responden) y análisis por varias dimensiones a la vez |

---

## 3. Minería de datos (Tema 9) 📁

### 3.1 Datos, información y conocimiento

- **Datos**: registros de observaciones o sucesos. **Información**: lo que se obtiene al detectar la utilidad de los datos. **Conocimiento**: reglas de cómo una cosa afecta a otra. "El conocimiento es poder".
- **Minería de datos** (*Data Mining*, DM): métodos y algoritmos para la **extracción automática** de información sintetizada que caracteriza **relaciones escondidas** en grandes volúmenes de datos, con capacidad **predictiva**. Reúne técnicas estadísticas y de **aprendizaje automático** (inteligencia artificial).
- **Analogía**: una montaña (los datos) con **diamantes** escondidos entre piedras (el conocimiento).
- Trabaja sobre **datos estáticos** (un estado pasado que no cambia mientras se analiza). **No confundir con monitoreo**, que trabaja con datos cambiantes en tiempo real y se dedica a reconocer patrones, no a descubrir.
- Apunte de clase: extracción de información o patrones **no triviales, implícitos, previamente desconocidos y potencialmente útiles**, por medios automatizados; objetivo, ayudar a decidir. Diferencia con BI según la clase: BI es más estático, saca conclusiones de datos estructurados que ya se tienen.

### 3.2 Proceso KDD

- **KDD** (*Knowledge Discovery in Databases*, descubrimiento de conocimiento en bases de datos): término usado desde **1989**. El descubrimiento es una **inducción no supervisada** con dos procesos: buscar regularidades interesantes y formular leyes que las describan.
- **Definición**: extracción **no trivial** de información **implícita**, **previamente desconocida** y **potencialmente útil** a partir de un conjunto de datos.
- **Cuatro ideas que diferencian al KDD**:

| Idea | Qué exige |
|---|---|
| **Lenguaje de alto nivel** | Conocimiento **inteligible para un humano**. Por eso quedan fuera del KDD las representaciones de bajo nivel como las de las **redes neuronales**, aunque sean un método válido de minería |
| **Precisión** | Los datos tienen ruido; se mide el **grado de certidumbre**. Si la certeza es baja, el patrón no es conocimiento |
| **Interés** | Solo es conocimiento lo **nuevo, potencialmente útil y no trivial** según criterios del usuario |
| **Eficiencia** | Tiempo y memoria que crecen de forma **polinomial** con el tamaño de los datos |

- Es la convergencia de aprendizaje automático, estadística, reconocimiento de patrones, inteligencia artificial, bases de datos, visualización, sistemas de apoyo a la decisión y recuperación de información.
- **KDD frente a minería de datos**: el **KDD es el proceso completo**; la **minería es solo la etapa de descubrimiento** dentro del KDD. Es la parte fundamental (la única que genera patrones) pero está **subordinada**.

**Los 9 pasos del proceso KDD** (interactivo e iterativo):

1. **Comprensión del dominio** y de los objetivos del usuario final.
2. **Creación del conjunto de datos objetivo** (selección de variables y ejemplos, muestreo).
3. **Preprocesado**: eliminar ruido, tratar valores ausentes, normalizar.
4. **Transformación y reducción**: características útiles, menos variables, proyección a espacios más simples. **Paso crítico**: marca el éxito o fracaso.
5. **Elección del tipo de sistema** de minería (clasificación, regresión, agrupamiento, detección de desviaciones).
6. **Elección del algoritmo**.
7. **Minería de datos**: búsqueda del conocimiento. Su éxito depende de los pasos previos.
8. **Interpretación** del conocimiento extraído, con posibilidad de volver al paso 1.
9. **Consolidación**: incorporar el conocimiento al sistema o documentarlo, resolviendo inconsistencias.

- **Fayyad** (según el artículo de la cátedra) resume el núcleo del KDD en **5 etapas**: **selección, preprocesamiento, transformación, minería de datos e interpretación/evaluación**. Antes va la comprensión del dominio y después la consolidación del conocimiento: así se llega a los 9 pasos.

Diagrama: **BD → Selección → Datos objetivo → Preprocesado → Datos preprocesados → Transformación → Datos transformados → Minería de datos → Patrones → Interpretación / Evaluación → Conocimiento**.

- **Por qué creció el análisis de datos** (tres factores): **potencia de las computadoras**, **ritmo de adquisición de datos** y **nuevos métodos** de aprendizaje.
- **Aprendizaje automático frente a minería**: el aprendizaje automático usa un conjunto **chico y seleccionado**; la minería parte de una base **grande** generada para **otros propósitos**.

### 3.3 Fases del KDD según la lectura (6 estados)

1. **Recolección de datos**: fuentes internas y externas, muchas transaccionales. Conviene una fuente **unificada, accesible y desconectada** del trabajo transaccional. Depende de la fuente (**OLAP** u **OLTP**, *On-Line Transaction Processing*; *datawarehouse* o copia; **ROLAP** o **MOLAP**) y del usuario: **picapedreros o granjeros** (informes periódicos, controlan valores) y **exploradores** (buscan patrones nuevos). Información externa: censos, datos de la industria, clima, calendarios, bases compradas.
2. **Selección, limpieza y transformación**: eliminar datos erróneos o inconsistentes (**limpieza**) e irrelevantes (**criba**), casi siempre con métodos estadísticos (histogramas, muestreo vertical u horizontal, redefinición de atributos).
3. **Minería de datos**: datos en disco, muy alta dimensionalidad, evidencia positiva, datos imperfectos. **Minería dirigida** (se sabe qué se busca: predecir) frente a **no dirigida** (no se sabe qué se busca).
4. **Evaluación y validación**: 1.ª fase, probar la precisión en un **banco de ejemplos independiente**; 2.ª fase, **experiencia piloto** (por ejemplo, un *mailing* a un grupo de clientes).
5. **Interpretación y difusión**: el modelo puede requerir implementación (fraude con tarjetas en tiempo real), interpretación (zonas geográficas) o difusión (cervezas y congelados se compran juntos → ponerlos en **estantes distantes**).
6. **Actualización y monitorización**: un modelo válido deja de serlo si cambia el contexto; hay que revalidarlo con datos nuevos.

### 3.4 Datos atípicos y faltantes

| Acción | Atípicos (*outliers*) | Faltantes (*missing values*) |
|---|---|---|
| **Ignorar** | Algoritmos robustos (árboles) | Algoritmos robustos (árboles) |
| **Filtrar la columna** | Solución extrema; mejor reemplazarla por una columna "normal / atípico" | Solución extrema; mejor una columna booleana "existía / no existía" |
| **Filtrar la fila** | **Sesga los datos** (las causas suelen ser casos especiales) | **Sesga los datos** |
| **Reemplazar el valor** | Por nulo, máximo, mínimo o media; o predecirlo | Por la media; o predecirlo |
| **Discretizar** | Muy alto, alto, medio, bajo, muy bajo: el atípico cae en un extremo | — |
| **Segmentar** | — | Modelos distintos por segmento según los datos disponibles, luego se combinan |
| **Esperar** | — | Cambiar la política de calidad y esperar los datos |

- **Razones de los faltantes**: pueden ser **relevantes** (no dar teléfono = no quiere ser molestado), **no existentes** (un cliente nuevo no tiene consumo de 12 meses) o **incompletos** (al unir fuentes distintas).

### 3.5 Evolución histórica

| Etapa | Pregunta típica | Tecnología | Característica |
|---|---|---|---|
| Recolección (años 60) | Beneficios totales de los últimos 4 años | Computadoras, cintas, discos | Retrospectivo, datos estáticos |
| Acceso a los datos (años 80) | Ventas en Cataluña la última Navidad | Bases relacionales (SQL), ODBC | Retrospectivo, dinámico a nivel registro |
| *Datawarehouse* y apoyo a decisiones (años 90) | Ventas en Andalucía bajando hasta la tienda | OLAP, bases multidimensionales | Retrospectivo, múltiples niveles |
| **Minería de datos** | Tendencia de venta en Castilla el próximo año | Algoritmos avanzados, multiprocesadores | **Prospectivo, proactivo** |

### 3.6 Qué no es minería de datos

**No es estadística**:

| Eje | Minería de datos | Estadística clásica |
|---|---|---|
| Automatización | Construye el modelo **automáticamente** | La maneja un **estadístico profesional** |
| Enfoque | **Exploratorio** | **Confirmatorio** (prueba hipótesis) |
| Inteligencia artificial | La incorpora | Teoría de la probabilidad |
| Dimensionalidad | Mejor con **muchas variables** | Difícil encontrar hipótesis con muchas variables |
| Supuestos | **Menos restrictiva** | Los datos deben cumplir requisitos |

Apunte de clase: la estadística toma **muestras** e infiere a la población; la minería trabaja con **toda la base** y usa estadística.

**No es OLAP**: OLAP **navega** rápido por los datos de forma asistida (análisis multidimensional) pero **no genera información nueva**. Arquitecturas: **MOLAP** (multidimensional; datos precompilados, para soluciones departamentales chicas) y **ROLAP** (relacional; traduce las consultas a SQL sobre el *datawarehouse*; más flexible).

### 3.7 Los tres retos

1. **Falsa interpretación**: es fácil engañarse con la estadística (los resultados valen para grupos, no individuos); con software de minería es aún más fácil "hacer creíble una falsedad".
2. **Correlación no es causalidad — Florida**: Florida tiene la edad promedio al fallecer más alta de Estados Unidos, pero no porque vivir allí alargue la vida: allí se jubilan y mudan los mayores (**efecto de selección**). La minería **genera hipótesis desde los datos** (es **explorativa, no explicativa**): hay que validarlas con datos nuevos. Además no puede ser experimental.
3. **Tiempo, espacio y privacidad**: variables que cambian en el período, **granularidad del tiempo** (con datos mensuales no se predice por semana) y **privacidad** (combinar las bases del teléfono, el banco y el supermercado arma un perfil completo de una persona; el marco jurídico no acompañó).

### 3.8 Tareas de la minería de datos

| Tarea | Qué hace | Paradigma |
|---|---|---|
| **Agrupamiento** (*clustering*) | Identifica categorías o grupos para describir los datos | No supervisado / descriptivo |
| **Clasificación** | Asigna un dato a una de varias **clases predefinidas** | Supervisado / predictivo |
| **Condensación** (descripción de conceptos) | Descripción **compacta** de un subconjunto | No supervisado / descriptivo |
| **Detección de desviaciones** | Cambios significativos respecto de valores pasados o normales | No supervisado / descriptivo |
| **Modelado de dependencias** | Dependencias entre variables, a nivel estructural y cuantitativo | No supervisado / descriptivo |
| **Regresión** | Predice un **valor real** (continuo) | Supervisado / predictivo |

**Proceso de minería** (4 estados): **preprocesado** → **selección de características** (las variables más influyentes) → **algoritmo de extracción** (modelo de conocimiento) → **evaluación y validación**.

### 3.9 Predictivo frente a descriptivo

- **Predictivo (supervisado)**: predice una **etiqueta** conocida en datos históricos. Dos fases: **entrenamiento** (subconjunto con etiqueta) y **prueba** (el resto).
- **Descriptivo (no supervisado)**: descubre patrones en los datos actuales.
- **Taxonomía**: interpolación, predicción secuencial, aprendizaje supervisado, aprendizaje no supervisado y abducción. En lo supervisado: **clasificación** (clases disjuntas) frente a **categorización** (pueden solaparse); clase con dos valores = ***concept learning***; clase continua = **estimación**.
- **Reglas de asociación**: **confianza** = casos que cumplen antecedente y consecuente / casos que cumplen el antecedente; **soporte** = casos (o porcentaje) donde se aplica la regla. Algoritmos tipo **Apriori** en dos fases: **A**, buscar conjuntos frecuentes (*large itemsets*) con soporte suficiente; **B**, partirlos en reglas y quedarse con las de confianza suficiente. También hay asociaciones entre jerarquías, **negativas** ("80 % de quienes compran pizza congelada no compra lentejas") y con valores continuos (se discretizan).
- **Combinación de hipótesis**: ***boosting*** (el **mismo** algoritmo sobre distintas particiones) y ***voting*** (**distintos** algoritmos sobre todos los datos).

### 3.10 Métodos y técnicas

**Métodos**: agrupamiento (segmentación estática o dinámica), asociación, **secuenciamiento** (asociación donde el **tiempo** es clave), reconocimiento de patrones, **previsión** (*forecasting*, series temporales), simulación (por ejemplo CAD-CAM), optimización (maximizar beneficios o minimizar costos con restricciones) y clasificación (*scoring*).

| Supervisados | No supervisados |
|---|---|
| Árboles de decisión | Detección de desviaciones |
| Inducción neuronal | Segmentación |
| Regresión | Agrupamiento (*clustering*) |
| Series temporales | Reglas de asociación |
| | Patrones secuenciales |

**Técnicas**:

- **Estadísticas**: **ANOVA** (análisis de la varianza: diferencias de medias entre grupos), **Ji cuadrado** (independencia entre variables), **componentes principales** (reduce variables), análisis de **clusters**, **análisis discriminante** (clasifica en grupos ya definidos), **regresión lineal** (la más básica; variables continuas) y **logística** (admite discretas).
- **Árboles de decisión**: dividen los datos en subconjuntos; **CART** parte en **2** (validación cruzada, índice de Gini), **CHAID** (*Chi Squared Automatic Interaction Detector*) parte en **más de 2** (test Ji cuadrado).
- **Reglas de asociación**: "cesta de la compra", reglas SI … ENTONCES.
- **Redes neuronales**: inspiradas en el cerebro (estudios desde 1930), capas de neuronas, aprenden patrones; supervisadas o no. Inconveniente: **no generan una ecuación que explique el modelo** (caja negra).
- **Algoritmos genéticos**: mutación y cruce para **optimizar**; se usan al principio para **elegir variables**.
- **Lógica difusa**: fronteras suaves entre grupos.
- **Series temporales**: ciclos, tendencias y estacionalidades para predecir, si no hay cambios estructurales.
- **Redes bayesianas**: aprenden dependencias y causalidad, combinan conocimiento con datos, evitan el sobreajuste, manejan datos incompletos.
- **Inducción de reglas** y **sistemas expertos** (con motor de inferencia).

### 3.11 Evaluación de la minería

- **Tres medidas clave** de una herramienta: **precisión**, **explicación** (que el usuario entienda cómo funciona) e **integración** (que se incruste en el proceso de negocio, sin copias de datos).

| Medida de precisión | Qué es |
|---|---|
| **Precisión** | % de predicciones correctas |
| **Tasa de error** | Complemento de la precisión; útil con precisiones muy altas (pasar de 99 % a 99,5 % reduce el error a la mitad) |
| **Tasa de error en rechazo** | Se descartan las predicciones con poca confianza (rechazando 80 % se puede duplicar la precisión) |
| **Error cuadrático medio** | Para variables continuas; pesa más los errores grandes |
| **Elevación** (*lift*) | Cuánto mejora la respuesta respecto del azar: 30 % / 10 % = **3** |
| **Beneficio / ROI** | La mejor medida: cuánto gana el negocio |

- **Explicación**: generación automática de reglas, OLAP integrado, evaluación automática del modelo. **Integración**: usar los datos como están, guardar el modelo como metadatos, preprocesar predictores, manejar datos sucios, valores perdidos y **escalabilidad**.

### 3.12 Apuntes de clase (14/9)

- **Aplicaciones**: retención de clientes, patrones de compra, detección de fraude, manejo del riesgo (a quién prestar), segmentación.
- **Ciclo de un proyecto** (9 pasos): aprender sobre el negocio, recolectar, limpiar y transformar, definir la meta y el modelo, elegir algoritmos, generar reportes, generar predicciones, aplicar los resultados, actualizar los modelos.
- **CRISP-DM** (*Cross-Industry Standard Process for Data Mining*): proceso confiable y repetible para personas con pocos conocimientos; **6 fases**: comprensión del negocio, comprensión de los datos, preparación de los datos, modelado, evaluación e implantación.
- **Bodega de datos**: base orientada a consultas, **consolidada, consistente, orientada a un tema, histórica y de solo lectura**; es el punto de partida de la minería y no cambia mientras se mina.
- **Minería frente a análisis de datos**: el análisis no suele ser automatizado ni con tanto volumen. **Frente a aprendizaje automático**: es el área de la inteligencia artificial que hace programas que aprenden; la minería lo usa para predecir.

### 3.13 Preguntas teóricas del TP8 (respuestas del grupo)

| Consigna | Respuesta clave |
|---|---|
| 1. Cuadro de los 9 pasos con insumo y producto; impacto de fallar el preprocesado | Cada paso toma el producto del anterior. Si falla el **preprocesado**, el **modelo clasificador** aprende el ruido como patrón, los faltantes mal tratados sesgan la muestra y los atípicos distorsionan; la evaluación puede parecer buena si el banco de prueba tiene el mismo defecto. Invalida el modelo |
| 2. Minería fundamental pero subordinada al KDD | "Minería sin KDD es una operación algorítmica **ciega**" (no sabe qué buscar, con qué calidad ni si lo hallado es válido); "KDD sin minería es un proceso **inconcluso**" (datos limpios sin patrones) |
| 3. Minería frente a estadística; Florida | Ver 3.6 y 3.7 |
| 4. Minería frente a OLAP frente a monitoreo | Minería **genera** información nueva sobre datos **estáticos** con descubrimiento **proactivo**; OLAP **navega** de forma asistida sobre datos **históricos agregados** con consulta del usuario (*drill-down*, *roll-up*, *slice & dice*); monitoreo **verifica** datos en **tiempo real** de forma reactiva (alertas) |
| 5. Mapa de tareas | Supervisado: clasificación y regresión. No supervisado: agrupamiento, dependencias, desviaciones y condensación |
| 6. Redes neuronales y lenguaje de alto nivel | Predicen bien, pero el conocimiento queda en miles de **pesos numéricos**: es una **caja negra** que no se puede explicar; choca con la exigencia de conocimiento **inteligible** del KDD |
| 7. Árbol de faltantes y atípicos con sesgo | Ver 3.4: filtrar filas **sesga**; la media **reduce la varianza**; discretizar **pierde precisión**; segmentar puede **sobreajustar** |
| 8. Ensayo | Escalabilidad del *hardware* + granularidad del tiempo + privacidad: más detalle temporal y más fuentes cruzadas = perfiles más precisos de las personas. Marco legal: Ley 25.326 de Protección de Datos Personales (Argentina) y GDPR (Reglamento General de Protección de Datos, Unión Europea) |
| 9. KDD, CRISP-DM y SEMMA | Ver tabla abajo |

| Eje | KDD | CRISP-DM | SEMMA |
|---|---|---|---|
| Origen | **Académico** (1989, Fayyad) | **Consorcio de empresas**: DaimlerChrysler, SPSS y NCR; ligado al *software* SPSS Clementine | **SAS Institute**; ligado al *software* SAS Enterprise Miner |
| Fases | 9 (5 en el núcleo de Fayyad) | 6, en una secuencia **no rígida** | 5: *Sample, Explore, Modify, Model, Assess*; el muestreo es **opcional** |
| Iteración | Muy iterativo, vuelve desde cualquier fase | Ciclo con fuerte retroalimentación | Más secuencial, con ajustes técnicos |
| Orientación al negocio | Empieza por el dominio, foco en validez científica | **La más orientada al negocio** | Técnica; supone los objetivos ya definidos |
| ¿Incluye negocio y despliegue? | Sí (antes y después del núcleo) | Sí, explícitamente | **No explícitamente**; según Azevedo y Santos queda implícito, porque no se puede muestrear sin entender el negocio |

**Mapeo de fases según el artículo de la cátedra** (Azevedo y Santos, "KDD, SEMMA and CRISP-DM: a parallel overview"):

| KDD | SEMMA | CRISP-DM |
|---|---|---|
| Antes del KDD (comprensión del dominio) | — | Comprensión del negocio |
| Selección | *Sample* | Comprensión de los datos |
| Preprocesamiento | *Explore* | Comprensión de los datos |
| Transformación | *Modify* | Preparación de los datos |
| Minería de datos | *Model* | Modelado |
| Interpretación / evaluación | *Assess* | Evaluación |
| Después del KDD (consolidación) | — | Despliegue |

- **Conclusión del artículo**: SEMMA y CRISP-DM son **implementaciones del proceso KDD**. CRISP-DM parece más completo, pero SEMMA también incluye implícitamente el negocio y la consolidación.
- **Ojo:** el cuadro del TP8 del grupo puso "preparación de los datos" junto al preprocesado; según el artículo, el preprocesado corresponde a **comprensión de los datos** y la transformación a **preparación de los datos**.

---

## 4. Big Data (Tema 10, entra en el final) 📁

### 4.1 Mapa conceptual

- **Definición**: ecosistema o paradigma para **capturar, almacenar y analizar** datos de **gran volumen, velocidad y variedad** que superan lo que manejan los sistemas tradicionales. Es la infraestructura base sobre la que se construyen el análisis y la estrategia (apunte de clase).
- **Las 3 V**: **volumen, velocidad, variedad**. La guía de PowerData advierte: **"Big" no es la clave**; el volumen es solo una parte del rompecabezas. Las empresas quieren saber no solo qué pasa, sino **qué va a pasar**, y lo más cerca posible del **tiempo real**.
- **Por qué importa**: impacta en la industria, el negocio y la sociedad y da **ventaja competitiva**. Hoy puede ser más valioso detectar al **cliente que más influye** sobre otros compradores que al que más compra.
- **Nace de nuevas necesidades del mercado**: **personalización máxima** del cliente, el paso **de la transacción a la interacción** y **nuevos dispositivos** (móviles, domótica, vehículos con sensores).
- **Requiere Big Analytics**: análisis **predictivo** y **clusterización** de clientes; trabaja con **datos en crudo, al mayor detalle**; lo operan el **Data Scientist** y el **Data Analyst**; evoluciona desde el **BI tradicional y el Data Warehouse**, cuyas limitaciones son **modelos rígidos, poco ágiles y sin tiempo real**; se integra con el **Analytic Data Warehouse (ADW)**, que puede convivir con el tradicional en un **modelo híbrido DWH + ADW**.
- **Metodología MAD**: **Magnética** (capta todo tipo de datos), **Ágil** (ingiere y se adapta rápido) y **Detallada** (análisis estadístico fino).
- **Origen de Hadoop**: nace cuando **Google** no puede indexar la web al ritmo que exige el mercado y aplica "divide y vencerás": muchas computadoras pequeñas que procesan cada una una porción pero actúan como una sola. En **2006** la comunidad de **código abierto** desarrolla Hadoop; luego **Yahoo** lo impulsa y lo adoptan empresas como **Facebook**. Permite, por ejemplo, una regresión lineal sobre millones de registros del histórico con un **ROI muy rápido**.
- **Tecnología: Hadoop**: **HDFS** (*Hadoop Distributed File System*, archivos distribuidos), **MapReduce** (procesamiento paralelo), **código abierto** y ***commodity hardware*** (equipos comunes y baratos).
- **4 megatendencias**: **Movilidad, Cloud, Social Media, Analytics**.
- **Tiempo real**: ***Data Stream*** (analiza datos en movimiento) y **CEP** (*Complex Event Processing*, procesamiento de eventos complejos: detecta eventos predefinidos, como operaciones sospechosas con tarjetas).
- **Megatendencias en detalle**: **Movilidad** (acceso a los datos desde cualquier lugar y desde dispositivos que no son de la empresa, lo que dificulta el control); **Cloud** (no hace falta comprar la infraestructura: baja la inversión inicial y se puede **prever el costo del crecimiento**); **Social Media** (gustos y preferencias para captar y fidelizar); **Analytics** (análisis de cualquier tipo de dato, sin patrones de búsqueda prefijados).
- **Big Analytics frente al BI tradicional**: el BI tradicional cargaba modelos tan lento que al terminar ya no servían; Analytics trabaja con los datos **en crudo, al nivel de granularidad más bajo**, con modelos más ágiles. El **Analytic Data Warehouse** **no reemplaza** al *data warehouse* actual: cada uno cubre necesidades distintas y conviven en un **modelo híbrido**. Aparece el perfil de **Data Science**.
- **CEP, ejemplos de la guía**: un banco que analiza en tiempo real lo que pasa con las **tarjetas de crédito** en cajeros y comercios; **sensores de maquinaria** que envían una alerta antes de que aparezca un fallo.
- **Implementación**: primero **conocer y cuantificar el valor** que puede dar al negocio (autoevaluación de límites, expectativas y restricciones); elegir la tecnología según las metas (para eventos en tiempo real, **CEP**; para análisis predictivo, bases con procesamiento **MPP**); perfiles de negocio que conozcan el sector (Data Scientist, Data Analyst); y herramientas según el tipo de análisis.
- **Privacidad**: en Google "no todo es gratis", el precio es la privacidad; las empresas deben equilibrar los datos que analizan con la **tolerancia** de sus clientes.
- **Implementación (mapa del TP)**: **medir el valor para el negocio**, **las metas determinan la tecnología** (no al revés) y perfiles de negocio con herramientas adecuadas.
- **Genera** innovación y ventaja competitiva; **plantea** el desafío de **seguridad y privacidad**: equilibrio entre los datos analizados y lo que el cliente tolera.
- Bases **MPP** (*Massively Parallel Processing*, procesamiento masivamente paralelo) para el análisis predictivo sobre todo el histórico.

### 4.2 BI, minería de datos y Big Data

| Aspecto | BI | Minería de datos | Big Data |
|---|---|---|---|
| Qué es | Procesos y herramientas que convierten datos en información para decidir | Descubrir patrones, relaciones y tendencias ocultas | Paradigma para capturar, almacenar y analizar datos masivos |
| Pregunta central | ¿Qué pasó y cómo vamos? | ¿Qué patrones hay en los datos? | ¿Qué va a pasar y qué descubrimos con todos los datos? |
| Enfoque temporal | Pasado y presente | Pasado, para descubrir y predecir | Presente y futuro, en tiempo real |
| Tipo de datos | Estructurados, internos | Estructurados y semiestructurados, ya preparados | Estructurados, semiestructurados y **no estructurados** (redes, sensores, logs) |
| Volumen | Moderado (lo que soporta un *datawarehouse*) | De moderado a grande | **Masivo**, infraestructura distribuida |
| Técnicas | Consultas, reportes, tableros, OLAP, KPI | Clasificación, agrupamiento, asociación, regresión, anomalías | Big Analytics, MapReduce, Data Stream, CEP |
| Tecnología | *Datawarehouse*, ETL, *reporting* | Algoritmos estadísticos y de aprendizaje automático | Hadoop, ADW, *cloud*, bases MPP |
| Perfil | Gerentes y analistas de negocio | Analistas de datos, estadísticos | Data Scientist, Data Analyst |
| Resultado | Informes y tableros | Modelos y patrones | Conocimiento nuevo y servicios personalizados casi en tiempo real |
| Limitación | Poco ágil, sin tiempo real | Depende de la calidad de los datos | Infraestructura nueva, perfiles caros, privacidad |

**Matriz de la clase** ("Ingeniería de datos"):

| | Big Data | Minería de datos | BI |
|---|---|---|---|
| Fin principal | Almacenar y procesar a escala masiva | **Descubrir patrones** | **Optimizar decisiones** corporativas |
| Tipo de datos | **Crudos** y variados | **Consolidados** | **Estructurados y depurados** |
| Perfil | **Ingeniero de datos** | **Científico de datos** | **Analista de BI** o consultor |
| Foco temporal | **Presente continuo** | **Futuro predictivo** | **Pasado y presente** descriptivo |

- **Cadena de la clase**: de los datos de **Big Data** se aplica **minería de datos**, y con lo extraído se hace **BI**.
- **No son excluyentes**: conviven en un **modelo híbrido**. BI mira hacia atrás; Big Data apunta hacia adelante; la minería es una herramienta que se aplica tanto sobre un *datawarehouse* como sobre Big Data.
- El TP pone el foco temporal de la minería en el "pasado" y la clase en el "futuro predictivo": si preguntan, la minería **analiza datos pasados para predecir el futuro**.

---

## 5. Repaso final

### 5.1 Mapa de relaciones entre los temas

- **Redes de Petri** modelan el **comportamiento** de un sistema concurrente (procesos, estados, recursos): es **diseño**.
- **BI, minería y Big Data** tratan los **datos** que esos sistemas generan para **decidir**: Big Data captura y procesa → la minería descubre patrones → BI los convierte en indicadores y decisiones.
- **Puntos de contacto**: el *datawarehouse* (BI) es el punto de partida de la minería; OLAP aparece en BI y en minería (que no es OLAP); la granularidad aparece en el modelo de datos de BI y en el tercer reto de la minería; la privacidad aparece en minería y en Big Data.

### 5.2 Trucos para memorizar

- **"Lu-Tra-Ar-Ma"**: elementos de una Red de Petri: **Lu**gares (círculos), **Tra**nsiciones (barras), **Ar**cos, **Ma**rcas.
- **"Más menos menos"**: C = C⁺ − C⁻ (posterior **menos** previa) y M' = M − Pre + Post.
- **Árbol finito: "Mu-Du-W"**: se corta en marcados **Mu**ertos, **Du**plicados o con **W** (infinito).
- **"VACCa"**: propiedades de comportamiento: **V**ivacidad, **A**cotamiento, **C**iclicidad, **C**onservación, **a**lcanzabilidad.
- **"Pi-E-A-Info-Á-Co"**: definición de Gartner: **P**roceso **i**nteractivo, **E**xplorar, **A**nalizar, **Info**rmación estructurada, **Á**rea, **Co**municar y cambiar.
- **"Tan-In-Es"**: beneficios de BI: **Tan**gibles, **In**tangibles, **Es**tratégicos.
- **"Re-Crí-Cuan-Co"**: requisitos de un KPI: **Re**flejar objetivos, **Crí**ticos, **Cuan**tificables y comparables, **Co**rrectivos.
- **"Qué-Quién-Por qué-Dónde-Cuándo"**: las dimensiones.
- **"Le-Pre-In-E"**: ideas del KDD: **Le**nguaje de alto nivel, **Pre**cisión, **In**terés, **E**ficiencia.
- **"Do-Ob-Pre-Trans | Sis-Al-Mi | In-Con"**: los 9 pasos del KDD en tres bloques (preparar, minar, aprovechar).
- **SEMMA se deletrea**: **S**ample, **E**xplore, **M**odify, **M**odel, **A**ssess.
- **"MAD = Ma-Ág-De"**: **Ma**gnética, **Ág**il, **De**tallada.
- **3 V**: **V**olumen, **V**elocidad, **V**ariedad. **4 megatendencias "MoCSA"**: **Mo**vilidad, **C**loud, **S**ocial Media, **A**nalytics.

### 5.3 Errores frecuentes en el examen

- ❌ "Una red viva siempre es cíclica." ✅ Son propiedades independientes: una red puede ser viva sin volver nunca a M0.
- ❌ "Red segura = red que no se bloquea." ✅ Segura = **1-acotada**; que no se bloquee es **vivacidad**.
- ❌ "C = C⁻ − C⁺." ✅ **C = C⁺ − C⁻**.
- ❌ "Un arco puede unir dos lugares." ✅ Siempre une **lugar y transición** (grafo bipartito).
- ❌ "En la matriz de incidencia, filas = lugares." ✅ Según la lectura, **filas = transiciones, columnas = lugares**.
- ❌ "BI es un análisis que se hace una vez." ✅ Es un **proceso continuo** (interactivo).
- ❌ "El esquema estrella está normalizado." ✅ La estrella es **desnormalizada**; el **copo de nieve** está normalizado.
- ❌ "Mayor granularidad = menos detalle." ✅ **Mayor granularidad = más detalle** (líneas de ticket > tickets).
- ❌ "Un Data Mart es más grande que un *datawarehouse*." ✅ Es **más chico** y para una comunidad de usuarios.
- ❌ "KDD y minería de datos son lo mismo." ✅ La minería es **una etapa** del KDD.
- ❌ "OLAP descubre patrones nuevos." ✅ OLAP **navega**; la minería **descubre**.
- ❌ "Si dos variables están correlacionadas, una causa la otra." ✅ **Correlación no es causalidad** (Florida).
- ❌ "Filtrar las filas con faltantes no tiene costo." ✅ **Sesga** los datos.
- ❌ "La regresión es una tarea descriptiva." ✅ Es **predictiva / supervisada** (predice un valor real).
- ❌ "Las redes neuronales cumplen con el lenguaje de alto nivel del KDD." ✅ Son una **caja negra**: quedan fuera de ese criterio aunque sean un método válido.
- ❌ "Big Data reemplaza al *datawarehouse*." ✅ Pueden **convivir** (modelo híbrido DWH + ADW).
- ❌ "SEMMA incluye la comprensión del negocio." ✅ SEMMA **la supone resuelta**; CRISP-DM es la más orientada al negocio.

### 5.4 Preguntas integradoras con respuesta modelo

1. **¿Por qué la minería de datos depende del *datawarehouse* de BI?** — Porque la minería necesita datos **consolidados, limpios e históricos**, desconectados de los sistemas transaccionales, y eso es lo que provee el **datawarehouse** cargado con **ETL**. La lectura de minería indica que el análisis es mucho más sencillo si la fuente es unificada, accesible y desconectada del trabajo transaccional. Por eso el *datawarehouse* es "el punto de partida" de la minería.
2. **Compará OLAP, minería de datos y Big Data.** — **OLAP** navega de forma asistida por datos históricos agregados en varias dimensiones, **sin generar información nueva**. La **minería** descubre de forma **automática** patrones nuevos y predice. **Big Data** es el **contexto** de datos masivos, veloces y variados (incluso no estructurados) que exige infraestructura distribuida (**Hadoop**) y análisis en tiempo real (**CEP**, **Data Stream**).
3. **¿Qué tienen en común la granularidad de un modelo estrella y el tercer reto de la minería?** — En los dos casos, el **nivel de detalle** decide qué preguntas se pueden responder. En BI, analizar tickets no permite analizar productos; en minería, con datos mensuales no se puede predecir por semana. **Cada vez que se agrega se pierde información**.

### 5.5 Autopreguntas

- ¿Qué es un nodo frontera y cuáles son los tres tipos?
- Dada una red, ¿podés armar C⁻, C⁺ y C sin mirar, con filas = transiciones?
- ¿Cuándo se escribe ω en el árbol y qué propiedad indica?
- ¿Cómo se pasa del árbol de alcanzabilidad a la máquina de testigos?
- ¿Por qué M' = M + f(σ)·C no alcanza para asegurar que una secuencia se puede disparar?
- ¿Cómo se reconoce en el grafo de marcados que una red es cíclica?
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

**Otras siglas y reglas para recordar**

| Sigla | Desarrollo | Original |
|---|---|---|
| TP | Trabajo Práctico | — |
| N° | Número | — |
| Lu-Tra-Ar-Ma | Elementos de una Red de Petri: Lugares, Transiciones, Arcos, Marcas | — |
| Mu-Du-W | Dónde se corta el árbol de alcanzabilidad: Muertos, Duplicados, con W | — |
| VACCa | Propiedades de comportamiento: Vivacidad, Acotamiento, Ciclicidad, Conservación, alcanzabilidad | — |
| Tan-In-Es | Beneficios de BI: Tangibles, Intangibles, Estratégicos | — |
| Re-Crí-Cuan-Co | Requisitos de un KPI: Reflejar objetivos, Críticos, Cuantificables, Correctivos | — |
| Le-Pre-In-E | Ideas del KDD: Lenguaje de alto nivel, Precisión, Interés, Eficiencia | — |
| MoCSA | Megatendencias del Big Data: Movilidad, Cloud, Social Media, Analytics | — |

---

## Cómo se armó

- **Material de la cátedra leído y cotejado** 📁 (carpeta *Análisis y Diseño de Sistemas II - 2026*): "Redes_de_petri" y "Formalización Redes de Petri" (presentaciones); "Introducción al BI", "BI_modelos", "Componentes de BI" y "experiencias BI_detalle" (libro *Business Intelligence: competir con información*); "NotasMD" (lectura de minería de Beatriz Beltrán Martínez, la misma que usó el grupo), "KDD-CRISP-SEMMA" (Azevedo y Santos) y "Data Mining: el arte de anticipar" (Palma y otros, 10 casos reales; no se volcó al resumen porque no aparece en los TP); "PowerData - Del bit… al Big Data".
- **Material del grupo**: TP6 a TP9 resueltos, guías de BI, caso CoffeeTime y su planilla, TP integrador de fútbol, apuntes de clase ("Redes Petri - Análisis y Diseño II", "Apuntes 14/9", "Ingeniería de datos") y el mapa conceptual de Big Data.
- **Verificado por computadora**: matrices, árboles de alcanzabilidad, máquinas de testigos, secuencias y propiedades de los tres ejemplos resueltos de Redes de Petri.
- **Recorte por alcance** (aclaración de la docente): se sacaron el TP6 de modelado (7 tareas y demás ejercicios), el caso CoffeeTime, el TP integrador de fútbol, la aplicación en comercio minorista y el caso de abandono de compra.
- **Cotejo con la cátedra**: se quitaron las marcas ⚠️ de la forma matricial de Petri, de los componentes de BI y de toda la unidad de Big Data. Se agregaron historia, subclases, máquina de testigos y métodos de análisis de Petri; calidad de datos, subprocesos de ETL, Inmon y Kimball, ODS y operaciones OLAP; el mapeo oficial de KDD, SEMMA y CRISP-DM; y detalles de la guía de PowerData.
- **Depuración (30/10)**: Big Data pasa al final. Se sacaron los ejemplos y casos puntuales (supermercado, paquetería, Wal-Mart, ROI del libro, K-means de empleados, Play Tennis, experiencias de BI) y los datos sueltos de estudios o encuestas (IDC, TDWI, Watson, Gartner 2005, hospitales). Se conservaron los ejemplos resueltos de Redes de Petri, porque esa práctica entra en el parcial.
- **Descartado**: del apunte de Redes de Petri, "una red viva es cíclica". Del cuadro del TP8, la correspondencia entre preprocesado y preparación de los datos (ver 3.13). De la lectura de BI, los desarrollos "Standard Query Language" y "Object Data Base Connector".
- **No disponible**: contenido de los videos de los temas 8 y 10.
