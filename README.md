This is an Ansible collection for managing [zinit](https://github.com/threefoldtech/zinit) services. It's modeled after the built in [`ansible.builtin.service`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html) module.

## Quickstart

```
ansible-galaxy collection install git+https://github.com/scottyeager/ansible-zinit.git
```

This will install the collection with name `zinit` under the `local` namespace on your machine.

## Usage

You can now use the `local.zinit.service` module inside your playbooks. This requires that you already created some zinit service files.

Here's an example that demonstrates all available functions:

```
- name: Manage services with zinit

  tasks:
    - name: Ensure my_service is running
      local.zinit.service:
        name: my_service
        state: started

    - name: Stop another_service if it's running
      local.zinit.service:
        name: another_service
        state: stopped

    - name: Restart web_service
      local.zinit.service:
        name: web_service
        state: restarted

    - name: Reload config_service
      local.zinit.service:
        name: config_service
        state: reloaded
```

## Updating

If you need to update the collection in the future, add the `-f` flag to force a fresh download:

```
ansible-galaxy collection install git+https://github.com/scottyeager/ansible-zinit.git -f
```
