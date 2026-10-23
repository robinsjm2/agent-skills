# CDK rules

For AWS infrastructure written with the CDK in TypeScript. Also read the shared rules in [SKILL.md](SKILL.md) and [typescript.md](typescript.md).

## Structure

1. **Model with constructs, deploy with stacks.** One construct per concern, each in its own file; the stack only wires them together.
2. **Prefer one stack.** Split only where lifecycles differ: stateful versus stateless, and one-off account-level setup such as CI roles.
3. **Protect stateful resources.** Termination protection, retain in prod, and a test that pins their logical IDs so a rename cannot replace them.
4. **Keep every per-stage setting in one config file.** Region, budget, protection, and thresholds. Design so a stage can move to its own account or region by editing that file and a few variables.
5. **Tag the whole app once** (`Application`, `Environment`) and name resources for their stage. Budgets and cost reports depend on it.

## The API

6. **Make an OpenAPI file the contract and build the API from it** with `SpecRestApi`. Write the API Gateway wiring (integrations, authorizer, request validators, CORS preflight, gateway errors) in that file, the way the AWS docs show it.
7. **Per-stage values in that file are `{{Placeholders}}`, and the CDK only fills them in.** Never add or change structure at synth time. Test that the deployed definition is the file with only the placeholders replaced.
8. **One Lambda per domain object, routes by method and path.** Give higher-trust operations such as admin their own function. Let API Gateway invoke a function only for its exact method and path.

## Packaging

9. **Ship dependencies as a `LayerVersion`.** Build them into a folder with an explicit npm script and attach with `Code.fromAsset`. No custom bundlers, no Docker fallbacks, no alpha constructs.
10. **Inject expensive inputs so unit tests stay fast.** Pass the layer code in as a prop; tests give it a stub and never run pip or touch the network.

## Security and isolation

11. **Use exact ARNs.** `*` only where AWS offers nothing narrower (X-Ray). Use separate roles for deploying and for verifying.
12. **A stage must never reach another stage.** Add a test that synthesizes every stage and fails if a policy, trust rule, or permission in one names another.
13. **Deploy from CI with OIDC and per-stage roles.** No static keys.
14. **Acknowledge a validator warning only on the exact resource, with a written reason.** Never suppress a rule globally.

## Cost and abuse

15. **Every stage gets the same guardrails:** a WAF with a per-IP rate limit, API throttles (tighter on routes that can be abused), alarms to one topic, a tagged budget, and a cost circuit breaker. Budgets only alert; the breaker is what stops spend.
16. **Make safety nets survive a deploy and be reversible.** Keep their state outside the template, and drill them (trip it, deploy while tripped, reset) before relying on them.

## Delivery

17. **Strict synth passes for every stage in CI.** Fix warnings or acknowledge them as in rule 14.
18. **Merge deploys beta, then gamma; each is verified by smoke and integration tests before the next.** Prod is a manual run with read-only smoke tests.
19. **Verify on real AWS before calling it done.** Deploy to beta, run the suites, and exercise the failure paths.
