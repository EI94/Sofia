# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 09:16:35
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 43
- **Failed:** 57
- **Success Rate:** 43.0%
- **Average Latency:** 6208ms
- **P95 Latency:** 6932ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 85.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 42.1%
- **ES:** 44.4%
- **FR:** 22.2%
- **HI:** 50.0%
- **IT:** 47.6%
- **UR:** 33.3%

## ❌ Top 10 Failures

- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: la tua lingua viola la nostra politica. questa con
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
| it_new_happy_1 | new | it | 6 | 6/6 | 9289ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 6142ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 6126ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 5706ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 5712ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 5818ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 5805ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 6275ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 5773ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 5901ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 5965ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 5968ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 6256ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 5998ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 5745ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 6217ms | ✅ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 5920ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 6489ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 6390ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 7130ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 7400ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 6778ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 5899ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 5950ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 5798ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 5878ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 6281ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 5930ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 5922ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 5962ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 6067ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 6174ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 6514ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 6150ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 6200ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 5917ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 6113ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 6195ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 6120ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 7260ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 5972ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 5768ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 4282ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 6283ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 6371ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 6246ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 6057ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 6132ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 6033ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 6932ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 6011ms | ✅ |
| en_active_variant_2 | active | en | 3 | 3/3 | 6226ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 6051ms | ❌ |
| es_active_variant_1 | active | es | 3 | 3/3 | 6077ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 6158ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 5918ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 5978ms | ✅ |
| edge_case_1 | new | it | 2 | 2/2 | 6405ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 6077ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 6252ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 5912ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 6290ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 6181ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 6114ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 6191ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 6125ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 6257ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 6265ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 6293ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 6425ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 6471ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 6287ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 6376ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 6194ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 6453ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 6411ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 6618ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 6654ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 6498ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 6436ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 4330ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 6241ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 6756ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 6495ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 6595ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 6514ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 6340ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 6595ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 6598ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 6582ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 6001ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 5863ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 5991ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 6327ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 5951ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 6132ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 5937ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 6792ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 5978ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 5936ms | ❌ |
