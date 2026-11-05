@gen
# Repaso del 2do parcial

Análisis y Diseño de Sistemas II · versión compacta de `resumen.md`, una idea por diapositiva.

**Cómo se usa:** flechas ← → o espacio para avanzar · **Esc** o **I** abre el índice · **T** cambia el tema.

---
@gen
## Qué entra

| Bloque | Qué entra |
|---|---|
| **Redes de Petri** (temas 6 y 7) | Teoría + **árbol de alcanzabilidad**, **propiedades** y **resolver una red con máquina de testigos y método matricial** |
| **Business Intelligence** (tema 8) | Solo teoría |
| **Minería de datos** (tema 9) | Solo teoría |
| **Big Data** (tema 10) | Solo teoría · **entra en el final** |

**No entra:** la práctica de los TP (CoffeeTime, TP integrador de fútbol, comercio minorista, abandono de compra, modelado del TP6).

---
@petri
# 1 · Redes de Petri

Temas 6 y 7 · teoría y práctica

---
@petri
## Qué es una Red de Petri

{{def:Red de Petri}}

- **Carl Adam Petri**, tesis de **1962** en Alemania: *Kommunikation mit Automaten* (comunicación entre componentes asíncronos).
- **1970**, **Holt y Commoner** ("Events and Conditions"): la aplican a sistemas concurrentes.
- Supera a las **máquinas de estado**, que no pueden modelar acciones simultáneas sin que exploten los estados.

---
@petri
## Elementos

| Elemento | Dibujo | Representa |
|---|---|---|
| **Lugar** | Círculo | Condición o estado |
| **Transición** | Barra | Evento |
| **Arco** | Flecha con peso (sin número = 1) | Une **lugar → transición** o **transición → lugar**, nunca dos del mismo tipo |
| **Marca** (*token*) | Punto en el lugar | La condición se cumple |

- Es un **multígrafo dirigido bipartito**. Truco: **Lu-Tra-Ar-Ma**.
- Representación **gráfica** y **matricial** son equivalentes.

---
@petri
## Definición formal

- **RdP = (P, T, I, O)**: P lugares y T transiciones (finitos, no vacíos y disjuntos), I incidencia previa, O incidencia posterior.

{{def:Marcado}}

- **Red marcada**: (RdP, M0).
- **Ordinaria**: todos los arcos pesan 1 · **Generalizada**: pesos enteros cualesquiera · **Pura**: ningún lugar es entrada y salida de la misma transición.

---
@petri
## Disparo de transiciones

{{def:Transición habilitada}}

- **Habilitada** si para cada lugar de entrada **M(p) ≥ I(p, t)**.
- **Nuevo marcado**: **M'(p) = M(p) − I(p, t) + O(t, p)**.
- **Fuente** (sin entradas): siempre habilitada · **Sumidero** (sin salidas): elimina marcas.
- Las marcas son **indivisibles**: disparar una transición puede deshabilitar a otra que compartía el lugar.
- Cuál de las habilitadas se dispara primero es **arbitrario**.

---
@petri
## Estructuras básicas

| Estructura | Cómo se ve |
|---|---|
| **Secuencial** | t2 solo después de t1 |
| **Selección** | Un lugar con dos o más transiciones de salida |
| **Atribución** | Dos transiciones que depositan en el mismo lugar |
| **Distribución** | Una transición con varios lugares de salida (se abre) |
| **Conjunción** | Una transición con varios lugares de entrada (se cierra) |
| **Sincronización** | Se habilita solo cuando **todas** las entradas tienen marca |
| **Concurrencia** | Dos habilitadas a la vez sin entradas compartidas |
| **Conflicto** | Dos habilitadas que comparten entrada: disparar una deshabilita a la otra |

---
@petri
## Propiedades (1): alcanzar, no trabarse, volver

{{def:Alcanzabilidad}}

{{def:Vivacidad}}

