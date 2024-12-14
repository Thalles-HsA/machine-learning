import numpy as np
from typing import List, Tuple

def generate_linear_data_with_outliers(
    m: float, 
    b: float, 
    num_points: int, 
    noise_std: float, 
    num_outliers: int, 
    outlier_range: float
) -> Tuple[List[float], List[float]]:
    """
    Gera dados lineares com ruído (normal) e adiciona outliers (com intervalo definido).
    :param m: Inclinação da linha
    :param b: Intercepto
    :param num_points: Número de pontos a serem gerados
    :param noise_std: Desvio padrão do ruído para os dados normais
    :param num_outliers: Número de outliers a serem adicionados
    :param outlier_range: Intervalo para os valores dos outliers (mínimo e máximo desvio)
    :return: X (entrada) e y (saída) como listas
    """
    # Gerar dados lineares com ruído normal
    X = np.linspace(0, 10, num_points)
    noise = np.random.normal(0, noise_std, num_points)
    y = m * X + b + noise

    # Adicionar outliers
    outlier_indices = np.random.choice(num_points, num_outliers, replace=False)  # Índices aleatórios para outliers
    for idx in outlier_indices:
        y[idx] += np.random.uniform(-outlier_range, outlier_range)  # Outlier significativo

    return X.tolist(), y.tolist()
