# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 12:42:50
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 40
- **Failed:** 60
- **Success Rate:** 40.0%
- **Average Latency:** 7699ms
- **P95 Latency:** 13486ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 77.5% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 22.2%
- **EN:** 42.1%
- **ES:** 44.4%
- **FR:** 22.2%
- **HI:** 50.0%
- **IT:** 47.6%
- **UR:** 16.7%

## ❌ Top 10 Failures

- **ar_active_final_1** (active - ar): Step 2 failed: HTTPSConnectionPool(host='sofia-lite-jtcm2gle4a-uc.a.run.app', port=443): Read timed out. (read timeout=30)
- **ar_active_variant_1** (active - ar): Step 3: Expected greeting, got: grazie per il tuo messaggio! sono sofia, l'assiste
- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: la tua lingua viola la nostra politica. questa con
- **edge_case_3** (new - it): Step 2: Expected name request, got: ciao marco! sono sofia, l'assistente virtuale di s

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 7345ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 6611ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 7191ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 6660ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 6651ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 6670ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 6785ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 6485ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 6612ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 6551ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 6922ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 7743ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 7355ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 6554ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 6511ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 6920ms | ✅ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 6467ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 7692ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 6959ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 7702ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 8344ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 7890ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 6186ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 6574ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 6537ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 6300ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 6449ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 6434ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 6537ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 6697ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 6532ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 6799ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 6883ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 7751ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 6682ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 6670ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 6671ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 6921ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 6837ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 6586ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 6635ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 6881ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 4705ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 7202ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 7333ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 6896ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 6545ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 6743ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 6790ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 7171ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 7027ms | ✅ |
| en_active_variant_2 | active | en | 3 | 3/3 | 7015ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 6665ms | ✅ |
| es_active_variant_1 | active | es | 3 | 3/3 | 6756ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 7757ms | ❌ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 6567ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 6594ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 6521ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 6776ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 10372ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 6816ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 6665ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 6471ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 6356ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 7329ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 8286ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 11039ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 11642ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 12958ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 7809ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 16754ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 17401ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 8617ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 8528ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 8051ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 10086ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 12836ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 2/3 | 5055ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 8419ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 11665ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 5005ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 6816ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 15211ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 7679ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 6942ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 12042ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 6983ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 6764ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 6590ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 13486ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 6953ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 7192ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 2/3 | 13703ms | ❌ |
| es_active_final_1 | active | es | 3 | 3/3 | 7300ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 10346ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 2/3 | 4506ms | ❌ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 6376ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 6420ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 6245ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 6952ms | ❌ |
