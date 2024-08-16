from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.keras.preprocessing.sequence import TimeseriesGenerator


def time_series_rnn(
    df: pd.DataFrame,
    column_name: str,
    test_size: float = 0.2,
    num_epochs: int = 10,
) -> Tuple[float, np.ndarray, np.ndarray]:
    """
    Train a time series model using RNN.

    Args:
        df (pd.DataFrame): The dataframe containing the time series data.
        column_name (str): The name of the column to train the model on.
    """

    data = df[[column_name]].copy()

    scaler = StandardScaler()
    data[column_name] = scaler.fit_transform(data)

    split_index = int(len(data) * (1 - test_size))
    train_data = data.iloc[:split_index]
    test_data = data.iloc[split_index:]

    # Prepare data for RNN
    sequence_length = 3  # Number of time steps to look back
    train_generator = TimeseriesGenerator(
        train_data.values, train_data.values, length=sequence_length, batch_size=1
    )
    test_generator = TimeseriesGenerator(
        test_data.values, test_data.values, length=sequence_length, batch_size=1
    )

    model = Sequential()

    model.add(
        LSTM(50, activation="relu", input_shape=(sequence_length, train_data.shape[1]))
    )

    model.add(Dense(1))  # Output layer for a single feature
    model.compile(optimizer="adam", loss="mse")

    # Train the model
    model.fit(
        train_generator,
        epochs=num_epochs,
        verbose=2,
    )
    predicted = model.predict(test_generator)
    predicted = scaler.inverse_transform(predicted)
    test_data_values = scaler.inverse_transform(test_data.values)

    test_data_values = test_data_values[sequence_length:]

    mse = mean_squared_error(test_data_values, predicted)
    accuracy = 100 - mse  # Convert MSE to percentage accuracy (0-100%)

    return accuracy, test_data_values, predicted
