#!/usr/bin/env python3
"""
gauss_curvature.py

Calculo da Curvatura de Gauss a partir de uma matriz de imagem (campo escalar z = I(x,y)).

Principais funções:
- `compute_gauss_curvature(image, sigma=1.0, spacing=1.0)`: retorna matriz K com mesma resolução.
- CLI: pode carregar `--image PATH` ou capturar da webcam `--webcam` e salvar/exibir mapa de curvatura.

Formula usada (para z = f(x,y)):
  K = (f_xx * f_yy - f_xy**2) / (1 + f_x**2 + f_y**2)**2

Dependências opcionais: numpy, opencv-python (cv2), matplotlib (para visualização).
"""
import argparse
import os
import sys
import numpy as np

try:
    import cv2
    HAS_CV2 = True
except Exception:
    HAS_CV2 = False

try:
    import matplotlib.pyplot as plt
    HAS_MPL = True
except Exception:
    HAS_MPL = False


def _smooth(image: np.ndarray, sigma: float = 1.0) -> np.ndarray:
    """Suaviza a imagem — usa GaussianBlur do OpenCV se disponível, senão aplica filtro simples."""
    if sigma <= 0:
        return image
    if HAS_CV2:
        ksize = max(3, int(2 * round(3 * sigma) + 1))
        return cv2.GaussianBlur(image, (ksize, ksize), sigmaX=sigma, sigmaY=sigma)
    # fallback: separable gaussian via numpy (very small kernel)
    from math import exp, sqrt, pi
    radius = int(3 * sigma)
    if radius <= 0:
        return image
    x = np.arange(-radius, radius + 1)
    gauss = np.exp(-x**2 / (2 * sigma**2))
    gauss = gauss / gauss.sum()
    # separable convolution
    tmp = np.apply_along_axis(lambda m: np.convolve(m, gauss, mode='same'), axis=0, arr=image)
    out = np.apply_along_axis(lambda m: np.convolve(m, gauss, mode='same'), axis=1, arr=tmp)
    return out


def compute_gauss_curvature(image: np.ndarray, sigma: float = 1.0, spacing: float = 1.0) -> np.ndarray:
    """Computa a curvatura de Gauss de uma imagem (grayscale float).

    Args:
        image: 2D numpy array (grayscale). Values will be cast to float64.
        sigma: smoothing sigma (Gaussian) to reduce noise before derivatives.
        spacing: pixel spacing (usually 1.0). Use to scale derivatives if pixels are not square.

    Returns:
        K: 2D numpy array same shape as image with Gaussian curvature values (float64).
    """
    if image.ndim != 2:
        raise ValueError('image must be 2D grayscale')

    f = image.astype(np.float64)
    if sigma > 0:
        f = _smooth(f, sigma=sigma)

    # first derivatives
    fy, fx = np.gradient(f, spacing, spacing)
    # second derivatives
    fyy, fxy = np.gradient(fy, spacing, spacing)
    fxy2, fxx = np.gradient(fx, spacing, spacing)
    # Note: fxy == fxy2 in exact math; numerical derivatives may differ slightly. Use average.
    fxy = 0.5 * (fxy + fxy2)

    # Gaussian curvature formula for surface z = f(x,y):
    # K = (f_xx * f_yy - f_xy**2) / (1 + f_x**2 + f_y**2)**2
    denom = (1.0 + fx**2 + fy**2)
    eps = 1e-12
    K = (fxx * fyy - fxy**2) / (denom + eps)**2
    return K


def _normalize_for_display(arr: np.ndarray) -> np.ndarray:
    a = arr.copy()
    vmin = np.nanpercentile(a, 2)
    vmax = np.nanpercentile(a, 98)
    if vmax - vmin == 0:
        return np.zeros_like(a)
    a = np.clip(a, vmin, vmax)
    a = (a - vmin) / (vmax - vmin)
    return a


def main():
    parser = argparse.ArgumentParser(description='Compute Gaussian curvature from image (z = intensity)')
    parser.add_argument('--image', '-i', help='Path to input image (grayscale or color)')
    parser.add_argument('--webcam', '-w', action='store_true', help='Capture one frame from webcam')
    parser.add_argument('--sigma', type=float, default=1.0, help='Gaussian smoothing sigma')
    parser.add_argument('--out', '-o', help='Path to save curvature visualization (PNG)')
    args = parser.parse_args()

    if not args.image and not args.webcam:
        parser.print_help()
        sys.exit(1)

    if args.webcam:
        if not HAS_CV2:
            print('[❌] OpenCV not available for webcam capture')
            sys.exit(1)
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print('[❌] Cannot open webcam')
            sys.exit(1)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            print('[❌] Failed to read frame from webcam')
            sys.exit(1)
        img = frame
    else:
        if not os.path.exists(args.image):
            print(f'[❌] Image not found: {args.image}')
            sys.exit(1)
        if HAS_CV2:
            img = cv2.imread(args.image, cv2.IMREAD_COLOR)
        else:
            # minimal image reader using matplotlib if available
            try:
                from PIL import Image
                img = np.array(Image.open(args.image).convert('RGB'))
            except Exception as e:
                print('[❌] Cannot read image (install opencv-python or pillow)')
                raise

    # Convert to grayscale float
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if HAS_CV2 else np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    else:
        gray = img

    gray = gray.astype(np.float64) / 255.0

    K = compute_gauss_curvature(gray, sigma=args.sigma)

    # for visualization, normalize and apply a colormap
    vis = _normalize_for_display(K)

    if HAS_MPL:
        plt.figure(figsize=(8, 6))
        plt.imshow(vis, cmap='seismic', interpolation='nearest')
        plt.colorbar(label='Normalized Gaussian Curvature')
        plt.title('Gaussian Curvature (normalized)')
        if args.out:
            plt.savefig(args.out, dpi=150)
            print(f'[✅] Visualization saved to {args.out}')
        else:
            plt.show()
    else:
        # fallback: save as numpy array or image via cv2
        out_path = args.out or 'gauss_curvature.png'
        if HAS_CV2:
            save_img = (vis * 255).astype(np.uint8)
            save_img = cv2.applyColorMap(save_img, cv2.COLORMAP_SEISMIC)
            cv2.imwrite(out_path, save_img)
            print(f'[✅] Visualization saved to {out_path}')
        else:
            np.save('gauss_curvature.npy', K)
            print('[ℹ️] matplotlib/opencv not available: curvature array saved to gauss_curvature.npy')


if __name__ == '__main__':
    main()
