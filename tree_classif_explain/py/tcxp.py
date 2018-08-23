# -*- coding: utf-8 -*-
"""
Created on Fri May  4 14:05:25 2018

@author: mrestrepo
@company: Yuxi Global (www.yuxiglobal.com)


TODO:
    - Extension multi-class classifiers
    - Extension to Boosted Tree models

"""
import numpy as np

def rf_explain( rfc, X ) :
    """
    Arguments :
        - rfc - a sklearn.ensemble.RandomForest already trained on a
                binary classification task.
        - X   - a data-frame  of features shape (N, p)
            all features must be numeric (p features)

    Returns (p0, E)
        - p0 : float - the a prioriy
        - E : np.array of shape (N, p) containing the explanations
    """

    assert_impl_limitations( rfc  )
    X = ensure_np_array_32( X )

    n = X.shape[0]
    explanations = np.zeros( ( n, rfc.n_features_ ) )

    p0_sum = 0.0
    for cls in rfc.estimators_ :
        E, p0 = tree_explain( cls, X )
        explanations[:] += E
        p0_sum  += p0


    n_est = len(rfc.estimators_)
    #%%
    return (explanations / n_est), (p0_sum / n_est)

def tree_explain( cls, X ) :
    """
    Arguments :
        - cls - a sklearn.tree.tree.DecisionTreeClassifier already trained
            on a binary classification task
        - X   - a data-frame or np.array of features shape (N, p)
        all features must be numeric (p features)

    Returns (p0, E)
        - p0 : float - the a prioriy
        - E : np.array of shape (N, p) containing case-by-case
        explanations
        -
    """

    assert_impl_limitations( cls )
    Xa = ensure_np_array_32( X )
    n = Xa.shape[0] # number of cases for evaluation

    #%% Compute constant  probability of class 1 for every node
    tree = cls.tree_
    node_probs_c1 =  (tree.value[:,0, 1]) / ( tree.value[:,0,:].sum(axis=1))


    explanations = np.zeros( ( n, cls.n_features_) )
    #explanations[:, cls.n_features_] = a_priori_prob

    dp = tree.decision_path( Xa )
    feature = tree.feature

    # the following loop should  be implemented in cython for efficiency!

    for i in range(n) :  # run over evaluation cases

        #path_len = len( path )
        prev_feat = feature[0]
        prev_prob = node_probs_c1[0]
        path = dp[i,:].indices  # indices of nodes in this case's path

        for j in path[ 1: ] :

            cur_prob = node_probs_c1[ j ]

            delta_p = cur_prob - prev_prob
            explanations[i, prev_feat ] += delta_p

            prev_prob = cur_prob
            prev_feat = feature[j]

    a_priori_prob = node_probs_c1[0]
    #%%
    return explanations, a_priori_prob
    #%%

def as_pyplot_figure( exp0, p0, feat_names, feat_vals, instance_desc,
                      limit=20, # only show first these many variables
                      color_theme=('green', 'red') ) :
    """Following lime.explanation.Explanation.as_pyplot_figure, almost verbatim"""
    import matplotlib.pyplot as plt

    exp_vals = list( exp0[:limit] )
    exp_vals.reverse()
    
    labels = [ "%s : %s" % (n,v) for n,v in zip(feat_names[:limit], feat_vals[:limit]) ]
    labels.reverse()
    
    colors = [ color_theme[0] if x > 0 else color_theme[1] for x in exp_vals]
    pos = np.arange(len(exp_vals)) + .5
        
    fig = plt.figure( dpi=300 )
    
    plt.barh(pos, exp_vals, align='center', color=colors)
    plt.yticks(pos, labels)
    plt.xlabel('Contribution to probability of positive class')

    prob =  p0 + exp0.sum() 
    title = 'Explanation for %s (Predicted prob.=%.3f)' % (instance_desc, prob )

    plt.title(title)
    return fig

def assert_impl_limitations( cls )  :
    #%%
    assert cls.n_classes_ == 2, ( "Explanation method implemented for binary "
            "classifiers only. However, generalization to any number of classes"
            " is pretty straigh forward! Please contribute!" )

    assert cls.n_outputs_ == 1, ("Explanation method implemented for single "
                                 "output classifiers only" )
    #%%

def ensure_np_array_32( X ) :

    if type(X) != np.ndarray :
        X = X.values

    if X.dtype != np.float32 :
        X = X.astype( np.float32 )

    return X