- **Parcialmente viva**: nunca se bloquea del todo, pero alguna transición deja de poder dispararse · **No viva**: llega a un **marcado muerto**.

---
@petri
## Propiedades (2): volver y tener tope

{{def:Ciclicidad}}

{{def:Acotamiento}}

---
@petri
## Propiedades (3): capacidad y recursos

{{def:Seguridad}}

{{def:Conservación}}

---
@petri
## Propiedades (4): competencia

{{def:Conflicto}}

{{def:Exclusión mutua}}

- **Estructurales** (no dependen de M0): pura, estructuralmente acotada, estructuralmente viva, completamente controlable, estructuralmente conservativa.

---
@petri
## Árbol de alcanzabilidad

{{def:Árbol de alcanzabilidad}}

- Desde M0, por cada transición habilitada se calcula el marcado nuevo, y se repite.
- Se corta en los **marcados frontera** (truco **Mu-Du-ω**):
  - **Muerto**: ninguna transición habilitada.
  - **Duplicado**: ya apareció en el árbol.
  - **Con ω**: cubre a un antecesor del mismo camino (igual o más en todos los lugares). ω = "crece sin límite" → **la red no es acotada**. ω + 1 = ω − 1 = ω.

---
@petri
## Máquina de testigos

{{def:Máquina de testigos}}

| | Árbol | Máquina de testigos |
|---|---|---|
| Estado | Vector completo (1,0,0,0,0) | Lugares marcados: **p1**; dos marcas = **p3 p3** |
| Repetidos | Se marcan como duplicados | Se juntan en un solo óvalo |
| Forma | Árbol | Grafo con ciclos |

---
@petri
## Método matricial

{{def:Matriz de incidencia}}

- **C⁻** (previa) = entradas · **C⁺** (posterior) = salidas · **C = C⁺ − C⁻** ("más menos menos").
- **Filas = transiciones, columnas = lugares.**
- tj habilitada si **M ≥ ej · C⁻** · al dispararla **M' = M + ej · C**.
- Secuencia σ: **M' = M + f(σ) · C**, con f(σ) = cuántas veces se dispara cada transición.
- La ecuación es condición **necesaria pero no suficiente**: no dice el **orden**; hay que comprobar cada habilitación.

---
@petri
## Receta para resolver una red

1. **Leer la red**: P, T, pesos, M0; escribir I(t) y O(t).
2. **Matrices** C⁻, C⁺ y C (filas = transiciones).
3. **Árbol de alcanzabilidad** numerando M1, M2… y cortando en muerto, duplicado o ω.
4. **Máquina de testigos**: juntar duplicados y dibujar el grafo.
5. **Método matricial**: verificar una secuencia con M' = M + f(σ)·C y cada habilitación.
6. **Propiedades**: leerlas del árbol y del grafo (siguiente diapositiva).

---
@petri
## Leer las propiedades en el árbol

| Propiedad | Cómo se ve |
|---|---|
| **Viva** | Sin muertos; desde todo estado se puede volver a disparar cada transición |
| **No viva** | Aparece un marcado muerto |
| **Acotada / segura** | No hay ω · k = máximo de marcas en un lugar · segura si k = 1 |
| **Cíclica** | Desde todos los estados del grafo se vuelve a M0 |
| **Conservativa** | La suma (o suma ponderada) de marcas es igual en todos |
| **Conflicto** | Lugar con 2+ salidas (estructural) y ambas habilitadas a la vez (efectivo) |
| **Exclusión mutua** | Dos lugares nunca marcados a la vez |

---
@petri
## Ejemplo resuelto (el de la lectura)

M0 = (1,0,0,0,0) · t1: p1 → p2, p3 · t2: p2 → p5 · t3: p3 → p4 · t4: p5 → p2 · t5: p4, p5 → p1

