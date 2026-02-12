import numpy as np
import matplotlib.pyplot as plt

def render_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter):
    """
    Renderiza o Conjunto de Mandelbrot usando vetorização NumPy para máxima performance.
    """
    # Criando o grid do plano complexo
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    C = X + 1j * Y
    
    # Inicialização do estado
    Z = np.zeros_like(C)
    # Matriz para contar em qual iteração cada ponto "escapou" para o infinito
    escape_time = np.zeros(C.shape, dtype=int)
    # Máscara para pontos que ainda estão dentro do limite (não escaparam)
    mask = np.full(C.shape, True, dtype=bool)
    
    for i in range(max_iter):
        Z[mask] = Z[mask]**2 + C[mask]
        
        # Detectando pontos que escaparam (|Z| > 2)
        escaped = np.abs(Z) > 2
        # Atualizando o tempo de escape apenas para os pontos que escaparam NESTA iteração
        escaping_now = escaped & mask
        escape_time[escaping_now] = i
        
        # Removendo pontos que escaparam da máscara de processamento
        mask[escaped] = False
        
        # Se todos os pontos escaparam, podemos parar cedo
        if not np.any(mask):
            break
            
    return escape_time

def save_fractal():
    print("[*] Iniciando renderização do infinito (Mandelbrot)...")
    
    # Parâmetros de alta resolução
    width, height = 2000, 2000
    max_iter = 100
    
    # Janela de visualização (Foco no corpo principal)
    xmin, xmax, ymin, ymax = -2.0, 0.5, -1.25, 1.25
    
    start_time = np.datetime64('now')
    fractal_data = render_mandelbrot(xmin, xmax, ymin, ymax, width, height, max_iter)
    end_time = np.datetime64('now')
    
    duration = (end_time - start_time).astype(float) / 1e6
    print(f"[*] Renderização concluída em {duration:.2f} segundos.")
    
    # Estética: Mapa de cores 'magma' para representar a energia do caos
    plt.figure(figsize=(10, 10), facecolor='black')
    plt.imshow(fractal_data, extent=[xmin, xmax, ymin, ymax], cmap='magma')
    plt.axis('off')
    
    output_path = "mandelbrot_fractal.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0, facecolor='black')
    print(f"[*] Fractal salvo em '{output_path}'")

if __name__ == "__main__":
    save_fractal()
