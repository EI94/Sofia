# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 14:04:26
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 41
- **Failed:** 59
- **Success Rate:** 41.0%
- **Average Latency:** 6901ms
- **P95 Latency:** 8626ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 80.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 31.6%
- **ES:** 44.4%
- **FR:** 33.3%
- **HI:** 50.0%
- **IT:** 47.6%
- **UR:** 16.7%

## ❌ Top 10 Failures

- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao! sono sofia, l'assistente virtuale di studio 
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: your language violates our policy. this conversati
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
| it_new_happy_1 | new | it | 6 | 6/6 | 7744ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 6935ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 6833ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 6592ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 6774ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 6570ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 6510ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 6648ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 6441ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 6848ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 6585ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 6373ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 7263ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 6310ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 6474ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 7069ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 9208ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 7318ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 7457ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 7156ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 8062ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 7456ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 6526ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 6603ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 6674ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 6519ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 8897ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 6457ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 6559ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 6736ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 7818ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 6478ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 6644ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 6399ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 6721ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 6475ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 6479ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 6725ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 9458ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 6994ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 8626ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 6517ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 5069ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 7110ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 7060ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 6321ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 6718ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 7036ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 6957ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 7200ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 7522ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 6873ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 6469ms | ✅ |
| es_active_variant_1 | active | es | 3 | 3/3 | 6610ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 6581ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 6195ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 6562ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 6536ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 6429ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 6641ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 6676ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 6550ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 6600ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 6573ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 6596ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 6666ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 7082ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 6923ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 7588ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 6886ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 6911ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 6677ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 6751ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 6920ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 6858ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 6508ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 6820ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 7396ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 7177ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 6598ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 4616ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 6597ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 6456ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 6865ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 6479ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 6535ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 6531ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 6617ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 6748ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 6841ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 7657ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 7103ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 7074ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 7216ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 6604ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 7260ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 6807ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 10669ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 7107ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 6766ms | ❌ |
