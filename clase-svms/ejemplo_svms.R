# Libro excelente y gratis de Aprendizaje estadístico:  
# Hastie et. al., Introduction to Statistical Learning
#   http://www-bcf.usc.edu/~gareth/ISL/

# Nuestra clase se basó fuertemente en el capítulo 9 de ese libro

# Videos y diapositivas del MOOC basado en l libro anteriors
# https://www.r-bloggers.com/in-depth-introduction-to-machine-learning-in-15-hours-of-expert-videos/

# Un tutorial chévere con explicación teórica del problema de optimización 
#     https://datascienceplus.com/understanding-linear-svm-with-r/

# Documentación del paquete e1071:
#     https://cran.r-project.org/web/packages/e1071/e1071.pdf
#
# Documentación del paquete LiblineaR
#     https://cran.r-project.org/web/packages/LiblineaR/LiblineaR.pdf


# install.packages("e1071") # quitar comentario y ejecutar si lo siguiente no funciona
library( e1071 )
# install.packages("LiblineaR") # quitar comentario y ejecutar si lo siguiente no funciona
# library( LiblineaR )

# IMPORTANTE: cambiar el siguiente directorio a la carpeta donde están los 
# archivos .RData y mnist.R
setwd( "C:/Users/Mateo/Desktop/Clase SVM" ) 
source( "mnist.R") 

load( "df56.RData") # También se puede cargar "df17.RData"

dim( df )

colnames( df )[0:10]
colnames( df )[ (ncol(df) -4): ncol(df) ]

n_pixels = ncol(df) - 1 

#px se refiere a pixel

#show_digit está definida en mnist.R
show_digit( df, 3 )    # un 6
show_digit( df, 1003 ) # otro 6 
show_digit( df, 7000 ) # y otro 6 
show_digit( df, 10002 ) # y otro..
show_digit( df, 10003 ) # y uno más
show_digit( df,  9567 ) # y uno más


show_digit( df, 10000 ) # un cinco
show_digit( df, 10001 ) # otro cinco
show_digit( df, 10004 ) # y otro 
show_digit( df, 10492 ) # y uno más
show_digit( df, 10656 ) # y uno más
show_digit( df, 10752 ) # y uno más


table( df$Label )  # Un factor con 10 categorías pero solo dos pobladas en los datos...

#Truquito para convertir el factor de 10 clases a solo dos clases
df$Label <- as.factor( as.numeric( as.character( df$Label ) )  ) 
table( df$Label )

# Separamos covariables de la variable etiqueta
X = df[ , 1:n_pixels ] / 255.0
X = scale( X, center = TRUE, scale = FALSE ) 
y = df$Label

# clases Negativa y Positiva
clsN =  which(df$Label == 5)
clsP =  which(df$Label == 6)

idx_train10 = c( clsN[1:1000], clsP[1:1000])
idx_test    = c( clsN[-c(1:5000)], clsP[-c(1:5000)])

### No ejecutar esta sección!

# Modelo de regressión logística (toma un rato...)
t_lr = system.time( { modelo_lr = glm( Label ~ . , 
                                       family=binomial(link='logit'),
                                       data = df[ idx_train10, ] ) 
                    } ) 
t_lr 

probs_train_lr = predict( modelo_lr, df[idx_train10,], type="response" )
preds_train_lr = as.numeric( probs_train_lr > 0.5 ) 

# Matriz de confusión sobre datos de entranamiento
table( df$Label[idx_train10], preds_train_lr  )

probs_test_lr = predict( modelo_lr, df[idx_test,], type="response" )
# Matriz de confusión sobre datos de test
preds_test_lr = as.numeric( probs_test_lr > 0.5 )

table( df$Label[idx_test], preds_test_lr)

VP = sum(  ( preds_test_lr == 1 ) & ( df$Label[idx_test] == 6 ) ) # Verdaderos positivos
VN = sum(  ( preds_test_lr == 0 ) & ( df$Label[idx_test] == 5 ) ) # Verdaderos negativos
exactitud_test_lr = 100 * ( VP + VN ) / length( idx_test )
error_test_lr = 100 - exactitud_test_lr
cat( sprintf( "Error de clasificación regresión logística : %.3f %%", error_test_lr ) ) 
     
### Fin de la sección

source("experimento_svm.R")

