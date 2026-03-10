# Kernel-Xiaomi-Umi

[English README](./README.md)

Kernel-Xiaomi-Umi 鏄竴涓潰鍚?Xiaomi 10锛坲mi锛夊唴鏍歌縼绉讳换鍔＄殑**缂栨帓浠撳簱**锛岀敤浜庤嚜鍔ㄥ寲鎵ц Phase2 杩佺Щ銆佹瀯寤哄皾璇曘€佽瘖鏂眹鎬讳笌宸ヤ欢鎵撳寘銆?

> 鏈粨搴?*涓嶆槸**瀹屾暣鍐呮牳婧愮爜浠撱€?

## 浠撳簱鍔熻兘

- 閫氳繃 GitHub Actions 鎵ц鍐呮牳鏋勫缓/杩佺Щ娴佺▼
- 鎵ц SO-TS 4.19 鈫?5+ 鍩虹嚎鐨?Phase2 杩佺Щ
- 鐢熸垚缁撴瀯鍖栬瘖鏂笌鍐崇瓥宸ヤ欢
- 浜у嚭鍊欓€夋墦鍖呯粨鏋滐紙鍚?AnyKernel 鍊欓€夊寘锛?

## 浠撳簱鏈€缁堢洰鏍?

- 浜у嚭 **Release 绾с€佸彲鐩存帴鍒峰叆鐨?`boot.img`**锛堥潰鍚?umi锛夈€?
- 淇濊瘉 **鍚屾満鍨嬪彲澶嶇幇**锛氱浉鍚屾満鍨?+ 鐩稿悓 workflow 杈撳叆锛屽彲鍦?GitHub Actions 绋冲畾鑷姪缂栬瘧骞朵骇鍑哄彲鍒峰啓宸ヤ欢銆?
- 鍦ㄤ繚鐣?Phase2 璇婃柇宸ヤ欢鑳藉姏鐨勫墠鎻愪笅锛屽皢浜や粯鐩爣浠庘€滃€欓€夊寘鈥濇帹杩涘埌鈥渞elease `boot.img` + 楠岃瘉娓呭崟鈥濄€?

## 涓婃父鍙傝€?

- SO-TS 鍙傝€冩簮锛歚SO-TS/android_kernel_xiaomi_sm8250`
- URL锛?https://github.com/SO-TS/android_kernel_xiaomi_sm8250>

## 宸ヤ綔娴?

### 蹇€熷紑濮嬶紙鎺ㄨ崘锛?

鍏堜互榛樿鍙傛暟杩愯 **`phase2-port-umi.yml`**锛岄殢鍚庢寜椤哄簭鏌ョ湅锛?

1. `artifacts/phase2-report.txt`
2. `artifacts/build-exit.txt`
3. `artifacts/build-error-summary.txt`
4. `artifacts/anykernel-info.txt`
5. `artifacts/next-focus.txt`

璇ラ『搴忓彲蹇€熷垽鏂湰杞槸鍚﹂€氳繃锛屼互鍙婁笅涓€姝ュ簲浼樺寲鏂瑰悜銆?

### `build-umi-kernel.yml`

鍙傝€冨紡浜戠鏋勫缓娴佺▼锛?

1. 瀹夎渚濊禆骞堕厤缃?ccache
2. 涓嬭浇 ZyC Clang 15
3. 鍏嬮殕鐩爣鍐呮牳浠撳簱/鍒嗘敮
4. 鎸夎澶囧弬鏁拌繍琛?`build.sh`锛堝彲閫?KernelSU锛?
5. 涓婁紶鏋勫缓浜х墿

杈撳叆鍙傛暟锛?

- `kernel_repo`
- `kernel_branch`
- `device`锛堥粯璁?`umi`锛?
- `ksu`锛堥粯璁?`false`锛?

### `phase2-port-umi.yml`

Phase2 杩佺Щ + 鏋勫缓 + 璇婃柇娴佺▼锛?

1. 鍑嗗 source/target 婧愮爜鏍?
2. 鎵ц Phase2 杩佺Щ
3. 鎵ц鏍稿績鏋勫缓涓?DTB 鐩爣鏋勫缓
4. 鏀堕泦宸ヤ欢骞剁敓鎴?umi 鑱氱劍鍖?
5. 鏋勫缓 AnyKernel 鍊欓€夊寘
6. 鐢熸垚姹囨€绘姤鍛婂苟涓婁紶鍏ㄩ儴宸ヤ欢

杈撳叆鍙傛暟锛?

- `source_repo`
- `source_branch`
- `target_repo`
- `target_branch`
- `device`锛堥粯璁?`umi`锛?
- `bootimg_required_bytes`锛堥粯璁?`268435456`锛屽嵆 256MiB锛?

## 鍏抽敭鑴氭湰

鏍稿績缂栨帓鑴氭湰锛?

- `tools/porting/install_ci_deps.sh`
- `tools/porting/prepare_phase2_sources.sh`
- `tools/porting/check_target_kernel_version.sh`
- `tools/porting/apply_phase2_migration.sh`
- `tools/porting/run_phase2_build.sh`
- `tools/porting/collect_phase2_artifacts.sh`
- `tools/porting/build_anykernel_candidate.sh`
- `tools/porting/write_run_meta.sh`
- `tools/porting/run_postprocess_suite.sh`

瀹屾暣鑴氭湰绱㈠紩锛?

- `tools/porting/README.md`

## Phase2 宸ヤ欢閫熻

寤鸿浼樺厛鏌ョ湅锛?

- `artifacts/phase2-report.txt`锛氬崟鏂囦欢姹囨€?
- `artifacts/build-exit.txt`锛歚defconfig_rc` / `build_rc` / `dtbs_rc`
- `artifacts/build-error-summary.txt`锛氬叧閿姤閿欐憳瑕?
- `artifacts/anykernel-info.txt`锛欰nyKernel 鍊欓€夊寘鐘舵€?
- `artifacts/next-focus.txt`锛氫笅涓€杞紭鍖栧缓璁?

琛ュ厖璇婃柇宸ヤ欢锛?

- `artifacts/make-defconfig.log`
- `artifacts/make-build.log`
- `artifacts/make-target-dtbs.log`
- `artifacts/make-dtb-manifest.log`
- `artifacts/dtb-postcheck.txt`
- `artifacts/dtb-miss-analysis.txt`
- `artifacts/phase2-metrics.json`

## 浠撳簱缁撴瀯

- `.github/workflows/`锛欳I 宸ヤ綔娴?
- `tools/porting/`锛氳縼绉讳笌璇婃柇宸ュ叿
- `porting/`锛氳鍒掋€佺洏鐐广€佹姤鍛娿€佸彉鏇磋褰?

## 鏂囨。鍏ュ彛

- 绉绘鏂囨。绱㈠紩锛歚porting/README.md`
- 鑴氭湰绱㈠紩锛歚tools/porting/README.md`
- 鑻辨枃鏂囨。锛歚README.md`

## 璐＄尞

- 涓枃璐＄尞鎸囧崡锛歚CONTRIBUTING.zh-CN.md`
- 鑻辨枃璐＄尞鎸囧崡锛歚CONTRIBUTING.md`
- 浠ｇ爜鎵€鏈夎€咃細`.github/CODEOWNERS`

## 璁稿彲璇?

鏈」鐩噰鐢?**GPL-2.0-only（GNU General Public License v2.0 only）** 璁稿彲璇侊紝璇﹁ `LICENSE`銆?

