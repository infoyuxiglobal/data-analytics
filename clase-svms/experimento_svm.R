

experimento_svm <- function( n_ejemplos, cost, kernel,  coef0 = 0.0 ) {
  
  if ( n_ejemplos > 5000 ) {
    message( "Error: n_ejemplos no puede ser mayor que 5000 !")
    return(NULL)
  }
  
  n_sobre_2 = as.integer( n_ejemplos / 2 )
  # Datos de entrenamiento: matrix de covariables y respuesta
  idx_train = c( clsN[1:n_sobre_2], clsP[1:n_sobre_2])
  X_train = X[idx_train, ]
  y_train = y[idx_train ]
  
  # Datos de test:
  idx_test    = c( clsN[-c(1:5000)], clsP[-c(1:5000)] )
  X_test  = X[idx_test, ]
  y_test  = y[idx_test ]
  # hacemos un ajuste de un SVM mediante 
  # svm, una función en el paquete e1071
  cat(sprintf("\n Ajustando svm con %d ejemplos, cost = %.3f, kernel = %s,  coef0=%g\n",
              length(idx_train), cost, kernel, coef0 ) )
  
  t_ajuste = system.time( { modelo = svm( x = X_train, y = y_train,
                                          scale = FALSE,
                                          cost = cost,   # constante C : "presupuesto para errores"
                                          coef0 = coef0, # necesario para kernel polynomial
                                          kernel = kernel ) } )
  
  cat(sprintf("\n Ajuste tardó: %.3f segundos\n", t_ajuste["elapsed"] ) )
  
  # predicciones sobre los datos de entranamiento
  preds_train = predict( modelo, X_train )
  
  cat( "\nMatriz de confusión para datos de entrenamiento:\n\n") 
  show( table( preds_train, y_train ) ) 
  
  # predicciones sobre los datos de test 
  preds_test = predict( modelo, X_test )
  
  cat( "\nMatriz de confusión para datos de test:\n\n") 
  show( table( preds_test, y_test  ) ) 
  
  
  # Ejemplos de falsos positivos y falsos negativos
  ejemplos_FP = idx_test[ (as.numeric(preds_test) == 2) & (as.numeric(y_test) ==1) ][1:5]
  ejemplos_FN = idx_test[ (as.numeric(preds_test) == 1) & (as.numeric(y_test) ==2) ][1:5]
  
  cat(   "\nEjemplos de falsos positivos: \n", format(ejemplos_FP) )
  cat( "\n\nEjemplos de falsos negativos: \n", format(ejemplos_FN) )
  
  exactitud_test = 100 * sum(y_test == preds_test) / length( y_test )
  error_test = 100 - exactitud_test 
  
  
  cat( sprintf("\n\nExactitud (accuracy): %.2f%%\n", exactitud_test) )
  
  cat(sprintf( paste( "\nkernel=%s, n_ejemplos = %d, cost = %.3f, coef0=%g\n ", 
                      "    => Error: %.2f %% (tiempo de ajuste:%.3f s )"),
              kernel, length(idx_train), cost, coef0, error_test, t_ajuste["elapsed"] ) )
  
  ret = data.frame( kernel = kernel, 
                      n_ejemplos = n_ejemplos,
                      cost = cost,
                      error_test = error_test, 
                      t_ajuste = t_ajuste["elapsed"] ) 

  rownames( ret ) <- c("")
  return( ret )
} 
