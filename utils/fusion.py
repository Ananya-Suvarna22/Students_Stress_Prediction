def hybrid_fusion(ml_prediction, cnn_prediction):

    final_score = (
        0.6 * ml_prediction
        +
        0.4 * cnn_prediction
    )

    if final_score < 0.8:

        stress = "Low"

    elif final_score < 1.5:

        stress = "Medium"

    else:

        stress = "High"

    return stress