| C | p1 | p2 | p3 | p4 | p5 |
|---|---|---|---|---|---|
| t1 | −1 | 1 | 1 | 0 | 0 |
| t2 | 0 | −1 | 0 | 0 | 1 |
| t3 | 0 | 0 | −1 | 1 | 0 |
| t4 | 0 | 1 | 0 | 0 | −1 |
| t5 | 1 | 0 | 0 | −1 | −1 |

**5 marcados**, sin muertos y sin ω → **viva, segura, cíclica y pura**. σ = t1 t3 t2 t5 → f(σ) = (1 1 1 0 1) → **M' = M0**. Conflicto en p5 (t4 y t5); t2 y t3 concurrentes.

---
@petri
## Subclases

| Subclase | Regla | Puede / no puede |
|---|---|---|
| **Máquina de estados** (grafo de estados) | Cada **transición**: 1 entrada y 1 salida | Conflictos sí; **no** paralelismo ni sincronización |
| **Grafo marcado** | Cada **lugar**: 1 entrada y 1 salida | Paralelismo y sincronización sí; **no** conflictos |
| **Red de libre elección** | Si un lugar es entrada de varias transiciones, es su **única** entrada | Concurrencia y conflicto restringidos |
| **Red simple** | Cada transición tiene como máximo **un** lugar de entrada compartido | — |

---
@petri
## Modelos clásicos

- **Exclusión mutua (semáforo)**: un lugar "recurso libre" con 1 marca; sin prioridades.
- **Productor–consumidor**: un *buffer* entre los dos; con capacidad finita, "llenos" + "vacíos" **siempre suman la capacidad**.
- **Lectores–escritores**: semáforo con **m marcas**; leer toma 1, escribir toma las m.
- **Cinco filósofos**: si todos toman el mismo tenedor, **estancamiento**; solución: tomar los dos tenedores a la vez o limitar con "sillas" (4 marcas).

**Ventajas**: gráficas, modelan concurrencia y recursos compartidos, *top-down* o *bottom-up*. **Desventajas**: **no modelan prioridades**, se complican con sistemas grandes.

---
@petri
## Errores frecuentes de Petri

- ❌ "Una red viva siempre es cíclica." ✅ Son **independientes**.
- ❌ "Segura = no se bloquea." ✅ Segura = **1-acotada**; no bloquearse es **vivacidad**.
- ❌ "C = C⁻ − C⁺." ✅ **C = C⁺ − C⁻**.
- ❌ "Filas = lugares." ✅ **Filas = transiciones**.
- ❌ "Si M' = M + f(σ)·C tiene solución, σ se puede disparar." ✅ Es **necesaria, no suficiente**.
- ❌ Seguir expandiendo un duplicado, o escribir una sola vez un lugar con dos marcas en la máquina de testigos.

---
@bi
# 2 · Business Intelligence

Tema 8 · solo teoría

---
@bi
## Qué es BI

{{def:Business Intelligence}}

- Término popularizado por **Howard Dresner** (Gartner).
- Idea central: **datos → información → conocimiento**.
- Partes de la definición (truco **Pi-E-A-Info-Á-Co**): **p**roceso **i**nteractivo, **e**xplorar, **a**nalizar, **info**rmación estructurada, **á**rea, **co**municar y cambiar.

---
@bi
## Para qué sirve y quién lo necesita

| Beneficio (truco **Tan-In-Es**) | Ejemplos |
|---|---|
| **Tangibles** | Segmentar clientes, reducir abandono, cesta de la compra, detectar fraude, "una sola versión de la verdad" |
| **Intangibles** | Mejor atención, información más actual y precisa, ventaja competitiva |
| **Estratégicos** | A qué clientes, mercados o productos apuntar |

- Lo necesita **todo el que decide** (decisiones operativas o estratégicas).
- Hospitales de EE. UU.: **80 %** del tiempo preparando datos, **20 %** analizando. IDC: solo el **15 %** de los directivos confía en sus informes.

