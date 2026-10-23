# Python rules

For Lambda handlers, shared backend code, and their tests. Also read the shared rules in [SKILL.md](SKILL.md).

## Structure

1. **Shared code goes in `common/`; one handler module per domain object,** with a route table keyed by `(method, path)`. The highest-trust routes get their own module and function.
2. **No module-level state.** Build AWS clients once in a single composition root and pass them in (`Services`, `DataStore`). Helpers take the data store as an argument. Tests hand in fakes and reset nothing. A guard test fails on any `global` or on environment reads outside the root.
3. **Use `@dataclass` for plain data; write no getters or setters.** Add a `@property` only when it computes or checks something.
4. **Never return null from an API.** Omit unset fields.

## Names and constants

5. **Use full-word names, including in DynamoDB expressions** (`:last_message`, not `:m`).
6. **Closed sets are `StrEnum`s generated from the contract.** Never hand-copy an enum. Build DynamoDB keys only through the functions in `db_keys.py`, never with ad hoc string joins.
7. **Pick units for the audience.** Miles for a US launch. Coordinates are `lat` and `lon`.

## Dependencies

8. **Prefer a maintained library to hand-rolled code** (`requests`, `geopy`). Pin runtime dependencies exactly, keep them pure Python, and ship them as a layer. A test enforces pinning and that deployed code imports only declared packages.

## Contract and validation

9. **The contract decides.** Handler routes equal the contract's routes, every response validates against the contract's schema, and whatever the schema rejects the handler rejects too. Tests check all three.
10. **Let the gateway check shapes.** Keep the rules a schema cannot express (consent, ownership, prohibited items) in code.

## Documentation

11. **Docstring shared public functions and classes,** saying what could surprise a caller: idempotency, failure behavior, what `None` means. Skip handlers (the contract documents them) and trivial one-liners. Keep them short; a guard test enforces this.

## Tests

12. **Use pytest with moto for AWS.** Name fixtures for what they hold (`moto_services`), and write test names that read as sentences.
13. **Integration tests use throwaway data and clean up after themselves,** under a role that can touch only that stage.
