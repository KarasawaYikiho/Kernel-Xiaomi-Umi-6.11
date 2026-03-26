# Reference Driver Analysis

Author-ID discovery context: `UtsavBalar1231`, `liyafe1997` (Strawing).

## Input Summary

- SO-TS drivers scanned: `145`
- 5+ base drivers scanned: `143`
- Additional donor-reference drivers: `15`

## Delta Summary

- Reference-only buckets missing in current base: `14`
- Sample buckets: `cam_core`, `cam_cpas`, `cam_isp`, `cam_sensor_module`, `cam_sync`, `cam_utils`

## UMI Prioritization

- Primary focus bucket: `cam_sensor_module`
- Secondary sequence: `xiaomi` -> `camera/video` -> `thermal/power` -> others

## Integration Rules

1. Keep source of truth as `so_ts + base_5plus`.
2. Use donor references only for targeted deltas.
3. Require Kconfig mapping + DTS compatibility + CI gate for every imported area.
4. No blind subtree copy.
