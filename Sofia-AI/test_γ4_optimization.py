#!/usr/bin/env python3
"""
Test Rapido - Verifica Ottimizzazioni γ4
"""

import asyncio
import time
import aiohttp
import json
from datetime import datetime

async def test_latency_optimization():
    """Testa la riduzione della latency dopo le ottimizzazioni γ4"""
    
    url = "https://sofia-lite-1075574333382.us-central1.run.app/webhook/whatsapp"
    
    test_cases = [
        "Ciao, mi chiamo Mario Rossi",
        "Bonjour, je m'appelle Jean-Pierre Dubois", 
        "Hola, me llamo María José García",
        "Hi, I'm John Smith",
        "مرحبا، اسمي أحمد محمد",
        "नमस्ते, मेरा नाम राजेश कुमार है",
        "হ্যালো, আমার নাম রাহুল দাস",
        "Merhaba, benim adım Ahmet Yılmaz",
        "Привет, меня зовут Александр Иванов"
    ]
    
    print("🚀 Test Ottimizzazioni γ4 - Verifica Latency")
    print("="*60)
    
    results = []
    
    async with aiohttp.ClientSession() as session:
        for i, message in enumerate(test_cases, 1):
            try:
                start_time = time.time()
                
                payload = {
                    "Body": message,
                    "From": f"whatsapp:+39333{i:03d}4567"
                }
                
                async with session.post(url, json=payload, timeout=10) as response:
                    response_time = (time.time() - start_time) * 1000  # Converti in ms
                    
                    if response.status == 200:
                        print(f"✅ {i}. {message[:30]}... | {response_time:.0f}ms")
                        results.append(response_time)
                    else:
                        print(f"❌ {i}. {message[:30]}... | {response.status} | {response_time:.0f}ms")
                        
            except Exception as e:
                print(f"❌ {i}. {message[:30]}... | Errore: {str(e)}")
    
    if results:
        avg_latency = sum(results) / len(results)
        max_latency = max(results)
        min_latency = min(results)
        
        print(f"\n📊 RISULTATI LATENCY:")
        print(f"   • Media: {avg_latency:.0f}ms")
        print(f"   • Min: {min_latency:.0f}ms")
        print(f"   • Max: {max_latency:.0f}ms")
        print(f"   • Test riusciti: {len(results)}/{len(test_cases)}")
        
        # Verifica obblighi γ4
        p95_estimate = max_latency  # Approssimazione
        success_ok = len(results) == len(test_cases)
        p95_ok = p95_estimate < 2500
        
        print(f"\n🎯 VERIFICA OBBLIGHI γ4:")
        print(f"   • Success ≥ 95%: {len(results)/len(test_cases)*100:.1f}% {'✅' if success_ok else '❌'}")
        print(f"   • P95 < 2500ms: {p95_estimate:.0f}ms {'✅' if p95_ok else '❌'}")
        
        if success_ok and p95_ok:
            print(f"\n🎉 ✅ OTTIMIZZAZIONI γ4 SUCCESSO!")
        else:
            print(f"\n❌ OTTIMIZZAZIONI γ4 INSUFFICIENTI")
            
        return success_ok and p95_ok
    else:
        print("❌ Nessun test riuscito")
        return False

async def main():
    """Funzione principale"""
    return await test_latency_optimization()

if __name__ == "__main__":
    asyncio.run(main()) 