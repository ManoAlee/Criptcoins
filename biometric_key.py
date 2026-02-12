#!/usr/bin/env python3
"""
biometric_key.py

Capture uma foto da webcam localmente e derive uma chave simétrica a partir
da imagem. O script NÃO realiza identificação biométrica nem envia dados.
Tudo roda OFFLINE e a chave é derivada apenas da imagem capturada.

Teoria resumida:
- Entropia da imagem: SHA-256(image_bytes) usado como fonte de entropia.
- KDF: PBKDF2-HMAC-SHA256 com 200k iterações para derivar 32 bytes seguros.
- Criptografia: AES-GCM para confidencialidade e integridade (nonce 96 bits).
- Derivação de chave Bitcoin: os 32 bytes derivados podem ser usados como
  chave privada (hex) para carteiras compatíveis com secp256k1.

Referências:
- PBKDF2: RFC 2898
- AES-GCM: NIST SP 800-38D
- Bitcoin key derivation: secp256k1 private key format

Avisos de segurança:
- Esta abordagem usa a imagem como "senha" — se a imagem for perdida, chave
  não pode ser reproducida. Se imagem for compartilhada, segurança é comprometida.
- Não use para fundos reais sem auditoria. Este código é educacional.

Dependências: opencv-python, cryptography
Instalação: pip install opencv-python cryptography

Uso: python biometric_key.py
"""
import sys
import os
import time
import json
import base64
from typing import Tuple
import hashlib
from getpass import getpass
import argparse
import secrets

try:
    import face_recog
    HAS_FACE_RECOG = True
except Exception:
    face_recog = None
    HAS_FACE_RECOG = False

try:
    import cv2
except Exception:
    print("[❌] OpenCV (cv2) não está instalado. Instale com: pip install opencv-python")
    sys.exit(1)

try:
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
except Exception:
    print("[❌] cryptography não está instalado. Instale com: pip install cryptography")
    sys.exit(1)

BACKEND = default_backend()

OUTPUT_ENC_FILE = 'biometric_secret.enc'
OUTPUT_META_FILE = 'biometric_meta.json'

# AES-GCM params
AESGCM_NONCE_SIZE = 12


def capture_image():
    """Captura uma imagem da webcam. Retorna os bytes da imagem PNG."""
    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("[❌] Não foi possível abrir a webcam. Verifique permissões e dispositivo.")
        return None

    print("[ℹ️] Webcam aberta. Pressione ESPAÇO para capturar, 'q' para sair.")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("[❌] Falha ao ler frame da webcam.")
            break

        cv2.imshow('Press SPACE to capture, q to quit', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord(' '):  # SPACE
            # Encode to PNG bytes
            ret2, buf = cv2.imencode('.png', frame)
            if not ret2:
                print("[❌] Falha ao codificar imagem.")
                break
            img_bytes = buf.tobytes()
            print("[✅] Imagem capturada.")
            cam.release()
            cv2.destroyAllWindows()
            return img_bytes

        if key == ord('q'):
            print("[⚠️] Captura cancelada pelo usuário.")
            break

    cam.release()
    cv2.destroyAllWindows()
    return None


def derive_key_from_image(image_bytes: bytes, salt: bytes = None) -> Tuple[bytes, bytes, bytes]:
    """Deriva uma chave de 32 bytes a partir dos bytes da imagem usando PBKDF2-HMAC-SHA256.

    Retorna (raw_key, image_hash, salt).
    """
    # Entropia base: sha256(image)
    image_hash = hashlib.sha256(image_bytes).digest()

    # Use salt: se fornecido, combine com parte do hash
    if salt is None:
        salt = image_hash[:16]

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=200_000,
        backend=BACKEND
    )

    # Use o hash bytes como 'password' para KDF
    password = image_hash
    raw_key = kdf.derive(password)
    return raw_key, image_hash, salt


def encrypt_with_aesgcm(raw_key: bytes, plaintext: bytes) -> bytes:
    return encrypt_with_aesgcm_impl(raw_key, plaintext)


