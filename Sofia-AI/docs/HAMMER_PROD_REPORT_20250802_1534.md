# Sofia Lite - Hammer Production Test Report

**Generated:** 2025-08-02 15:41:43
**Target:** https://sofia-lite-1075574333382.us-central1.run.app
**Test Webhook:** true

## 📊 Overall Results

- **Total Scenarios:** 100
- **Passed:** 0
- **Failed:** 100
- **Success Rate:** 0.0%
- **Average Latency:** 267ms
- **P95 Latency:** 304ms

## 📈 Success Rates by Type

- **New Users:** 0.0% (60 scenarios)
- **Active Users:** 0.0% (40 scenarios)

## 🌍 Success Rates by Language

- **AR:** 0.0%
- **EN:** 0.0%
- **ES:** 0.0%
- **FR:** 0.0%
- **HI:** 0.0%
- **IT:** 0.0%
- **UR:** 0.0%

## ❌ Top 10 Failures

- **ar_active_final_1** (active - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **ar_active_final_2** (active - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **ar_active_status_1** (active - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **ar_active_variant_1** (active - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **ar_new_final_1** (new - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **ar_new_final_2** (new - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **ar_new_happy_1** (new - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **ar_new_variant_1** (new - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **ar_new_variant_2** (new - ar): Step 1 failed: HTTP 404: {"detail":"Not Found"}
- **edge_case_1** (new - it): Step 1 failed: HTTP 404: {"detail":"Not Found"}

## 🎯 Target Compliance

- **Success Rate Target:** ≥ 95%
- **P95 Latency Target:** < 1500ms
- **Current Status:** ❌ FAILED

## 📋 Detailed Results

| Scenario ID | Type | Lang | Steps | Success | Avg Latency | Journey Pass |
|-------------|------|------|-------|---------|-------------|--------------|
| it_new_happy_1 | new | it | 6 | 0/6 | 2368ms | ❌ |
| it_new_service_1 | new | it | 5 | 0/5 | 244ms | ❌ |
| it_new_name_1 | new | it | 4 | 0/4 | 239ms | ❌ |
| it_new_clarify_1 | new | it | 3 | 0/3 | 237ms | ❌ |
| it_new_cost_1 | new | it | 3 | 0/3 | 220ms | ❌ |
| en_new_happy_1 | new | en | 4 | 0/4 | 230ms | ❌ |
| en_new_service_1 | new | en | 3 | 0/3 | 239ms | ❌ |
| fr_new_happy_1 | new | fr | 3 | 0/3 | 225ms | ❌ |
| es_new_happy_1 | new | es | 3 | 0/3 | 224ms | ❌ |
| ar_new_happy_1 | new | ar | 2 | 0/2 | 226ms | ❌ |
| hi_new_happy_1 | new | hi | 2 | 0/2 | 219ms | ❌ |
| ur_new_happy_1 | new | ur | 1 | 0/1 | 233ms | ❌ |
| it_active_status_1 | active | it | 2 | 0/2 | 222ms | ❌ |
| it_active_new_service_1 | active | it | 2 | 0/2 | 229ms | ❌ |
| it_active_clarify_1 | active | it | 2 | 0/2 | 238ms | ❌ |
| en_active_status_1 | active | en | 2 | 0/2 | 240ms | ❌ |
| en_active_new_service_1 | active | en | 2 | 0/2 | 259ms | ❌ |
| fr_active_status_1 | active | fr | 2 | 0/2 | 232ms | ❌ |
| es_active_status_1 | active | es | 2 | 0/2 | 233ms | ❌ |
| ar_active_status_1 | active | ar | 1 | 0/1 | 241ms | ❌ |
| hi_active_status_1 | active | hi | 1 | 0/1 | 217ms | ❌ |
| ur_active_status_1 | active | ur | 1 | 0/1 | 223ms | ❌ |
| it_loop_test_1 | new | it | 3 | 0/3 | 238ms | ❌ |
| mixed_lang_test_1 | new | it | 2 | 0/2 | 236ms | ❌ |
| rapid_fire_test_1 | new | it | 4 | 0/4 | 235ms | ❌ |
| payment_test_1 | new | it | 3 | 0/3 | 229ms | ❌ |
| reminder_test_1 | active | it | 2 | 0/2 | 232ms | ❌ |
| it_new_complete_1 | new | it | 7 | 0/7 | 264ms | ❌ |
| en_new_complete_1 | new | en | 7 | 0/7 | 232ms | ❌ |
| it_active_complete_1 | active | it | 5 | 0/5 | 238ms | ❌ |
| en_active_complete_1 | active | en | 5 | 0/5 | 267ms | ❌ |
| it_new_variant_1 | new | it | 3 | 0/3 | 247ms | ❌ |
| it_new_variant_2 | new | it | 3 | 0/3 | 226ms | ❌ |
| it_new_variant_3 | new | it | 3 | 0/3 | 234ms | ❌ |
| it_new_variant_4 | new | it | 3 | 0/3 | 269ms | ❌ |
| it_new_variant_5 | new | it | 3 | 0/3 | 385ms | ❌ |
| en_new_variant_1 | new | en | 3 | 0/3 | 239ms | ❌ |
| en_new_variant_2 | new | en | 3 | 0/3 | 243ms | ❌ |
| en_new_variant_3 | new | en | 3 | 0/3 | 231ms | ❌ |
| fr_new_variant_1 | new | fr | 3 | 0/3 | 253ms | ❌ |
| fr_new_variant_2 | new | fr | 3 | 0/3 | 269ms | ❌ |
| es_new_variant_1 | new | es | 3 | 0/3 | 236ms | ❌ |
| es_new_variant_2 | new | es | 3 | 0/3 | 250ms | ❌ |
| ar_new_variant_1 | new | ar | 3 | 0/3 | 233ms | ❌ |
| ar_new_variant_2 | new | ar | 3 | 0/3 | 235ms | ❌ |
| hi_new_variant_1 | new | hi | 3 | 0/3 | 236ms | ❌ |
| ur_new_variant_1 | new | ur | 3 | 0/3 | 235ms | ❌ |
| it_active_variant_1 | active | it | 3 | 0/3 | 230ms | ❌ |
| it_active_variant_2 | active | it | 3 | 0/3 | 304ms | ❌ |
| it_active_variant_3 | active | it | 3 | 0/3 | 232ms | ❌ |
| en_active_variant_1 | active | en | 3 | 0/3 | 235ms | ❌ |
| en_active_variant_2 | active | en | 3 | 0/3 | 226ms | ❌ |
| fr_active_variant_1 | active | fr | 3 | 0/3 | 234ms | ❌ |
| es_active_variant_1 | active | es | 3 | 0/3 | 240ms | ❌ |
| ar_active_variant_1 | active | ar | 3 | 0/3 | 240ms | ❌ |
| hi_active_variant_1 | active | hi | 3 | 0/3 | 236ms | ❌ |
| ur_active_variant_1 | active | ur | 3 | 0/3 | 238ms | ❌ |
| edge_case_1 | new | it | 2 | 0/2 | 248ms | ❌ |
| edge_case_2 | new | it | 2 | 0/2 | 229ms | ❌ |
| edge_case_3 | new | it | 2 | 0/2 | 247ms | ❌ |
| mixed_edge_1 | new | it | 2 | 0/2 | 234ms | ❌ |
| mixed_edge_2 | new | it | 2 | 0/2 | 269ms | ❌ |
| rapid_edge_1 | new | it | 5 | 0/5 | 228ms | ❌ |
| payment_edge_1 | new | it | 4 | 0/4 | 239ms | ❌ |
| reminder_edge_1 | active | it | 3 | 0/3 | 231ms | ❌ |
| it_new_long_1 | new | it | 8 | 0/8 | 240ms | ❌ |
| en_new_long_1 | new | en | 8 | 0/8 | 233ms | ❌ |
| it_active_long_1 | active | it | 7 | 0/7 | 233ms | ❌ |
| en_active_long_1 | active | en | 7 | 0/7 | 245ms | ❌ |
| it_new_final_1 | new | it | 3 | 0/3 | 238ms | ❌ |
| it_new_final_2 | new | it | 3 | 0/3 | 249ms | ❌ |
| it_new_final_3 | new | it | 3 | 0/3 | 250ms | ❌ |
| it_new_final_4 | new | it | 3 | 0/3 | 234ms | ❌ |
| it_new_final_5 | new | it | 3 | 0/3 | 252ms | ❌ |
| en_new_final_1 | new | en | 3 | 0/3 | 263ms | ❌ |
| en_new_final_2 | new | en | 3 | 0/3 | 249ms | ❌ |
| en_new_final_3 | new | en | 3 | 0/3 | 224ms | ❌ |
| fr_new_final_1 | new | fr | 3 | 0/3 | 227ms | ❌ |
| fr_new_final_2 | new | fr | 3 | 0/3 | 260ms | ❌ |
| es_new_final_1 | new | es | 3 | 0/3 | 240ms | ❌ |
| es_new_final_2 | new | es | 3 | 0/3 | 244ms | ❌ |
| ar_new_final_1 | new | ar | 3 | 0/3 | 258ms | ❌ |
| ar_new_final_2 | new | ar | 3 | 0/3 | 238ms | ❌ |
| hi_new_final_1 | new | hi | 3 | 0/3 | 338ms | ❌ |
| ur_new_final_1 | new | ur | 3 | 0/3 | 237ms | ❌ |
| it_active_final_1 | active | it | 3 | 0/3 | 227ms | ❌ |
| it_active_final_2 | active | it | 3 | 0/3 | 300ms | ❌ |
| it_active_final_3 | active | it | 3 | 0/3 | 290ms | ❌ |
| en_active_final_1 | active | en | 3 | 0/3 | 255ms | ❌ |
| en_active_final_2 | active | en | 3 | 0/3 | 235ms | ❌ |
| en_active_final_3 | active | en | 3 | 0/3 | 350ms | ❌ |
| fr_active_final_1 | active | fr | 3 | 0/3 | 297ms | ❌ |
| fr_active_final_2 | active | fr | 3 | 0/3 | 225ms | ❌ |
| es_active_final_1 | active | es | 3 | 0/3 | 235ms | ❌ |
| es_active_final_2 | active | es | 3 | 0/3 | 240ms | ❌ |
| ar_active_final_1 | active | ar | 3 | 0/3 | 236ms | ❌ |
| ar_active_final_2 | active | ar | 3 | 0/3 | 287ms | ❌ |
| hi_active_final_1 | active | hi | 3 | 0/3 | 238ms | ❌ |
| ur_active_final_1 | active | ur | 3 | 0/3 | 279ms | ❌ |
| final_scenario_100 | new | it | 3 | 0/3 | 235ms | ❌ |
