# Sofia Lite Load Testing with k6

Questo modulo contiene i test di carico per Sofia Lite utilizzando k6, uno strumento moderno per il testing delle performance.

## 🚀 Configurazione Rapida

### Prerequisiti

- Node.js 18+
- k6 (installato automaticamente dallo script)

### Installazione

```bash
# Installa k6
brew install k6  # macOS
# oppure
sudo apt-get install k6  # Ubuntu/Debian

# Installa dipendenze
cd load
npm install
```

## 📊 Tipi di Test

### 1. Smoke Test
- **VUs**: 1
- **Durata**: 30 secondi
- **Scopo**: Verifica base funzionalità

```bash
./run_load_test.sh http://localhost:8000 smoke
```

### 2. Quick Test
- **VUs**: 5
- **Durata**: 1 minuto
- **Scopo**: Test rapido performance

```bash
./run_load_test.sh http://localhost:8000 quick
```

### 3. Standard Test
- **VUs**: 50
- **Durata**: 5 minuti
- **Scopo**: Test carico normale

```bash
./run_load_test.sh http://localhost:8000 standard
```

### 4. Stress Test
- **VUs**: 100
- **Durata**: 10 minuti
- **Scopo**: Test stress massimo

```bash
./run_load_test.sh http://localhost:8000 stress
```

## 🎯 Thresholds

I test verificano i seguenti threshold:

- **P95 Response Time**: < 1500ms
- **Error Rate**: < 10%
- **Custom Error Rate**: < 10%

## 📈 Metriche Monitorate

### Performance
- Tempo di risposta (media, P95, P99)
- Throughput (richieste/secondo)
- Latenza di connessione

### Affidabilità
- Tasso di errore HTTP
- Errori personalizzati
- Timeout

### Business Logic
- Stati conversazione corretti
- Flusso completo conversazione
- Estrazione nomi

## 🔧 Configurazione

### Variabili d'Ambiente

```bash
export SOFIA_URL=http://localhost:8000
export K6_OUT=influxdb=http://localhost:8086/k6
```

### Personalizzazione Test

Modifica `k6_script.js` per:

- Cambiare il flusso conversazione
- Aggiungere nuovi stati
- Modificare threshold
- Personalizzare metriche

## 📊 Risultati

I test generano:

- **JSON**: Risultati dettagliati
- **CSV**: Dati per analisi
- **Markdown**: Report leggibile
- **InfluxDB**: Metriche time-series

### Esempio Output

```
🚀 Sofia Lite Load Test Runner
==============================
Target URL: http://localhost:8000
Test Type: standard
Output Dir: load_results

✅ k6 version: v0.47.0
✅ Health check passed

📊 Running standard test (50 VUs, 5 minutes)...
✅ Report generated: load_results/load_test_report_20250801_143022.md

🎯 Load Test Summary:
====================
📊 Test Type: standard
🎯 Target: http://localhost:8000
📁 Results: load_results/
📄 Report: load_results/load_test_report_20250801_143022.md
```

## 🔄 CI/CD Integration

I test di carico sono integrati in GitHub Actions:

- **Trigger**: Push su `main` o `sofia-lite-boot`
- **Matrix**: Smoke e Quick test su PR, Standard e Stress su main
- **Artifacts**: Risultati disponibili per 30 giorni
- **Comments**: Risultati automatici su PR

### Manual Trigger

```bash
# Via GitHub Actions UI
# Actions > Load Testing with k6 > Run workflow
```

## 🛠️ Troubleshooting

### Problemi Comuni

1. **k6 non installato**
   ```bash
   brew install k6  # macOS
   ```

2. **Sofia Lite non raggiungibile**
   ```bash
   curl http://localhost:8000/health
   ```

3. **Threshold falliti**
   - Controlla log Sofia Lite
   - Verifica risorse sistema
   - Ottimizza LLM calls

### Debug

```bash
# Test con più logging
k6 run --verbose k6_script.js

# Test singolo VU
k6 run --vus 1 --duration 30s k6_script.js

# Test con output dettagliato
k6 run --out json=debug.json k6_script.js
```

## 📚 Risorse

- [k6 Documentation](https://k6.io/docs/)
- [Performance Testing Best Practices](https://k6.io/docs/testing-guides/)
- [Sofia Lite Architecture](../README.md)

## 🤝 Contributi

Per aggiungere nuovi test:

1. Modifica `k6_script.js`
2. Aggiungi nuovi scenari
3. Aggiorna threshold se necessario
4. Testa localmente
5. Crea PR

---

**Nota**: I test di carico sono critici per garantire le performance di Sofia Lite in produzione. Esegui sempre i test prima di deploy importanti. 