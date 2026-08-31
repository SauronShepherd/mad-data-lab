# Security and trust boundaries

- Case data is synthetic and canonical; private truth is server-only.
- Genie receives only the case-scoped curated source set and validated protocol fields.
- Trusted SQL uses a closed registry, validated identifiers, and bounded parameters.
- Client rendering uses text/React values rather than model-provided HTML.
- API errors and structured logs use stable public codes without provider secrets or private paths.
- Production configuration fails closed when required resources are absent; fixture mode is a local/testing concern.
- Security, dependency, accessibility, and browser gates are required before release.