---
@bi
## Componentes

**De un proyecto (6):** problema de negocio · equipo · información interna · información externa · *datawarehouse* · aplicación de BI.

**Cadena técnica:** fuentes → **ETL** → ***datawarehouse*** (+ metadata) → **OLAP** → herramientas de visualización.

- En un proyecto real primero se definen **objetivos, alcance y modelo de negocio**.
- Herramientas fundamentales (6): consultas e informes, cubos OLAP, minería de datos, tableros de control, alertas y notificaciones, modelado y predicción.

---
@bi
## Retorno de la inversión (ROI)

- **Simple**: valor para el negocio / costo del proyecto.
- **Completo**: **ROI = NPV / inversión inicial × 100** (NPV = valor actual neto de los flujos de caja).
- **TCO** (costo total de propiedad): *hardware*, *software*, consultoría, personal, mantenimiento, formación.
- **Ejemplo del libro**: inversión 40.000 €, mantenimiento 15.000 €/año, tasa 15 % → **NPV 87.656 €, ROI 219 %**.
- **IDC 1996**: ROI medio a 3 años **401 %**, *payback* **2,3 años**.

---
@bi
## Modelo de negocio y KPI

{{def:Modelo de negocio}}

{{def:KPI}}

- Un KPI tiene que (truco **Re-Crí-Cuan-Co**): **re**flejar objetivos, ser **crí**tico, **cuan**tificable y comparable, y permitir acciones **co**rrectivas.
- Ejemplo: repetición de ventas a clientes, mejorar **3 % por trimestre** desde el 48 %.

---
@bi
## Modelo de datos

- **Hechos**: lo que se mide (importe del ticket) · **Dimensiones**: el contexto (¿qué? ¿quién? ¿por qué? ¿dónde? ¿cuándo?).
- **Dimensión degenerada**: no tiene tabla propia (número de ticket, caja).
- **Dimensión tiempo**: día, mes, trimestre, feriados… no están en el transaccional: se agregan.

| | Estrella | Copo de nieve |
|---|---|---|
| Dimensiones | Una tabla por dimensión, **desnormalizada** | **Normalizadas**, en varias tablas |
| A favor | Simple y rápida | Menos redundancia y espacio |

---
@bi
## Granularidad y jerarquías

{{def:Granularidad}}

- **Jerarquías**: año → trimestre → mes → día · familia → subfamilia → artículo · zona → centro. Permiten agregar y desagregar.
- **Multidimensionalidad**: analizar por varias dimensiones a la vez (ventas de un artículo por centro y por mes).
- Cada vez que se **agrega**, se **pierde información**: conviene guardar al máximo detalle.

---
@bi
## Calidad de datos

- Datos de calidad (7): precisión, integridad, coherencia, totalidad, validez, disponibilidad, accesibilidad. Conviene **corregir en el origen**.
- Los errores en el *datawarehouse* se **propagan a toda la organización**: es un problema de negocio, no solo técnico.

---
@bi
## Proceso ETL

{{def:ETL}}

| Subproceso | Qué hace |
|---|---|
| 1. Extracción | Saca los datos en bruto de las fuentes |
| 2. Limpieza | Duplicados, errores, vacíos |
| 3. Transformación | Formatos, códigos, agregados; fija la granularidad |
| 4. Integración | Valida y carga en el *datawarehouse* |
| 5. Actualización | Define cada cuánto se carga |

---
@bi
## Datawarehouse

{{def:Datawarehouse}}

- **Inmon**: orientado a un área, integrado, indexado en el tiempo, **no volátil**.
- **Estrategias**: Inmon, *datawarehouse* corporativo primero (de arriba hacia abajo) · Kimball, Data Marts por área (más barato, riesgo de silos).

---
@bi
## Data Mart y ODS

{{def:Data Mart}}

- **Dependiente**: se alimenta del *datawarehouse* corporativo · **Independiente**: directo de las fuentes (puede mantener silos).

