# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 20:14:08
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 40
- **Failed:** 60
- **Success Rate:** 40.0%
- **Average Latency:** 4235ms
- **P95 Latency:** 5359ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 77.5% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 33.3%
- **EN:** 36.8%
- **ES:** 44.4%
- **FR:** 22.2%
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
- **edge_case_2** (new - it): Step 1: Expected clarification, got: la tua lingua viola la nostra politica. questa con
- **edge_case_3** (new - it): Step 2: Expected name request, got: ciao marco! sono sofia, l'assistente virtuale di s
- **en_active_final_1** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 4743ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 4113ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 4221ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 3675ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 3734ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 3824ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 4774ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 3998ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 4608ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 3847ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 4644ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 3976ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 4551ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 4416ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 3657ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 4318ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 3555ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 5359ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 4425ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 5414ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 6128ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 4785ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 3978ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 4029ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 3933ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 3891ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 4094ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 4084ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 3774ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 4019ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 4086ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 3783ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 4092ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 4175ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 4046ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 4030ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 3864ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 4192ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 4211ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 3929ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 4047ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 3876ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 2934ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 3855ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 4050ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 3601ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 3924ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 4081ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 4188ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 4152ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 4223ms | ✅ |
| en_active_variant_2 | active | en | 3 | 3/3 | 4309ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 4908ms | ❌ |
| es_active_variant_1 | active | es | 3 | 3/3 | 3981ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 4262ms | ❌ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 3956ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 3861ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 4373ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 4004ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 4269ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 4095ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 3956ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 3995ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 4075ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 3958ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 4077ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 4504ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 3961ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 3984ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 4408ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 4013ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 4228ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 4283ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 5833ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 4350ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 4391ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 4520ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 4317ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 3912ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 4144ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 3016ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 4359ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 5551ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 4624ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 4485ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 4651ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 4497ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 4420ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 4531ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 4429ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 4560ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 4664ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 4218ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 4712ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 4210ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 4815ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 4464ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 4112ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 4139ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 4186ms | ❌ |
