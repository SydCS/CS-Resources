import numpy as np
import requests


def load_data(url):
    response = requests.get(url)

    data = []
    labels = []
    for line in response.text.strip().split("\n"):
        parts = line.split()
        # Extract features and append a 1 for the bias term x0
        features = [1.0] + [float(x) for x in parts[:-1]]
        label = int(parts[-1])
        data.append(features)
        labels.append(label)
    return np.array(data), np.array(labels)


def perceptron_learning_algorithm(X, y):
    w = np.zeros(X.shape[1])

    iteration_count = 0
    while True:
        is_error = False
        for i in range(len(X)):
            if np.sign(np.dot(w, X[i])) != y[i]:
                w += y[i] * X[i]
                is_error = True
                iteration_count += 1
                # break
        if not is_error:
            break
    return w, iteration_count


if __name__ == "__main__":
    data_url = (
        "https://www.csie.ntu.edu.tw/~htlin/mooc/datasets/mlfound_math/hw1_15_train.dat"
    )
    X, y = load_data(data_url)
    w, num_updates = perceptron_learning_algorithm(X, y)
    print(f"The algorithm halted after {num_updates} updates.")
