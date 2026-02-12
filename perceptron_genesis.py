import numpy as np
import time

# --- PERCEPTRON GENESIS: A DESCIDA DO GRADIENTE ---

def sigmoid(x):
    """Função de ativação para introduzir não-linearidade."""
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    """Derivada da sigmoid para o Backpropagation."""
    s = sigmoid(x)
    return s * (1 - s)

# 1. SETUP DOS DADOS (XOR Simples ou OR) - Operação OR
# Entradas: [0,0], [0,1], [1,0], [1,1]
# Alvos:    [0, 1, 1, 1]
inputs = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
targets = np.array([[0], [1], [1], [1]])

# 2. INICIALIZAÇÃO "TABULA RASA" (Pesos e Biases Aleatórios)
np.random.seed(42)
weights = np.random.randn(2, 1)
bias = np.random.randn(1)
learning_rate = 0.5
epochs = 1000

print("\n--- INICIANDO GÊNESE DO PERCEPTRON: APRENDIZADO DA LÓGICA 'OR' ---\n")

# 3. O LOOP DO APRENDIZADO (Epochs)
for epoch in range(epochs):
    # FORWARD PROPAGATION
    # Z = (W1*X1 + W2*X2) + B
    weighted_sum = np.dot(inputs, weights) + bias
    predictions = sigmoid(weighted_sum)
    
    # CÁLCULO DA PERDA (Mean Squared Error)
    error = targets - predictions
    loss = np.mean(error**2)
    
    # BACKPROPAGATION (A Iluminação)
    # 1. Quão longe está a previsão? (Error)
    # 2. Qual a inclinação do gatilho? (Sigmoid Derivative)
    # 3. Qual entrada causou isso? (Inputs)
    d_loss_prediction = -2 * error / inputs.shape[0]
    d_prediction_z = sigmoid_derivative(weighted_sum)
    
    # O Gradiente Combinado (Regra da Cadeia)
    gradient = d_loss_prediction * d_prediction_z
    
    # AJUSTE DOS PESOS E BIAS (Descida do Gradiente)
    weights -= learning_rate * np.dot(inputs.T, gradient)
    bias -= learning_rate * np.sum(gradient)
    
    if epoch % 100 == 0:
        # Visualização básica da perda caindo
        bar = "#" * int(abs(loss) * 50)
        print(f"Época {epoch:4d} | Perda (Loss): {loss:.6f} | {bar}")

print("\n--- APRENDIZADO CONCLUÍDO ---")
print("\nVerificação da Lógica Reconstruída:")

final_pred = sigmoid(np.dot(inputs, weights) + bias)
for i in range(len(inputs)):
    res = "True" if final_pred[i] > 0.5 else "False"
    print(f"  Input: {inputs[i]} -> Output: {final_pred[i][0]:.4f} (Interpretado: {res})")

print("\n[SÍNTESE FILOSÓFICA]")
print("Inteligência não é mística; é a descida de um gradiente.")
print("A máquina não 'conhece' a porta OR. Ela apenas encontrou o vale")
print("onde o erro é mínimo através do ajuste iterativo de suas conexões.")
