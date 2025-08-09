# Sofia Client Tests - Guida per il Cliente

## 📋 **Panoramica**

Questo pacchetto contiene i test **condivisibili con il cliente** per verificare le funzionalità core di Sofia Lite e Sofia Bulk API. I test coprono l'**80% delle funzionalità pubbliche** e sono progettati per essere eseguiti in ambiente isolato.

## ⚠️ **DISCLAIMER IMPORTANTE**

- **Copertura**: I test coprono l'80% delle funzionalità pubbliche
- **Esclusi**: I test interni sono esclusi per motivi di sicurezza
- **Ambiente**: I test sono progettati per essere eseguiti in ambiente isolato
- **Supporto**: Per problemi specifici, contattare il team di sviluppo
- **Sicurezza**: Questo pacchetto è completamente sicuro per la condivisione con i clienti

## 🚀 **Prerequisiti**

### **Opzione 1: Python Virtual Environment (Raccomandato)**
```bash
# Python 3.11+ richiesto
python3.11 --version

# Crea ambiente virtuale
python3.11 -m venv .venv

# Attiva ambiente
source .venv/bin/activate  # Linux/Mac
# oppure
.venv\Scripts\activate     # Windows

# Installa dipendenze
pip install -e .
pip install tox
```

### **Opzione 2: pipx (Alternativa)**
```bash
# Installa pipx se non presente
python3.11 -m pip install --user pipx
python3.11 -m pipx ensurepath

# Esegui direttamente
pipx run tox -e client311
```

## 🧪 **Comandi Rapidi**

### **Esegui tutti i test client**
```bash
# Con tox (raccomandato)
tox -e client311

# Con pytest diretto
pytest tests_client/ -v

# Con Makefile
make client-tests
```

### **Esegui test specifici**
```bash
# Solo test di configurazione
pytest tests_client/test_config.py -v

# Solo test di estrazione nomi
pytest tests_client/test_name_extract.py -v

# Solo test Bulk API
pytest tests_client/test_auth.py tests_client/test_flow.py tests_client/test_rate.py -v
```

## 📊 **Risultati e Report**

### **JUnit XML Report**
I test generano automaticamente un report JUnit XML in `reports/client-junit.xml`:
```bash
# Visualizza report
cat reports/client-junit.xml

# Converte in HTML (richiede junit2html)
pip install junit2html
junit2html reports/client-junit.xml reports/client-report.html
```

### **Coverage Report (Opzionale)**
Per generare report di copertura:
```bash
# Installa coverage
pip install coverage

# Esegui con coverage
coverage run -m pytest tests_client/
coverage report
coverage html  # Genera HTML in htmlcov/
```

## 🏗️ **Struttura Test**

### **Test Core (sofia_lite)**
- **`test_simple_suite.py`**: Test di base per funzionalità core
- **`test_config.py`**: Test di configurazione e validazione
- **`test_simple.py`**: Test semplici di import e funzionalità base
- **`test_name_extract.py`**: Test per estrazione e pulizia nomi
- **`test_prompt_builder.py`**: Test per costruzione prompt

### **Test Bulk API (sofia_bulk_api)**
- **`test_auth.py`**: Test autenticazione e autorizzazione
- **`test_flow.py`**: Test flusso conversazioni
- **`test_rate.py`**: Test rate limiting e gestione richieste

## 🔧 **Risoluzione Problemi**

### **Errori Comuni**

#### **ModuleNotFoundError**
```bash
# Soluzione: Installa il pacchetto in modalità development
pip install -e .
```

#### **Import Errors**
```bash
# Verifica che l'ambiente sia attivo
which python
pip list | grep sofia
```

#### **Test Failures**
```bash
# Esegui test specifico per debug
pytest tests_client/test_name_extract.py::test_clean_name -v -s

# Verifica dipendenze
pip check
```

### **Debug Avanzato**
```bash
# Esegui con output dettagliato
pytest tests_client/ -v -s --tb=long

# Esegui con pdb per debug interattivo
pytest tests_client/ --pdb

# Esegui con coverage dettagliato
coverage run -m pytest tests_client/ --cov=sofia_lite --cov=sofia_bulk_api
```

## 📁 **File e Directory**

```
tests_client/
├── test_simple_suite.py      # Test suite principale
├── test_config.py            # Test configurazione
├── test_simple.py            # Test base
├── test_name_extract.py      # Test estrazione nomi
├── test_prompt_builder.py    # Test prompt builder
├── test_auth.py              # Test autenticazione Bulk API
├── test_flow.py              # Test flusso Bulk API
└── test_rate.py              # Test rate limiting

reports/
└── client-junit.xml          # Report JUnit XML

docs/
└── CLIENT_TESTS_README.md    # Questa documentazione
```

## 🚫 **Test Esclusi (Interni)**

I seguenti test sono **NON condivisibili** e sono esclusi dal pacchetto client:
- `tests_internal/`: Test per funzionalità interne
- `tests_legacy/`: Test legacy e sperimentali
- `tests/`: Test completi del repository

## 📞 **Supporto e Contatto**

Per problemi con i test o richieste di funzionalità:
- **Email**: [Inserire email supporto]
- **Repository**: [Inserire link repository]
- **Documentazione**: [Inserire link documentazione]

## 📝 **Changelog**

### **v1.0.0** (Data corrente)
- ✅ Test core Sofia Lite
- ✅ Test Bulk API
- ✅ Report JUnit XML
- ✅ Documentazione completa
- ✅ Ambiente isolato e sicuro

---

**Nota**: Questo pacchetto è progettato per essere **completamente autonomo** e **sicuro per la condivisione** con i clienti. Non contiene informazioni sensibili o codice interno.
