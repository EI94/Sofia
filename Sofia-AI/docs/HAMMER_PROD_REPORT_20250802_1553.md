# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 16:10:09
**Target:** https://sofia-lite-1075574333382.us-central1.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 41
- **Failed:** 59
- **Success Rate:** 41.0%
- **Average Latency:** 2090ms
- **P95 Latency:** 2878ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 80.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 31.6%
- **ES:** 44.4%
- **FR:** 44.4%
- **HI:** 50.0%
- **IT:** 45.2%
- **UR:** 16.7%

## ❌ Top 10 Failures

- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao ahmad, sono sofia, l'assistente virtuale di s
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: la tua lingua viola la nostra politica. questa con
- **edge_case_3** (new - it): Step 2: Expected name request, got: ciao marco, sono sofia, l'assistente virtuale di s
- **en_active_final_1** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 
- **en_active_final_3** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 1956ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 2226ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 2658ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 1921ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 2090ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 1679ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 2299ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 1632ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 1622ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 1702ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 1699ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 1674ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 2584ms | ❌ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 1653ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 1767ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 2182ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 1648ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 2878ms | ✅ |
| es_active_status_1 | active | es | 2 | 2/2 | 2588ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 2665ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 2785ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 2412ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 2109ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 1607ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 1851ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 1872ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 1654ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 1663ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 1593ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 2559ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 1897ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 3219ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 3311ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 1727ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 1973ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 2166ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 1935ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 3073ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 1918ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 1942ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 1846ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 1876ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 1398ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 1729ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 1741ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 1524ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 1904ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 2125ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 2074ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 2036ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 1850ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 1909ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 2230ms | ✅ |
| es_active_variant_1 | active | es | 3 | 3/3 | 1738ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 1856ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 1693ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 1633ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 1952ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 1622ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 1979ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 1893ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 1811ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 1850ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 1992ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 2085ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 1868ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 1826ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 1747ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 1886ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 2044ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 2073ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 2125ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 1883ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 3800ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 2400ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 2190ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 2218ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 2503ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 2064ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 2272ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 1623ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 2110ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 1947ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 2102ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 2572ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 2409ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 2785ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 2274ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 2273ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 2233ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 2523ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 2574ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 2120ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 2353ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 2095ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 2128ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 2170ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 2444ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 2396ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 2232ms | ❌ |
