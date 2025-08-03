# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 11:45:15
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 40
- **Failed:** 60
- **Success Rate:** 40.0%
- **Average Latency:** 6908ms
- **P95 Latency:** 8231ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 77.5% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 36.8%
- **ES:** 44.4%
- **FR:** 33.3%
- **HI:** 33.3%
- **IT:** 45.2%
- **UR:** 16.7%

## ❌ Top 10 Failures

- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: il tuo linguaggio viola la nostra politica. questa
- **edge_case_3** (new - it): Step 2: Expected name request, got: ciao marco! sono sofia, l'assistente virtuale di s
- **en_active_final_3** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 
- **en_active_status_1** (active - en): Step 2: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 9549ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 7046ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 8382ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 6648ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 6718ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 6725ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 7053ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 6902ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 6705ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 6812ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 6827ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 6521ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 7555ms | ❌ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 7282ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 6790ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 7167ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 6590ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 7609ms | ✅ |
| es_active_status_1 | active | es | 2 | 2/2 | 7392ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 7223ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 8372ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 8231ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 7370ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 7296ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 8494ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 6776ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 6823ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 7397ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 6742ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 7226ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 6798ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 6841ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 6921ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 6533ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 7033ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 7160ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 6755ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 6789ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 6756ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 6632ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 6801ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 6890ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 4843ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 7579ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 7174ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 6657ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 7209ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 7244ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 7659ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 7759ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 7229ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 6950ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 7169ms | ❌ |
| es_active_variant_1 | active | es | 3 | 3/3 | 7015ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 6811ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 6717ms | ❌ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 6693ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 7454ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 6517ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 6845ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 6865ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 6869ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 6625ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 6558ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 6870ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 6576ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 6559ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 6448ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 6543ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 6565ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 6504ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 6897ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 6698ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 6343ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 6771ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 6487ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 6762ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 6736ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 6767ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 6857ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 4728ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 6671ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 6591ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 6523ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 6556ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 6954ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 6620ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 6720ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 6547ms | ✅ |
| en_active_final_2 | active | en | 3 | 3/3 | 6583ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 7126ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 6825ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 6395ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 6888ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 7074ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 6486ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 6424ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 6399ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 6964ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 6818ms | ❌ |
