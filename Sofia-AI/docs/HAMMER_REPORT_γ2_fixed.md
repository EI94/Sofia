# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-03 22:15:07
**Target:** https://sofia-lite-jtcm2gle4a-uc.a.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 101
- **Passed:** 41
- **Failed:** 60
- **Success Rate:** 40.6%
- **Average Latency:** 5618ms
- **P95 Latency:** 8235ms

## 📈 Success Rates by Type

- **New Users:** 0.0% (53 scenarios)
- **Active Users:** 85.4% (48 scenarios)

## 🌍 Success Rates by Language

- **AR:** 50.0%
- **EN:** 41.7%
- **ES:** 33.3%
- **FR:** 50.0%
- **HI:** 25.0%
- **IT:** 37.8%
- **UR:** 50.0%

## ❌ Top 10 Failures

- **ar_new_happy_1** (new - ar): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **ar_new_happy_2** (new - ar): Step 2: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_active_new_service_1** (active - en): Step 4: Expected name request, got: mi dispiace, c'è stato un errore nel processare il
- **en_active_status_1** (active - en): Step 1 failed: HTTPSConnectionPool(host='sofia-lite-jtcm2gle4a-uc.a.run.app', port=443): Read timed out. (read timeout=30)
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
| it_new_happy_1 | new | it | 6 | 6/6 | 5760ms | ❌ |
| it_new_service_1 | new | it | 7 | 6/7 | 8104ms | ❌ |
| it_new_name_1 | new | it | 6 | 6/6 | 8511ms | ❌ |
| it_new_clarify_1 | new | it | 4 | 4/4 | 5837ms | ❌ |
| it_new_cost_1 | new | it | 5 | 5/5 | 6630ms | ❌ |
| en_new_happy_1 | new | en | 8 | 7/8 | 8137ms | ❌ |
| en_new_service_1 | new | en | 6 | 6/6 | 4943ms | ❌ |
| fr_new_happy_1 | new | fr | 7 | 6/7 | 6127ms | ❌ |
| es_new_happy_1 | new | es | 7 | 7/7 | 4979ms | ❌ |
| ar_new_happy_1 | new | ar | 5 | 5/5 | 5714ms | ❌ |
| hi_new_happy_1 | new | hi | 3 | 2/3 | 3729ms | ❌ |
| ur_new_happy_1 | new | ur | 3 | 3/3 | 6132ms | ❌ |
| it_active_status_1 | active | it | 4 | 3/4 | 9747ms | ❌ |
| it_active_new_service_1 | active | it | 6 | 5/6 | 8281ms | ❌ |
| it_active_clarify_1 | active | it | 3 | 3/3 | 6479ms | ❌ |
| en_active_status_1 | active | en | 4 | 3/4 | 7772ms | ❌ |
| en_active_new_service_1 | active | en | 6 | 6/6 | 4703ms | ❌ |
| fr_active_status_1 | active | fr | 4 | 4/4 | 5836ms | ✅ |
| es_active_status_1 | active | es | 4 | 4/4 | 5234ms | ✅ |
| ar_active_status_1 | active | ar | 3 | 3/3 | 5905ms | ✅ |
| hi_active_status_1 | active | hi | 3 | 3/3 | 5405ms | ✅ |
| ur_active_status_1 | active | ur | 3 | 3/3 | 5729ms | ✅ |
| it_loop_test_1 | new | it | 3 | 3/3 | 5939ms | ❌ |
| mixed_lang_test_1 | new | it | 5 | 5/5 | 5585ms | ❌ |
| rapid_fire_test_1 | new | it | 6 | 6/6 | 7102ms | ❌ |
| it_new_happy_2 | new | it | 7 | 7/7 | 5576ms | ❌ |
| it_new_happy_3 | new | it | 6 | 6/6 | 5685ms | ❌ |
| it_new_happy_4 | new | it | 7 | 7/7 | 5857ms | ❌ |
| it_new_happy_5 | new | it | 6 | 6/6 | 5638ms | ❌ |
| en_new_happy_2 | new | en | 7 | 7/7 | 5656ms | ❌ |
| en_new_happy_3 | new | en | 6 | 6/6 | 5812ms | ❌ |
| fr_new_happy_2 | new | fr | 6 | 6/6 | 4808ms | ❌ |
| es_new_happy_2 | new | es | 6 | 6/6 | 5807ms | ❌ |
| ar_new_happy_2 | new | ar | 4 | 4/4 | 5759ms | ❌ |
| hi_new_happy_2 | new | hi | 3 | 2/3 | 8235ms | ❌ |
| ur_new_happy_2 | new | ur | 3 | 3/3 | 5629ms | ❌ |
| it_active_status_2 | active | it | 4 | 4/4 | 5851ms | ✅ |
| it_active_status_3 | active | it | 4 | 4/4 | 5485ms | ✅ |
| it_active_status_4 | active | it | 4 | 4/4 | 5709ms | ✅ |
| it_active_status_5 | active | it | 4 | 4/4 | 4216ms | ✅ |
| en_active_status_2 | active | en | 4 | 4/4 | 7194ms | ✅ |
| en_active_status_3 | active | en | 4 | 4/4 | 11834ms | ✅ |
| fr_active_status_2 | active | fr | 4 | 4/4 | 5652ms | ✅ |
| es_active_status_2 | active | es | 4 | 3/4 | 4290ms | ❌ |
| ar_active_status_2 | active | ar | 3 | 3/3 | 11373ms | ✅ |
| hi_active_status_2 | active | hi | 3 | 2/3 | 3400ms | ❌ |
| ur_active_status_2 | active | ur | 3 | 3/3 | 6256ms | ✅ |
| it_new_rapid_1 | new | it | 3 | 3/3 | 3803ms | ❌ |
| it_new_rapid_2 | new | it | 3 | 3/3 | 5790ms | ❌ |
| it_new_rapid_3 | new | it | 3 | 3/3 | 5153ms | ❌ |
| it_new_rapid_4 | new | it | 3 | 3/3 | 4207ms | ❌ |
| it_new_rapid_5 | new | it | 3 | 3/3 | 5526ms | ❌ |
| en_new_rapid_1 | new | en | 3 | 3/3 | 5579ms | ❌ |
| en_new_rapid_2 | new | en | 3 | 3/3 | 3783ms | ❌ |
| en_new_rapid_3 | new | en | 3 | 3/3 | 5586ms | ❌ |
| fr_new_rapid_1 | new | fr | 3 | 3/3 | 3427ms | ❌ |
| fr_new_rapid_2 | new | fr | 3 | 3/3 | 4323ms | ❌ |
| es_new_rapid_1 | new | es | 3 | 3/3 | 3719ms | ❌ |
| it_active_rapid_1 | active | it | 2 | 2/2 | 5661ms | ✅ |
| it_active_rapid_2 | active | it | 2 | 2/2 | 5374ms | ✅ |
| it_active_rapid_3 | active | it | 2 | 2/2 | 6326ms | ✅ |
| it_active_rapid_4 | active | it | 2 | 2/2 | 3079ms | ✅ |
| it_active_rapid_5 | active | it | 2 | 2/2 | 5595ms | ✅ |
| en_active_rapid_1 | active | en | 2 | 2/2 | 5828ms | ✅ |
| en_active_rapid_2 | active | en | 2 | 2/2 | 5562ms | ✅ |
| en_active_rapid_3 | active | en | 2 | 2/2 | 6351ms | ✅ |
| fr_active_rapid_1 | active | fr | 2 | 2/2 | 5614ms | ✅ |
| fr_active_rapid_2 | active | fr | 2 | 2/2 | 3052ms | ✅ |
| es_active_rapid_1 | active | es | 2 | 2/2 | 7952ms | ✅ |
| it_new_final_1 | new | it | 2 | 2/2 | 3309ms | ❌ |
| it_new_final_2 | new | it | 2 | 2/2 | 6314ms | ❌ |
| it_new_final_3 | new | it | 2 | 2/2 | 5944ms | ❌ |
| it_new_final_4 | new | it | 2 | 2/2 | 3105ms | ❌ |
| it_new_final_5 | new | it | 2 | 2/2 | 6987ms | ❌ |
| it_new_final_6 | new | it | 2 | 2/2 | 5592ms | ❌ |
| it_new_final_7 | new | it | 2 | 2/2 | 3261ms | ❌ |
| it_new_final_8 | new | it | 2 | 2/2 | 6535ms | ❌ |
| en_new_final_1 | new | en | 2 | 2/2 | 6575ms | ❌ |
| en_new_final_2 | new | en | 2 | 2/2 | 3180ms | ❌ |
| en_new_final_3 | new | en | 2 | 2/2 | 5299ms | ❌ |
| en_new_final_4 | new | en | 2 | 2/2 | 2991ms | ❌ |
| en_new_final_5 | new | en | 2 | 2/2 | 5938ms | ❌ |
| fr_new_final_1 | new | fr | 2 | 2/2 | 2977ms | ❌ |
| fr_new_final_2 | new | fr | 2 | 2/2 | 3325ms | ❌ |
| fr_new_final_3 | new | fr | 2 | 2/2 | 3390ms | ❌ |
| it_active_final_1 | active | it | 2 | 2/2 | 6081ms | ✅ |
| it_active_final_2 | active | it | 2 | 2/2 | 5945ms | ✅ |
| it_active_final_3 | active | it | 2 | 2/2 | 5758ms | ✅ |
| it_active_final_4 | active | it | 2 | 2/2 | 2980ms | ✅ |
| it_active_final_5 | active | it | 2 | 2/2 | 6773ms | ✅ |
| it_active_final_6 | active | it | 2 | 2/2 | 6045ms | ✅ |
| it_active_final_7 | active | it | 2 | 2/2 | 6628ms | ✅ |
| it_active_final_8 | active | it | 2 | 2/2 | 6054ms | ✅ |
| en_active_final_1 | active | en | 2 | 2/2 | 6039ms | ✅ |
| en_active_final_2 | active | en | 2 | 2/2 | 5438ms | ✅ |
| en_active_final_3 | active | en | 2 | 2/2 | 6342ms | ✅ |
| en_active_final_4 | active | en | 2 | 2/2 | 3040ms | ✅ |
| en_active_final_5 | active | en | 2 | 2/2 | 5620ms | ✅ |
| fr_active_final_1 | active | fr | 2 | 2/2 | 6171ms | ✅ |
| fr_active_final_2 | active | fr | 2 | 2/2 | 2997ms | ✅ |
| fr_active_final_3 | active | fr | 2 | 2/2 | 5414ms | ✅ |
