# CCC v10.1 Vanguard Aesthetic System

## FACT

The original v10.1 frontend was intentionally functional and sparse: system typography, raw JSON presentation, minimal cards, a basic Canvas sphere and a basic exception-dot field. This aesthetic branch upgrades only the human control surface while preserving the v10.1 API, evidence, authority and safety contracts.

## DESIGN THESIS

CCC should not resemble a generic cyberpunk dashboard, a game HUD, or a decorative finance terminal. The control surface must feel like an institutional instrument that happens to be alive.

The visual doctrine combines five disciplines:

- **Proportion**: balanced geometric spacing, orbital relationships, disciplined negative space and visual rhythm.
- **Energy**: restrained luminous fields communicate activity, evidence and exception pressure without turning telemetry into decoration.
- **Tension**: asymmetry is used deliberately so the interface feels spatial rather than trapped in identical cards.
- **Narrative**: the eye moves from identity -> system state -> command mode -> Living Sphere -> weakest dimension -> organs -> exceptions -> authority footer.
- **Utility**: familiar controls, readable typography, responsive layouts and evidence-first labels outrank spectacle.

## VISUAL LANGUAGE

### Foundation

- Obsidian/graphite base rather than pure black.
- Platinum text for institutional legibility.
- Ion cyan for BUILD/data flow.
- Warm gold for VERIFY/attention/strategic weight.
- Emerald for proven READY/PASS states.
- Coral red for HOLD/STALE/ISOLATE/failure states.
- Violet for Exception Intelligence and exploratory signal space.

Color never independently establishes truth. Every state remains textual and data-bound.

### Geometry

- 48px atmospheric grid establishes scale without becoming a literal spreadsheet.
- 20-26px primary surface radii create a continuous instrument body.
- Orbital ellipses and concentric rings provide the central Living Sphere grammar.
- Asymmetric 1.7:0.72 hero split gives the Living Sphere dominance while preserving Mission/Pressure visibility.

### Motion

The 963ms cadence remains symbolic UI heartbeat only. Critical telemetry refresh remains independent. Motion respects `prefers-reduced-motion` and may never imply a state transition that data has not earned.

## INFORMATION HIERARCHY

1. **Identity**: Freedom Architect / CCC Living Organism.
2. **Release truth**: current VERIFY/HOLD/READY state.
3. **Command mode**: COACH / PLAN / SIMULATE / DIVE / PROCEED / PAUSE / HALT.
4. **Digital twin**: 4D Living Sphere.
5. **Pressure**: weakest dimension and next executable action.
6. **Operational organs**: SOC, Exception Intelligence, Revenue Flywheel.
7. **Alpha signals**: Exception Constellation.
8. **Authority boundary**: GitHub / Ledger / Orchestra / Human authority.

## 4D LIVING SPHERE

The Canvas fallback is promoted from a dot ring to an evidence-bound orbital instrument:

- orbital rings communicate system layers;
- node radius derives from importance/productive weight;
- brightness derives from confidence/evidence;
- lifecycle state controls semantic color;
- edge curvature shows relationship without implying physical topology;
- the central CCC core displays FACT / EVIDENCE / EXECUTION;
- X/Y/W/S semantic dimensions remain visible;
- Canvas remains the required fallback so aesthetic ambition does not create a hardware dependency.

## EXCEPTION CONSTELLATION

The constellation is a priority field, not decoration:

- horizontal placement is tied to exception score;
- radius is tied to score;
- freshness changes semantic color;
- >=90 signals receive a restrained shooting-star trail;
- labels retain type, title, score and freshness;
- no private application/customer/financial payload is rendered.

## EXECUTIVE CONTROL RULES

1. No decorative green.
2. No animation may invent telemetry.
3. No financial visual may imply realized revenue without reconciliation evidence.
4. No exception may appear high priority after freshness failure.
5. No external font/CDN dependency is required for first render.
6. Consequential actions remain approval requests only.
7. Every visual must degrade safely on the HP/Crostini target.
8. Accessibility and reduced-motion support are release gates, not optional polish.

## TEST CONTRACT

The aesthetic layer adds machine checks for:

- required CCC DOM/control IDs;
- all seven control modes;
- Vanguard identity;
- human-authority boundary text;
- reduced-motion CSS;
- semantic color tokens;
- honest UNKNOWN/HOLD telemetry fallback;
- absence of unexpected external frontend dependencies;
- enhanced Sphere Canvas rendering;
- enhanced Exception Constellation rendering;
- live dashboard root shell smoke through the existing backend.

## STATE

This branch remains **VERIFY** until GitHub CI/security/dashboard smoke passes and the interface is visually inspected on the actual HP/Crostini display. Aesthetic sophistication does not bypass physical-host evidence.
