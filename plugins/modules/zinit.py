#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import subprocess

DOCUMENTATION = r'''
---
module: scottyeager.zinit.service
short_description: Manage zinit services
description:
  - This module allows you to manage zinit services
version_added: "1.0.0"
options:
  name:
    description:
      - Name of the service
    required: true
    type: str
  state:
    description:
      - Desired state of the service
    choices: ['started', 'stopped', 'restarted', 'reloaded', 'unmonitored']
    required: true
    type: str
author:
  - Scott Yeager
'''

EXAMPLES = r'''
- name: Start a service
  scottyeager.zinit.service:
    name: myservice
    state: started

- name: Stop a service
  scottyeager.zinit.service:
    name: myservice
    state: stopped
'''

RETURN = r'''
changed:
  description: Whether the state was changed
  type: bool
  returned: always
state:
  description: The target state that was set
  type: str
  returned: always
'''

def run_zinit_command(command, service):
    cmd = ['zinit', command, service]
    return subprocess.run(cmd, capture_output=True, text=True)

def service_exists(service):
    import os.path
    return os.path.exists(f"/etc/zinit/{service}.yaml")

def is_monitored(service):
    result = run_zinit_command('list', '')
    return service in result.stdout

def service_status(service):
    result = run_zinit_command('status', service)
    return 'running' if 'running' in result.stdout.lower() else 'stopped'

def main():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', choices=['started', 'stopped', 'restarted', 'reloaded', 'unmonitored'])
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    service = module.params['name']
    state = module.params['state']
    changed = False

    if not service_exists(service):
        module.fail_json(msg=f"Service {service} does not exist in zinit")

    current_state = service_status(service)

    if state == 'started':
        if not is_monitored(service):
            if not module.check_mode:
                run_zinit_command('monitor', service)
            changed = True
        elif current_state == 'stopped':
            if not module.check_mode:
                run_zinit_command('start', service)
            changed = True
    elif state == 'stopped':
        if current_state == 'running':
            if not module.check_mode:
                run_zinit_command('stop', service)
            changed = True
    elif state == 'restarted':
        if not is_monitored(service):
            if not module.check_mode:
                run_zinit_command('monitor', service)
            changed = True
        if not module.check_mode:
            # Use stop/start instead of restart for compatibility with older zinit versions
            run_zinit_command('stop', service)
            run_zinit_command('start', service)
        changed = True
    elif state == 'reloaded':
        if not module.check_mode:
            run_zinit_command('stop', service)
            run_zinit_command('forget', service)
            run_zinit_command('monitor', service)
        changed = True
    elif state == 'unmonitored':
        if is_monitored(service):
            if not module.check_mode:
                run_zinit_command('forget', service)
            changed = True

    module.exit_json(changed=changed, state=state)

if __name__ == '__main__':
    main()