# Ejercicios:
#
# 1.) Ejecutar cada una de las llamadas a experimento_svm  que se muestran a continuación
#     Usar la combinación: Ctrl + Enter para más eficiencia
#
# 2.) Construir la tabla resumen con el comando que se muestra más abajo y visualizarla con 
#     el comando : View( resumen )
#     Al construir resumen Asegurese de listar todos los expX que haya calculado
#
# 3.) a) Qué combinación de parámetros da un menor error_test?
#     b) Intente cambiar algunos de los parámetros como cost o coef0 para obtener un menor valor de error
#     
# 4.) Con los comandos plot abajo explere la dependencia del tiempo de ajuste con el número 
#     de ejemplos (n_ejemplos)
#     a) Qué forma tiene la dependencia para el caso del kernel lineal?
#     b) Qué forma tiene la depenencia para el caso del kernel polynomial?


 
exp1  = experimento_svm( n_ejemplos = 1000, cost =    1  , kernel = "linear"  )   # 2.95% 
exp2  = experimento_svm( n_ejemplos = 1000, cost =   10  , kernel = "linear"  )   # 2.95%
exp3  = experimento_svm( n_ejemplos = 1000, cost =    0.1, kernel = "linear"  )   # ?? 
exp4a = experimento_svm( n_ejemplos = 1000, cost =   0.01, kernel = "linear"  )  # ??
exp4b = experimento_svm( n_ejemplos = 1000, cost =  0.001, kernel = "linear"  )  # ??

exp6a = experimento_svm( n_ejemplos = 1000, cost =   0.1, kernel = "linear"  )  # ??
exp6b = experimento_svm( n_ejemplos = 2000, cost =   0.1, kernel = "linear"  )  # ??
exp6c = experimento_svm( n_ejemplos = 3000, cost =   0.1, kernel = "linear"  )  # ??
exp6d = experimento_svm( n_ejemplos = 4000, cost =   0.1, kernel = "linear"  )  # ??
exp6e = experimento_svm( n_ejemplos = 5000, cost =   0.1, kernel = "linear"  )  # ??

exp5a = experimento_svm( n_ejemplos = 2000, cost =    1,  kernel = "linear"  )  # 2.63%
exp5b = experimento_svm( n_ejemplos = 2000, cost =  0.01, kernel = "linear"  )  # ???
exp7  = experimento_svm( n_ejemplos = 3000, cost =  10  , kernel = "linear"  )  # 2.63%

exp8a = experimento_svm( n_ejemplos = 1000, cost =  1, kernel = "polynomial"  )  #47.13%
exp8b = experimento_svm( n_ejemplos = 1000, cost =  1, kernel = "polynomial", coef0=1.0 ) # %
exp8b = experimento_svm( n_ejemplos = 3000, cost =  10, kernel = "polynomial", coef0=1.0 ) # %
exp8c = experimento_svm( n_ejemplos = 3000, cost =  100, kernel = "polynomial", coef0=1.0 ) # %

# Lo siguiente explora la dependencia del tiempo de ajuste con el número de ejemplos 
# para el kernel polynomial
exp9a = experimento_svm( n_ejemplos = 200, cost = 0.1, kernel = "polynomial", coef0=1.0 ) 
exp9b = experimento_svm( n_ejemplos = 500, cost = 0.1, kernel = "polynomial", coef0=1.0 ) 
exp9c = experimento_svm( n_ejemplos = 1000, cost = 0.1, kernel = "polynomial", coef0=1.0 ) 
exp9d = experimento_svm( n_ejemplos = 2000, cost = 0.1, kernel = "polynomial", coef0=1.0 ) 
exp9e = experimento_svm( n_ejemplos = 3000, cost = 0.1, kernel = "polynomial", coef0=1.0 ) 
exp9f = experimento_svm( n_ejemplos = 4000, cost = 0.1, kernel = "polynomial", coef0=1.0 ) 

exp10a = experimento_svm( n_ejemplos = 500,  cost = 10,   kernel = "radial", coef0=1.0 ) 
exp10d = experimento_svm( n_ejemplos = 500,  cost =  5,   kernel = "radial", coef0=1.0 ) 
exp10b = experimento_svm( n_ejemplos = 1000, cost =  1,   kernel = "radial", coef0=1.0 ) 
exp10c = experimento_svm( n_ejemplos = 1000, cost =  0.1, kernel = "radial", coef0=1.0 ) 


# RECUERDE: ajustar la lista de expX's para tener todos los experimentos 
resumen = rbind( exp1, exp2, exp3, exp4a, 
                 exp5a, exp5b, exp6a, exp6b, exp6c, exp6d, exp6e, exp7,  exp8a, exp8b,
                 exp9a, exp9b,exp9c, exp9d, exp9e, exp9f ) 
View( resumen )

t_vs_n_ejemplos_lin = resumen[ (resumen$kernel == "linear") & resumen$cost == 0.01 ,  ]

plot( t_vs_n_ejemplos_lin$n_ejemplos, t_vs_n_ejemplos_lin$t_ajuste )

t_vs_n_ejemplos_poly = resumen[ (resumen$kernel == "polynomial") & resumen$cost ==0.1 , ]

plot( t_vs_n_ejemplos_poly$n_ejemplos, t_vs_n_ejemplos_poly$t_ajuste )


