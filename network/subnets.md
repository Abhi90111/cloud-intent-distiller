# Network Subnet Design & Stateless NACL Architecture (10.20.0.0/16)

**Author:** V Abhiram (Roll 220103011)

---

## 1. Variable Length Subnet Masking (VLSM) Strategy

To optimize address space utilization across the assigned `10.20.0.0/16` CIDR block, subnets are provisioned strictly in descending order of required host capacity. 
The number of assignable IP addresses for any subnet with prefix length `p` is calculated as:
$$N_{\text{usable}} = 2^{(32 - p)} - 2$$
*(accounting for the reserved network identifier and directed broadcast address).*

### Capacity Derivations:
1. **Application Tier (`app`)**:
   - Host requirement: 1,000 addresses.
   - Sizing: A `/23` block provides $2^9 - 2 = 510$ hosts (insufficient). A `/22` block yields $2^{10} - 2 = 1,022$ hosts.
   - Allocation: `10.20.0.0/22` (spanning `10.20.0.0` through `10.20.3.255`).

2. **Public / Ingress Tier (`public`)**:
   - Host requirement: 250 addresses.
   - Sizing: A `/25` block provides 126 hosts (insufficient). A `/24` block yields $2^8 - 2 = 254$ hosts.
   - Allocation: `10.20.4.0/24` (spanning `10.20.4.0` through `10.20.4.255`).

3. **Database / Storage Tier (`data`)**:
   - Host requirement: 100 addresses.
   - Sizing: A `/26` block provides 62 hosts (insufficient). A `/25` block yields $2^7 - 2 = 126$ hosts.
   - Allocation: `10.20.5.0/25` (spanning `10.20.5.0` through `10.20.5.127`).

4. **Management & Bastion Tier (`management`)**:
   - Host requirement: 20 addresses.
   - Sizing: A `/28` block provides 14 hosts (insufficient). A `/27` block yields $2^5 - 2 = 30$ hosts.
   - Allocation: `10.20.5.128/27` (spanning `10.20.5.128` through `10.20.5.159`).

---

## 2. Complete Subnet Allocation Table

| Subnet Name | Host Requirement | Network Address | Subnet Mask | Usable Range | Broadcast | Total Usable |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **app** | 1,000 | `10.20.0.0` | `/22` (255.255.252.0) | `10.20.0.1` – `10.20.3.254` | `10.20.3.255` | 1,022 |
| **public** | 250 | `10.20.4.0` | `/24` (255.255.255.0) | `10.20.4.1` – `10.20.4.254` | `10.20.4.255` | 254 |
| **data** | 100 | `10.20.5.0` | `/25` (255.255.255.128) | `10.20.5.1` – `10.20.5.126` | `10.20.5.127` | 126 |
| **management** | 20 | `10.20.5.128` | `/27` (255.255.255.224) | `10.20.5.129` – `10.20.5.158` | `10.20.5.159` | 30 |

---

## 3. Stateless NACL Principles & Evaluation Order

Unlike stateful security groups which automatically maintain connection tracking states for bi-directional TCP flows, a **Network Access Control List (NACL) is entirely stateless**:
* Every single packet crossing the subnet boundary is evaluated independently.
* Inbound and outbound reply traffic must both have explicit permit rules.
  - Ephemeral reply traffic (`1024-65535`) returning from application pods requires explicit allow rules.
  - Ephemeral client return traffic (`1024-65535`) exiting to external clients must also be explicitly allowed.

### Deterministic Rule Ordering:
Rules are processed sequentially in ascending numerical index, halting at first match:
1. **Hostile IP Rejection**: Deny rule 50 explicitly blocks `198.51.100.0/24`. Placed before permissive rules (rule 100 for HTTP, rule 150 for HTTPS), malicious packets are filtered before hitting broader port allowances.
2. **Implicit Deny Default**: Any packet not explicitly matched against an allow rule drops through to the default implicit deny.
