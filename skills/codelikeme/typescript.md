# TypeScript rules

Nearly all the TypeScript steering so far was about CDK code and its tests, so this list is short. Add web-client rules when that work happens. Also read the shared rules in [SKILL.md](SKILL.md), and [cdk.md](cdk.md) for infrastructure.

1. **Use full-word names:** `operation`, `template`, `config`, not `op`, `t`, `cfg`.
2. **Import the CDK by subpath and namespace** (`import * as lambda from 'aws-cdk-lib/aws-lambda'`). That is fine: CDK code runs at synth time and never ships. Code that is bundled and shipped is different; avoid barrel imports there.
3. **Write constructs as classes with a typed props interface** and a doc comment saying what they own. Stacks only compose them.
4. **Keep pure logic in plain modules** (reading the contract, filling placeholders) so tests do not need a synth.
5. **Test with Jest and `aws-cdk-lib/assertions`.** Read the real contract file in tests instead of copying expected values. Name each test for the rule it protects, and add guard tests for invariants (stateful logical IDs, stage isolation, nothing sets reserved concurrency).
6. **Never hand-write API types for a client.** Generate them from the contract (`openapi-typescript`) and fail CI when the generated files are stale.
7. **Make build steps explicit npm scripts** (`build:layer`, `synth`, `deploy`), not hidden hooks.
8. **Keep `tsc --noEmit` clean** alongside strict synth.