{{def:ODS}}

---
@bi
## OLAP y metadata

{{def:OLAP}}

- **FASMI**: *Fast Analysis of Shared Multidimensional Information*.
- Operaciones: **rotar**, **seleccionar**, **agregar** (*roll-up*), **bajar al detalle** (*drill-down*).
- Tipos: **ROLAP** (relacional, sin límite, más lento) · **MOLAP** (multidimensional, muy rápido) · **HOLAP** (híbrido) · **DOLAP** (escritorio).

{{def:Metadata}}

---
@bi
## Errores frecuentes de BI

- ❌ "BI se hace una vez." ✅ Es un **proceso continuo**.
- ❌ "La estrella está normalizada." ✅ La estrella es **desnormalizada**; el copo de nieve, normalizado.
- ❌ "Más granularidad = menos detalle." ✅ **Más granularidad = más detalle**.
- ❌ "Un Data Mart es más grande que el *datawarehouse*." ✅ Es **más chico**.
- ❌ "El ODS guarda historia." ✅ El ODS es **volátil**; el *datawarehouse* es histórico.

---
@dm
# 3 · Minería de datos

Tema 9 · solo teoría

---
@dm
## Minería de datos y KDD

{{def:Minería de datos}}

{{def:KDD}}

- Datos = registros · Información = utilidad de los datos · Conocimiento = reglas de cómo una cosa afecta a otra.
- Analogía: una **montaña** de datos con **diamantes** escondidos.

---
@dm
## Las 4 ideas del KDD

Truco **Le-Pre-In-E**:

| Idea | Qué exige |
|---|---|
| **Lenguaje de alto nivel** | Conocimiento **entendible por una persona** (por eso las redes neuronales, "caja negra", quedan afuera) |
| **Precisión** | Medir el grado de certidumbre; si es bajo, no es conocimiento |
| **Interés** | Nuevo, útil y no trivial para el usuario |
| **Eficiencia** | Tiempo y memoria que crecen de forma **polinomial** |

---
@dm
## Etapas del KDD según cada fuente

- **Fayyad (5)**: selección → preprocesamiento → transformación → minería → interpretación/evaluación.
- **Resumen de cátedra (7)**: recolección, selección, preprocesamiento, transformación, minería, interpretación y evaluación, actualización y monitorización.
- **Lectura, 9 pasos**: comprensión del dominio · conjunto de datos objetivo · preprocesado · **transformación y reducción (paso crítico)** · tipo de sistema · algoritmo · minería · interpretación · consolidación.
- **Lectura, 6 fases**: recolección · selección, limpieza y transformación · minería · evaluación y validación · interpretación y difusión · actualización y monitorización.

En el examen, **aclarar qué versión se usa**.

---
@dm
## CRISP-DM y SEMMA

{{def:CRISP-DM}}

{{def:SEMMA}}

---
@dm
## Equivalencia KDD, SEMMA y CRISP-DM

Según el artículo de la cátedra (Azevedo y Santos): SEMMA y CRISP-DM son **implementaciones del proceso KDD**.

| KDD | SEMMA | CRISP-DM |
|---|---|---|
| (comprensión del dominio) | — | Comprensión del negocio |
| Selección / preprocesamiento | *Sample* / *Explore* | Comprensión de los datos |
| Transformación | *Modify* | Preparación de los datos |
| Minería | *Model* | Modelado |
| Interpretación / evaluación | *Assess* | Evaluación |
| (consolidación) | — | Implantación |

---
@dm
## Datos atípicos y faltantes

| Acción | Atípicos | Faltantes |
|---|---|---|
| Ignorar | Algoritmos robustos (árboles) | Algoritmos robustos |
| Filtrar la fila | **Sesga** los datos | **Sesga** los datos |
| Reemplazar | Nulo, máximo, mínimo, media o predecirlo | Media o predecirlo (la media **reduce la varianza**) |
| Discretizar / segmentar | Discretizar: cae en un extremo | Segmentar: un modelo por grupo |

