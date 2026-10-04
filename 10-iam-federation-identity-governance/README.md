# 10 -- IAM Federation & Identity Governance

## What this does
Runs Keycloak in Docker as a self-hosted identity provider and demonstrates:
- OIDC: a full authorization code flow done by hand (code, then token exchange, then inspecting the JWT)
- SAML: a registered SAML client and exported IdP metadata
- Identity governance: joiner/mover/leaver automation in Python against Keycloak's Admin REST API

## Stack
Keycloak (Docker), OAuth 2.0 / OIDC, SAML 2.0, SCIM v2 concepts, Python (requests), NIST 800-53

## Lifecycle automation mapped to SCIM
| lifecycle.py function | Keycloak Admin API | SCIM v2 equivalent |
|---|---|---|
| onboard_joiner() | POST /users, PUT /users/{id}/groups/{gid} | POST /Users |
| move_user() | DELETE then PUT group membership | PATCH /Users/{id} |
| offboard_leaver() | PUT /users/{id} {enabled: false} | PATCH /Users/{id} (active: false) |

## Controls addressed
- NIST 800-53 AC-2 (Account Management): automated create, modify and disable
- NIST 800-53 IA-4 (Identifier Management): consistent identifiers and disablement of leavers

## OIDC vs SAML (what I observed)
- OIDC returned JSON/JWT tokens; the ID token carried who (sub, preferred_username), the access token carried what (roles).
- SAML uses signed XML; the IdP metadata file lists the entity ID, signing certificate and SSO endpoints.

## Real issues hit
- Authorization codes are single-use and expire in 60 seconds: I raised Client login timeout to 5 minutes for the lab.
- A pasted placeholder code and a stale client secret each caused invalid_grant and unauthorized_client errors.
- The master-realm admin does not exist in the portfolio realm: login needed a user created in that realm.
- Group names must match exactly (lowercase) or the Admin API lookup fails.

## Reproduce it
cp .env.example .env   # fill in values, never commit .env
docker compose up -d
# create realm "portfolio", client "portfolio-oidc-app", groups, roles, users
python3 scripts/lifecycle.py

## Lab shortcuts and the production fix
- start-dev, HTTP -> production mode with HTTPS
- master admin password grant in the script -> a scoped service account client
- throwaway passwords -> a secrets manager



docker compose down -v
git status
c
cat > README.md <<'EOF'
# 10 -- IAM Federation & Identity Governance

## What this does
Runs Keycloak in Docker as a self-hosted identity provider and demonstrates:
- OIDC: a full authorization code flow done by hand (code, then token exchange, then inspecting the JWT)
- SAML: a registered SAML client and exported IdP metadata
- Identity governance: joiner/mover/leaver automation in Python against Keycloak's Admin REST API

## Stack
Keycloak (Docker), OAuth 2.0 / OIDC, SAML 2.0, SCIM v2 concepts, Python (requests), NIST 800-53

## Lifecycle automation mapped to SCIM
| lifecycle.py function | Keycloak Admin API | SCIM v2 equivalent |
|---|---|---|
| onboard_joiner() | POST /users, PUT /users/{id}/groups/{gid} | POST /Users |
| move_user() | DELETE then PUT group membership | PATCH /Users/{id} |
| offboard_leaver() | PUT /users/{id} {enabled: false} | PATCH /Users/{id} (active: false) |

## Controls addressed
- NIST 800-53 AC-2 (Account Management): automated create, modify and disable
- NIST 800-53 IA-4 (Identifier Management): consistent identifiers and disablement of leavers

## OIDC vs SAML (what I observed)
- OIDC returned JSON/JWT tokens; the ID token carried who (sub, preferred_username), the access token carried what (roles).
- SAML uses signed XML; the IdP metadata file lists the entity ID, signing certificate and SSO endpoints.

## Real issues hit
- Authorization codes are single-use and expire in 60 seconds: I raised Client login timeout to 5 minutes for the lab.
- A pasted placeholder code and a stale client secret each caused invalid_grant and unauthorized_client errors.
- The master-realm admin does not exist in the portfolio realm: login needed a user created in that realm.
- Group names must match exactly (lowercase) or the Admin API lookup fails.

## Reproduce it
cp .env.example .env   # fill in values, never commit .env
docker compose up -d
# create realm "portfolio", client "portfolio-oidc-app", groups, roles, users
python3 scripts/lifecycle.py

## Lab shortcuts and the production fix
- start-dev, HTTP -> production mode with HTTPS
- master admin password grant in the script -> a scoped service account client
- throwaway passwords -> a secrets manager

## What I learned
[3-5 sentences in your own words: what surprised you comparing OIDC and SAML, and what you would add next, for example a real SCIM server or Entra ID as a second IdP]
