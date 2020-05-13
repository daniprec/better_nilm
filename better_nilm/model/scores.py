import numpy as np

from sklearn.metrics import mean_squared_error

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score


def _assert_shape(y_pred, y_real, appliances):
    if not y_pred.shape == y_real.shape:
        raise ValueError("Array shape mismatch.\n"
                         f"y_pred shape: {y_pred.shape}\n"
                         f"y_real_shape: {y_real.shape}")

    if y_pred.shape[2] != len(appliances):
        raise ValueError("Number of appliances mismatch.\n"
                         f"Appliances in y_pred array: {y_pred.shape[2]}\n"
                         f"Appliances in appliances list: {len(appliances)}")


def regression_score_dict(y_pred, y_real, appliances):
    """
    Returns a dictionary with some regression scores, for each appliance.
        - RMSE, Root Mean Squared Error

    Parameters
    ----------
    y_pred : numpy.array
        shape = (num_series, series_len, num_appliances)
        - num_series : Amount of time series.
        - series_len : Length of each time series.
        - num_appliances : Meters contained in the array.
    y_real : numpy.array
        shape = (num_series, series_len, num_appliances)
    appliances : list
        len = num_appliances
        Must be sorted following the order of both y_pred and y_real

    Returns
    -------
    scores : dict
        'appliance': {'metric': value}

    """
    _assert_shape(y_pred, y_real, appliances)

    if np.mean(y_real) <= 1:
        print("Warning!\nThe predicted values appear to be normalized.\n"
              "It is recommended to use the de-normalized values\n"
              "when computing the regression errors")

    # Initialize dict
    scores = {}

    for idx, app in enumerate(appliances):
        app_pred = y_pred[:, :, idx].flatten()
        app_real = y_real[:, :, idx].flatten()

        # RMSE
        app_rmse = mean_squared_error(app_real, app_pred)

        scores[app] = {"rmse": round(app_rmse, 2)}

    return scores


def classification_scores_dict(y_pred, y_real, appliances, threshold=.5):
    """
    Returns a dictionary with some regression scores, for each appliance.
        -

    Parameters
    ----------
    y_pred : numpy.array
        shape = (num_series, series_len, num_appliances)
        - num_series : Amount of time series.
        - series_len : Length of each time series.
        - num_appliances : Meters contained in the array.
    y_real : numpy.array
        shape = (num_series, series_len, num_appliances)
    appliances : list
        len = num_appliances
        Must be sorted following the order of both y_pred and y_real
    threshold : float, default=0.5
        Minimum value (form 0 to 1) at which we consider the appliance to be ON

    Returns
    -------
    scores : dict
        'appliance': {'metric': value}

    """

    _assert_shape(y_pred, y_real, appliances)

    if ((y_pred.max() > 1).any() or (y_real > 1).any()
            or (y_pred.min() < 0).any() or (y_real.min() < 0).any()):
        raise ValueError("Classification values must be between 0 and 1.")

    # Binarize the arrays
    bin_pred = np.zeros(y_pred.shape)
    bin_pred[y_pred >= threshold] = 1
    bin_pred = bin_pred.astype(int)

    bin_real = np.zeros(y_real.shape)
    bin_real[y_real >= threshold] = 1
    bin_real = bin_real.astype(int)

    # Initialize dict
    scores = {}

    for idx, app in enumerate(appliances):
        app_pred = bin_pred[:, :, idx].flatten()
        app_real = bin_real[:, :, idx].flatten()

        # Precision
        app_accuracy = accuracy_score(app_real, app_pred)

        # F1-Score
        app_f1 = f1_score(app_real, app_pred)

        # Precision
        app_precision = precision_score(app_real, app_pred)

        # Recall
        app_recall = recall_score(app_real, app_pred)

        scores[app] = {"accuracy": round(app_accuracy, 4),
                       "f1": round(app_f1, 4),
                       "precision": round(app_precision, 4),
                       "recall": round(app_recall, 4)}

    return scores
