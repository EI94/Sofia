# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 23:44:56
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 39
- **Failed:** 61
- **Success Rate:** 39.0%
- **Average Latency:** 5609ms
- **P95 Latency:** 7156ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 75.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 31.6%
- **ES:** 44.4%
- **FR:** 22.2%
- **HI:** 50.0%
- **IT:** 45.2%
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
| it_new_happy_1 | new | it | 6 | 6/6 | 5925ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 5937ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 5800ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 5772ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 5896ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 5854ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 5204ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 5465ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 5306ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 5345ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 5611ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 5064ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 7194ms | ❌ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 5545ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 7699ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 5555ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 5048ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 6020ms | ✅ |
| es_active_status_1 | active | es | 2 | 2/2 | 5976ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 4973ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 6884ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 7156ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 4725ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 4735ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 4946ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 4854ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 4727ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 4973ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 5258ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 5177ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 5279ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 5138ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 5275ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 5170ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 5332ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 5892ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 5680ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 6031ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 5331ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 5319ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 5264ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 5339ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 3779ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 5329ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 5197ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 5143ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 5256ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 5270ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 5412ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 5631ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 5568ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 5364ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 5993ms | ❌ |
| es_active_variant_1 | active | es | 3 | 3/3 | 5193ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 5440ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 5247ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 7541ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 5358ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 5157ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 5443ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 5564ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 5175ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 5198ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 6479ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 5342ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 5374ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 5434ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 5676ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 5624ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 5642ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 5619ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 8419ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 5397ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 5665ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 5767ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 5511ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 5785ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 5753ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 5416ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 5593ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 4153ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 5798ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 5798ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 5768ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 5748ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 5815ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 5725ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 5794ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 5914ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 6053ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 5643ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 6183ms | ❌ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 6482ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 5831ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 5603ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 6257ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 5624ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 5529ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 6023ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 5690ms | ❌ |
