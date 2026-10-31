# ARGUS catalogue

Reusable, versioned definitions of the equipment ARGUS Knowledge Hub tracks: **manufacturers** and **product
models** — pumps, gauges, power supplies, DAQ systems, ADCs, motion controllers, cameras and the rest of the
accelerator's commercial equipment. ARGUS installs a pinned release of this repository into its shared catalogue
workspace, where every workspace's units point at the same Product Model records.

IT devices (switches, serial device servers, servers…) are defined in the NetBox Device Type Library format, in
the fork [`infn-argus/devicetype-library`](https://github.com/infn-argus/devicetype-library), so that suitable
additions can go back upstream. This repository holds the ARGUS side of those models — device class, the ARGUS
object type of their units, end of life, successor — never their physical definition.

The design, and how ARGUS installs, adopts and upgrades from these collections, is in
[`docs/catalogue-collections.md`](https://github.com/infn-argus/argus-knowledge-hub/blob/main/docs/catalogue-collections.md)
of the ARGUS repository.

## What goes here, and what never does

- **Here:** what is true of a product wherever it is installed — the manufacturer's model code and part number,
  typed specifications with units, the datasheet, end of life, successors and compatible models, and the
  evidence each value comes from.
- **Never:** serial numbers, inventory numbers, installed units, locations, sellers, prices, contracts, people,
  or any other site data. The validator refuses keys it does not know, so there is nowhere to put them.
- **No invented values.** A model's specifications cite the manufacturer document they were checked against
  (`sources`, with the date). A value that cannot be checked is left out.
- **Identity first.** The first entries carry only what identifies a product — manufacturer, model code, name,
  device class — taken from the records of the INFN installation that uses them, with a source note saying
  their specifications are not yet verified. Specifications are added entry by entry, from the manufacturer's
  datasheet, and the note goes. [`VERIFICATION.md`](VERIFICATION.md) lists what is still waiting.

## Layout

```
collections/
  vendors/                  every manufacturer, once (IT and accelerator); NetBox manufacturer names as aliases
  <domain>/                 vacuum, accelerator-power, accelerator-diagnostics, daq, motion, … (added with
    collection.yaml         their first verified entries)
    models.yaml
schema/                     the format as JSON Schema, for editors
.github/workflows/          CI: the ARGUS validator, on every pull request and release
```

## Identity

- A vendor id is a slug (`pfeiffer-vacuum`). A model id is `vendor/model-slug` (`pfeiffer-vacuum/tpg-366`).
- **One commercial model, one entry,** across this repository and the NetBox fork together: a model the NetBox
  library defines is never defined again here. The validator checks every collection of both sources at once:
  an id used twice, two vendors that are one company, two entries with the same vendor and model code.
- Ids are never reused or renamed. A rename keeps the old id in `former_ids`; an entry leaves only by
  `retired: {since, reason, replaced_by}` or by moving to another collection (`moved` in the old one,
  `transferred_from` in the new). Absence never retires anything: a release that drops an entry is refused.

## Releases

Each release is a tag `vX.Y.Z`, with its changes in `CHANGELOG.md`. A collection's own `version` goes up when
its content changes. ARGUS pins a release by tag and commit, and records each collection's checksum when it
installs it; an upgrade is previewed, and a value a site keeps locally is never overwritten.

## Contributing an entry

1. Add the vendor to `collections/vendors/vendors.yaml` if it is not there.
2. Add the model to the collection of its domain, with `sources` naming the manufacturer document checked.
3. Open a pull request: CI validates it with the ARGUS validator, together with the previous release.

A correction found in ARGUS (a site that knows a value is wrong) arrives as a patch against the entry's file,
for the same review.

## Licence

[CC0 1.0](LICENSE), like the NetBox Device Type Library, so entries can move between the two without friction.
