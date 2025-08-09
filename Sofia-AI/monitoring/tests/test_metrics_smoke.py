import requests
import re
import sys

def test_metrics_endpoint():
    """Test smoke per verificare che l endpoint delle metriche funzioni"""
    try:
        # URL del servizio monitoring
        monitor_url = "https://sofia-monitor-1075574333382.europe-west1.run.app"
        
        # Test endpoint root
        print("🔍 Testando endpoint root...")
        response = requests.get(f"{monitor_url}/")
        assert response.status_code == 200, f"Status code root: {response.status_code}"
        print("✅ Endpoint root OK")
        
        # Test endpoint metrics
        print("🔍 Testando endpoint metrics...")
        response = requests.get(f"{monitor_url}/metrics")
        assert response.status_code == 200, f"Status code metrics: {response.status_code}"
        print("✅ Endpoint metrics OK")
        
        # Verifica presenza metrica sofia_new_leads_total
        print("🔍 Verificando presenza metrica sofia_new_leads_total...")
        metrics_text = response.text
        assert re.search(r"sofia_new_leads_total \d+", metrics_text), "Metrica sofia_new_leads_total non trovata"
        print("✅ Metrica sofia_new_leads_total trovata")
        
        # Verifica formato Prometheus
        assert "# HELP" in metrics_text, "Formato Prometheus non valido"
        assert "# TYPE" in metrics_text, "Formato Prometheus non valido"
        print("✅ Formato Prometheus valido")
        
        print("🎉 Tutti i test smoke passati!")
        return True
        
    except Exception as e:
        print(f"❌ Test fallito: {e}")
        return False

if __name__ == "__main__":
    success = test_metrics_endpoint()
    sys.exit(0 if success else 1)
