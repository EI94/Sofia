# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 19:35:53
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 42
- **Failed:** 58
- **Success Rate:** 42.0%
- **Average Latency:** 4048ms
- **P95 Latency:** 5097ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 82.5% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 44.4%
- **EN:** 36.8%
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
- **en_active_final_3** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 
- **en_active_status_1** (active - en): Step 2: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 8586ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 3824ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 3739ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 3433ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 3589ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 3538ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 3647ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 4559ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 3599ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 3632ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 3802ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 3516ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 4124ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 3303ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 3802ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 4325ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 3686ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 4225ms | ❌ |
| es_active_status_1 | active | es | 2 | 2/2 | 4143ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 4935ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 4424ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 12438ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 3675ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 3375ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 3612ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 3470ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 3548ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 5097ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 4048ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 3801ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 3641ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 3610ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 3937ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 3945ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 4104ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 4042ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 3675ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 4013ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 3696ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 4128ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 4170ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 3766ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 2806ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 3652ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 3957ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 6143ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 3819ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 3862ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 4237ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 3868ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 3954ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 3975ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 4479ms | ✅ |
| es_active_variant_1 | active | es | 3 | 3/3 | 3684ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 3558ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 3362ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 3525ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 3843ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 3280ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 3474ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 3329ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 3648ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 3673ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 3533ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 4222ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 3573ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 3828ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 3641ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 4269ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 3797ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 6495ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 3589ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 3890ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 4088ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 4091ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 3824ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 3833ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 3877ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 3970ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 3968ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 3335ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 4649ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 3833ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 3797ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 3954ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 3992ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 4055ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 4225ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 4047ms | ✅ |
| en_active_final_2 | active | en | 3 | 3/3 | 4299ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 3720ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 4237ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 4057ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 4155ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 3595ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 3779ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 3/3 | 3779ms | ✅ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 4139ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 4405ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 3941ms | ❌ |
