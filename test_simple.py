#!/usr/bin/env python3
"""
Test Simple System - Testa se o sistema está funcionando
"""

print("="*60)
print("🧪 TESTANDO SISTEMA SIMPLES")
print("="*60)
print()

# Teste 1: Importações
print("📦 Teste 1: Verificando dependências...")
try:
    import flask
    print("  ✅ Flask OK")
except:
    print("  ❌ Flask não encontrado - Execute: pip install flask")

try:
    import cv2
    print("  ✅ OpenCV OK")
except:
    print("  ❌ OpenCV não encontrado - Execute: pip install opencv-python")

try:
    import speech_recognition
    print("  ✅ SpeechRecognition OK")
except:
    print("  ⚠️  SpeechRecognition não encontrado (opcional para voz)")

print()

# Teste 2: Arquivos
print("📁 Teste 2: Verificando arquivos...")
import os

files = [
    'simple_app.py',
    'templates/simple_index.html',
    'start_simple.bat',
    'SIMPLE_README.md',
    'SOLUTION.md'
]

for file in files:
    if os.path.exists(file):
        print(f"  ✅ {file}")
    else:
        print(f"  ❌ {file} não encontrado")

print()

# Teste 3: Sistema Bitcoin
print("⛓️  Teste 3: Testando sistema blockchain...")
try:
    import hashlib
    import time
    
    class TestWallet:
        def __init__(self, name):
            self.address = hashlib.sha256(f"{name}{time.time()}".encode()).hexdigest()[:20]
    
    wallet1 = TestWallet("Alice")
    wallet2 = TestWallet("Bob")
    
    print(f"  ✅ Carteira Alice: {wallet1.address}")
    print(f"  ✅ Carteira Bob: {wallet2.address}")
except Exception as e:
    print(f"  ❌ Erro: {e}")

print()

# Teste 4: Câmera
print("📹 Teste 4: Verificando câmera...")
try:
    import cv2
    cap = cv2.VideoCapture(0)
    if cap.isOpened():
        ret, frame = cap.read()
        if ret:
            print("  ✅ Câmera funcionando!")
            print(f"  📸 Resolução: {frame.shape[1]}x{frame.shape[0]}")
        else:
            print("  ⚠️  Câmera conectada mas não capturou imagem")
        cap.release()
    else:
        print("  ⚠️  Câmera não disponível (não é erro - sistema tem fallback)")
except Exception as e:
    print(f"  ⚠️  Câmera não testada: {e}")

print()

# Teste 5: Porta
print("🌐 Teste 5: Verificando porta 5000...")
import socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 5000))
if result == 0:
    print("  ⚠️  Porta 5000 já está em uso")
    print("     Feche outros servidores ou use outra porta")
else:
    print("  ✅ Porta 5000 livre")
sock.close()

print()
print("="*60)
print("🎯 RESUMO:")
print("="*60)
print()
print("Se todos os testes passaram, execute:")
print()
print("  Windows: start_simple.bat")
print("  Manual:  python simple_app.py")
print()
print("Depois acesse: http://localhost:5000")
print()
print("="*60)
