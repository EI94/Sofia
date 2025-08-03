# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 21:05:09
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 41
- **Failed:** 59
- **Success Rate:** 41.0%
- **Average Latency:** 4664ms
- **P95 Latency:** 6171ms

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
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
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
| it_new_happy_1 | new | it | 6 | 6/6 | 6736ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 4701ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 4795ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 3976ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 6907ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 4196ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 4204ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 4319ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 4262ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 4293ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 4210ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 4494ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 4996ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 4244ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 4162ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 4647ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 4089ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 4834ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 5714ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 5878ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 6748ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 5794ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 4270ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 5758ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 4354ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 4184ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 4195ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 4407ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 4278ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 4255ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 5217ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 4329ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 4420ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 4194ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 4504ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 5221ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 4390ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 4535ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 4702ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 4394ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 6171ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 4353ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 3544ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 4392ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 4465ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 4592ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 4347ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 4912ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 4608ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 4552ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 4660ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 4539ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 4388ms | ✅ |
| es_active_variant_1 | active | es | 3 | 3/3 | 4461ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 4299ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 4161ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 4190ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 4585ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 4037ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 4570ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 4238ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 4344ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 4439ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 4201ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 7007ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 4379ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 4311ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 4565ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 4628ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 4712ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 4733ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 4494ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 4609ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 4618ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 4659ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 4561ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 4827ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 4725ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 4499ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 4510ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 3290ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 4857ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 4866ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 4707ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 4660ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 4910ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 4765ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 4635ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 4988ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 4850ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 4888ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 4819ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 5016ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 4830ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 4550ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 4671ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 4566ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 4897ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 4408ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 4570ms | ❌ |
