# Máquinas de soporte vectorial


**Nota**: Para visualizar correctamente las expresiones matemáticas 
 este documento recomendamos el siguiente procedimiento.:
 1. Descargue este archivo como texto plano (extensión `.md`) a sus disco duro.
 2. Descargue la extensión de Chrome llamada [markdown viewer](https://chrome.google.com/webstore/detail/markdown-viewer/ckkdlimhmcjmikdlpkmbgfkaikojcbjk?hl=en). 
 3. Luego de instalarla, abrir la versión descargada del documento y dar clic en el botón de configuración de markdown viewer a la derecha de la berra de dirección (Una 'm' minúscula encerrada en un círculo). Luego ir a la pestaña *Content* y asegurarse de que 
 *mathjax* esté activado. 
  

Las máquinas de soporte vectorial son un enfoque para resolver
el problema de clasificación de dos clases de una manera directa.

La idea clave es: 
   Tratar de encontrar un plano que separa las clases en el espacio 
   de covariables. 
   
Si esto no es posible (casi nunca lo es), 
hay dos ideas para lograr crear un clasificador (aproximado) 

  * Relajamos/ suavizamos la definición de lo que es "separar"
  
  * Enriquecemos el espacio de covariables de manera que sí sea 
posible hacer una separación


## ¿Qué es un hiperplano?


Un hiperplano en un espacio de $p$ dimensiones es un subespacio 
afin de dimensión $p - 1$. 

Un subespacio afin es parecido a un subespacio vectorial pero
no pasa por el origen necesariamente.

De hecho todo espacio afin es el resultado de tomar
un subespacio vectorial y trasladarlo (sumar un vector fijo a 
cada vector del mismo)

La ecuación general para un hyperplano es: 

$$b_0 + b_1 x_1 + b_2 x_2 + ... + b_p x_p = 0$$

En d=2 dimensiones el hyperplano es una línea 

 * Si $b_0 = 0$ el hiperplano contiene al origen  
(es un subespacio vectorial), sino no 
 * Al vector $b = (b_1, b_2, ..., b_p)$ se le llama 
el vector normal (apunta en dirección ortogonal 
al hiperplano) 

** Hacer dibujo de hiperplano en dos dimensiones. 

### Hiperplanos de separación: 

Si definimos $f_b(\mathbf{x}) := b_0 + b_1 x_1 + ... + b_p x_p$

Entonces $f_b(\mathbf{x}) > 0$ para puntos a un lado del hiperplano 
y $f(\mathbf{x}) < 0$ para puntos al otro lado

(**Notación**: En lo que sigue $\mathbf x = (x_1,...,x_p)$ denota cualquier 
punto del espacio $\mathbb R^p$ - note la negrilla cuando no se indica una componente. 
Por otro lado, $\mathbf x ^{(i)} = ( x_{i1}, x_{i2}, ..., x_{ip} )$ denota
una de las instancias de entrenamiento. El índice $i$ variará entre $1$, y $n$, el número total de instancias. 
Finalmente, $\langle \mathbf b, \mathbf x \rangle := b_1 x_1 + \cdots + b_p x_p $ denota el producto interior usual en $\mathbb R ^p$. ) 

Digamos que $y_i = +1$  si i es un ejemplo de la clase positiva
y $y_i = -1$ si i es un ejemplo de la clase negativa 

Observamos que  $y_i f_b(\mathbf{x}^{(i)})$ corresponde exactamente la distancia
(con signo) desde el punto $\mathbf{x}^{(i)}$ hasta el hiperplano. 
La distancia es positiva si el punto está correctamente clasificado 

Si encontramos un vector $b$ tal que 

$y_i \cdot f_b( \mathbf{x}^{(i)} ) > 0$  para todo i (es decir, que clasifique correctamente todos los puntos)
entonces decimos que $f_b(\mathbf{x}) = 0$ define un hiperplano de separación

Generalmente si existe un hiperplano de separación, entonces
hay infinitos.  

** Hacer dibujo!

### ¿Cuál escoger?

Un criterio natural  y que además se presta para encontrar 
un hiperplano de forma computacionalmente eficiente es el siguiente:

Escoger el hiperplano que maximiza la distancia al 
punto más cercano. 

Esta distancia se denomina el **margen**

Esto se puede formular como un problema de optimización 
de la siguiente manera:

$$     \max_{b_0,b_1, ...,b_p}   M  \\
\text{sujeto a} \sum_{j=1}^p b_j^2   = 1 \\ 
 y_i ( b_0 + b_1 x_{i1} + \cdots + b_p x_{ip} ) \geq M,  \text{ para todo } i 
   $$
   
Esto se puede transforma en un problema de optimización cuadrática y 
se puede resolver eficientemente.

 
### Problemas:
 
 
   1. Casi todos los problemas en el mundo real son NO SEPARABLES 
   ** Hacer dibujo.
    
   2.  Incluso si los datos reales son separables, puede haber ruido 
   **Hacer dibujo
   
   Esto hace que el clasificador de margen máximo sea
   poco chévere 

     * No va a ser robusto a la muestra que se haya tomado
     * No va a generalizar bien 
     * El margen podría ser demasiado pequeño, lo que 
   corresponden a poca confianza en la classificación 
   de algunos ejemplos. 
 
   
 ## Classificador de soporte vectorial


Un clasificador de soporte vectorial maximiza un margen *suave*

$$ \max_{ b, \varepsilon} M \\
\text{sujeto a} \sum b_i^2 = 1 \\
y_i ( b_0 + b_1 x_{i1} + ... + b_p x_{ip} ) \geq M( 1 -\varepsilon_i ) \\
\varepsilon_i \geq 0, \\
\sum_{i=1} ^n\varepsilon_i \leq C
   $$
 
Es decir, fijamos una constante C.
  
Los $\varepsilon_i$ son holguras (interpretadas como una fracción del margen)
 
Se puede poner $\varepsilon_i = 0$ si la distancia al punto i desde el hiperplano 
es al menos $M$

Si $\varepsilon_i \geq 0$ pero $\varepsilon_i < 1$ entonces el punto está al lado 
correcto del hiperplano pero viola el margen.

Si $\varepsilon_i > 1$ el punto queda incorrectamente clasificado por el hiperplano.
  
  * Algunos puntos podríaan estar  a distancia menos de M del 
 hiperplano b , incluso en el lado incorrecto... 
  * Pero la suma de las holguras **no puede sobrepasar C**, que
 es como el presupuesto total de holgura que nos permitimos.
  * C actua como un parámetro de regularización:
 
 A medida que se aumenta C, nos volvemos más tolerantes
 a violaciones del margen y el margen se puede aumentar.
 
 En la práctica, $C$ es un hiper-parámetro que se puede 
afinar con validación cruzada. 

$C$ pequeño => poca toleracia a violar el margen y el 
clasificador se ajusta apretadamente a los datos. 
(sesgo bajo, varianza alta)

$C$ grande => más holgura. Más observaciones violan el 
margen, menos ajuste a los datos de entrenamiento, mayor
sesgo, pero menor varianza...

Una propiedad importante del problema de optimización anterior
es la siguiente:

* Solo observaciones que estón justo en el margen ($\varepsilon  = 0$) 
o que violan el margen afectan el hiperplano y por lo tanto el 
clasificador que se obtiene.  Una observación que está estricatemente
más all del margen no afecta al clasificador de soporte vectorial.
Si se cambia esta observación, sin violar el margen, no se afecta en 
absoluto el clasificador. 

Los puntos que violan el margen o están sobre el margen se conocen como 
**vectores de soporte**.
De ahí el nombre del clasificador 

Una conclusión importante de lo anterior es que el 
clasificador es bastante robusto a observaciones que están
lejos del hiperplano. Esta propiedad es distinta de algunos
métodos de clasificación tradicionales como LDA

## Máquinas de soporte vectorial.

Incluso admitiendo violaciones del margen, 
en muchos casos una separador lineal simplemente no tiene sentido
para la distribución de las covariables de un problema.

** Dibujar un ejemplo.

### ¿Qué hacer?

* Expansión de covariables:

- Aumentar el espacio de características para incluir, 
por ejemplo, $x_1^2, x_1^3, ..., x_1x_2, x_1 x_2^2 ...$
Así pasamos de dimensión d a dimension d > p. 

- Ajustar el clasificador en el espacio aumentado.

- El resultado es una frontera de decisión no lineal en
el espacio original.


**Ejemplos:**

 Supongamos que usamos las 5 dimensiones 
$(x_1, x_2, x_1^2, x_2^2, x_1 x_2)$ en lugar  de solo $(x_1, x_2)$
entonces la frontera de decisión es cualquier curva 
que se pueda expresar como 
$b_0 + b_1 x_1 + b_2 x_2 + b_3 x_1^2 + b_4 x_2^2 + b_5 x_1 x_2  = 0$

**Ejemplo 1:** círculo

**Ejemplo 2:** función XOR continua 

Ejemplo: Polinomios de grado 3: 
Se pasa de 2 dimensiones a 9 

Uno podría seguir así: 

Pero los polinomios de dimensiones altas se salen rápidamente
de control.

Hay una manera más elegante y controlada de introducir 
no linealidad en los SVCs: usando kernels

Se puede mostrar que: 

1. La solución al problema de optimización cuadrática 
de arriba depende solamente de los productos interiores 
entre los diferentes $\mathbf{x}^{(i)}$'s es decir de los $n (n-1) / 2$ números
$\langle \mathbf{x}^{(i)}, \mathbf{x}^{(j)}\rangle $ con i != j.  

2. La función de clasificación también está dada por: 

$$f(\mathbf{x}) = b_0 + \sum_i \alpha_i \langle \mathbf{x},\mathbf{x}^{(i)} \rangle  $$

Por lo tanto, si se pueden calcular productos interiores entre
observaciones se puede ajustar un SVC y se puede evaluar la 
función de clasificación

Ejemplo: $p = 2$, 
$h : \mathbb R^2 -> \mathbb R^6$ está dada por 

$$h( x ) = ( 1, \sqrt 2 x_1, \sqrt 2  x_2, x_1^2 , x_2^2 ,\sqrt 2  x_1 x_2 ) \\
h( w ) = ( 1, \sqrt 2 w_1,\sqrt 2  w_2, w_1^2 , w_2^2 , \sqrt 2 w_1 w_2 )  \\

 \langle h(x), h(w) \rangle = 1 + x_1 w_1 + x_2 w_2 + x_1^2 w_1^2 + 
x_2 ^2 w_2^2 + 2 *x_1 w_1 x_2 w_2 \\
 = ( 1 + x_1w_1 + x_2w_2 )^2 $$

Es decir es fácil y eficiente de  calcular $\langle h(x), h(w) \rangle$
sin *necesidad* de calcular $h(x)$ o $h(w)$ antes!

### Kernel exponencial (potencia $k$)

Esta dado por
 
$$ K(x,w) = ( 1 + \langle x,w \rangle )^k$$

Este toma marginalmente un poco más de esfuerzo que calcular $\langle x,w \rangle$  pero equivale a 
mapear todo el problema a un espacio de dimensión ${ d + k \choose k } $


### Kernel radial:

$K( x, w ) = \exp( -\gamma  ||x-w||^2 )$

Es equivalente a mapear el problema a un espacio de infinitas
dimensiones, pero contrayendo la mayoría de estas dimensiones
bastante, lo que controla la varianza del clasificador
resultante.
 

## SVC vs. regresión logística:


Otra forma de formular el problema de optimización de un SVC
es:

$$\min_{b_0, ..., b_p }   \sum_{i=1}^n \max \{0, 1- y_i f_b(\mathbf{x}^{(i)})\} + \lambda \sum_{j=1}^p  b_j^2 $$
 
En esta formulación la norma de $b$ no está restringida de ningún modo.

Nótese que para una observación i, 

$$ma\{ 0, 1 - y_i f_b(\mathbf{x}^{(i)}) \}  > 0, \text{sii} $$
$1 - y_i f_b(\mathbf{x}^{(i)}) > 0$, sii
$1 > y_i f_b(\mathbf{x}^{(i)})$  es decir si la distancia al hiperplano definido por 
las $b$ es menor que 1, o se viola un margen de 1. 
 
Por lo tanto, la función objetivo tiene la forma: 
- pérdida (debido a ejemplos que violan el margen), más
- penalidad

La función de pérdida es muy similar a la "pérdida" que
se usa en regresión logística: el negativo del logaritmo de 
la verosimilitud.

Cuándo usar SVC vs. regresión logística: 

  * Cuando las clases son (aproximadamente) separables  SVC funcioname mejor que LR también LDA funciona mejor que LR 

  * Cuando no, entonces SVC y RL con penalidad "ridge" funcionan muy parecido!

  * Si se quieren estimar probabilidades entonces muy seguramente RL es lo que se quiere. 

  * Si se quieren estimar fronteras no lineales entonces se prefiere SVMs con Kernel.
     Es posible usar kernels con RL y LDA , pero los cálculos son más costosos.

