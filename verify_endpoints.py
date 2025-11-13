#!/usr/bin/env python3
"""
Script para verificar que todos los endpoints estén funcionando correctamente
Uso: python verify_endpoints.py [URL]
Ejemplo: python verify_endpoints.py https://porpagar.mx
"""

import sys
import requests
from typing import Dict, List, Tuple

def test_endpoint(
    method: str, 
    url: str, 
    headers: Dict = None, 
    data: Dict = None,
    description: str = ""
) -> Tuple[bool, str, int]:
    """Test a single endpoint and return success status"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=10)
        else:
            return False, "Método no soportado", 0
        
        success = response.status_code < 400
        return success, response.text[:200], response.status_code
    except Exception as e:
        return False, str(e), 0


def main():
    # Get base URL from command line or use default
    base_url = sys.argv[1] if len(sys.argv) > 1 else "https://porpagar.mx"
    api_url = f"{base_url}/api"
    
    print(f"🔍 Verificando endpoints en: {base_url}\n")
    print("=" * 80)
    
    # Test results
    results = []
    
    # 1. Health check
    print("\n📋 ENDPOINTS PÚBLICOS (sin autenticación)\n")
    success, response, status = test_endpoint("GET", f"{api_url}/health")
    results.append(("Health Check", success, status))
    print(f"{'✅' if success else '❌'} GET /api/health → {status}")
    
    # 2. Login
    print("\n🔐 AUTENTICACIÓN\n")
    login_data = {"username": "MAURO", "password": "Mauro123456"}
    success, response, status = test_endpoint("POST", f"{api_url}/auth/login", data=login_data)
    results.append(("Login", success, status))
    print(f"{'✅' if success else '❌'} POST /api/auth/login → {status}")
    
    # Extract token if login successful
    token = None
    if success:
        import json
        try:
            token_data = json.loads(response)
            token = token_data.get("access_token")
            print(f"   🔑 Token obtenido: {token[:20]}...")
        except:
            print("   ⚠️  No se pudo extraer token")
    
    if not token:
        print("\n❌ No se pudo obtener token. No se pueden probar endpoints autenticados.")
        return
    
    # Headers with authentication
    auth_headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Protected endpoints
    print("\n🔒 ENDPOINTS PROTEGIDOS (requieren autenticación)\n")
    
    protected_endpoints = [
        ("GET", "/auth/me", "Información usuario actual"),
        ("GET", "/empresas", "Listar empresas"),
    ]
    
    for method, endpoint, description in protected_endpoints:
        success, response, status = test_endpoint(method, f"{api_url}{endpoint}", headers=auth_headers)
        results.append((description, success, status))
        print(f"{'✅' if success else '❌'} {method} {endpoint} → {status}")
    
    # Get first empresa ID for testing
    print("\n🏢 Obteniendo ID de empresa para pruebas...")
    success, response, status = test_endpoint("GET", f"{api_url}/empresas", headers=auth_headers)
    empresa_id = None
    if success:
        import json
        try:
            empresas = json.loads(response)
            if empresas and len(empresas) > 0:
                empresa_id = empresas[0].get("id")
                print(f"   ✅ Empresa ID: {empresa_id}")
        except:
            print("   ⚠️  No se pudo extraer empresa_id")
    
    if empresa_id:
        # Test empresa-specific endpoints
        print("\n📊 ENDPOINTS ESPECÍFICOS DE EMPRESA\n")
        
        empresa_endpoints = [
            ("GET", f"/invoices/{empresa_id}", "Listar facturas"),
            ("GET", f"/resumen/{empresa_id}", "Resumen general"),
            ("GET", f"/estado-cuenta-pagadas/{empresa_id}", "Estado cuenta pagadas"),
            ("GET", f"/export/facturas-pendientes/{empresa_id}", "Exportar pendientes"),
            ("GET", f"/export/facturas-pagadas/{empresa_id}", "Exportar pagadas"),
            ("GET", f"/export/resumen-general/{empresa_id}", "Exportar resumen"),
        ]
        
        for method, endpoint, description in empresa_endpoints:
            success, response, status = test_endpoint(method, f"{api_url}{endpoint}", headers=auth_headers)
            results.append((description, success, status))
            print(f"{'✅' if success else '❌'} {method} {endpoint} → {status}")
    
    # Get invoice ID for download tests
    print("\n📄 Obteniendo ID de factura para pruebas de descarga...")
    if empresa_id:
        success, response, status = test_endpoint("GET", f"{api_url}/invoices/{empresa_id}", headers=auth_headers)
        invoice_id = None
        if success:
            import json
            try:
                invoices = json.loads(response)
                if invoices and len(invoices) > 0:
                    invoice_id = invoices[0].get("id")
                    print(f"   ✅ Invoice ID: {invoice_id}")
                    
                    # Test download endpoints (these will return 404 if no files)
                    print("\n⬇️  ENDPOINTS DE DESCARGA\n")
                    download_endpoints = [
                        ("GET", f"/invoices/{invoice_id}/download", "Descargar PDF"),
                        ("GET", f"/invoices/{invoice_id}/download-comprobante", "Descargar comprobante"),
                        ("GET", f"/invoices/{invoice_id}/download-xml", "Descargar XML"),
                    ]
                    
                    for method, endpoint, description in download_endpoints:
                        success, response, status = test_endpoint(method, f"{api_url}{endpoint}", headers=auth_headers)
                        # 404 is OK if no file uploaded
                        ok = success or status == 404
                        results.append((description, ok, status))
                        symbol = "✅" if success else "⚠️" if status == 404 else "❌"
                        print(f"{symbol} {method} {endpoint} → {status}")
                        if status == 404:
                            print(f"   ℹ️  404 es OK si no hay archivo subido")
            except Exception as e:
                print(f"   ⚠️  Error: {e}")
    
    # Summary
    print("\n" + "=" * 80)
    print("\n📊 RESUMEN\n")
    
    total = len(results)
    passed = sum(1 for _, success, _ in results if success)
    failed = total - passed
    
    print(f"Total endpoints probados: {total}")
    print(f"✅ Exitosos: {passed}")
    print(f"❌ Fallidos: {failed}")
    print(f"📈 Tasa de éxito: {(passed/total*100):.1f}%")
    
    if failed > 0:
        print("\n❌ ENDPOINTS CON ERRORES:\n")
        for name, success, status in results:
            if not success:
                print(f"   • {name} → {status}")
    
    print("\n" + "=" * 80)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
