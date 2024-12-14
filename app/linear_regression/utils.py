import numpy as np
from typing import List, Tuple
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from linear_regression.model import compute_cost, predict
import os

def plot_regression(X: List[float], y: List[float], predictions: List[float]) -> None:
    """
    Plota os dados reais e a linha ajustada pelo modelo de regressão.
    """
    plt.scatter(X, y, color="blue", label="Dados reais")
    plt.plot(X, predictions, color="red", label="Linha ajustada")
    plt.xlabel("X")
    plt.ylabel("y")
    plt.legend()
    plt.show()

def generate_cost_grid(
    X: List[float], 
    y: List[float], 
    b_vals: np.ndarray, 
    w_vals: np.ndarray
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Gera o grid de valores para b, w e o custo correspondente.
    """
    b_grid, w_grid = np.meshgrid(b_vals, w_vals)
    cost_grid = np.zeros_like(b_grid)

    for i in range(b_grid.shape[0]):
        for j in range(b_grid.shape[1]):
            cost_grid[i, j] = compute_cost(X, y, w_grid[i, j], b_grid[i, j])

    return b_grid, w_grid, cost_grid


def plot_gradient_descent_3d(
    X: List[float],
    y: List[float],
    wb_history: List[Tuple[float, float]],
    cost_history: List[float],
    margin: float = 1.0
) -> None:
    """
    Plota a superfície da função de custo e o caminho do gradiente descendente em 3D.
    Ajusta automaticamente o intervalo do eixo w.
    """
    # Determinar intervalo dinâmico para w
    w_min = min(w for w, _ in wb_history) - margin
    w_max = max(w for w, _ in wb_history) + margin
    b_min = -5  # Ajuste fixo para b (pode ser dinâmico se necessário)
    b_max = 5

    # Gerar grid de valores para b e w
    b_vals = np.linspace(b_min, b_max, 75)
    w_vals = np.linspace(w_min, w_max, 75)
    b_grid, w_grid = np.meshgrid(b_vals, w_vals)

    # Calcular o custo no grid
    cost_grid = np.zeros_like(b_grid)
    for i in range(b_grid.shape[0]):
        for j in range(b_grid.shape[1]):
            cost_grid[i, j] = compute_cost(X, y, w_grid[i, j], b_grid[i, j])

    # Trajetória do gradiente descendente
    w_path, b_path = zip(*wb_history)

    # Criar o gráfico 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Superfície da função de custo
    ax.plot_surface(b_grid, w_grid, cost_grid, alpha=0.7, cmap="viridis")

    # Caminho do gradiente descendente
    ax.plot(
        w_path,
        b_path,
        cost_history,
        color="red",
        marker="o",
        markersize=2,
        linewidth=0.5,
        label="Gradiente Descendente"
    )

    # Ajustar limites dos eixos
    min_cost = np.min(cost_grid)
    max_cost = np.max(cost_grid)
    ax.set_xlim(b_vals.min(), b_vals.max())
    ax.set_ylim(w_min, w_max)
    ax.set_zlim(min_cost, max_cost)

    # Rótulos
    ax.set_xlabel("Intercepto (b)")
    ax.set_ylabel("Inclinação (w)")
    ax.set_zlabel("Custo")
    ax.set_title("Gradiente Descendente na Função de Custo")
    ax.legend()

    plt.show()

def plot_cost(cost_history: List[float]) -> None:
    """
    Plota a evolução do custo ao longo das iterações do treinamento.
    """
    plt.plot(range(len(cost_history)), cost_history, label="Custo")
    plt.xlabel("Iterações")
    plt.ylabel("Erro (Custo)")
    plt.title("Evolução do Erro durante o Treinamento")
    plt.legend()
    plt.show()
    
def plot_combined(
    X: List[float], 
    y: List[float],
    wb_history: List[Tuple[float, float]], 
    cost_history: List[float],
    margin: float = 1.0,
    output_dir: str = "data/output",
    filename: str = "combined_plot.png"
) -> None:
    """
    Plota o gráfico 3D da superfície de custo, o gráfico 2D do custo e a evolução
    das linhas de regressão ao longo das iterações do gradiente descendente.
    Salva o gráfico gerado em vez de exibi-lo.
    """
    # Criar pasta de saída, se não existir
    os.makedirs(output_dir, exist_ok=True)

    # Caminho completo do arquivo
    filepath = os.path.join(output_dir, filename)

    # Criar figura com 3 gráficos
    fig = plt.figure(figsize=(24, 6))

    # Gráfico 1: Todas as Linhas de Regressão
    ax1 = fig.add_subplot(131)
    ax1.scatter(X, y, color="blue", label="Dados Reais")

    # Para cada w, b no histórico, calcular e plotar a linha correspondente
    for i, (w, b) in enumerate(wb_history):
        predictions = [w * xi + b for xi in X]
        if i == len(wb_history) - 1:  # Linha final em vermelho
            ax1.plot(X, predictions, color="red", label=f"Final: w={w:.2f}, b={b:.2f}")
        else:
            ax1.plot(X, predictions, color="gray", alpha=0.5)  # Linhas intermediárias em cinza

    # Configurações do gráfico de linhas de regressão
    ax1.set_xlabel("X")
    ax1.set_ylabel("y")
    ax1.set_title("Evolução das Linhas de Regressão")
    ax1.legend()

    # Gráfico 2: Evolução do Custo
    ax2 = fig.add_subplot(132)
    ax2.plot(range(len(cost_history)), cost_history, label="Custo", color="blue")
    ax2.set_xlabel("Iterações")
    ax2.set_ylabel("Custo")
    ax2.set_title("Evolução do Custo")
    ax2.legend()

    # Gráfico 3: Superfície de Custo em 3D
    # Determinar intervalo dinâmico para w
    w_min = min(w for w, _ in wb_history) - margin
    w_max = max(w for w, _ in wb_history) + margin
    b_min = -5  # Ajuste fixo para b (pode ser dinâmico se necessário)
    b_max = 5

    # Gerar grid de valores para w e b
    w_vals = np.linspace(w_min, w_max, 75)
    b_vals = np.linspace(b_min, b_max, 75)
    w_grid, b_grid = np.meshgrid(w_vals, b_vals)

    # Calcular o custo no grid
    cost_grid = np.zeros_like(w_grid)
    for i in range(w_grid.shape[0]):
        for j in range(w_grid.shape[1]):
            w = w_grid[i, j]
            b = b_grid[i, j]
            predictions = [w * xi + b for xi in X]  # Calcular previsões para o par (w, b)
            cost_grid[i, j] = compute_cost(predictions, y)  # Calcular custo com base nas previsões

    # Trajetória do gradiente descendente
    w_path, b_path = zip(*wb_history)

    # Configurar gráfico 3D
    ax3 = fig.add_subplot(133, projection='3d')

    # Superfície da função de custo
    ax3.plot_surface(w_grid, b_grid, cost_grid, alpha=0.7, cmap="viridis")

    # Caminho do gradiente descendente
    ax3.plot(
        w_path,
        b_path,
        cost_history,
        color="red",
        marker="o",
        markersize=2,
        linewidth=0.5,
        label="Gradiente Descendente"
    )

    # Configurações dos eixos
    ax3.set_xlabel("Inclinação (w)")
    ax3.set_ylabel("Intercepto (b)")
    ax3.set_zlabel("Custo")
    ax3.set_title("Superfície da Função de Custo")
    ax3.legend()

    # Ajustar layout e salvar
    plt.tight_layout()
    plt.savefig(filepath)
    print(f"Gráfico salvo em: {filepath}")


