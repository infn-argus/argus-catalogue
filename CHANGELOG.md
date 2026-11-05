# Changelog

## v0.2.0 — 2026-10-31

- Every collection names its domain: the ARGUS packages whose workspaces its models are offered to
  (accelerator-diagnostics, accelerator-power, accelerator-rf and timing-control: accelerator; motion:
  accelerator and optics-alignment; vacuum: vacuum-cryo; it-classification: it; vendors stay for every workspace).
  Each collection's patch version is raised; no entry changed. Needs ARGUS 1.35.59 or later to validate.

## v0.1.0 — 2026-10-31

- it-classification: ARGUS metadata for the Moxa NPort and Basler camera device types INFN uses.

- 50 accelerator models in six collections (vacuum, motion, accelerator-diagnostics, accelerator-power,
  accelerator-rf, timing-control), identity only: specifications to be verified (VERIFICATION.md).
- 18 manufacturers, with the spellings found in INFN's records and NetBox's names as aliases (vendors 0.2.0).

- The repository: layout, licence (CC0-1.0), schema, and CI with the ARGUS validator. No entries yet: they are
  added with the manufacturer documents they were checked against.
