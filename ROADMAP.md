# Cutlist optimizer roadmap

## Phase 0 — Scaffold (done Sep 28, 2026)
- [x] Greedy guillotine packer (best-area-fit, rotation, kerf)
- [x] Waste % reporting, SVG cut diagrams, CLI, pytest suite
- [x] README, MIT license, milestones

## Phase 1 — Smarter solver (~3 weekends)
- [ ] MaxRects packer alongside greedy
- [ ] A/B comparison harness: run both, report waste deltas on sample cut lists
- [ ] Grain-direction constraints (parts locked to an axis)

## Phase 2 — Usable tool
- [ ] Web UI (Next.js, pairs with the Boxwise stack)
- [ ] Save/load projects (JSON), printable cut list
- [ ] Publish to PyPI as `cutlist-optimizer`

## Phase 3 — Launch
- [ ] Dogfood on a real build (bookshelf? workbench?)
- [ ] Launch post with before/after waste numbers
