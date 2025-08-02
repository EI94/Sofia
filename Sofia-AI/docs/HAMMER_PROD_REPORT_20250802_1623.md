# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 16:43:21
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 38
- **Failed:** 62
- **Success Rate:** 38.0%
- **Average Latency:** 2718ms
- **P95 Latency:** 3498ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 72.5% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 31.6%
- **ES:** 33.3%
- **FR:** 22.2%
- **HI:** 33.3%
- **IT:** 47.6%
- **UR:** 16.7%

## ❌ Top 10 Failures

- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: your language violates our policy. this conversati
- **edge_case_3** (new - it): Step 2: Expected name request, got: ciao marco! sono sofia, l'assistente virtuale di s
- **en_active_final_1** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 
- **en_active_final_3** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 2271ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 3183ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 2466ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 2480ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 2309ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 2286ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 2205ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 2374ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 2283ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 2426ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 2286ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 2479ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 3313ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 6215ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 2630ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 2901ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 2554ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 3498ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 3324ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 2604ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 5716ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 4221ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 2425ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 2753ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 2338ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 2509ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 2482ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 2482ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 2381ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 2441ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 2562ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 2540ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 2634ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 2362ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 2445ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 3425ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 2540ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 2484ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 2558ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 2484ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 2864ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 2457ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 1973ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 2444ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 2602ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 2307ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 2427ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 3045ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 2666ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 2597ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 2798ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 2485ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 2526ms | ✅ |
| es_active_variant_1 | active | es | 3 | 3/3 | 2377ms | ❌ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 2506ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 2248ms | ❌ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 2214ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 2482ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 2105ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 2656ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 2329ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 2468ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 2438ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 2193ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 2528ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 2540ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 2389ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 2777ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 2623ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 2744ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 2652ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 2908ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 2744ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 2566ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 2868ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 4495ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 2913ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 2914ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 2811ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 2563ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 2179ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 3073ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 3037ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 2732ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 2857ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 2837ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 2773ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 2913ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 3187ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 2723ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 2858ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 3095ms | ❌ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 2637ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 2802ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 3223ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 2563ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 2448ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 2459ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 2723ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 2570ms | ❌ |
