# Keycloak Helm Chart
Helm chart for installing [Keycloak](https://www.keycloak.org/) on Kubernetes. It uses
[pfeiffermax/keycloak-postgresql](https://hub.docker.com/r/pfeiffermax/keycloak-postgresql) as Docker image which is
specifically built to use PostgresSQL as database.

Per default, this chart installs Keycloak with TLS disabled. Just set `ingress.enabled: true` in [values.yaml](values.yaml)
to add an Ingress for this default configuration.

## values.yaml
Please see [values.yaml](values.yaml) for configuration options.

### Examples 
#### HTTP only
Using nginx ingress controller without TLS (default config, for testing purposes):
```yaml
ingress:
  enabled: true
  className: "nginx"
  hosts:
    - host: "keycloak.lan"
      paths:
        - path: /
          pathType: Prefix
    - host: "keycloak-admin.lan"
      paths:
        - path: /
          pathType: Prefix

configMap:
  KC_HOSTNAME: "http://keycloak.lan"
  KC_HOSTNAME_ADMIN: "http://keycloak-admin.lan"
  KC_HTTP_ENABLED: "true"
  KC_DB_URL_HOST: "postgresql-keycloak.persistence"
  KC_DB_URL_DATABASE: "keycloak"

secrets:
  KC_BOOTSTRAP_ADMIN_USERNAME: "username"
  KC_BOOTSTRAP_ADMIN_PASSWORD: "password"
  KC_DB_USERNAME: "username"
  KC_DB_PASSWORD: "password"
```

#### TLS Edge Termination 
Using nginx ingress controller with TLS edge termination is a bit tricky. You need to make sure that
[nginx ingress controller sets the `Forwarded` or `X-Forwarded-*` headers correctly](https://www.keycloak.org/server/reverseproxy#_configure_the_reverse_proxy_headers).
Depending on what header you are using, you need to set `KC_PROXY_HEADERS` environment variable accordingly.

**Important: [nginx ingress controller currently does not have support for the standard `Forwarded` header specified in RFC7239](https://github.com/kubernetes/ingress-nginx/issues/10263).
So you currently need to go for that `X-Forwarded-*` header option.**

With nginx ingress controller you have basically two options to do that:
1. [Configure nginx ingress controller globally to pass the `X-Forwarded-*` headers](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#use-forwarded-headers)
   in its ConfigMap.
2. [Using snippet annotation](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/annotations/#configuration-snippet)
   to configure the headers in the Keycloak Ingress configuration.

The first option has the disadvantage that it's applied to all ingresses in your cluster. You can configure it in your
`values.yaml` when you install nginx ingress controller using Helm or by some other means.
[The default setting for that header does not need to get changed](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#forwarded-for-header)
as it is already set to `X-Forwarded-For`.

The second option is a bit hacky and has some security concerns because you need to
[enable snippet annotations in your nginx ingress controller ConfigMap](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/configmap/#allow-snippet-annotations)
for your cluster globally, which has its misuse potential by itself. So choose your poison. :smiley:
Here we choose to go for the second option, snippet annotation. 

It's also important to [configure the hostname correctly when using edge TLS termination](https://www.keycloak.org/server/hostname#_using_edge_tls_termination).

```yaml
ingress:
  enabled: true
  className: "nginx"
  annotations:
    cert-manager.io/cluster-issuer: ca-issuer-selfsigned
    nginx.ingress.kubernetes.io/force-ssl-redirect: "true"
    nginx.ingress.kubernetes.io/configuration-snippet: |
      more_set_headers "X-Forwarded-For $http_x_forwarded_for";
  hosts:
    - host: "keycloak.lan"
      paths:
        - path: /
          pathType: Prefix
    - host: "keycloak-admin.lan"
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: keycloak-tls
      hosts:
        - "keycloak.lan"
    - secretName: keycloak-admin-tls
      hosts:
        - "keycloak-admin.lan"

configMap:
  KC_HOSTNAME: "https://keycloak.lan"
  KC_HOSTNAME_ADMIN: "https://keycloak-admin.lan"
  KC_HTTP_ENABLED: "true"
  KC_DB_URL_HOST: "postgresql-keycloak.persistence"
  KC_DB_URL_DATABASE: "keycloak"
  KC_PROXY_HEADERS: "xforwarded"
  KC_LOG_LEVEL: "debug"
  KC_HOSTNAME_DEBUG: "true"

secrets:
  KC_BOOTSTRAP_ADMIN_USERNAME: "username"
  KC_BOOTSTRAP_ADMIN_PASSWORD: "password"
  KC_DB_USERNAME: "username"
  KC_DB_PASSWORD: "password"
```

#### TLS Passthrough
coming soon...