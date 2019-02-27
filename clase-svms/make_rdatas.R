

source( "mnist.R") 

# Prerrequisito para ejecutar la siguiente línea es haber descargado a la carpeta c:/_tmp
# los cuatro archivos .gz que están disponibles en en:
# http://yann.lecun.com/exdb/mnist/
  
df0 <- download_mnist( "c:/_tmp/", local = TRUE, verbose = TRUE )

df = df0[ df0$Label == 5 | df0$Label ==6 , ]
save( df, file = "df56.RData" )

df = df0[ df0$Label == 1 | df0$Label ==7 , ]
save( df, file = "df17.RData" )

