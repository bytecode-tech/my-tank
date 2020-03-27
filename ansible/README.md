# ansible-observer
Ansible playbooks for observer configuration

### Example run
ansible-playbook -i 192.168.0.112, --vault-id ~/.ansible_vault_observer -v -b -k -u pi configure-observer.yml --extra-vars "observer_hostname=frog-tank observer_appliance_version=feature/admin-controls observer_one_wire_port=8"

ansible-playbook -i raspberrypi.local, --vault-id ~/.ansible_vault_observer -v -b -k -u pi setup-observer-ap-mode.yml 
