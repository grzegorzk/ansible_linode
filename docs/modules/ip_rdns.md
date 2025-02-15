# ip_rdns

Manage a Linode IP address's rDNS.

- [Examples](#examples)
- [Parameters](#parameters)
- [Return Values](#return-values)

## Examples

```yaml
- name: Update reverse DNS
  linode.cloud.ip_rdns:
    state: present
    address: 97.107.143.141
    rdns: 97.107.143.141.nip.io

```

```yaml
- name: Remove the reverse DNS
  linode.cloud.ip_rdns:
    state: absent
    address: 97.107.143.141

```


## Parameters

| Field     | Type | Required | Description                                                                  |
|-----------|------|----------|------------------------------------------------------------------------------|
| `address` | <center>`str`</center> | <center>**Required**</center> | The IP address.   |
| `state` | <center>`str`</center> | <center>Optional</center> | The state of this rDNS of the IP address.  **(Choices: `present`, `absent`)** |
| `rdns` | <center>`str`</center> | <center>Optional</center> | The desired rDNS value.  **(Updatable)** |

## Return Values

- `ip` - The updated IP address with the new reverse DNS in JSON serialized form.

    - Sample Response:
        ```json
        {
          "address": "97.107.143.141",
          "gateway": "97.107.143.1",
          "linode_id": 123,
          "prefix": 24,
          "public": true,
          "rdns": "test.example.org",
          "region": "us-east",
          "subnet_mask": "255.255.255.0",
          "type": "ipv4"
        }
        ```
    - See the [Linode API response documentation](https://www.linode.com/docs/api/profile/#ip-address-rdns-update) for a list of returned fields


