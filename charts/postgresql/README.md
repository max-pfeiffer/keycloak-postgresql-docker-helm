# PostgreSQL Helm Chart
Helm chart for installing [PostgreSQL database](https://www.postgresql.org/) on Kubernetes.

## values.yaml
Please see [values.yaml](values.yaml) for configuration options.

### Example
Simple example configuration using [Ceph-CSI RBD](https://github.com/ceph/ceph-csi) storage class: 
```yaml
configMap:
  POSTGRES_DB: "keycloak"

secrets:
  POSTGRES_USER: "username"
  POSTGRES_PASSWORD: "password"

persistentVolumeClaim:
  storageClassName: "csi-rbd-sc"
  accessModes:
    - ReadWriteOnce
  storageSize: 1Gi
```


