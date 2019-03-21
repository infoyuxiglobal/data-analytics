package org.apache.spark.ml  // this is a bit of hack but unfortunately necessary ( I think )  as the ml.tree.Node class doesn't expose some things that we are using...

import org.apache.spark.sql.{Datasetm, DataFrame}
import org.apache.spark.ml.classification.RandomForestClassificationModel
import org.apache.spark.ml.classification.DecisionTreeClassificationModel
import org.apache.spark.ml.tree.{InternalNode, LeafNode, Node, Split}
import org.apache.spark.ml.linalg.{Vector, DenseVector}


object ExplRFUtil {

  /*
   This following function takes a RandomForestClassificationModel 
   that has been trained on a **2-class** classification problem and 
   and Dataset as input, and adds a column named explanationCol"to it .

   On row i this column will contain a vector v_i of dimension f + 1 where 
    f is the dimension of the 'features' column in the dataset

   Each vector will contain a prediction explanation with the following properties. 
   
   1. \sum_{j=0}^{f} v_i(j) = p_i
    where p_i is the probability  predicted by the random forest that 
    instance i  belongs to the positive class.

   2. The last component of v, v_i(f) is tha a priori probability that
   instance i belongs to the positive class, without looking at any variables. 
   This is the same probability for all instances and it roughly corresponds 
   to the fraction of positive class samples in the training set. 

   3.  For j in in [0, f-1], v_i(j) corresponds to the contribution to the probability 
   p_i that is attributable to covariable (feature) X_j.  These constributions 
   can be either positive or negative.

   This contribution is camputed as the average, over all trees, of all probability 
   increments observed every time variable X_j is used in a tree bifurcation .
   Ver función ExplRFUtil.explanationForTree
   for more details.

  */

  def explanationForRF(model : RandomForestClassificationModel, dataset: Dataset[_],
                        explanationCol : String) : DataFrame = {

      val bcastModel = dataset.sparkSession.sparkContext.broadcast(model)
      val bcastErfu  = dataset.sparkSession.sparkContext.broadcast( new ExplRFUtil() )

      val explainUDF = udf { (features: Vector) =>
         bcastErfu.value.explanationForRF1( bcastModel.value, features)
      }

      dataset.withColumn( explanationCol, explainUDF( col(model.getFeaturesCol) )  )
  }

} // object ExplRFUtil

class ExplRFUtil {
  def getImpurityStats( n : Node ) = n.impurityStats

  def getPrediction( n: Node, v : Vector ) = {
    n match  {
        case in : InternalNode =>
              println( s"${in.getClass()}")
              in.predictImpl( v )
        case _ =>
              throw new IllegalArgumentException(s"class of n is ${n.getClass()}")
    }
  }

  def shouldGoLeft( split : Split, feats : Vector ) = split.shouldGoLeft( feats )

  def getFeatureIdx( split : Split ) = split.featureIndex

  def explanationForTree( tree : DecisionTreeClassificationModel,
                          feats : Vector ) : Vector = {

    val nfeats = feats.size

    val exp = Array.fill( feats.size + 1 )(0.0)
    
    var currNode = tree.rootNode
    var done = false
    var prevProb = getProbC1FromStats( currNode )
    exp( feats.size ) = prevProb

    while( !done ) {
        currNode = currNode match {
           case in : InternalNode =>
              // index j of the variable used in this split 
              val featIndex  = getFeatureIdx( in.split )

              val nextNode = if( shouldGoLeft( in.split, feats) ) {
                                 in.leftChild
                             } else {
                                 in.rightChild
                             }

              val currProb = getProbC1FromStats( nextNode )
              val probChange = currProb - prevProb
              // we increment this variable's explanation by probChange 
              exp( featIndex ) += probChange

              prevProb = currProb

              nextNode

           case ln : LeafNode =>
              done = true
              currNode // we return this just to satisfy type-constraints but it won't be used
        }
    }

    return new DenseVector( exp )
} // explanationForTree

def explanationForRF1( model : RandomForestClassificationModel, feats : Vector ) : Vector = {
    val numFeats1 = feats.size + 1
    val aggr = Array.fill[Double](numFeats1)(0.0)
    val nTrees = model.trees.size

    // just take average of explanations for each variable and over all trees
    model.trees.view.foreach { tree =>
        val expTree = explanationForTree( tree, feats )
        var i = 0
        while (i < numFeats1) {
          aggr(i) += expTree(i) / nTrees
          i += 1
        }
    }

    Vectors.dense(aggr)
}

def getProbC1FromStats( n : Node ) = {
    val arr = getImpurityStats( n ).stats
    val tot = arr.sum

    arr(1) / tot
} // class ExplRFUtil
