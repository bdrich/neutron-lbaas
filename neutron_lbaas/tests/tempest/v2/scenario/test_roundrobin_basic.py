# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
from neutron_lbaas.tests.tempest.lib import test
from neutron_lbaas.tests.tempest.v2.scenario import base

networks = []
server_list = []

class TestRoundRobinBasic(base.BaseTestCase):
    """
    This test checks load balancing and validates traffic
    The following is the scenario outline:
    1. Create an instance
    2. SSH to the instance and start two servers: primary, secondary
    3. Create a load balancer, listener and pool with two members using
    ROUND_ROBIN algorithm, associate the VIP with a floating ip
    4. Send NUM requests to the floating ip and check that they are shared
       between the two servers.
    5. Delete listener and validate the traffic is not sent to any members
    """

#    def _delete_listener(self):
#        """Delete a listener to test listener scenario."""
#        self._cleanup_listener(self.listener['id'], self.load_balancer['id'])
#
#    def _delete_pool(self):
#        """Delete a pool to test basic scenario."""
#        self._cleanup_pool(self.pool['id'], self.load_balancer['id'])
#
#    def _delete_load_balancer(self):
#        """Delete a load balancer to test basic scenario."""
#        self._cleanup_load_balancer(self.load_balancer['id'])
#
    def _set_router_gateway_external(self):
        self.router.set_gateway(self._get_network_by_name('external').network_id)
#
    def _create_custom_group_rules(self):
        custom_rulesets = [
                #http
#                dict(
#                direction= 'ingress',
#                protocol= 'tcp',
#                port_range_min = 80,
#                port_range_max = 80
#                ),
#
                #https
                dict(
                direction= 'ingress',
                protocol= 'tcp',
                port_range_min= 443,
                port_range_max= 443
                )
        ]
        for ruleset in custom_rulesets:
          self._create_security_group_rule(self.security_group, self.network_client, self.tenant_id, **ruleset)

    @test.services('compute', 'network')
    def test_roundrobin_basic(self, number_of_vms=3):
#        networks[0] = self._create_network('network-rr-')
#        subnets[0] = self._create_subnet(network[0], 'subnet-rr-')
#        self._create_router()
#        self._set_router_gateway_external()
#        self._create_security_group()
        self._create_custom_group_rules()
        for vm in range(number_of_vms):
          server_list.append(self._create_server('rr-server%s' % (vm + 1)))
          self.servers['position-%s' % (vm + 1)] = server_list[vm]['id']
        self._create_load_balancer()
        self._assign_floating_ip_to_lb_vip(self.load_balancer)
        self._wait_for_load_balancer_status(self.load_balancer['id'])
        self._create_listener(self.load_balancer['id'], 'HTTPS', 443)
        self._wait_for_load_balancer_status(self.load_balancer['id'])
        self._create_pool(self.listener['id'], 'HTTPS')
        set_ip = self.server_fixed_ips[server_list[0]['id']]
        self._wait_for_load_balancer_status(self.load_balancer['id'])
        self._create_member(set_ip, 443, self.pool['id'], self.subnet['id'])
#        self._update_member_weight(5)
        self._check_load_balancing()
#        self._delete_listener()
#        self._check_load_balancing_after_deleting_resources()
