#!/usr/bin/env python3
"""
Script per generare il pacchetto completo dei test client
Crea un ZIP con test, documentazione, esempi e collezioni Postman
"""

import os
import json
import zipfile
import shutil
from pathlib import Path
from datetime import datetime

def create_directory_structure():
    """Crea la struttura delle directory necessarie"""
    dist_dir = Path("./dist/client_test_pack")
    
    # Rimuovi directory esistenti
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # Crea struttura
    (dist_dir / "tests_client").mkdir(parents=True, exist_ok=True)
    (dist_dir / "docs").mkdir(parents=True, exist_ok=True)
    (dist_dir / "examples").mkdir(parents=True, exist_ok=True)
    (dist_dir / "postman").mkdir(parents=True, exist_ok=True)
    
    return dist_dir

def copy_client_tests(dist_dir):
    """Copia i test client"""
    print("📁 Copiando test client...")
    
    src_tests = Path("./tests_client")
    dst_tests = dist_dir / "tests_client"
    
    if not src_tests.exists():
        raise FileNotFoundError(f"Directory tests_client non trovata: {src_tests}")
    
    # Copia tutti i file di test
    for test_file in src_tests.glob("*.py"):
        shutil.copy2(test_file, dst_tests)
        print(f"  ✅ Copiato: {test_file.name}")
    
    print(f"  📊 Copiati {len(list(dst_tests.glob('*.py')))} file di test")

def copy_documentation(dist_dir):
    """Copia la documentazione"""
    print("📚 Copiando documentazione...")
    
    src_docs = Path("./docs/CLIENT_TESTS_README.md")
    dst_docs = dist_dir / "docs"
    
    if not src_docs.exists():
        raise FileNotFoundError(f"File CLIENT_TESTS_README.md non trovato: {src_docs}")
    
    shutil.copy2(src_docs, dst_docs)
    print(f"  ✅ Copiato: {src_docs.name}")

def create_example_dataset(dist_dir):
    """Crea dataset di esempio con 5 conversazioni"""
    print("💬 Creando dataset di esempio...")
    
    example_conversations = [
        {
            "id": "conv_001",
            "language": "it",
            "user_type": "new",
            "messages": [
                {"role": "user", "content": "Ciao, vorrei prenotare una consulenza per immigrazione"},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": "Sono cittadino ucraino, ho bisogno di aiuto per il permesso di soggiorno"},
                {"role": "assistant", "content": ""}
            ],
            "expected_intents": ["GREETING", "SERVICE", "BOOKING"],
            "expected_state": "BOOKING"
        },
        {
            "id": "conv_002", 
            "language": "en",
            "user_type": "active",
            "messages": [
                {"role": "user", "content": "Hi, I need to change my appointment from tomorrow to next week"},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": "I have a work emergency and can't make it tomorrow"},
                {"role": "assistant", "content": ""}
            ],
            "expected_intents": ["STATUS", "BOOKING"],
            "expected_state": "SLOT_SELECT"
        },
        {
            "id": "conv_003",
            "language": "fr",
            "user_type": "new",
            "messages": [
                {"role": "user", "content": "Bonjour, j'ai besoin d'aide pour un visa de travail"},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": "Je suis ingénieur et j'ai une offre d'emploi en Italie"},
                {"role": "assistant", "content": ""}
            ],
            "expected_intents": ["GREETING", "SERVICE", "BOOKING"],
            "expected_state": "SERVICE"
        },
        {
            "id": "conv_004",
            "language": "es",
            "user_type": "active",
            "messages": [
                {"role": "user", "content": "Hola, ¿puedo cancelar mi cita de la próxima semana?"},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": "Tengo un problema familiar y no puedo asistir"},
                {"role": "assistant", "content": ""}
            ],
            "expected_intents": ["GREETING", "STATUS"],
            "expected_state": "SLOT_SELECT"
        },
        {
            "id": "conv_005",
            "language": "it",
            "user_type": "new",
            "messages": [
                {"role": "user", "content": "Salve, vorrei sapere i prezzi per una consulenza legale"},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": "Ho bisogno di aiuto per ricongiungimento familiare"},
                {"role": "assistant", "content": ""}
            ],
            "expected_intents": ["GREETING", "PRICE", "SERVICE"],
            "expected_state": "PRICE"
        }
    ]
    
    dataset_file = dist_dir / "examples" / "client_dataset.json"
    with open(dataset_file, 'w', encoding='utf-8') as f:
        json.dump(example_conversations, f, indent=2, ensure_ascii=False)
    
    print(f"  ✅ Creato: client_dataset.json con {len(example_conversations)} conversazioni")

