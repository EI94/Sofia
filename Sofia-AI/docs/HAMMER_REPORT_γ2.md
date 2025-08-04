# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 21:02:28
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 101
- **Passed:** 44
- **Failed:** 57
- **Success Rate:** 43.6%
- **Average Latency:** 5735ms
- **P95 Latency:** 8090ms

## 📈 Success Rates by Type

- **New Users:** 0.0% (53 scenarios)
- **Active Users:** 91.7% (48 scenarios)

## 🌍 Success Rates by Language

- **AR:** 50.0%
- **EN:** 41.7%
- **ES:** 50.0%
- **FR:** 50.0%
- **HI:** 50.0%
- **IT:** 40.0%
- **UR:** 50.0%

## ❌ Top 10 Failures

- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **ar_new_happy_2** (new - ar): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_active_new_service_1** (active - en): Step 4: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_active_status_3** (active - en): Step 3 failed: HTTPSConnectionPool(host='sofia-lite-jtcm2gle4a-uc.a.run.app', port=443): Read timed out. (read timeout=30)
- **en_new_final_1** (new - en): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_new_final_2** (new - en): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_new_final_3** (new - en): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_new_final_4** (new - en): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_new_final_5** (new - en): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_new_happy_1** (new - en): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 4/6 | 6556ms | ❌ |
| it_new_service_1 | new | it | 7 | 7/7 | 5905ms | ❌ |
| it_new_name_1 | new | it | 6 | 6/6 | 5842ms | ❌ |
| it_new_clarify_1 | new | it | 4 | 4/4 | 6135ms | ❌ |
| it_new_cost_1 | new | it | 5 | 4/5 | 8090ms | ❌ |
| en_new_happy_1 | new | en | 8 | 8/8 | 5752ms | ❌ |
| en_new_service_1 | new | en | 6 | 6/6 | 5407ms | ❌ |
| fr_new_happy_1 | new | fr | 7 | 7/7 | 4949ms | ❌ |
| es_new_happy_1 | new | es | 7 | 7/7 | 5031ms | ❌ |
| ar_new_happy_1 | new | ar | 5 | 5/5 | 5966ms | ❌ |
| hi_new_happy_1 | new | hi | 3 | 2/3 | 2137ms | ❌ |
| ur_new_happy_1 | new | ur | 3 | 3/3 | 11579ms | ❌ |
| it_active_status_1 | active | it | 4 | 4/4 | 5733ms | ✅ |
| it_active_new_service_1 | active | it | 6 | 6/6 | 5484ms | ❌ |
| it_active_clarify_1 | active | it | 3 | 3/3 | 5734ms | ❌ |
| en_active_status_1 | active | en | 4 | 4/4 | 5453ms | ✅ |
| en_active_new_service_1 | active | en | 6 | 6/6 | 5196ms | ❌ |
| fr_active_status_1 | active | fr | 4 | 4/4 | 5770ms | ✅ |
| es_active_status_1 | active | es | 4 | 4/4 | 5971ms | ✅ |
| ar_active_status_1 | active | ar | 3 | 3/3 | 5615ms | ✅ |
| hi_active_status_1 | active | hi | 3 | 3/3 | 6002ms | ✅ |
| ur_active_status_1 | active | ur | 3 | 3/3 | 5400ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 6429ms | ❌ |
| mixed_lang_test_1 | new | it | 5 | 5/5 | 8793ms | ❌ |
| rapid_fire_test_1 | new | it | 6 | 6/6 | 5012ms | ❌ |
| it_new_happy_2 | new | it | 7 | 7/7 | 6499ms | ❌ |
| it_new_happy_3 | new | it | 6 | 6/6 | 5852ms | ❌ |
| it_new_happy_4 | new | it | 7 | 7/7 | 9215ms | ❌ |
| it_new_happy_5 | new | it | 6 | 6/6 | 6295ms | ❌ |
| en_new_happy_2 | new | en | 7 | 7/7 | 5983ms | ❌ |
| en_new_happy_3 | new | en | 6 | 6/6 | 6200ms | ❌ |
| fr_new_happy_2 | new | fr | 6 | 5/6 | 4352ms | ❌ |
| es_new_happy_2 | new | es | 6 | 5/6 | 8447ms | ❌ |
| ar_new_happy_2 | new | ar | 4 | 4/4 | 11732ms | ❌ |
| hi_new_happy_2 | new | hi | 3 | 3/3 | 7330ms | ❌ |
| ur_new_happy_2 | new | ur | 3 | 3/3 | 6256ms | ❌ |
| it_active_status_2 | active | it | 4 | 4/4 | 6199ms | ✅ |
| it_active_status_3 | active | it | 4 | 4/4 | 6049ms | ✅ |
| it_active_status_4 | active | it | 4 | 4/4 | 6076ms | ✅ |
| it_active_status_5 | active | it | 4 | 4/4 | 4470ms | ✅ |
| en_active_status_2 | active | en | 4 | 4/4 | 6245ms | ✅ |
| en_active_status_3 | active | en | 4 | 3/4 | 7808ms | ❌ |
| fr_active_status_2 | active | fr | 4 | 4/4 | 5883ms | ✅ |
| es_active_status_2 | active | es | 4 | 4/4 | 6221ms | ✅ |
| ar_active_status_2 | active | ar | 3 | 3/3 | 6224ms | ✅ |
| hi_active_status_2 | active | hi | 3 | 3/3 | 6299ms | ✅ |
| ur_active_status_2 | active | ur | 3 | 3/3 | 6153ms | ✅ |
| it_new_rapid_1 | new | it | 3 | 3/3 | 4059ms | ❌ |
| it_new_rapid_2 | new | it | 3 | 3/3 | 6269ms | ❌ |
| it_new_rapid_3 | new | it | 3 | 3/3 | 6031ms | ❌ |
| it_new_rapid_4 | new | it | 3 | 3/3 | 4599ms | ❌ |
| it_new_rapid_5 | new | it | 3 | 3/3 | 6296ms | ❌ |
| en_new_rapid_1 | new | en | 3 | 3/3 | 6497ms | ❌ |
| en_new_rapid_2 | new | en | 3 | 3/3 | 4118ms | ❌ |
| en_new_rapid_3 | new | en | 3 | 3/3 | 6284ms | ❌ |
| fr_new_rapid_1 | new | fr | 3 | 3/3 | 4164ms | ❌ |
| fr_new_rapid_2 | new | fr | 3 | 3/3 | 4521ms | ❌ |
| es_new_rapid_1 | new | es | 3 | 3/3 | 4075ms | ❌ |
| it_active_rapid_1 | active | it | 2 | 2/2 | 6277ms | ✅ |
| it_active_rapid_2 | active | it | 2 | 2/2 | 6039ms | ✅ |
| it_active_rapid_3 | active | it | 2 | 2/2 | 6370ms | ✅ |
| it_active_rapid_4 | active | it | 2 | 2/2 | 3228ms | ✅ |
| it_active_rapid_5 | active | it | 2 | 2/2 | 5731ms | ✅ |
| en_active_rapid_1 | active | en | 2 | 2/2 | 6194ms | ✅ |
| en_active_rapid_2 | active | en | 2 | 2/2 | 6099ms | ✅ |
| en_active_rapid_3 | active | en | 2 | 2/2 | 6565ms | ✅ |
| fr_active_rapid_1 | active | fr | 2 | 2/2 | 5876ms | ✅ |
| fr_active_rapid_2 | active | fr | 2 | 2/2 | 3164ms | ✅ |
| es_active_rapid_1 | active | es | 2 | 2/2 | 6469ms | ✅ |
| it_new_final_1 | new | it | 2 | 2/2 | 3013ms | ❌ |
| it_new_final_2 | new | it | 2 | 2/2 | 5967ms | ❌ |
| it_new_final_3 | new | it | 2 | 2/2 | 6556ms | ❌ |
| it_new_final_4 | new | it | 2 | 2/2 | 3234ms | ❌ |
| it_new_final_5 | new | it | 2 | 2/2 | 5605ms | ❌ |
| it_new_final_6 | new | it | 2 | 2/2 | 6582ms | ❌ |
| it_new_final_7 | new | it | 2 | 2/2 | 4754ms | ❌ |
| it_new_final_8 | new | it | 2 | 2/2 | 5549ms | ❌ |
| en_new_final_1 | new | en | 2 | 2/2 | 5525ms | ❌ |
| en_new_final_2 | new | en | 2 | 2/2 | 3020ms | ❌ |
| en_new_final_3 | new | en | 2 | 2/2 | 6997ms | ❌ |
| en_new_final_4 | new | en | 2 | 2/2 | 3487ms | ❌ |
| en_new_final_5 | new | en | 2 | 2/2 | 5265ms | ❌ |
| fr_new_final_1 | new | fr | 2 | 2/2 | 3768ms | ❌ |
| fr_new_final_2 | new | fr | 2 | 2/2 | 3488ms | ❌ |
| fr_new_final_3 | new | fr | 2 | 2/2 | 3511ms | ❌ |
| it_active_final_1 | active | it | 2 | 2/2 | 5622ms | ✅ |
| it_active_final_2 | active | it | 2 | 2/2 | 5479ms | ✅ |
| it_active_final_3 | active | it | 2 | 2/2 | 6047ms | ✅ |
| it_active_final_4 | active | it | 2 | 2/2 | 3010ms | ✅ |
| it_active_final_5 | active | it | 2 | 2/2 | 5391ms | ✅ |
| it_active_final_6 | active | it | 2 | 2/2 | 5725ms | ✅ |
| it_active_final_7 | active | it | 2 | 2/2 | 6076ms | ✅ |
| it_active_final_8 | active | it | 2 | 2/2 | 6732ms | ✅ |
| en_active_final_1 | active | en | 2 | 2/2 | 5566ms | ✅ |
| en_active_final_2 | active | en | 2 | 2/2 | 6979ms | ✅ |
| en_active_final_3 | active | en | 2 | 2/2 | 6437ms | ✅ |
| en_active_final_4 | active | en | 2 | 2/2 | 3884ms | ✅ |
| en_active_final_5 | active | en | 2 | 2/2 | 5995ms | ✅ |
| fr_active_final_1 | active | fr | 2 | 2/2 | 6285ms | ✅ |
| fr_active_final_2 | active | fr | 2 | 2/2 | 3287ms | ✅ |
| fr_active_final_3 | active | fr | 2 | 2/2 | 5747ms | ✅ |
