# CDK rules

For AWS infrastructure written with the CDK in TypeScript. Also read the shared rules in [SKILL.md](SKILL.md) and [typescript.md](typescript.md).

## Structure

1. **Model with constructs, deploy with stacks.** One construct per concern, each in its own file; the stack only wires them together.
2. **Prefer one stack per lifecycle.** Split only where lifecycles differ: stateful versus stateless, and one-off account-level setup such as CI roles. The [CDK best practices](https://docs.aws.amazon.com/cdk/v2/guide/best-practices.html) say the same: keep stateful resources (tables, user pools, buckets) apart so the stateless stack can be destroyed or recreated without losing data.
3. **Protect stateful resources.** Termination protection, retain in prod, and a test that pins their logical IDs so a rename cannot replace them.
4. **Dependencies run one way: stateless to stateful.** The stateful stack must never need a value from the stateless one. Put what watches a stateful resource (its alarms, and the alert topic they publish to) in the stateful stack, beside the resource, and let the stateless stack use that topic. Constructs group by concern; they do not remove the stack boundary, and a value passed between stacks becomes a CloudFormation export and import.
5. **Removing a cross-stack reference takes two deploys.** CloudFormation updates the stateful stack first and refuses to delete an export another stack still imports. Keep the export with `exportValue` for one deploy, then delete that line in a follow-up.
6. **Keep every per-stage setting in one config file.** Region, budget, protection, and thresholds. Design so a stage can move to its own account or region by editing that file and a few variables.
7. **Tag the whole app once** (`Application`, `Environment`) and name resources for their stage. Budgets and cost reports depend on it.

## The API

8. **Make an OpenAPI file the contract and build the API from it** with `SpecRestApi`. Write the API Gateway wiring (integrations, authorizer, request validators, CORS preflight, gateway errors) in that file, the way the AWS docs show it.
9. **Per-stage values in that file are `{{Placeholders}}`, and the CDK only fills them in.** Never add or change structure at synth time. Test that the deployed definition is the file with only the placeholders replaced.
10. **One Lambda per domain object, routes by method and path.** Give higher-trust operations such as admin their own function. Let API Gateway invoke a function only for its exact method and path.

## Packaging

11. **Ship dependencies as a `LayerVersion`.** Build them into a folder with an explicit npm script and attach with `Code.fromAsset`. No custom bundlers, no Docker fallbacks, no alpha constructs.
12. **Inject expensive inputs so unit tests stay fast.** Pass the layer code in as a prop; tests give it a stub and never run pip or touch the network.

## Security and isolation

13. **Use exact ARNs.** `*` only where AWS offers nothing narrower (X-Ray). Use separate roles for deploying and for verifying.
14. **A stage must never reach another stage.** Add a test that synthesizes every stage and fails if a policy, trust rule, or permission in one names another.
15. **Deploy from CI with OIDC and per-stage roles.** No static keys.
16. **Acknowledge a validator warning only on the exact resource, with a written reason.** Never suppress a rule globally.

## Cost and abuse

Design for the nightmare bill: assume a flood, a bug or a leaked URL, and decide in advance what stops the spending.

17. **Every stage gets the same guardrails:** a WAF with a per-IP rate limit, API throttles (tighter on routes that can be abused), alarms to one topic, a tagged budget, and a cost circuit breaker. Budgets only alert and billing lags by hours; the breaker is what stops spend.
18. **Cap every function with reserved concurrency,** one per-stage number in the config file, sized with Little's law (requests per second times seconds per request) from measured traffic, and written next to the number. Reserved concurrency comes out of the account's shared pool, so add up all stages and other projects. The breaker sets it to 0 and restores the saved numbers.
19. **Put a WAF in front of every CDN too.** A CloudFront ACL is a separate resource from the API's: CLOUDFRONT scope, created in us-east-1, one per stage shared by its distributions. Alarm on bytes sent per hour (transfer is the CloudFront charge that grows fast; work out the dollars per day at the threshold) and on the ACL blocking.
20. **Limit what a caller can make you store or process, at the API.** Cap upload size and type in the signed upload's conditions, cap decoded size before decoding, and make the web copy yourself. CORS and CSP are enforced by browsers only, so they never protect an asset from direct access.
21. **Keep unprocessed uploads out of the CDN's reach.** Put originals under their own prefix with a short expiry, and add an explicit deny for the CDN on that prefix: the CDN's access control grants the whole bucket.
22. **Make safety nets survive a deploy and be reversible.** Keep their state outside the template, and drill them (trip it, deploy while tripped, reset) before relying on them. A deploy leaves a trip alone only while the standing number is unchanged, so reset before changing it.
23. **Price a guardrail before adding it,** per stage per month, and say so. Prefer the one that fits the traffic: a static CDN needs a rate limit, not managed rule groups for input it never takes.
24. **A resource that must be replaced to change, and has a fixed name, carries a hash of everything that forces replacement in its name** (a budget's limit, notifications and topics, by construct path, never by ARN). Otherwise the replacement collides with the old one.

## Delivery

25. **Strict synth passes for every stage in CI.** Fix warnings or acknowledge them as in rule 16.
26. **Merge deploys beta, then gamma; each is verified by smoke and integration tests before the next.** Prod is a manual run with read-only smoke tests.
27. **Verify on real AWS before calling it done.** Deploy to beta, run the suites, and exercise the failure paths.
28. **Deploying a branch to a shared stage puts that stage ahead of main.** The next deploy from main can then fail (for example on an export the branch added). Merge before the next main deploy, or deploy main's version back first, and say which in the PR.