def create_postman_collection(dist_dir):
    """Crea collezione Postman minima per Bulk API"""
    print("📮 Creando collezione Postman...")
    
    postman_collection = {
        "info": {
            "name": "Sofia Bulk API - Client Tests",
            "description": "Collezione Postman per testare l'API Bulk di Sofia",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [
            {
                "name": "Process Conversation",
                "request": {
                    "method": "POST",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Bearer {{BULK_API_KEY}}",
                            "type": "text"
                        },
                        {
                            "key": "Content-Type",
                            "value": "application/json",
                            "type": "text"
                        }
                    ],
                    "body": {
                        "mode": "raw",
                        "raw": "{\n  \"conversation\": {\n    \"id\": \"test_conv_001\",\n    \"language\": \"it\",\n    \"messages\": [\n      {\n        \"role\": \"user\",\n        \"content\": \"Ciao, vorrei prenotare una consulenza\"\n      },\n      {\n        \"role\": \"assistant\",\n        \"content\": \"\"\n      }\n    ]\n  }\n}"
                    },
                    "url": {
                        "raw": "{{BULK_API_BASE_URL}}/api/sofia/conversation",
                        "host": ["{{BULK_API_BASE_URL}}"],
                        "path": ["api", "sofia", "conversation"]
                    }
                }
            },
            {
                "name": "Get Conversation",
                "request": {
                    "method": "GET",
                    "header": [
                        {
                            "key": "Authorization",
                            "value": "Bearer {{BULK_API_KEY}}",
                            "type": "text"
                        }
                    ],
                    "url": {
                        "raw": "{{BULK_API_BASE_URL}}/api/sofia/conversation/{{CONVERSATION_ID}}",
                        "host": ["{{BULK_API_BASE_URL}}"],
                        "path": ["api", "sofia", "conversation", "{{CONVERSATION_ID}}"]
                    }
                }
            },
            {
                "name": "Health Check",
                "request": {
                    "method": "GET",
                    "url": {
                        "raw": "{{BULK_API_BASE_URL}}/health",
                        "host": ["{{BULK_API_BASE_URL}}"],
                        "path": ["health"]
                    }
                }
            }
        ],
        "variable": [
            {
                "key": "BULK_API_BASE_URL",
                "value": "https://sofia-bulk-api-ew1-xxxx.run.app",
                "type": "string"
            },
            {
                "key": "BULK_API_KEY",
                "value": "your-api-key-here",
                "type": "string"
            },
            {
                "key": "CONVERSATION_ID",
                "value": "test_conv_001",
                "type": "string"
            }
        ]
    }
    
    collection_file = dist_dir / "postman" / "Sofia_BulkAPI.postman_collection.json"
    with open(collection_file, 'w', encoding='utf-8') as f:
        json.dump(postman_collection, f, indent=2, ensure_ascii=False)
    
    print("  ✅ Creata: Sofia_BulkAPI.postman_collection.json")

def generate_openapi_spec(dist_dir):
    """Genera specifica OpenAPI per Bulk API"""
    print("📋 Generando specifica OpenAPI...")
    
    # Specifica OpenAPI minima basata su FastAPI
    openapi_spec = {
        "openapi": "3.0.2",
        "info": {
            "title": "Sofia Bulk API",
            "description": "API per processare conversazioni in bulk per Sofia Lite",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "https://sofia-bulk-api-ew1-xxxx.run.app",
                "description": "Production server"
            }
        ],
        "paths": {
            "/api/sofia/conversation": {
                "post": {
                    "summary": "Process Conversation",
                    "description": "Processa una conversazione e completa i messaggi assistant vuoti",
                    "security": [{"BearerAuth": []}],
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "conversation": {
                                            "type": "object",
                                            "properties": {
                                                "id": {"type": "string"},
                                                "language": {"type": "string"},
                                                "messages": {
                                                    "type": "array",
                                                    "items": {
                                                        "type": "object",
                                                        "properties": {
                                                            "role": {"type": "string"},
                                                            "content": {"type": "string"}
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Conversazione processata con successo",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "conversation_id": {"type": "string"},
                                            "processed_messages": {"type": "integer"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/sofia/conversation/{conversation_id}": {
                "get": {
                    "summary": "Get Conversation",
                    "description": "Recupera una conversazione salvata",
                    "security": [{"BearerAuth": []}],
                    "parameters": [
                        {
                            "name": "conversation_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Conversazione trovata",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "id": {"type": "string"},
                                            "status": {"type": "string"},
                                            "messages": {"type": "array"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/health": {
                "get": {
                    "summary": "Health Check",
                    "description": "Verifica lo stato del servizio",
                    "responses": {
                        "200": {
                            "description": "Servizio operativo",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "status": {"type": "string"},
                                            "timestamp": {"type": "string"}
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "securitySchemes": {
                "BearerAuth": {
                    "type": "http",
                    "scheme": "bearer",
                    "bearerFormat": "JWT"
                }
            }
        }
    }
    
    openapi_file = dist_dir / "openapi.json"
    with open(openapi_file, 'w', encoding='utf-8') as f:
        json.dump(openapi_spec, f, indent=2, ensure_ascii=False)
    
    print("  ✅ Generata: openapi.json")

def create_zip_archive(dist_dir):
    """Crea l'archivio ZIP finale"""
    print("📦 Creando archivio ZIP...")
    
    zip_path = Path("./dist/client_test_pack.zip")
    
    # Rimuovi ZIP esistente
    if zip_path.exists():
        zip_path.unlink()
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(dist_dir)
                zipf.write(file_path, arcname)
                print(f"  📁 Aggiunto: {arcname}")
    
    print(f"  ✅ Archivio creato: {zip_path}")
    return zip_path

def main():
    """Funzione principale"""
    print("🚀 Sofia Client Test Pack Builder")
    print("=" * 50)
    
    try:
        # Crea struttura directory
        dist_dir = create_directory_structure()
        
        # Copia componenti
        copy_client_tests(dist_dir)
        copy_documentation(dist_dir)
        create_example_dataset(dist_dir)
        create_postman_collection(dist_dir)
        generate_openapi_spec(dist_dir)
        
        # Crea ZIP
        zip_path = create_zip_archive(dist_dir)
        
        print("\n" + "=" * 50)
        print("🎉 PACCHETTO COMPLETATO CON SUCCESSO!")
        print(f"📦 File: {zip_path.absolute()}")
        print(f"📊 Dimensione: {zip_path.stat().st_size / 1024:.1f} KB")
        print(f"⏰ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        
        return str(zip_path.absolute())
        
    except Exception as e:
        print(f"\n❌ ERRORE: {e}")
        return None

if __name__ == "__main__":
    main()