def encrypt_with_aesgcm_impl(raw_key: bytes, plaintext: bytes) -> bytes:
    aesgcm = AESGCM(raw_key)
    nonce = secrets.token_bytes(AESGCM_NONCE_SIZE)
    ct = aesgcm.encrypt(nonce, plaintext, None)
    return nonce + ct


def decrypt_with_aesgcm_impl(raw_key: bytes, data: bytes) -> bytes:
    if len(data) < AESGCM_NONCE_SIZE:
        raise ValueError("Dados encriptados inválidos")
    nonce = data[:AESGCM_NONCE_SIZE]
    ct = data[AESGCM_NONCE_SIZE:]
    aesgcm = AESGCM(raw_key)
    return aesgcm.decrypt(nonce, ct, None)


def main():
    print("\n🔒 Biometric Key Utility - Offline")
    print("Este script captura uma foto localmente e deriva uma chave simétrica a partir dela.")
    print("O processo NÃO identifica você e NÃO envia dados para nenhum servidor.\n")

    consent = input("Deseja continuar e abrir a webcam local? [s/N]: ").strip().lower()
    if consent != 's':
        print("Operação cancelada pelo usuário.")
        return

    img = capture_image()
    if img is None:
        print("Nenhuma imagem capturada. Saindo.")
        return

    # Derivar chave (raw_key = 32 bytes)
    raw_key, img_hash, salt = derive_key_from_image(img)

    print(f"\n[🔑] Chave derivada (fingerprint): {img_hash.hex()[:32]}...")
    print("⚠️  Guarde uma cópia segura da sua imagem se quiser reproduzir a chave depois.")

    # Opções adicionais: criptografar, descriptografar, derivar carteira Bitcoin, reconhecimento facial
    extra_opts = "(r)econhecimento facial, " if HAS_FACE_RECOG else ""
    choice = input(f"Ações: {extra_opts}(e)ncriptar, (d)escriptografar, (w)allet derivation, (N)ada ? [e/d/w/N]: ").strip().lower()
    if choice == 'r':
        if not HAS_FACE_RECOG:
            print('[❌] Módulo face_recog não disponível. Instale opencv-python e certifique-se de que face_recog.py está no projeto.')
            return

        sub = input('(e)nroll or (a)uthenticate? [e/a]: ').strip().lower()
        if sub == 'e':
            username = input('Username to enroll: ').strip()
            if not username:
                print('[❌] Nome de usuário inválido')
                return
            face_recog.enroll_user_interactive(username)
            return
        elif sub == 'a':
            print('[ℹ️] Capturando imagem para autenticação...')
            img_bytes = img
            user, score = face_recog.authenticate_from_image_bytes(img_bytes)
            if user:
                print(f"[✅] Usuário autenticado: {user} (score={score:.2f})")
            else:
                if score is None:
                    print('[❌] Nenhuma face detectada na imagem')
                else:
                    print(f'[❌] Nenhuma correspondência (melhor score={score:.2f})')
            return
        else:
            print('Opção inválida.')
            return

    if choice == 'e':
        mode = input("Criptografar (t)exto ou (f)ile? [t/f]: ").strip().lower()

        if mode == 't':
            secret = getpass("Digite o texto secreto: ")
            secret_bytes = secret.encode('utf-8')
            encrypted = encrypt_with_aesgcm_impl(raw_key, secret_bytes)

            with open(OUTPUT_ENC_FILE, 'wb') as fh:
                fh.write(encrypted)

            meta = {
                'method': 'aesgcm_pbkdf2_image',
                'image_hash': img_hash.hex(),
                'salt': salt.hex(),
                'enc_file': OUTPUT_ENC_FILE,
                'note': 'Para descriptografar, recapture a mesma imagem com biometric_key.py e escolha descriptografar.'
            }
            with open(OUTPUT_META_FILE, 'w') as fm:
                json.dump(meta, fm, indent=2)

            print(f"[✅] Texto criptografado salvo em: {OUTPUT_ENC_FILE}")
            print(f"[ℹ️] Metadados salvos em: {OUTPUT_META_FILE}")
            return

        elif mode == 'f':
            path = input("Caminho do arquivo a criptografar: ").strip()
            if not os.path.exists(path):
                print("[❌] Arquivo não encontrado.")
                return
            with open(path, 'rb') as f:
                data = f.read()
            encrypted = encrypt_with_aesgcm_impl(raw_key, data)
            out_path = path + '.enc'
            with open(out_path, 'wb') as fh:
                fh.write(encrypted)

            meta = {
                'method': 'aesgcm_pbkdf2_image',
                'image_hash': img_hash.hex(),
                'salt': salt.hex(),
                'enc_file': out_path,
                'note': 'Para descriptografar, recapture a mesma imagem com biometric_key.py e escolha descriptografar.'
            }
            with open(OUTPUT_META_FILE, 'w') as fm:
                json.dump(meta, fm, indent=2)

            print(f"[✅] Arquivo criptografado salvo em: {out_path}")
            print(f"[ℹ️] Metadados salvos em: {OUTPUT_META_FILE}")
            return

        else:
            print("Opção inválida. Saindo.")
            return

    if choice == 'd':
        # Descriptografar arquivo usando imagem atual
        enc_path = input(f"Caminho do arquivo encriptado (ou ENTER para usar {OUTPUT_ENC_FILE}): ").strip()
        if not enc_path:
            enc_path = OUTPUT_ENC_FILE
        if not os.path.exists(enc_path):
            print('[❌] Arquivo encriptado não encontrado.')
            return

        with open(enc_path, 'rb') as fh:
            enc_data = fh.read()

        try:
            plain = decrypt_with_aesgcm_impl(raw_key, enc_data)
        except Exception as e:
            print(f"[❌] Falha ao descriptografar: {e}")
            return

        # Tentar decodificar como texto
        try:
            text = plain.decode('utf-8')
            print('\n[✅] Conteúdo descriptografado (texto):\n')
            print(text)
        except Exception:
            out_file = enc_path + '.dec'
            with open(out_file, 'wb') as fo:
                fo.write(plain)
            print(f"[✅] Conteúdo binário salvo em: {out_file}")

        return

    if choice == 'w':
        # Derivar carteira Bitcoin a partir do raw_key (32 bytes)
        try:
            from bitcoin_crypto import BitcoinWallet
            import ecdsa
        except Exception:
            print('[❌] Módulo bitcoin_crypto não disponível. Instale dependências do projeto.')
            return
        # Garantir que a chave privada esteja no intervalo válido [1, n-1]
        curve_order = ecdsa.SECP256k1.order
        priv_int = (int.from_bytes(raw_key, 'big') % (curve_order - 1)) + 1
        priv_bytes = priv_int.to_bytes(32, 'big')
        priv_hex = priv_bytes.hex()
        wallet = BitcoinWallet()
        wallet.import_from_private_key(priv_hex)
        out = wallet.export_wallet()
        out_path = 'derived_wallet.json'
        with open(out_path, 'w') as fo:
            json.dump(out, fo, indent=2)
        print(f"[🔐] Carteira derivada e salva em: {out_path}")
        print(f"    Endereço: {out['address']}")
        print('⚠️  NÃO compartilhe o arquivo derived_wallet.json se contiver sua chave privada!')
        return

    # Se não escolheu as ações acima, oferecer salvar imagem criptografada
    save_choice = input("Deseja salvar a imagem (criptografada) localmente? [s/N]: ").strip().lower()
    if save_choice == 's':
        encrypted_img = encrypt_with_aesgcm_impl(raw_key, img)
        with open('captured_image.enc', 'wb') as fh:
            fh.write(encrypted_img)
        meta = {
            'method': 'aesgcm_pbkdf2_image',
            'image_hash': img_hash.hex(),
            'salt': salt.hex(),
            'enc_file': 'captured_image.enc'
        }
        with open(OUTPUT_META_FILE, 'w') as fm:
            json.dump(meta, fm, indent=2)
        print('[✅] Imagem capturada e salva (criptografada) em captured_image.enc')
    else:
        print('Nenhum arquivo salvo. Lembre-se: sem a mesma imagem não será possível reproduzir a chave.')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[🛑] Operação cancelada pelo usuário')
    except Exception as e:
        print(f"[❌] Erro: {e}")
        import traceback
        traceback.print_exc()
