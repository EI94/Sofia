# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 18:16:47
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 39
- **Failed:** 61
- **Success Rate:** 39.0%
- **Average Latency:** 3570ms
- **P95 Latency:** 4360ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 75.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 31.6%
- **ES:** 44.4%
- **FR:** 22.2%
- **HI:** 33.3%
- **IT:** 47.6%
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
- **en_active_final_1** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 
- **en_active_final_3** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 3405ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 3305ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 3286ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 3047ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 3275ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 3254ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 3264ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 3242ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 3177ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 3405ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 3235ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 3295ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 3976ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 3266ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 3192ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 3882ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 3030ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 3947ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 3698ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 4099ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 4529ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 4383ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 2826ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 3102ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 3118ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 3140ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 3215ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 3204ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 3106ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 4189ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 3272ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 3296ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 3299ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 3386ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 3606ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 3664ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 3701ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 3382ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 3543ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 5463ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 3336ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 3170ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 2628ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 3404ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 3390ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 3391ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 3575ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 3352ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 5123ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 3681ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 3635ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 3565ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 3851ms | ❌ |
| es_active_variant_1 | active | es | 3 | 3/3 | 3478ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 3374ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 3368ms | ❌ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 3245ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 3454ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 3307ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 3047ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 3160ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 3388ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 3405ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 3372ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 3422ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 3429ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 3462ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 3717ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 3521ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 3723ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 3854ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 3469ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 3467ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 3743ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 4311ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 3534ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 3879ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 3586ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 3620ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 4008ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 2778ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 3825ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 3514ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 3801ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 3347ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 3727ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 3667ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 3726ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 3674ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 3809ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 3551ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 3991ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 3969ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 4360ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 4299ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 4056ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 3726ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 4268ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 4176ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 3554ms | ❌ |
