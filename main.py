from linear_regression.data import generate_linear_data_with_outliers
from linear_regression.model import predict, gradient_descent, compute_cost
from linear_regression.utils import plot_combined

# Dados Gerados
m = 10  # Inclinação real
b = 1.0  # Intercepto real

# Parâmetros dos dados
num_points = 200
noise_std = 20  # Desvio padrão do ruído normal
num_outliers = 20# Número de outliers
outlier_range = 50  # Intervalo para os outliers

# Gerar dados
X, y = generate_linear_data_with_outliers(m, b, num_points, noise_std, num_outliers, outlier_range)

# 2. Inicializar parâmetros
w, b = 0, 0  # Inclinação (w) e intercepto (b)
alpha, epochs = 0.003, 1000

# Gradiente descendente ajustado
w, b, cost_history, wb_history = gradient_descent(X, y, w, b, alpha, epochs)

# Previsões finais
predictions = predict(X, w, b)

# Cálculo do custo final
final_cost = compute_cost(predictions, y)

# Erro Médio Absoluto (MAE)
mae = sum(abs(y_i - y_pred) for y_i, y_pred in zip(y, predictions)) / len(y)
print(f"Erro Médio Absoluto (MAE): {mae}")

# Visualizar os resultados
plot_combined(X, y, wb_history, cost_history)
