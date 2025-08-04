# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-04 00:42:21
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 101
- **Passed:** 72
- **Failed:** 29
- **Success Rate:** 71.3%
- **Average Latency:** 4669ms
- **P95 Latency:** 6127ms

## 📈 Success Rates by Type

- **New Users:** 50.9% (53 scenarios)
- **Active Users:** 93.8% (48 scenarios)

## 🌍 Success Rates by Language

- **AR:** 100.0%
- **EN:** 100.0%
- **ES:** 66.7%
- **FR:** 78.6%
- **HI:** 100.0%
- **IT:** 48.9%
- **UR:** 75.0%

## ❌ Top 10 Failures

- **es_new_happy_2** (new - es): Step 2 failed: HTTPSConnectionPool(host='sofia-lite-jtcm2gle4a-uc.a.run.app', port=443): Read timed out. (read timeout=30)
- **es_new_rapid_1** (new - es): Step 2: Expected name request, got: ciao! come posso aiutarti con il tuo caso oggi?
- **fr_new_final_3** (new - fr): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **fr_new_rapid_1** (new - fr): Step 2: Expected name request, got: ciao! come posso aiutarti con il tuo caso oggi?
- **fr_new_rapid_2** (new - fr): Step 2: Expected name request, got: ciao! come posso aiutarti con il tuo caso oggi?
- **it_active_clarify_1** (active - it): Step 1: Expected clarification, got: ciao! sono sofia di studio immigrato. come ti chia
- **it_active_new_service_1** (active - it): Step 4: Expected name request, got: perfetto! per aiutarti con la cittadinanza abbiamo
- **it_loop_test_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia di studio immigrato. come ti chia
- **it_new_clarify_1** (new - it): Step 1: Expected clarification, got: ciao! sono sofia di studio immigrato. come ti chia
- **it_new_cost_1** (new - it): Step 2: Expected name request, got: perfetto! possiamo aiutarti con diversi servizi: p

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 6/6 | 5255ms | ❌ |
| it_new_service_1 | new | it | 7 | 7/7 | 5707ms | ✅ |
| it_new_name_1 | new | it | 6 | 6/6 | 5331ms | ❌ |
| it_new_clarify_1 | new | it | 4 | 4/4 | 5426ms | ❌ |
| it_new_cost_1 | new | it | 5 | 5/5 | 5614ms | ❌ |
| en_new_happy_1 | new | en | 8 | 8/8 | 6127ms | ✅ |
| en_new_service_1 | new | en | 6 | 6/6 | 5088ms | ✅ |
| fr_new_happy_1 | new | fr | 7 | 7/7 | 4734ms | ✅ |
| es_new_happy_1 | new | es | 7 | 7/7 | 4590ms | ✅ |
| ar_new_happy_1 | new | ar | 5 | 5/5 | 6512ms | ✅ |
| hi_new_happy_1 | new | hi | 3 | 3/3 | 3307ms | ✅ |
| ur_new_happy_1 | new | ur | 3 | 3/3 | 4850ms | ✅ |
| it_active_status_1 | active | it | 4 | 4/4 | 10949ms | ✅ |
| it_active_new_service_1 | active | it | 6 | 6/6 | 4968ms | ❌ |
| it_active_clarify_1 | active | it | 3 | 3/3 | 7027ms | ❌ |
| en_active_status_1 | active | en | 4 | 4/4 | 4921ms | ✅ |
| en_active_new_service_1 | active | en | 6 | 6/6 | 4876ms | ✅ |
| fr_active_status_1 | active | fr | 4 | 4/4 | 5155ms | ✅ |
| es_active_status_1 | active | es | 4 | 4/4 | 5276ms | ✅ |
| ar_active_status_1 | active | ar | 3 | 3/3 | 4826ms | ✅ |
| hi_active_status_1 | active | hi | 3 | 3/3 | 4282ms | ✅ |
| ur_active_status_1 | active | ur | 3 | 3/3 | 11026ms | ❌ |
| it_loop_test_1 | new | it | 3 | 3/3 | 5220ms | ❌ |
| mixed_lang_test_1 | new | it | 5 | 5/5 | 4397ms | ✅ |
| rapid_fire_test_1 | new | it | 6 | 6/6 | 4654ms | ❌ |
| it_new_happy_2 | new | it | 7 | 7/7 | 4876ms | ❌ |
| it_new_happy_3 | new | it | 6 | 6/6 | 4991ms | ✅ |
| it_new_happy_4 | new | it | 7 | 7/7 | 5184ms | ❌ |
| it_new_happy_5 | new | it | 6 | 6/6 | 5173ms | ✅ |
| en_new_happy_2 | new | en | 7 | 7/7 | 5112ms | ✅ |
| en_new_happy_3 | new | en | 6 | 6/6 | 4868ms | ✅ |
| fr_new_happy_2 | new | fr | 6 | 6/6 | 4375ms | ✅ |
| es_new_happy_2 | new | es | 6 | 5/6 | 4862ms | ❌ |
| ar_new_happy_2 | new | ar | 4 | 4/4 | 5283ms | ✅ |
| hi_new_happy_2 | new | hi | 3 | 3/3 | 3925ms | ✅ |
| ur_new_happy_2 | new | ur | 3 | 3/3 | 5001ms | ✅ |
| it_active_status_2 | active | it | 4 | 4/4 | 5492ms | ✅ |
| it_active_status_3 | active | it | 4 | 4/4 | 4204ms | ✅ |
| it_active_status_4 | active | it | 4 | 4/4 | 4660ms | ✅ |
| it_active_status_5 | active | it | 4 | 4/4 | 4407ms | ✅ |
| en_active_status_2 | active | en | 4 | 4/4 | 4906ms | ✅ |
| en_active_status_3 | active | en | 4 | 4/4 | 7430ms | ✅ |
| fr_active_status_2 | active | fr | 4 | 4/4 | 4776ms | ✅ |
| es_active_status_2 | active | es | 4 | 4/4 | 4838ms | ✅ |
| ar_active_status_2 | active | ar | 3 | 3/3 | 4818ms | ✅ |
| hi_active_status_2 | active | hi | 3 | 3/3 | 4621ms | ✅ |
| ur_active_status_2 | active | ur | 3 | 3/3 | 5347ms | ✅ |
| it_new_rapid_1 | new | it | 3 | 3/3 | 3258ms | ❌ |
| it_new_rapid_2 | new | it | 3 | 3/3 | 5143ms | ❌ |
| it_new_rapid_3 | new | it | 3 | 3/3 | 5001ms | ❌ |
| it_new_rapid_4 | new | it | 3 | 3/3 | 3737ms | ❌ |
| it_new_rapid_5 | new | it | 3 | 3/3 | 4185ms | ❌ |
| en_new_rapid_1 | new | en | 3 | 3/3 | 5341ms | ✅ |
| en_new_rapid_2 | new | en | 3 | 3/3 | 3064ms | ✅ |
| en_new_rapid_3 | new | en | 3 | 3/3 | 4957ms | ✅ |
| fr_new_rapid_1 | new | fr | 3 | 3/3 | 3710ms | ❌ |
| fr_new_rapid_2 | new | fr | 3 | 3/3 | 3278ms | ❌ |
| es_new_rapid_1 | new | es | 3 | 3/3 | 3926ms | ❌ |
| it_active_rapid_1 | active | it | 2 | 2/2 | 4947ms | ✅ |
| it_active_rapid_2 | active | it | 2 | 2/2 | 4373ms | ✅ |
| it_active_rapid_3 | active | it | 2 | 2/2 | 3972ms | ✅ |
| it_active_rapid_4 | active | it | 2 | 2/2 | 2735ms | ✅ |
| it_active_rapid_5 | active | it | 2 | 2/2 | 4735ms | ✅ |
| en_active_rapid_1 | active | en | 2 | 2/2 | 4703ms | ✅ |
| en_active_rapid_2 | active | en | 2 | 2/2 | 4525ms | ✅ |
| en_active_rapid_3 | active | en | 2 | 2/2 | 4486ms | ✅ |
| fr_active_rapid_1 | active | fr | 2 | 2/2 | 4719ms | ✅ |
| fr_active_rapid_2 | active | fr | 2 | 2/2 | 3110ms | ✅ |
| es_active_rapid_1 | active | es | 2 | 2/2 | 4428ms | ✅ |
| it_new_final_1 | new | it | 2 | 2/2 | 3306ms | ❌ |
| it_new_final_2 | new | it | 2 | 2/2 | 5220ms | ❌ |
| it_new_final_3 | new | it | 2 | 2/2 | 4387ms | ❌ |
| it_new_final_4 | new | it | 2 | 2/2 | 3342ms | ❌ |
| it_new_final_5 | new | it | 2 | 2/2 | 4546ms | ❌ |
| it_new_final_6 | new | it | 2 | 2/2 | 4103ms | ❌ |
| it_new_final_7 | new | it | 2 | 2/2 | 3477ms | ❌ |
| it_new_final_8 | new | it | 2 | 2/2 | 4716ms | ❌ |
| en_new_final_1 | new | en | 2 | 2/2 | 4489ms | ✅ |
| en_new_final_2 | new | en | 2 | 2/2 | 2195ms | ✅ |
| en_new_final_3 | new | en | 2 | 2/2 | 4483ms | ✅ |
| en_new_final_4 | new | en | 2 | 2/2 | 3880ms | ✅ |
| en_new_final_5 | new | en | 2 | 2/2 | 4367ms | ✅ |
| fr_new_final_1 | new | fr | 2 | 2/2 | 2924ms | ✅ |
| fr_new_final_2 | new | fr | 2 | 2/2 | 2661ms | ✅ |
| fr_new_final_3 | new | fr | 2 | 2/2 | 2258ms | ❌ |
| it_active_final_1 | active | it | 2 | 2/2 | 5153ms | ✅ |
| it_active_final_2 | active | it | 2 | 2/2 | 5119ms | ✅ |
| it_active_final_3 | active | it | 2 | 2/2 | 3855ms | ✅ |
| it_active_final_4 | active | it | 2 | 2/2 | 2774ms | ✅ |
| it_active_final_5 | active | it | 2 | 2/2 | 4583ms | ✅ |
| it_active_final_6 | active | it | 2 | 2/2 | 4771ms | ✅ |
| it_active_final_7 | active | it | 2 | 2/2 | 4615ms | ✅ |
| it_active_final_8 | active | it | 2 | 2/2 | 4501ms | ✅ |
| en_active_final_1 | active | en | 2 | 2/2 | 4225ms | ✅ |
| en_active_final_2 | active | en | 2 | 2/2 | 5461ms | ✅ |
| en_active_final_3 | active | en | 2 | 2/2 | 4710ms | ✅ |
| en_active_final_4 | active | en | 2 | 2/2 | 2895ms | ✅ |
| en_active_final_5 | active | en | 2 | 2/2 | 5389ms | ✅ |
| fr_active_final_1 | active | fr | 2 | 2/2 | 4327ms | ✅ |
| fr_active_final_2 | active | fr | 2 | 2/2 | 2495ms | ✅ |
| fr_active_final_3 | active | fr | 2 | 2/2 | 4766ms | ✅ |
