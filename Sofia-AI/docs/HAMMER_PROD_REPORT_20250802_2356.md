# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 00:33:46
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 43
- **Failed:** 57
- **Success Rate:** 43.0%
- **Average Latency:** 6008ms
- **P95 Latency:** 7228ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 85.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 33.3%
- **EN:** 47.4%
- **ES:** 44.4%
- **FR:** 33.3%
- **HI:** 50.0%
- **IT:** 47.6%
- **UR:** 16.7%

## ❌ Top 10 Failures

- **ar_active_variant_1** (active - ar): Step 3: Expected greeting, got: grazie per il tuo messaggio! sono sofia, l'assiste
- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: your language violates our policy. this conversati
- **edge_case_3** (new - it): Step 2: Expected name request, got: ciao marco! sono sofia, l'assistente virtuale di s
- **en_active_variant_1** (active - en): Step 3: Expected greeting, got: grazie per il tuo messaggio! sono sofia, l'assiste

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 6016ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 5883ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 5717ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 5307ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 5501ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 5596ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 5569ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 5809ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 5884ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 5687ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 5650ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 5653ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 6527ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 5476ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 5650ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 5982ms | ✅ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 5192ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 6149ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 6150ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 7016ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 6772ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 6761ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 5624ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 5589ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 5745ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 5394ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 5582ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 6068ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 5553ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 6808ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 5795ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 5778ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 5752ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 6391ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 5937ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 5968ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 5700ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 6115ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 6058ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 5774ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 8982ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 7798ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 4171ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 5891ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 5842ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 5528ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 5940ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 8158ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 6137ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 5943ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 6195ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 7579ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 6676ms | ✅ |
| es_active_variant_1 | active | es | 3 | 3/3 | 5665ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 5985ms | ❌ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 5654ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 5553ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 5913ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 5738ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 5763ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 5837ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 5829ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 5733ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 6055ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 6129ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 5718ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 5812ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 6130ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 5887ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 5935ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 6075ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 5976ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 6341ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 6333ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 6481ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 6237ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 6262ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 6197ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 6104ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 6173ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 4395ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 5939ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 6075ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 6125ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 5870ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 6005ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 6062ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 5954ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 6077ms | ✅ |
| en_active_final_2 | active | en | 3 | 3/3 | 5795ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 6353ms | ✅ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 5927ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 5622ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 5916ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 6014ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 6165ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 5683ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 5570ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 6067ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 7228ms | ❌ |
