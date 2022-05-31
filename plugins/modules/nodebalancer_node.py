#!/usr/bin/python
# -*- coding: utf-8 -*-

"""This module contains all of the functionality for Linode Domains."""

from __future__ import absolute_import, division, print_function

# pylint: disable=unused-import
import copy
from typing import Optional, cast, Any, Set, List

import linode_api4
from linode_api4 import Domain

from ansible_collections.linode.cloud.plugins.module_utils.linode_common import LinodeModuleBase
from ansible_collections.linode.cloud.plugins.module_utils.linode_helper import \
    filter_null_values, paginated_list_to_json, handle_updates
from ansible_collections.linode.cloud.plugins.module_utils.linode_docs import global_authors, \
    global_requirements

import ansible_collections.linode.cloud.plugins.module_utils.doc_fragments.nodebalancer_node as docs

MODULE_SPEC = dict(
    nodebalancer_id=dict(
        type='int', required=True,
        description='The ID of the NodeBalancer that contains this node.',
        ),

    config_id=dict(
        type='int', required=True,
        description='The ID of the NodeBalancer Config that contains this node.',
        ),

    label=dict(
        type='str', required=True,
        description='The label for this node. This is used to identify nodes within a config.',
    ),

    address=dict(
        type='str',
        description='The private IP Address where this backend can be reached. '
                    'This must be a private IP address.',
    ),

    state=dict(
        type='str',
        description='Whether the NodeBalancer node should be present or absent.',
        choices=['present', 'absent'],
        required=True
    ),

    mode=dict(
        type='str',
        description='The mode this NodeBalancer should use when sending traffic to this backend.',
        choices=['accept', 'reject', 'drain', 'backup'],
    ),

    weight=dict(
        type='int',
        description='Nodes with a higher weight will receive more traffic.',
    ),
)

specdoc_meta = dict(
    description=[
        'Manage Linode NodeBalancer Nodes.'
    ],
    requirements=global_requirements,
    author=global_authors,
    spec=MODULE_SPEC,
    examples=docs.specdoc_examples,
    return_values=dict(
        node=dict(
            description='The NodeBalancer Node in JSON serialized form.',
            docs_url='https://www.linode.com/docs/api/nodebalancers/#node-view__responses',
            type='dict',
            sample=docs.result_node_samples
        )
    )
)

MUTABLE_FIELDS: Set[str] = {
    'address',
    'mode',
    'weight'
}


class LinodeNodeBalancerNode(LinodeModuleBase):
    """Module for managing Linode NodeBalancer nodes"""

    def __init__(self) -> None:
        self.module_arg_spec = MODULE_SPEC
        self.required_one_of: List[str] = []
        self.results = dict(
            changed=False,
            actions=[],
            node=None,
        )

        super().__init__(module_arg_spec=self.module_arg_spec,
                         required_one_of=self.required_one_of)

    def _get_node(self) -> Optional[linode_api4.NodeBalancerNode]:
        try:
            params = self.module.params
            config_id = params['config_id']
            nodebalancer_id = params['nodebalancer_id']
            node_label = params['label']

            config = linode_api4.NodeBalancerConfig(self.client, config_id, nodebalancer_id)
            for node in config.nodes:
                if node.label == node_label:
                    return node

            return None
        except Exception as exception:
            return self.fail(msg='failed to get node {0}: {1}'.format(node_label, exception))

    def _create_node(self) -> linode_api4.NodeBalancerNode:
        try:
            local_params = copy.deepcopy(self.module.params)

            config_id = local_params.pop('config_id')
            nodebalancer_id = local_params.pop('nodebalancer_id')
            node_label = local_params.pop('label')
            node_address = local_params.pop('address')

            config = linode_api4.NodeBalancerConfig(self.client, config_id, nodebalancer_id)

            node = config.node_create(node_label, node_address, **local_params)
            self.register_action('Created Node {}: {}'.
                                 format(node_label, node.id))

            return node
        except Exception as exception:
            return self.fail(msg='failed to create node {0}: {1}'
                             .format(self.module.params.get('label'), exception))

    def _update_node(self, node: linode_api4.NodeBalancerNode) -> None:
        """Handles all update functionality for the current Node"""

        handle_updates(node, self.module.params, MUTABLE_FIELDS, self.register_action)

    def _handle_present(self) -> None:
        node = self._get_node()

        # Create the node if it does not already exist
        if node is None:
            node = self._create_node()

        self._update_node(node)

        # Force lazy-loading
        node._api_get()

        self.results['node'] = node._raw_json

    def _handle_absent(self) -> None:
        node = self._get_node()

        if node is not None:
            self.results['node'] = node._raw_json

            node.delete()
            self.register_action('Deleted node {0}'.format(self.module.params.get('label')))

    def exec_module(self, **kwargs: Any) -> Optional[dict]:
        """Entrypoint for nodebalancer_node module"""
        state = kwargs.get('state')

        if state == 'absent':
            self._handle_absent()
            return self.results

        self._handle_present()

        return self.results


def main() -> None:
    """Constructs and calls the Linode Domain module"""
    LinodeNodeBalancerNode()


if __name__ == '__main__':
    main()

DOCUMENTATION='''
author:
- Luke Murphy (@decentral1se)
- Charles Kenney (@charliekenney23)
- Phillip Campbell (@phillc)
- Lena Garber (@lbgarber)
- Jacob Riddle (@jriddle)
description:
- Manage Linode NodeBalancer Nodes.
module: nodebalancer_node
options:
  address:
    description: The private IP Address where this backend can be reached. This must
      be a private IP address.
    required: false
    type: str
  config_id:
    description: The ID of the NodeBalancer Config that contains this node.
    required: true
    type: int
  label:
    description: The label for this node. This is used to identify nodes within a
      config.
    required: true
    type: str
  mode:
    choices:
    - accept
    - reject
    - drain
    - backup
    description: The mode this NodeBalancer should use when sending traffic to this
      backend.
    required: false
    type: str
  nodebalancer_id:
    description: The ID of the NodeBalancer that contains this node.
    required: true
    type: int
  state:
    choices:
    - present
    - absent
    description: Whether the NodeBalancer node should be present or absent.
    required: true
    type: str
  weight:
    description: Nodes with a higher weight will receive more traffic.
    required: false
    type: int
requirements:
- python >= 3
'''

RETURN = '''
node:The NodeBalancer Node in JSON serialized form.
  description: 
  linode_api_docs: "https://www.linode.com/docs/api/nodebalancers/#node-view__responses"
  returned: always
  type: dict
  sample: {
  "address": "123.123.123.123:80",
  "config_id": 12345,
  "id": 12345,
  "label": "mynode",
  "mode": "accept",
  "nodebalancer_id": 12345,
  "status": "Unknown",
  "weight": 10
}
'''
