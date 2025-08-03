# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 15:29:03
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 25
- **Failed:** 75
- **Success Rate:** 25.0%
- **Average Latency:** 11080ms
- **P95 Latency:** 13367ms

## 📈 Success Rates by Type

- **New Users:** 21.7% (60 scenarios)
- **Active Users:** 30.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 22.2%
- **EN:** 36.8%
- **ES:** 22.2%
- **FR:** 22.2%
- **HI:** 33.3%
- **IT:** 19.0%
- **UR:** 33.3%

## ❌ Top 10 Failures

- **ar_active_final_1** (active - ar): Step 1: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **ar_active_final_2** (active - ar): Step 1: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **ar_active_variant_1** (active - ar): Step 1: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **ar_new_final_1** (new - ar): Step 1: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **ar_new_final_2** (new - ar): Step 1: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **ar_new_variant_2** (new - ar): Step 1: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **edge_case_1** (new - it): Step 2: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **edge_case_2** (new - it): Step 2: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 
- **edge_case_3** (new - it): Step 1: Expected greeting, got: mi dispiace, non ho capito bene. puoi specificare 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 11997ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 11385ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 11893ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 9550ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 12543ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 11281ms | ✅ |
| en_new_service_1 | new | en | 3 | 3/3 | 11268ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 11767ms | ✅ |
| es_new_happy_1 | new | es | 3 | 3/3 | 11809ms | ✅ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 11113ms | ✅ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 10892ms | ✅ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 10597ms | ✅ |
| it_active_status_1 | active | it | 2 | 2/2 | 12048ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 10666ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 11182ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 11480ms | ✅ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 11934ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 10651ms | ✅ |
| es_active_status_1 | active | es | 2 | 2/2 | 10939ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 9630ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 11439ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 11401ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 13021ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 10948ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 9626ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 9004ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 10369ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 11031ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 10898ms | ✅ |
| it_active_complete_1 | active | it | 5 | 5/5 | 10622ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 10723ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 11258ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 10640ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 9337ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 11229ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 11018ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 10835ms | ✅ |
| en_new_variant_2 | new | en | 3 | 3/3 | 10783ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 11063ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 10949ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 11121ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 10832ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 9244ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 10529ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 10931ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 10483ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 10761ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 10878ms | ❌ |
| it_active_variant_2 | active | it | 3 | 3/3 | 10895ms | ❌ |
| it_active_variant_3 | active | it | 3 | 3/3 | 10878ms | ❌ |
| en_active_variant_1 | active | en | 3 | 3/3 | 10829ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 10567ms | ❌ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 10919ms | ❌ |
| es_active_variant_1 | active | es | 3 | 3/3 | 14862ms | ❌ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 10994ms | ❌ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 12085ms | ❌ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 11014ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 10544ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 10775ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 13367ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 10854ms | ❌ |
| mixed_edge_2 | new | it | 2 | 2/2 | 10941ms | ❌ |
| rapid_edge_1 | new | it | 5 | 5/5 | 10756ms | ❌ |
| payment_edge_1 | new | it | 4 | 4/4 | 11262ms | ❌ |
| reminder_edge_1 | active | it | 3 | 3/3 | 10708ms | ❌ |
| it_new_long_1 | new | it | 8 | 8/8 | 11851ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 12713ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 10815ms | ❌ |
| en_active_long_1 | active | en | 7 | 6/7 | 9745ms | ❌ |
| it_new_final_1 | new | it | 3 | 3/3 | 13187ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 13898ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 12540ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 12361ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 12432ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 10952ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 10543ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 10653ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 10563ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 10878ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 10653ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 8850ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 10981ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 10816ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 10883ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 2/3 | 6976ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 13250ms | ❌ |
| it_active_final_2 | active | it | 3 | 3/3 | 11680ms | ❌ |
| it_active_final_3 | active | it | 3 | 3/3 | 10913ms | ❌ |
| en_active_final_1 | active | en | 3 | 2/3 | 7580ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 15591ms | ❌ |
| en_active_final_3 | active | en | 3 | 1/3 | 3802ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 11833ms | ❌ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 13624ms | ❌ |
| es_active_final_1 | active | es | 3 | 3/3 | 10868ms | ❌ |
| es_active_final_2 | active | es | 3 | 3/3 | 11215ms | ❌ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 12291ms | ❌ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 11557ms | ❌ |
| hi_active_final_1 | active | hi | 3 | 2/3 | 8970ms | ❌ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 11642ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 13084ms | ❌ |
