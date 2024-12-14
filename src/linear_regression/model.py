from typing import List, Tuple

def predict(X: List[float], w: float, b: float) -> List[float]:
    """
    Retorna as previsões baseadas nos valores de X e nos parâmetros w e b.
    """
    return [w * xi + b for xi in X]

def predict_multivariate(X: List[List[float]], w: List[float], b: float) -> List[float]:
    """
    Retorna as previsões baseadas nos valores de X (matriz) e nos parâmetros w e b.
    """
    return [sum(w[j] * xi[j] for j in range(len(w))) + b for xi in X]


def compute_cost(predictions: List[float], y: List[float]) -> float:
    """
    Calcula o custo (erro médio quadrático) usando as previsões da função predict.
    O custo é calculado como a média dos erros ao quadrado entre as previsões e os valores reais.
        A equação matemática para o custo é:
        J = (1/2m) * Σ(y_pred - y)^2
    """
    m = len(y)
    total_cost = sum((y_pred - yi) ** 2 for y_pred, yi in zip(predictions, y))
    return total_cost / (2 * m)

def gradient_descent(
    X: List[float],
    y: List[float],
    w: float,
    b: float,
    alpha: float,
    max_epochs: int,
    tolerance: float = 1e-2
) -> Tuple[float, float, List[float], List[Tuple[float, float]]]:
    """
    Ajusta os parâmetros w e b usando gradiente descendente com critério de parada.
    """
    cost_history = []
    wb_history = []

    for epoch in range(max_epochs):
        # Calcular os gradientes
        
        predictions = predict(X, w, b)
        
        m = len(y)
        d_w = sum((y_pred - yi) * xi for y_pred, xi, yi in zip(predictions, X, y)) / m
        d_b = sum((y_pred - yi) for y_pred, yi in zip(predictions, y)) / m
        
        w -= alpha * d_w
        b -= alpha * d_b

        # Calcular o custo atual
        predictions = predict(X, w, b) #Atualiza a predição com os novos valores de w e b
        cost = compute_cost(predictions, y)
        cost_history.append(cost)
        wb_history.append((w, b))

        # # Verificar se a mudança no custo é menor que a tolerância
        if epoch > 0 and abs(cost_history[-2] - cost_history[-1]) < tolerance:
            print(f"Convergência atingida em {epoch} iterações.")
            break

    return w, b, cost_history, wb_history
