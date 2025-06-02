#!/usr/bin/env python3
"""
Script de teste para o serviço de backup do MongoDB
"""

import requests
import json
import time

def test_health_check():
    """Testa o endpoint de health check"""
    print("🔍 Testando health check...")
    try:
        response = requests.get("http://localhost:5000/")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no health check: {e}")
        return False

def test_backup():
    """Testa o endpoint de backup"""
    print("\n📦 Testando backup...")
    try:
        response = requests.post("http://localhost:5000/trigger_backup")
        print(f"Status: {response.status_code}")
        print(f"Resposta: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Erro no backup: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 Iniciando testes do MongoDB Backup Service")
    print("=" * 50)
    
    # Teste 1: Health Check
    health_ok = test_health_check()
    
    if not health_ok:
        print("❌ Health check falhou. Verifique se o serviço está rodando.")
        return
    
    print("✅ Health check passou!")
    
    # Aguarda um pouco antes do próximo teste
    time.sleep(1)
    
    # Teste 2: Backup
    backup_ok = test_backup()
    
    if backup_ok:
        print("✅ Backup executado com sucesso!")
    else:
        print("❌ Backup falhou. Verifique as configurações do MongoDB.")
    
    print("\n" + "=" * 50)
    print("🏁 Testes concluídos!")

if __name__ == "__main__":
    main() 