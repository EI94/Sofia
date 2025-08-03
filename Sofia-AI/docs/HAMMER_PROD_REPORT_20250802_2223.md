# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 22:56:45
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 39
- **Failed:** 61
- **Success Rate:** 39.0%
- **Average Latency:** 5283ms
- **P95 Latency:** 6466ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 75.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 31.6%
- **ES:** 44.4%
- **FR:** 33.3%
- **HI:** 50.0%
- **IT:** 42.9%
- **UR:** 16.7%

## ❌ Top 10 Failures

- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao! sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: il tuo linguaggio viola la nostra policy. questa c
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
| it_new_happy_1 | new | it | 6 | 6/6 | 7672ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 5338ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 5000ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 4762ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 5304ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 5008ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 5388ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 5161ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 5226ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 4658ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 4650ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 5046ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 8081ms | ❌ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 5215ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 4442ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 5144ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 4909ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 5040ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 6890ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 6115ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 5514ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 6131ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 4751ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 4603ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 5244ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 4661ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 4540ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 4605ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 4834ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 4993ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 5065ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 4888ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 4934ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 5068ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 4971ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 5182ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 4811ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 5318ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 5136ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 5674ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 4825ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 5152ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 3744ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 4927ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 5037ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 5008ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 5063ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 5174ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 5215ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 5359ms | ❌ |
| en_active_variant_1 | active | en | 3 | 3/3 | 5391ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 5186ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 5115ms | ✅ |
| es_active_variant_1 | active | es | 3 | 3/3 | 5208ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 5061ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 5256ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 5244ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 5156ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 5387ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 5093ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 5235ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 5104ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 5037ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 5036ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 6466ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 5307ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 5415ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 5332ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 5115ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 5698ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 5195ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 5157ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 5302ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 5398ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 5600ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 5209ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 6788ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 5438ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 5405ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 5436ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 3770ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 5091ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 5240ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 5844ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 5284ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 6388ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 5663ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 5655ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 5346ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 5449ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 5432ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 5718ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 5242ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 5431ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 5363ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 5366ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 5182ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 5684ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 5484ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 5380ms | ❌ |
