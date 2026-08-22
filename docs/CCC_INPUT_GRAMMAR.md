# CCC Input Grammar — P0

Essential functions must be available without precision pointer input.

## Mouse / touch

- click / tap: select object
- explicit button: invoke a request or view
- no hidden destructive gesture
- drag/drop consequential assignment is deferred from P0

## Keyboard

- `H`: return to CCC Horizon
- `D`: open/close Command Deck
- `E`: open Evidence
- `Enter` / `Space`: inspect focused CCC Object Card
- `Escape`: close Context Lens or Command Deck
- `Tab` / `Shift+Tab`: linear browser focus order

Keyboard shortcuts do not fire while typing into text inputs, textareas, selects or editable fields.

## Focus law

Visible `:focus-visible` treatment is mandatory. State may not be conveyed by color alone. Every CCC Object Card has a textual state and keyboard focus target.

## Deferred

Gamepad, touch gestures beyond normal browser behavior, controller cycling, and advanced graph navigation are P1 after SOC live-evidence acceptance.
