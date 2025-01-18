This is an Ansible role for managing [zinit](https://github.com/threefoldtech/zinit) services. It's modeled after the built in [`ansible.builtin.service`](https://docs.ansible.com/ansible/latest/collections/ansible/builtin/service_module.html) module.

## Quickstart

```
ansible-galaxy install git+https://github.com/scottyeager/ansible-zinit.git,main,zinit
```

This will install the `main` branch of this repo as a role named `zinit`. You can use a different name if you want, but it must be consistent whenever using the role.

## Usage
You can now add the role to a playbook and use the included tasks. Here's an example that demonstrates all available functions:

```
- name: Manage services with zinit

  roles:
    - role: zinit

  tasks:
    - name: Ensure my_service is running
      zinit:
        name: my_service
        state: started

    - name: Stop another_service if it's running
      zinit:
        name: another_service
        state: stopped

    - name: Restart web_service
      zinit:
        name: web_service
        state: restarted

    - name: Reload config_service
      zinit:
        name: config_service
        state: reloaded
```

## Updating

If you need to update the role in the future, add the `-f` flag to force a fresh download:

```
ansible-galaxy install git+https://github.com/scottyeager/ansible-zinit.git,main,zinit -f
```