Los faltantes pueden ser **relevantes** (no dio el teléfono), **no existentes** (cliente nuevo) o **incompletos** (al unir fuentes).

---
@dm
## Qué no es la minería y sus retos

| | Minería | Otro |
|---|---|---|
| **Estadística** | Automática, exploratoria, muchas variables, toda la base | Confirmatoria (prueba hipótesis), muestras |
| **OLAP** | **Genera** información nueva | **Navega** datos agregados |
| **Monitoreo** | Datos **estáticos**, descubre | Datos en **tiempo real**, reconoce |

**Retos:** falsa interpretación · **correlación no es causalidad** (Florida: viven más porque allí se jubilan los mayores) · tiempo, espacio y **privacidad**.

---
@dm
## Tareas y modelos

| Tarea | Tipo |
|---|---|
| **Clasificación** (clases predefinidas) | Predictiva / supervisada |
| **Regresión** (valor continuo) | Predictiva / supervisada |
| **Agrupamiento** (*clustering*) | Descriptiva / no supervisada |
| **Condensación**, **detección de desviaciones**, **modelado de dependencias** | Descriptivas / no supervisadas |

- **Predictivo**: entrenamiento + prueba (árbol "*Play Tennis*") · **Descriptivo**: descubre grupos (**K-means**).
- Proceso de minería (4): preprocesado → selección de características → algoritmo → evaluación.

---
@dm
## Técnicas

- **Estadísticas**: ANOVA, Ji cuadrado, componentes principales, *clusters*, discriminante, regresión lineal y logística.
- **Árboles de decisión**: **CART** parte en 2 (Gini) · **CHAID** en más de 2 (Ji cuadrado).
- **Reglas de asociación** (cesta de la compra): **soporte** = casos donde se aplica · **confianza** = casos con antecedente y consecuente / casos con antecedente. Algoritmo **Apriori**.
- **Redes neuronales** (caja negra) · **algoritmos genéticos** (optimizar, elegir variables) · **lógica difusa** · **series temporales** · **redes bayesianas**.
- ***Boosting***: mismo algoritmo, distintas particiones · ***Voting***: distintos algoritmos.

---
@dm
## Evaluación y evolución

- Tres medidas clave: **precisión**, **explicación** (que se entienda) e **integración** (con el negocio).
- **Elevación** (*lift*): respuesta con el modelo / respuesta al azar → 30 % / 10 % = **3**. La mejor medida: **beneficio / ROI**.

| Etapa | Característica |
|---|---|
| Recolección (60) | Retrospectiva, estática |
| Acceso a datos (80, SQL) | Retrospectiva, dinámica por registro |
| *Datawarehouse* y OLAP (90) | Retrospectiva, varios niveles |
| **Minería de datos** | **Prospectiva y proactiva** |

---
@dm
## Errores frecuentes de minería

- ❌ "KDD y minería son lo mismo." ✅ La minería es **una etapa** del KDD.
- ❌ "OLAP descubre patrones." ✅ OLAP **navega**; la minería **descubre**.
- ❌ "Correlación implica causalidad." ✅ No (Florida).
- ❌ "Filtrar filas con faltantes no cuesta nada." ✅ **Sesga** los datos.
- ❌ "La regresión es descriptiva." ✅ Es **predictiva**.
- ❌ "SEMMA incluye la comprensión del negocio." ✅ La **supone resuelta**; CRISP-DM es la más orientada al negocio.

---
@bd
# 4 · Big Data

Tema 10 · solo teoría · **entra en el final**

---
@bd
## Big Data

{{def:Big Data}}

