#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.basic import AnsibleModule
import subprocess

def run_zinit_command(command, service):
    cmd = ['zinit', command, service]
    return subprocess.run(cmd, capture_output=True, text=True)

def service_exists(service):
    result = run_zinit_command('list', '')
    return service in result.stdout

def service_status(service):
    result = run_zinit_command('status', service)
    return 'running' if 'running' in result.stdout.lower() else 'stopped'

def main():
    module_args = dict(
        name=dict(type='str', required=True),
        state=dict(type='str', choices=['started', 'stopped', 'restarted', 'reloaded'])
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
        if current_state == 'stopped':
            if not module.check_mode:
                run_zinit_command('start', service)
            changed = True
    elif state == 'stopped':
        if current_state == 'running':
            if not module.check_mode:
                run_zinit_command('stop', service)
            changed = True
    elif state == 'restarted':
        if not module.check_mode:
            run_zinit_command('restart', service)
        changed = True
    elif state == 'reloaded':
        if not module.check_mode:
            run_zinit_command('reload', service)
        changed = True

    module.exit_json(changed=changed, state=state)

if __name__ == '__main__':
    main()
