# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 21:50:30
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 40
- **Failed:** 60
- **Success Rate:** 40.0%
- **Average Latency:** 4811ms
- **P95 Latency:** 5661ms

## 📈 Success Rates by Type

- **New Users:** 15.0% (60 scenarios)
- **Active Users:** 77.5% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 33.3%
- **EN:** 31.6%
- **ES:** 44.4%
- **FR:** 33.3%
- **HI:** 50.0%
- **IT:** 47.6%
- **UR:** 16.7%

## ❌ Top 10 Failures

- **ar_active_final_2** (active - ar): Step 1 failed: ('Connection aborted.', RemoteDisconnected('Remote end closed connection without response'))
- **ar_new_final_1** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_final_2** (new - ar): Step 2: Expected name request, got: ciao, sono sofia, l'assistente virtuale di studio 
- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: ciao ahmed, sono sofia, l'assistente virtuale di s
- **ar_new_variant_1** (new - ar): Step 1: Expected greeting, got: buonasera! sono sofia, l'assistente virtuale di st
- **ar_new_variant_2** (new - ar): Step 2: Expected name request, got: ciao ali, sono sofia, l'assistente virtuale di stu
- **edge_case_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia, l'assistente virtuale di studio 
- **edge_case_2** (new - it): Step 1: Expected clarification, got: your language violates our policy. this conversati
- **edge_case_3** (new - it): Step 2: Expected name request, got: ciao marco, sono sofia, l'assistente virtuale di s
- **en_active_final_1** (active - en): Step 3: Expected greeting, got: grazie a te! sono sofia, l'assistente virtuale di 

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 4858ms | ❌ |
| it_new_service_1 | new | it | 5 | 5/5 | 4728ms | ✅ |
| it_new_name_1 | new | it | 4 | 4/4 | 4275ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 3/3 | 4328ms | ❌ |
| it_new_cost_1 | new | it | 3 | 3/3 | 4235ms | ❌ |
| en_new_happy_1 | new | en | 4 | 4/4 | 4209ms | ❌ |
| en_new_service_1 | new | en | 3 | 3/3 | 5544ms | ✅ |
| fr_new_happy_1 | new | fr | 3 | 3/3 | 4291ms | ❌ |
| es_new_happy_1 | new | es | 3 | 3/3 | 4308ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 2/2 | 4622ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 2/2 | 4242ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 1/1 | 4405ms | ❌ |
| it_active_status_1 | active | it | 2 | 2/2 | 5329ms | ✅ |
| it_active_new_service_1 | active | it | 2 | 2/2 | 4570ms | ✅ |
| it_active_clarify_1 | active | it | 2 | 2/2 | 4742ms | ❌ |
| en_active_status_1 | active | en | 2 | 2/2 | 4442ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 2/2 | 4260ms | ✅ |
| fr_active_status_1 | active | fr | 2 | 2/2 | 4817ms | ✅ |
| es_active_status_1 | active | es | 2 | 2/2 | 4643ms | ✅ |
| ar_active_status_1 | active | ar | 1 | 1/1 | 5083ms | ✅ |
| hi_active_status_1 | active | hi | 1 | 1/1 | 4969ms | ✅ |
| ur_active_status_1 | active | ur | 1 | 1/1 | 5071ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 4055ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 2/2 | 4231ms | ✅ |
| rapid_fire_test_1 | new | it | 4 | 4/4 | 4190ms | ✅ |
| payment_test_1 | new | it | 3 | 3/3 | 4072ms | ✅ |
| reminder_test_1 | active | it | 2 | 2/2 | 4303ms | ✅ |
| it_new_complete_1 | new | it | 7 | 7/7 | 4385ms | ❌ |
| en_new_complete_1 | new | en | 7 | 7/7 | 4376ms | ❌ |
| it_active_complete_1 | active | it | 5 | 5/5 | 4301ms | ✅ |
| en_active_complete_1 | active | en | 5 | 5/5 | 4334ms | ✅ |
| it_new_variant_1 | new | it | 3 | 3/3 | 5140ms | ❌ |
| it_new_variant_2 | new | it | 3 | 3/3 | 4543ms | ❌ |
| it_new_variant_3 | new | it | 3 | 3/3 | 4455ms | ❌ |
| it_new_variant_4 | new | it | 3 | 3/3 | 4451ms | ❌ |
| it_new_variant_5 | new | it | 3 | 3/3 | 4633ms | ❌ |
| en_new_variant_1 | new | en | 3 | 3/3 | 4441ms | ❌ |
| en_new_variant_2 | new | en | 3 | 3/3 | 4891ms | ❌ |
| en_new_variant_3 | new | en | 3 | 3/3 | 4474ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 3/3 | 4674ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 3/3 | 4443ms | ❌ |
| es_new_variant_1 | new | es | 3 | 3/3 | 4517ms | ❌ |
| es_new_variant_2 | new | es | 3 | 3/3 | 3728ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 3/3 | 4586ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 3/3 | 4635ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 3/3 | 4515ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 3/3 | 5411ms | ❌ |
| it_active_variant_1 | active | it | 3 | 3/3 | 4814ms | ✅ |
| it_active_variant_2 | active | it | 3 | 3/3 | 4652ms | ✅ |
| it_active_variant_3 | active | it | 3 | 3/3 | 4939ms | ✅ |
| en_active_variant_1 | active | en | 3 | 3/3 | 4831ms | ❌ |
| en_active_variant_2 | active | en | 3 | 3/3 | 4853ms | ✅ |
| fr_active_variant_1 | active | fr | 3 | 3/3 | 4631ms | ❌ |
| es_active_variant_1 | active | es | 3 | 3/3 | 5124ms | ✅ |
| ar_active_variant_1 | active | ar | 3 | 3/3 | 4579ms | ✅ |
| hi_active_variant_1 | active | hi | 3 | 3/3 | 4500ms | ✅ |
| ur_active_variant_1 | active | ur | 3 | 3/3 | 4468ms | ❌ |
| edge_case_1 | new | it | 2 | 2/2 | 4835ms | ❌ |
| edge_case_2 | new | it | 2 | 2/2 | 4825ms | ❌ |
| edge_case_3 | new | it | 2 | 2/2 | 4916ms | ❌ |
| mixed_edge_1 | new | it | 2 | 2/2 | 4361ms | ✅ |
| mixed_edge_2 | new | it | 2 | 2/2 | 4518ms | ✅ |
| rapid_edge_1 | new | it | 5 | 5/5 | 5034ms | ✅ |
| payment_edge_1 | new | it | 4 | 4/4 | 4599ms | ✅ |
| reminder_edge_1 | active | it | 3 | 3/3 | 4705ms | ✅ |
| it_new_long_1 | new | it | 8 | 8/8 | 4520ms | ❌ |
| en_new_long_1 | new | en | 8 | 8/8 | 4795ms | ❌ |
| it_active_long_1 | active | it | 7 | 7/7 | 4582ms | ✅ |
| en_active_long_1 | active | en | 7 | 7/7 | 4698ms | ✅ |
| it_new_final_1 | new | it | 3 | 3/3 | 4765ms | ❌ |
| it_new_final_2 | new | it | 3 | 3/3 | 4893ms | ❌ |
| it_new_final_3 | new | it | 3 | 3/3 | 5572ms | ❌ |
| it_new_final_4 | new | it | 3 | 3/3 | 4806ms | ❌ |
| it_new_final_5 | new | it | 3 | 3/3 | 5620ms | ❌ |
| en_new_final_1 | new | en | 3 | 3/3 | 4830ms | ❌ |
| en_new_final_2 | new | en | 3 | 3/3 | 4737ms | ❌ |
| en_new_final_3 | new | en | 3 | 3/3 | 5012ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 3/3 | 5202ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 3/3 | 4966ms | ❌ |
| es_new_final_1 | new | es | 3 | 3/3 | 6276ms | ❌ |
| es_new_final_2 | new | es | 3 | 3/3 | 3514ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 3/3 | 4904ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 3/3 | 4982ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 3/3 | 5646ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 3/3 | 5661ms | ❌ |
| it_active_final_1 | active | it | 3 | 3/3 | 5074ms | ✅ |
| it_active_final_2 | active | it | 3 | 3/3 | 4905ms | ✅ |
| it_active_final_3 | active | it | 3 | 3/3 | 5370ms | ✅ |
| en_active_final_1 | active | en | 3 | 3/3 | 5106ms | ❌ |
| en_active_final_2 | active | en | 3 | 3/3 | 5182ms | ✅ |
| en_active_final_3 | active | en | 3 | 3/3 | 8989ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 3/3 | 5886ms | ✅ |
| fr_active_final_2 | active | fr | 3 | 3/3 | 5295ms | ✅ |
| es_active_final_1 | active | es | 3 | 3/3 | 5581ms | ✅ |
| es_active_final_2 | active | es | 3 | 3/3 | 5005ms | ✅ |
| ar_active_final_1 | active | ar | 3 | 3/3 | 7055ms | ✅ |
| ar_active_final_2 | active | ar | 3 | 1/3 | 3518ms | ❌ |
| hi_active_final_1 | active | hi | 3 | 3/3 | 5034ms | ✅ |
| ur_active_final_1 | active | ur | 3 | 3/3 | 4811ms | ❌ |
| final_scenario_100 | new | it | 3 | 3/3 | 5389ms | ❌ |