- **3 V**: volumen, velocidad, variedad. "Big" no es la clave: importa **qué va a pasar** y en tiempo real.
- **Metodología MAD**: **M**agnética (capta todo tipo de datos), **Á**gil (se adapta rápido), **D**etallada (análisis fino).
- **Megatendencias** (truco **MoCSA**): Movilidad, Cloud, Social Media, Analytics.

---
@bd
## Hadoop y tiempo real

{{def:Hadoop}}

- Nace de **Google** ("divide y vencerás"); código abierto desde **2006**; lo impulsa Yahoo y lo adopta Facebook.
- **HDFS** guarda los archivos repartidos · **MapReduce** procesa en paralelo · corre en ***commodity hardware***.
- **Tiempo real**: **Data Stream** analiza datos en movimiento · **CEP** detecta eventos predefinidos (fraude con tarjetas).

---
@bd
## BI, minería y Big Data

| | BI | Minería | Big Data |
|---|---|---|---|
| Pregunta | ¿Qué pasó? | ¿Qué patrones hay? | ¿Qué va a pasar? |
| Tiempo | Pasado y presente | Pasado para predecir | Presente continuo |
| Datos | Estructurados, depurados | Consolidados | Crudos, también no estructurados |
| Perfil | Analista de BI | Científico de datos | Ingeniero de datos |

- **No se excluyen**: Big Data captura → la minería descubre → BI decide. El **ADW** convive con el *datawarehouse* (modelo híbrido).

---
@rep
# 5 · Repaso final

---
@rep
## Datos para memorizar

| Dato | Valor |
|---|---|
| Petri | Carl Adam Petri, **1962** · Holt y Commoner **1970** |
| Subclases de RdP | **4** |
| BI | Howard Dresner (Gartner) |
| Componentes de un proyecto de BI | **6** |
| ETL | **60–80 %** del tiempo · **5** subprocesos |
| Modelo relacional | E. F. Codd, **1970** |
| KDD | desde **1989** · Fayyad **5** etapas |
| CRISP-DM / SEMMA | **6** fases / **5** fases |
| Tareas de la minería | **6** |
| Hadoop | HDFS + MapReduce · **2006** |

---
@rep
## Trucos para memorizar

| Truco | Qué recuerda |
|---|---|
| **Lu-Tra-Ar-Ma** | Lugares, transiciones, arcos, marcas |
| **Mu-Du-ω** | Dónde se corta el árbol |
| **Más menos menos** | C = C⁺ − C⁻ · M' = M − I + O |
| **Pi-E-A-Info-Á-Co** | Definición de BI de Gartner |
| **Tan-In-Es** | Beneficios de BI |
| **Re-Crí-Cuan-Co** | Requisitos de un KPI |
| **Le-Pre-In-E** | Las 4 ideas del KDD |
| **MAD** · **MoCSA** | Metodología de Big Data · megatendencias |

---
@rep
## Autopreguntas

Tocá cada pregunta para ver la respuesta.

<details><summary>¿Cuáles son los tres tipos de marcado frontera?</summary>Muerto, duplicado y con ω.</details>
<details><summary>¿Qué indica una ω en el árbol?</summary>Que la red no es acotada.</details>
<details><summary>¿Por qué M' = M + f(σ)·C no alcanza?</summary>Porque no dice el orden de los disparos: es necesaria pero no suficiente.</details>
<details><summary>¿Qué diferencia hay entre Data Mart y ODS?</summary>El Data Mart es un datawarehouse chico para un grupo de usuarios; el ODS es operativo, volátil y en tiempo real.</details>
<details><summary>¿Cuál es el paso crítico del KDD?</summary>Transformación y reducción (lectura, 9 pasos).</details>
<details><summary>¿Cómo se calcula la elevación?</summary>Respuesta con el modelo / respuesta al azar (30 % / 10 % = 3).</details>
<details><summary>¿Qué diferencia hay entre Data Stream y CEP?</summary>Data Stream analiza datos en movimiento; CEP detecta eventos predefinidos.</details>
