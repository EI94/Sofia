# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 10:13:23
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 40
- **Failed:** 60
- **Success Rate:** 40.0%
- **Average Latency:** 6669ms
- **P95 Latency:** 7517ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 77.5% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 36.8%
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
- **edge_case_2** (new - it): Step 1: Expected clarification, got: la tua lingua viola la nostra politica. questa con
- **edge_case_3** (new - it): Step 2: Expected name request, got: ciao marco, sono sofia, l'assistente virtuale di s
- **en_active_final_3** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 
- **en_active_status_1** (active - en): Step 2: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 8894ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 6000ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 6233ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 5860ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 6132ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 7457ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 6742ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 6643ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 7079ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 6144ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 7468ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 5898ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 6865ms | ❌ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 5998ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 6736ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 6569ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 6333ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 6739ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 6790ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 6701ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 7624ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 7421ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 6680ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 6293ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 6258ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 6284ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 6321ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 6375ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 6356ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 6276ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 6601ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 6347ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 6878ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 6709ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 6524ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 6701ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 6273ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 6727ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 6857ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 6901ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 6930ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 6405ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 4659ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 6852ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 7061ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 6534ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 6531ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 6578ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 6517ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 6589ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 7797ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 6947ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 6508ms | ❌ |
| es_active_variant_1 | active | es | 3 | 3/3 | 6927ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 6027ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 6005ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 6470ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 6129ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 5928ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 5980ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 6203ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 6046ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 5796ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 6130ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 5994ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 6215ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 6970ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 6523ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 6506ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 6865ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 7025ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 6855ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 6827ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 7222ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 8006ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 6885ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 7174ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 7481ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 7003ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 7308ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 5010ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 7515ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 7517ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 7216ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 6759ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 6835ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 6837ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 6681ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 7103ms | ✅ |
| en_active_final_2 | active | en | 3 | 3/3 | 6965ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 7138ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 7111ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 6911ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 7038ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 6835ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 6953ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 6806ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 6489ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 6527ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 6518ms | ❌ |
