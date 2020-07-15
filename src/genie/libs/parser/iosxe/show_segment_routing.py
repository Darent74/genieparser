'''
show_segment_routing.py

IOSXE parsers for the following show commands:
    * 'show segment-routing mpls lb'
    * 'show segment-routing mpls state'
    * 'show segment-routing mpls lb lock'
    * 'show segment-routing mpls lb assigned-sids'
    * 'show segment-routing mpls connected-prefix-sid-map ipv4'
    * 'show segment-routing mpls connected-prefix-sid-map ipv6'
    * 'show segment-routing mpls gb'
    * 'show segment-routing mpls gb lock'
    * 'show segment-routing mpls connected-prefix-sid-map local ipv4'
    * 'show segment-routing mpls connected-prefix-sid-map local ipv6'
    * 'show segment-routing traffic-eng topology ipv4'
    * 'show segment-routing traffic-eng policy all'
    * 'show segment-routing traffic-eng policy name {name}'
    * 'show segment-routing mpls mapping-server ipv4'
    * 'show segment-routing mpls mapping-server ipv6'
'''

# Python
import re

# Genie
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Optional

# =============================================================
# Schema for:
#    * 'show segment-routing mpls connected-prefix-sid-map ipv4'
#    * 'show segment-routing mpls connected-prefix-sid-map local ipv4'
#    * 'show segment-routing mpls connected-prefix-sid-map ipv6'
#    * 'show segment-routing mpls connected-prefix-sid-map local ipv6'
# =============================================================
class ShowSegmentRoutingMplsConnectedPrefixSidMapSchema(MetaParser):
    ''' Schema for:
        * 'show segment-routing mpls connected-prefix-sid-map ipv4'
        * 'show segment-routing mpls connected-prefix-sid-map local ipv4'
        * 'show segment-routing mpls connected-prefix-sid-map ipv6'
        * 'show segment-routing mpls connected-prefix-sid-map local ipv6'
    '''

    schema = {
        'segment_routing':
            {'bindings':
                {Optional('connected_prefix_sid_map'):
                    {Optional('ipv4'):
                        {'ipv4_prefix_sid':
                            {Any():
                                {'algorithm':
                                    {Any():
                                        {'prefix': str,
                                        'value_type': str,
                                        'sid': str,
                                        'range': str,
                                        'srgb': str,
                                        Optional('source'): str,
                                        'algorithm': str,
                                        },
                                    },
                                },
                            },
                        },
                    Optional('ipv6'):
                        {'ipv6_prefix_sid':
                            {Any():
                                {'algorithm':
                                    {Any():
                                        {'prefix': str,
                                        'value_type': str,
                                        'sid': str,
                                        'range': str,
                                        'srgb': str,
                                        Optional('source'): str,
                                        'algorithm': str,
                                        },
                                    },
                                },
                            },
                        },
                    },
                    Optional('local_prefix_sid'): {
                        Optional('ipv4'): {
                            'ipv4_prefix_sid_local':{
                                Any():{
                                    'algorithm': {
                                        Any():{
                                            'prefix': str,
                                            'value_type': str,
                                            'sid': str,
                                            'range': str,
                                            'srgb': str,
                                            'algorithm': str
                                        }
                                    }
                                }
                            }
                        },
                        Optional('ipv6'): {
                            'ipv6_prefix_sid_local':{
                                Any():{
                                    'algorithm': {
                                        Any():{
                                            'prefix': str,
                                            'value_type': str,
                                            'sid': str,
                                            'range': str,
                                            'srgb': str,
                                            'algorithm': str
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
            },
        }

# ====================================================================
# Parser for:
#    * 'show segment-routing mpls connected-prefix-sid-map ipv4'
#    * 'show segment-routing mpls connected-prefix-sid-map ipv6'
# ====================================================================
class ShowSegmentRoutingMplsConnectedPrefixSidMap(ShowSegmentRoutingMplsConnectedPrefixSidMapSchema):
    ''' Parser for:
        * 'show segment-routing mpls connected-prefix-sid-map ipv4'
        * 'show segment-routing mpls connected-prefix-sid-map ipv6'
    '''
    
    cli_command = 'show segment-routing mpls connected-prefix-sid-map {address_family}'
    
    def cli(self, address_family, output=None):

        assert address_family in ['ipv4', 'ipv6']

        # Get output
        if output is None:
            out = self.device.execute(self.cli_command.format(address_family=address_family))
        else:
            out = output

        # Mapping dict
        mapping_dict = {
            'ipv4': 'ipv4_prefix_sid',
            'ipv6': 'ipv6_prefix_sid',
        }

        mapping_dict_local = {
            'ipv4': 'ipv4_prefix_sid_local',
            'ipv6': 'ipv6_prefix_sid_local',
        }

        # Init
        ret_dict = {}

        # PREFIX_SID_CONN_MAP ALGO_0
        # PREFIX_SID_CONN_MAP ALGO_1
        p1 = re.compile(r'^PREFIX_SID_CONN_MAP +(?P<algorithm>(.*))$')

        # PREFIX_SID_PROTOCOL_ADV_MAP ALGO_0
        # PREFIX_SID_PROTOCOL_ADV_MAP ALGO_1
        p2 = re.compile(r'^PREFIX_SID_PROTOCOL_ADV_MAP +(?P<algorithm>(.*))$')

        # Prefix/masklen   SID Type Range Flags SRGB
        # 10.4.1.1/32         1 Indx     1         Y
        p3 = re.compile(r'(?P<prefix>(\S+))\/(?P<masklen>(\d+)) +(?P<sid>(\d+))'
                         ' +(?P<type>(\S+)) +(?P<range>(\d+))'
                         '(?: +(?P<flags>(\S+)))? +(?P<srgb>(Y|N))$')

        # Prefix/masklen   SID Type Range Flags SRGB Source
        # 10.4.1.1/32         1 Indx     1         Y  OSPF Area 8 10.4.1.1
        # 10.16.2.2/32         2 Indx     1         Y  OSPF Area 8 10.16.2.2
        p4 = re.compile(r'(?P<prefix>(\S+))\/(?P<masklen>(\d+)) +(?P<sid>(\d+))'
                         ' +(?P<type>(\S+)) +(?P<range>(\d+))'
                         '(?: +(?P<flags>(\S+)))? +(?P<srgb>(Y|N))'
                         ' +(?P<source>(.*))$')

        for line in out.splitlines():
            line = line.strip()

            # PREFIX_SID_CONN_MAP ALGO_0
            # PREFIX_SID_CONN_MAP ALGO_1
            m = p1.match(line)
            if m:
                algorithm = m.groupdict()['algorithm']
                address_family_dict = ret_dict.setdefault('segment_routing', {}). \
                                    setdefault('bindings', {}). \
                                    setdefault('local_prefix_sid', {}). \
                                    setdefault(address_family, {}). \
                                    setdefault(mapping_dict_local[address_family], {})
                continue

            # PREFIX_SID_PROTOCOL_ADV_MAP ALGO_0
            # PREFIX_SID_PROTOCOL_ADV_MAP ALGO_1
            m = p2.match(line)
            if m:
                algorithm = m.groupdict()['algorithm']
                continue

            # Prefix/masklen   SID Type Range Flags SRGB
            # 10.4.1.1/32         1 Indx     1         Y
            m = p3.match(line)
            if m:
                group = m.groupdict()
                prefix = group['prefix'] + '/' + group['masklen']
                algo_dict = address_family_dict.setdefault(prefix, {}). \
                                setdefault('algorithm', {}). \
                                setdefault(algorithm, {})
                # Set values
                algo_dict['prefix'] = prefix
                algo_dict['algorithm'] = algorithm
                algo_dict['value_type'] = group['type']
                algo_dict['sid'] = group['sid']
                algo_dict['range'] = group['range']
                algo_dict['srgb'] = group['srgb']
                if group['flags']:
                    algo_dict['flags'] = group['flags']
                continue

            # Prefix/masklen   SID Type Range Flags SRGB Source
            # 10.4.1.1/32         1 Indx     1         Y  OSPF Area 8 10.4.1.1
            m = p4.match(line)
            if m:
                group = m.groupdict()
                prefix = group['prefix'] + '/' + group['masklen']
                # Set dict
                algo_dict = ret_dict.setdefault('segment_routing', {}).\
                                     setdefault('bindings', {}).\
                                     setdefault('connected_prefix_sid_map', {}).\
                                     setdefault(address_family, {}).\
                                     setdefault(mapping_dict[address_family], {}).\
                                     setdefault(prefix, {}).\
                                     setdefault('algorithm', {}).\
                                     setdefault(algorithm, {})
                # Set values
                algo_dict['prefix'] = prefix
                algo_dict['algorithm'] = algorithm
                algo_dict['value_type'] = group['type']
                algo_dict['sid'] = group['sid']
                algo_dict['range'] = group['range']
                algo_dict['srgb'] = group['srgb']
                algo_dict['source'] = group['source']
                if group['flags']:
                    algo_dict['flags'] = group['flags']
                continue

        return ret_dict

# ==================================
# Schema for:
#   * 'show segment-routing mpls gb'
# ==================================
class ShowSegmentRoutingMplsGbSchema(MetaParser):
    ''' Schema for:
        * 'show segment-routing mpls gb'
    '''

    schema = {
        'label_min': int,
        'label_max': int,
        'state': str,
        'default': str,
        }


# ==================================
# Parser for:
#   * 'show segment-routing mpls gb'
# ==================================
class ShowSegmentRoutingMplsGb(ShowSegmentRoutingMplsGbSchema):
    ''' Parser for:
        * 'show segment-routing mpls gb'
    '''
    
    cli_command = 'show segment-routing mpls gb'
    
    def cli(self, output=None):

        # Get output
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # Init
        ret_dict = {}

        # LABEL-MIN  LABEL_MAX  STATE           DEFAULT  
        # 16000      23999      ENABLED         Yes  
        p1 = re.compile(r'^(?P<label_min>(\d+)) +(?P<label_max>(\d+))'
                         ' +(?P<state>(\S+)) +(?P<default>(\S+))$')

        for line in out.splitlines():
            line = line.strip()

            # LABEL-MIN  LABEL_MAX  STATE           DEFAULT  
            # 16000      23999      ENABLED         Yes  
            m = p1.match(line)
            if m:
                group = m.groupdict()
                ret_dict['label_min'] = int(group['label_min']) 
                ret_dict['label_max'] = int(group['label_max'])
                ret_dict['state'] = group['state']
                ret_dict['default'] = group['default']
                continue

        return ret_dict


# =============================================
# Parser for 'show segment-routing mpls lb'
# =============================================

class ShowSegmentRoutingMplsLBSchema(MetaParser):
    """Schema for show segment-routing mpls lb
    """

    schema = {
        'label_min': int,
        'label_max': int,
        'state': str,
        'default': str
    }

class ShowSegmentRoutingMplsLB(ShowSegmentRoutingMplsLBSchema):
    """ Parser for show segment-routing mpls lb"""
    
    cli_command = 'show segment-routing mpls lb'
    
    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        # 15000      15999      ENABLED         Yes
        p1 = re.compile(r'^(?P<label_min>\d+) +(?P<label_max>\d+) +'
                        '(?P<state>\S+) +(?P<default>\S+)$')
        
        # initial variables
        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            # 15000      15999      ENABLED         Yes
            m = p1.match(line)
            if m:
                group = m.groupdict()
                label_min = int(group['label_min'])
                label_max = int(group['label_max'])
                state = group['state']
                default = group['default']

                ret_dict.update({'label_min': label_min})
                ret_dict.update({'label_max': label_max})
                ret_dict.update({'state': state})
                ret_dict.update({'default': default})
                
                continue
        
        return ret_dict

# =============================================
# Parser for 'show segment-routing mpls state'
# =============================================

class ShowSegmentRoutingMplsStateSchema(MetaParser):
    """Schema for show segment-routing mpls state
    """

    schema = {
        'sr_mpls_state': str
    }

class ShowSegmentRoutingMplsState(ShowSegmentRoutingMplsStateSchema):
    """ Parser for show segment-routing mpls state"""
    
    cli_command = 'show segment-routing mpls state'
    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
            
        # Segment Routing MPLS State : ENABLED
        p1 = re.compile(r'^Segment +Routing +MPLS +State +: +(?P<state>\S+)$')
        
        # initial variables
        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            # Segment Routing MPLS State : ENABLED
            m = p1.match(line)
            if m:
                group = m.groupdict()
                state = group['state']
                ret_dict.update({'sr_mpls_state': state})
                continue
        
        return ret_dict

# ==============================================
# Parser for 'show segment-routing mpls lb lock'
# ==============================================

class ShowSegmentRoutingMplsLbLockSchema(MetaParser):
    """Schema for show segment-routing mpls lb lock
    """

    schema = {
        'label_min': int,
        'label_max': int
    }

class ShowSegmentRoutingMplsLbLock(ShowSegmentRoutingMplsLbLockSchema):
    """ Parser for show segment-routing mpls lb lock"""

    cli_command = 'show segment-routing mpls lb lock'
    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output
        # SR LB (15000, 15999) Lock Users :
        p1 = re.compile(r'^SR +LB +\((?P<label_min>\d+)\, +'
            '(?P<label_max>\d+)\) +Lock +Users +:')

        # initial variables
        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            # SR LB (15000, 15999) Lock Users :
            m = p1.match(line)
            if m:
                group = m.groupdict()
                label_min = int(group['label_min'])
                label_max = int(group['label_max'])

                ret_dict.update({'label_min': label_min})
                ret_dict.update({'label_max': label_max})

                continue

        return ret_dict

# ==============================================
# Parser for 'show segment-routing mpls gb lock'
# ==============================================
class ShowSegmentRoutingMplsGbLock(ShowSegmentRoutingMplsLbLockSchema):
    """ Parser for 'show segment-routing mpls gb lock'
    """

    cli_command = 'show segment-routing mpls gb lock'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # SR GB (9000, 10000) Lock Users :
        p1 = re.compile(r'^SR +GB +\((?P<label_min>\d+), +(?P<label_max>\d+)\) +Lock +Users +:$')

        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            m = p1.match(line)
            if m:
                group = m.groupdict()
                ret_dict.update({k: int(v) for k, v in group.items() if v})
                continue

        return ret_dict

# ====================================================================
# Parser for:
#    * 'show segment-routing mpls connected-prefix-sid-map local ipv4'
#    * 'show segment-routing mpls connected-prefix-sid-map local ipv6'
# ====================================================================
class ShowSegmentRoutingMplsConnectedPrefixSidMapLocal(ShowSegmentRoutingMplsConnectedPrefixSidMap):
    ''' Parser for:
        * 'show segment-routing mpls connected-prefix-sid-map local ipv4'
        * 'show segment-routing mpls connected-prefix-sid-map local ipv6'
    '''
    
    cli_command = 'show segment-routing mpls connected-prefix-sid-map local {address_family}'
    
    def cli(self, address_family, output=None):

        assert address_family in ['ipv4', 'ipv6']

        # Get output
        if output is None:
            out = self.device.execute(self.cli_command.format(address_family=address_family))
        else:
            out = output
        return super().cli(address_family=address_family, output=out)


# ==================================================================
# Parser for:
#    * 'show segment-routing traffic-eng topology ipv4'
# ==================================================================
class ShowSegmentRoutingTrafficEngTopologySchema(MetaParser):
    """ Schema for 
        'show segment-routing traffic-eng topology ipv4'
    """
    schema = {
        "nodes": {
            Any(): {
                "ospf_router_id": str,
                "area_id": int,
                "domain_id": int,
                "asn": int,
                Optional("prefix_sid"): {
                    "prefix": str,
                    "label": int,
                    "label_type": str,
                    "domain_id": int,
                    "flags": str,
                },
                "links": {
                    Any(): {
                        "local_address": str,
                        "remote_address": str,
                        "local_node": {
                            "ospf_router_id": str,
                            "area_id": int,
                            "domain_id": int,
                            "asn": int,
                        },
                        "remote_node": {
                            "ospf_router_id": str,
                            "area_id": int,
                            "domain_id": int,
                            "asn": int,
                        },
                        "metric": {
                            Any(): int,
                        },
                        "bandwidth_total": int,
                        "bandwidth_reservable": int,
                        "admin_groups": str,
                        Optional("adj_sid"): {
                            Any(): str,
                        },
                    },
                },
            },
        },
    }

class ShowSegmentRoutingTrafficEngTopology(ShowSegmentRoutingTrafficEngTopologySchema):
    """ Parser for 
        'show segment-routing traffic-eng topology ipv4'
    """

    cli_command = 'show segment-routing traffic-eng topology ipv4'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # Node 1:
        p1 = re.compile(r'^Node +(?P<node>\d+):$')

        #   TE router ID: 10.19.198.239
        p2 = re.compile(r'^TE +router +ID: +(?P<te_router_id>\S+)\)$')

        #   OSPF router ID: 10.19.198.239 area ID: 8 domain ID: 0 ASN: 65109
        p3 = re.compile(r'^OSPF router ID: +(?P<ospf_router_id>\S+) +area ID: '
                         '+(?P<area_id>\d+) +domain ID: +(?P<domain_id>\d+) '
                         '+ASN: +(?P<asn>\d+)$')

        #   Prefix SID:
        #     Prefix 10.19.198.239, label 16073 (regular), domain ID 0, flags: N , E
        p4 = re.compile(r'^Prefix +(?P<prefix>\S+), +label +(?P<label>\d+) '
                         '+\((?P<label_type>\S+)\), +domain +ID +(?P<domain_id>\d+), '
                         '+flags: +(?P<flags>[\S\s]+)$')

        #   Link[0]: local address 10.19.198.26, remote address 10.19.198.25
        p5 = re.compile(r'^Link\[(?P<link>\d+)\]: +local +address +(?P<local_address>\S+), '
                         '+remote +address +(?P<remote_address>\S+)$')

        #     Local node:
        p6 = re.compile(r'^Local +node:$')

        #     Remote node:
        p6_1 = re.compile(r'^Remote +node:$')

        #     Metric: IGP 1000, TE 1000, Delay 1000
        p7 = re.compile(r'^Metric: +(?P<metric>[\S\s]+)$')
        p7_1 = re.compile(r'(?P<type>\w+) +(?P<num>\d+)')

        #     Bandwidth: Total 125000000, Reservable 0
        p8 = re.compile(r'^Bandwidth: +Total +(?P<total>\d+), +Reservable +(?P<reservable>\d+)$')

        #     Admin-groups: 0x00000000
        p9 = re.compile(r'^Admin-groups: +(?P<admin_groups>\S+)$')

        #     Adj SID: 18 (unprotected)  36 (protected)
        p10 = re.compile(r'^Adj +SID: +(?P<adj_sid>[\S\s]+)$')
        p10_1 = re.compile(r'(?P<num>\d+) +\((?P<state>\S+)\)')

        # initial variables
        ret_dict = {}
        index = 0

        for line in out.splitlines():
            line = line.strip()
            if not line:
                continue

            # Node 1:
            m = p1.match(line)
            if m:
                group = m.groupdict()
                node = int(group['node'])
                node_dict = ret_dict.setdefault('nodes', {}).setdefault(node, {})
                index = 0
                continue

            #   TE router ID: 10.19.198.239
            m = p2.match(line)
            if m:
                group = m.groupdict()
                if index == 0:
                    target = node_dict
                elif index == 1:
                    target = local_dict
                else:
                    target = remote_dict
                target.update({'te_router_id': group['te_router_id']})
                continue

            #   OSPF router ID: 10.19.198.239 area ID: 8 domain ID: 0 ASN: 65109
            m = p3.match(line)
            if m:
                group = m.groupdict()
                if index == 0:
                    target = node_dict
                elif index == 1:
                    target = local_dict
                else:
                    target = remote_dict
                target.update({k: (int(v) if v.isdigit() else v) for k, v in group.items()})
                continue

            #   Prefix SID:
            #     Prefix 10.19.198.239, label 16073 (regular), domain ID 0, flags: N , E
            m = p4.match(line)
            if m:
                group = m.groupdict()
                pref_dict = node_dict.setdefault('prefix_sid', {})
                pref_dict.update({k: (int(v) if v.isdigit() else v) for k, v in group.items()})
                continue

            #   Link[0]: local address 10.19.198.26, remote address 10.19.198.25
            m = p5.match(line)
            if m:
                group = m.groupdict()
                link = int(group['link'])
                link_dict = node_dict.setdefault('links', {}).setdefault(link, {})
                link_dict.update({'local_address': group['local_address']})
                link_dict.update({'remote_address': group['remote_address']})
                continue

            #     Local node:
            m = p6.match(line)
            if m:
                local_dict = link_dict.setdefault('local_node', {})
                index = 1
                continue

            #     Remote node:
            m = p6_1.match(line)
            if m:
                remote_dict = link_dict.setdefault('remote_node', {})
                index = 2
                continue

            #     Metric: IGP 1000, TE 1000, Delay 1000
            m = p7.match(line)
            if m:
                metric = m.groupdict()['metric']
                metric_dict = link_dict.setdefault('metric', {})

                mlist = p7_1.findall(metric)
                for item in mlist:
                    metric_dict.update({item[0].lower(): int(item[1])})

                continue

            #     Bandwidth: Total 125000000, Reservable 0
            m = p8.match(line)
            if m:
                group = m.groupdict()
                link_dict.update({'bandwidth_total': int(group['total'])})
                link_dict.update({'bandwidth_reservable': int(group['reservable'])})
                continue

            #     Admin-groups: 0x00000000
            m = p9.match(line)
            if m:
                group = m.groupdict()
                link_dict.update({'admin_groups': group['admin_groups']})
                continue

            #     Adj SID: 18 (unprotected)  36 (protected)
            m = p10.match(line)
            if m:
                adj_sid = m.groupdict()['adj_sid']
                adj_dict = link_dict.setdefault('adj_sid', {})

                adj_list = p10_1.findall(adj_sid)
                for item in adj_list:
                    adj_dict.update({item[0]: item[1].lower()})

                continue

        return ret_dict


# ==================================================================
# Parser for:
#    * 'show segment-routing traffic-eng policy all'
#    * 'show segment-routing traffic-eng policy name {name}'
# ==================================================================
class ShowSegmentRoutingTrafficEngPolicySchema(MetaParser):
    """ Schema for 
        'show segment-routing traffic-eng policy all'
        'show segment-routing traffic-eng policy name {name}'
        'show segment-routing traffic-eng policy all detail'
        'show segment-routing traffic-eng policy name {name} detail'
    """

    schema = {
        Any(): {
            "name": str,
            "color": int,
            Optional("end_point"): str,
            "status": {
                "admin": str,
                "operational": {
                    "state": str,
                    "time_for_state": str,
                    "since": str,
                },
            },
            Optional("candidate_paths"): {
                "preference": {
                    Any(): {
                        Optional("constraints"): {
                            "affinity": {
                                Any(): list
                            },
                        Optional("client"): str
                        },
                        "path_type": {
                            Optional("dynamic"): {
                                "status": str,
                                Optional("pce"): bool,
                                Optional("weight"): int,
                                "metric_type": str,
                                Optional("path_accumulated_metric"): int,
                                Optional("hops"): {
                                    Any(): {
                                        "sid": int,
                                        Optional("sid_type"): str,
                                        Optional("local_address"): str,
                                        Optional("remote_address"): str,
                                    },
                                },
                            },
                            Optional("explicit"): {
                                Any(): {
                                    Any(): {
                                        "status": str,
                                        "weight": int,
                                        "metric_type": str,
                                        Optional("hops"): {
                                            Any(): {
                                                "sid": int,
                                                Optional("sid_type"): str,
                                                Optional("local_address"): str,
                                                Optional("remote_address"): str,
                                            },
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
            Optional("attributes"): {
                "binding_sid": {
                    Any(): {
                        "allocation_mode": str,
                        "state": str,
                    },
                },
            },
            Optional("forwarding_id"): str,
            Optional("stats"): {
                "packets": int,
                "bytes": int,
            },
            Optional("event_history"): {
                Any(): {
                    "timestamp": str,
                    "client": str,
                    "event_type": str,
                    "context": str,
                },
            },
        },
    }


class ShowSegmentRoutingTrafficEngPolicy(ShowSegmentRoutingTrafficEngPolicySchema):
    """ Parser for 
        'show segment-routing traffic-eng policy all'
        'show segment-routing traffic-eng policy name {name}'
    """

    cli_command = ['show segment-routing traffic-eng policy all', 
                   'show segment-routing traffic-eng policy name {name}']

    def cli(self, name=None, output=None):
        if output is None:
            if name:
                cmd = self.cli_command[1].format(name=name)
            else:
                cmd = self.cli_command[0]

            out = self.device.execute(cmd)
        else:
            out = output

        # Name: test1 (Color: 100 End-point: 10.169.196.241)
        # Name: test_genie_1 (Color: 0 End-point: )
        p1 = re.compile(r'^Name: +(?P<name>\S+) +\(Color: +(?P<color>\d+) '
                         '+End-point: *(?P<end_point>\S+)?\)$')

        # Status:
        #     Admin: up, Operational: up for 09:38:18 (since 08-28 20:56:55.275)
        p2 = re.compile(r'^Admin: +(?P<admin>\S+), +Operational: +(?P<oper>\S+) '
                         '+for +(?P<time>\S+) +\(since +(?P<since>[\S\s]+)\)$')

        # Candidate-paths:
        #     Preference 400:
        p3 = re.compile(r'^Preference +(?P<preference>\d+)+\s*\w*:$')

        #     Dynamic (pce) (inactive)
        #     Dynamic (active)
        p4 = re.compile(r'^Dynamic( +(?P<pce>\(pce.*\)))? +\((?P<status>\w+)\)$')

        #         Weight: 0, Metric Type: TE
        p5 = re.compile(r'^Weight: +(?P<weight>[\d]+), +Metric +Type: '
                         '+(?P<metric_type>[\S]+)$')

        #         Metric Type: IGP, Path Accumulated Metric: 2200
        p6 = re.compile(r'^Metric +Type: +(?P<metric_type>[\S]+), Path +Accumulated '
                         '+Metric: +(?P<path_accumulated_metric>[\d]+)$')

        #         16063 [Prefix-SID, 10.169.196.241]
        #         16072 [Prefix-SID, 10.189.5.253 - 10.189.6.253]
        #         16063
        p7 = re.compile(r'^(?P<sid>[\d]+)(?: +\[(?P<sid_type>[\S]+), +(?P<local_address>[\S]+)'
                         '( +- +(?P<remote_address>[\S]+))?\])?$')

        #     Explicit: segment-list test1 (inactive)
        p8 = re.compile(r'^Explicit: +(?P<category>\S+) +(?P<name>\S+) +\((?P<status>\w+)\)$')

        # Attributes:
        #     Binding SID: 15000
        p9 = re.compile(r'^Binding +SID: +(?P<binding_sid>[\d]+)$')

        #     Allocation mode: explicit
        p10 = re.compile(r'^Allocation +mode: +(?P<allocation_mode>[\S]+)$')

        #     State: Programmed
        p11 = re.compile(r'^State: +(?P<state>[\S]+)$')

        #  Forwarding-ID: 65536 (0x18)
        #  Forwarding-ID: 65536
        p12 = re.compile(r'^Forwarding-ID: +(?P<id>[\d]+)(?P<extra>[\S\s]+)?$')

        # Stats:
        #   Packets: 44         Bytes: 1748
        p13 = re.compile(r'^Packets: +(?P<packets>[\d]+) +Bytes: +(?P<bytes>[\d]+)$')

        # Event history:
        #   Timestamp                   Client                  Event type              Context: Value
        #   08-29 14:51:29.074          FH Resolution           REOPT triggered         Status: REOPTIMIZED
        p14 = re.compile(r'^(?P<timestamp>[\d\-]+ [\d:.]+) +(?P<client>(?:[\S]+ )+) '
                          '+(?P<event_type>(?:[\S]+ )+) +(?P<context>(?: [\S]+)+: +(?:[\s\S]+))$')

        # Affinity:
        p15 = re.compile(r'^Affinity:$')

        # exclude-any
        # include-all
        # include-any
        p16 = re.compile(r'^(?P<affinity_type>exclude-any|include-all|include-any):$')

        # blue
        # green
        p17 = re.compile(r'^(?P<affinity>\w+)$')

        # initial variables
        aff_flag=False
        ret_dict = {}

        for line in out.splitlines():
            line = line.replace('\t', '    ')
            line = line.strip()
            if not line:
                continue

            # Name: test1 (Color: 100 End-point: 10.169.196.241)
            m = p1.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                name = group['name']
                policy_dict = ret_dict.setdefault(name, {})

                policy_dict.update({'name': name})
                policy_dict.update({'color': int(group['color'])})
                if group.get('end_point', None):
                    policy_dict.update({'end_point': group['end_point']})
                event_index = 0
                continue

            # Status:
            #     Admin: up, Operational: up for 09:38:18 (since 08-28 20:56:55.275)
            m = p2.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                status_dict = policy_dict.setdefault('status', {})
                status_dict.update({'admin': group['admin']})

                oper_dict = status_dict.setdefault('operational', {})
                oper_dict.update({'state': group['oper']})
                oper_dict.update({'time_for_state': group['time']})
                oper_dict.update({'since': group['since']})
                continue

            # Candidate-paths:
            #   Preference 400:
            m = p3.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                pref = int(group['preference'])
                pref_dict = policy_dict.setdefault("candidate_paths", {}).\
                            setdefault('preference', {}).setdefault(pref, {})
                hop_index = 0
                continue

            #   Dynamic (pce) (inactive)
            m = p4.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                path_dict = pref_dict.setdefault('path_type', {}).setdefault('dynamic', {})
                path_dict.update({'status': group['status']})
                if group['pce']:
                    path_dict.update({'pce': True})
                continue

            #   Weight: 0, Metric Type: TE
            m = p5.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                path_dict.update({'weight': int(group['weight'])})
                path_dict.update({'metric_type': group['metric_type']})
                continue

            #   Metric Type: IGP, Path Accumulated Metric: 2200
            m = p6.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                path_dict.update({'metric_type': group['metric_type']})

                metric = int(group['path_accumulated_metric'])
                path_dict.update({'path_accumulated_metric': metric})
                continue

            #   16063 [Prefix-SID, 10.169.196.241]
            #   16063
            m = p7.match(line)
            if m:
                aff_flag = False
                hop_index += 1
                group = m.groupdict()
                hop_dict = path_dict.setdefault('hops', {}).setdefault(hop_index, {})
                
                hop_dict.update({'sid': int(group['sid'])})
                if group.get('sid_type'):
                    hop_dict.update({'sid_type': group['sid_type']})
                if group.get('local_address'):
                    hop_dict.update({'local_address': group['local_address']})
                if group.get('remote_address'):
                    hop_dict.update({'remote_address': group['remote_address']})
                continue

            #   Explicit: segment-list test1 (inactive)
            m = p8.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                category = group['category'].replace('-', '_')
                name = group['name']

                path_dict = pref_dict.setdefault('path_type', {}).\
                            setdefault('explicit', {}).\
                            setdefault(category, {}).\
                            setdefault(name, {})
                path_dict.update({'status': group['status']})
                continue
                
            # Attributes:
            #   Binding SID: 15000
            m = p9.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                sid = int(group['binding_sid'])
                bind_dict = policy_dict.setdefault("attributes", {}).\
                            setdefault('binding_sid', {}).setdefault(sid, {})
                continue

            #   Allocation mode: explicit
            m = p10.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                bind_dict.update({'allocation_mode': group['allocation_mode'].lower()})
                continue

            #   State: Programmed
            m = p11.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                bind_dict.update({'state': group['state'].lower()})
                continue

            #   Forwarding-ID: 65536 (0x18)
            m = p12.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                policy_dict.update({'forwarding_id': group['id']})
                continue

            #   Packets: 44         Bytes: 1748
            m = p13.match(line)
            if m:
                aff_flag = False
                group = m.groupdict()
                stats = policy_dict.setdefault('stats', {})
                stats.update({k: int(v) for k, v in group.items()})
                continue

            # Timestamp                   Client                  Event type              Context: Value 
            # 08-29 14:51:29.074          FH Resolution           REOPT triggered         Status: REOPTIMIZED
            m = p14.match(line)
            if m:
                aff_flag = False
                event_index += 1
                group = m.groupdict()
                event = policy_dict.setdefault('event_history', {}).setdefault(event_index, {})
                event.update({k: v.strip() for k, v in group.items()})
                continue

            # Affinity:
            m = p15.match(line)
            if m:
                aff_flag = True
                aff_dict = pref_dict.setdefault('constraints', {}).setdefault('affinity', {})
                continue

            if aff_flag:
                # exclude-any
                # include-all
                # include-any
                m = p16.match(line)
                if m:
                    aff_type = m.groupdict()['affinity_type']
                    aff_dict.update({aff_type: []})
                    continue

            if aff_flag:
                # blue
                m = p17.match(line)
                if m:
                    temp_list = aff_dict.get(aff_type)
                    if temp_list is not None:
                        temp_list.append(m.groupdict()['affinity'])
                        aff_dict.update({aff_type: temp_list})

        return ret_dict


class ShowSegmentRoutingTrafficEngPolicyDetail(ShowSegmentRoutingTrafficEngPolicy):
    """ Parser for 
        'show segment-routing traffic-eng policy all detail'
        'show segment-routing traffic-eng policy name {name} detail'
    """

    cli_command = ['show segment-routing traffic-eng policy all detail',
                   'show segment-routing traffic-eng policy name {name} detail']

    def cli(self, name=None, output=None):
        if output is None:
            if name:
                cmd = self.cli_command[1].format(name=name)
            else:
                cmd = self.cli_command[0]

            out = self.device.execute(cmd)
        else:
            out = output

        return super().cli(output=out)


# ====================================================
# Schema for:
#   * 'show segment-routing mpls mapping-server ipv4'
#   * 'show segment-routing mpls mapping-server ipv6'
# ====================================================
class ShowSegmentRoutingMplsMappingServerSchema(MetaParser):
    ''' Schema for:
        * 'show segment-routing mpls mapping-server ipv4'
        * 'show segment-routing mpls mapping-server ipv6'
    '''

    schema = {
        'segment_routing': {
                'bindings': {
                    'mapping_server': {
                        'policy': {
                            Optional('prefix_sid_export_map'): {
                                Optional('ipv4'): {
                                    Optional('mapping_entry'): {
                                        Any(): {
                                            'algorithm': {
                                                Any(): {
                                                    'prefix': str,
                                                    'value_type': str,
                                                    'sid': int,
                                                    'range': str,
                                                    'algorithm': str,
                                                    'srgb': str,
                                                }
                                            }
                                        }
                                    }
                                },
                                Optional('ipv6'): {
                                    Optional('mapping_entry'): {
                                        Any(): {
                                            'algorithm': {
                                                Any(): {
                                                    'prefix': str,
                                                    'value_type': str,
                                                    'sid': int,
                                                    'range': str,
                                                    'algorithm': str,
                                                    'srgb': str,
                                                }
                                            }
                                        }
                                    }
                                }
                            },
                            Optional('prefix_sid_remote_export_map'): {
                                Optional('ipv4'): {
                                    Optional('mapping_entry'): {
                                        Any(): {
                                            'algorithm': {
                                                Any(): {
                                                    'prefix': str,
                                                    'value_type': str,
                                                    'sid': int,
                                                    'range': str,
                                                    'algorithm': str,
                                                    Optional('source'): str,
                                                    'srgb': str,
                                                }
                                            }
                                        }
                                    }
                                },
                                Optional('ipv6'): {
                                    Optional('mapping_entry'): {
                                        Any(): {
                                            'algorithm': {
                                                Any(): {
                                                    'prefix': str,
                                                    'value_type': str,
                                                    'sid': int,
                                                    'range': str,
                                                    'algorithm': str,
                                                    Optional('source'): str,
                                                    'srgb': str,
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
# ====================================================
# Parser for:
#   * 'show segment-routing mpls mapping-server ipv4'
#   * 'show segment-routing mpls mapping-server ipv6'
# ====================================================

class ShowSegmentRoutingMplsMappingServer(ShowSegmentRoutingMplsMappingServerSchema):
    ''' Parser for:
        * 'show segment-routing mpls mapping-server ipv4'
        * 'show segment-routing mpls mapping-server ipv6'
    '''
    
    cli_command = 'show segment-routing mpls mapping-server {address_family}'
    
    def cli(self, address_family, output=None):

        assert address_family in ['ipv4', 'ipv6']

        # Get output
        if output is None:
            out = self.device.execute(self.cli_command.format(address_family=address_family))
        else:
            out = output
        
        # Mapping dict
        mapping_dict_export = {
            'ipv4': 'ipv4_prefix_sid_export_map',
            'ipv6': 'ipv6_prefix_sid_export_map',
        }

        mapping_dict_remote_export = {
            'ipv4': 'ipv4_prefix_sid_remote_export_map',
            'ipv6': 'ipv6_prefix_sid_remote_export_map',
        }

        # Init
        ret_dict = {}

        # PREFIX_SID_EXPORT_MAP ALGO_0
        # PREFIX_SID_EXPORT_MAP ALGO_1
        p1 = re.compile(r'^PREFIX_SID_EXPORT_MAP +(?P<algorithm>(\S+))$')

        # PREFIX_SID_REMOTE_EXPORT_MAP ALGO_0
        # PREFIX_SID_REMOTE_EXPORT_MAP ALGO_1
        p2 = re.compile(r'^PREFIX_SID_REMOTE_EXPORT_MAP +(?P<algorithm>(\S+))$')

        # Prefix/masklen   SID Type Range Flags SRGB
        # 10.4.1.1/32         1 Indx     1         Y
        p3 = re.compile(r'(?P<prefix>(\S+))\/(?P<masklen>(\d+)) +(?P<sid>(\d+))'
                         ' +(?P<type>(\S+)) +(?P<range>(\d+))'
                         '(?: +(?P<flags>(\S+)))? +(?P<srgb>(Y|N))$')

        # Prefix/masklen   SID Type Range Flags SRGB Source
        # 10.4.1.1/32         1 Indx     1         Y  OSPF Area 8 10.4.1.1
        # 10.16.2.2/32         2 Indx     1         Y  OSPF Area 8 10.16.2.2
        p4 = re.compile(r'(?P<prefix>(\S+))\/(?P<masklen>(\d+)) +(?P<sid>(\d+))'
                         ' +(?P<type>(\S+)) +(?P<range>(\d+))'
                         '(?: +(?P<flags>(\S+)))? +(?P<srgb>(Y|N))'
                         ' +(?P<source>(.*))$')

        for line in out.splitlines():
            line = line.strip()

            # PREFIX_SID_EXPORT_MAP ALGO_0
            # PREFIX_SID_EXPORT_MAP ALGO_1
            m = p1.match(line)
            if m:
                algorithm = m.groupdict()['algorithm']
                continue

            # PREFIX_SID_REMOTE_EXPORT_MAP ALGO_0
            # PREFIX_SID_REMOTE_EXPORT_MAP ALGO_1
            m = p2.match(line)
            if m:
                algorithm = m.groupdict()['algorithm']
                continue

            # Prefix/masklen   SID Type Range Flags SRGB
            # 10.4.1.1/32         1 Indx     1         Y
            m = p3.match(line)
            if m:
                group = m.groupdict()
                address_family_dict = ret_dict.setdefault('segment_routing', {}). \
                                    setdefault('bindings', {}). \
                                    setdefault('mapping_server', {}). \
                                    setdefault('policy', {}). \
                                    setdefault('prefix_sid_export_map', {}). \
                                    setdefault(address_family, {})

                prefix = group['prefix'] + '/' + group['masklen']
                algo_dict = address_family_dict.setdefault('mapping_entry', {}). \
                                setdefault(prefix, {}). \
                                setdefault('algorithm', {}). \
                                setdefault(algorithm, {})
                # Set values
                algo_dict['prefix'] = prefix
                algo_dict['algorithm'] = algorithm
                algo_dict['value_type'] = group['type']
                algo_dict['sid'] = int(group['sid'])
                algo_dict['range'] = group['range']
                algo_dict['srgb'] = group['srgb']
                if group['flags']:
                    algo_dict['flags'] = group['flags']
                continue

            # Prefix/masklen   SID Type Range Flags SRGB Source
            # 10.4.1.1/32         1 Indx     1         Y  OSPF Area 8 10.4.1.1
            m = p4.match(line)
            if m:
                group = m.groupdict()
                address_family_dict = ret_dict.setdefault('segment_routing', {}). \
                                    setdefault('bindings', {}). \
                                    setdefault('mapping_server', {}). \
                                    setdefault('policy', {}). \
                                    setdefault('prefix_sid_remote_export_map', {}). \
                                    setdefault(address_family, {})
                                    
                prefix = group['prefix'] + '/' + group['masklen']
                # Set dict
                algo_dict = address_family_dict.setdefault('mapping_entry', {}). \
                                setdefault(prefix, {}). \
                                setdefault('algorithm', {}). \
                                setdefault(algorithm, {})
                # Set values
                algo_dict['prefix'] = prefix
                algo_dict['algorithm'] = algorithm
                algo_dict['value_type'] = group['type']
                algo_dict['sid'] = int(group['sid'])
                algo_dict['range'] = group['range']
                algo_dict['srgb'] = group['srgb']
                algo_dict['source'] = group['source']
                if group['flags']:
                    algo_dict['flags'] = group['flags']
                continue

        return ret_dict


class ShowSegmentRoutingMplsLbAssignedSidsSchema(MetaParser):
    """ Schema for:
            * show segment-routing mpls lb assigned-sids
    """
    schema = {
        'segment_routing': {
            'sid': {
                Any(): {
                    'state': str,
                    'state_info': str,
                    Optional('protocol'): str,
                    Optional('topoid'): int,
                    Optional('lan'): str,
                    Optional('pro'): str,
                    Optional('neighbor'): str,
                    Optional('interface'): str
                }
            }
        }
    }


class ShowSegmentRoutingMplsLbAssignedSids(ShowSegmentRoutingMplsLbAssignedSidsSchema):
    """ Parser for:
            * show segment-routing mpls lb assigned-sids
    """

    cli_command = "show segment-routing mpls lb assigned-sids"

    state_mapping = {
        "C": "In conflict",
        "S": "Shared",
        "R": "In range"
    }

    def cli(self, output=None):
        if not output:
            output = self.device.execute(self.cli_command)

        # 12345   R
        # 12345    S ISIS     2        N   N   192.168.0.1 Ethernet1
        p1 = re.compile(r"^(?P<sid>\d+) +(?P<state>\w)(?: +(?P<protocol>\w+) +"
                        r"(?P<topoid>\d+) +(?P<lan>\w+) +(?P<pro>\w+) +"
                        r"(?P<neighbor>[\d\.]+) +(?P<interface>[\w\/\.]+))?$")

        ret_dict = {}

        for line in output.splitlines():
            line = line.strip()

            # 12345   R
            # 12345    S ISIS     2        N   N   192.168.0.1 Ethernet1
            m = p1.match(line)
            if m:
                groups = m.groupdict()

                sid_dict = ret_dict.setdefault("segment_routing", {})\
                                   .setdefault("sid", {})\
                                   .setdefault(groups["sid"], {})

                sid_dict.update({"state": groups["state"]})
                sid_dict.update({"state_info": self.state_mapping[groups["state"]]})

                if groups["protocol"]:
                    sid_dict.update({"protocol": groups["protocol"]})
                    sid_dict.update({"topoid": int(groups['topoid'])})
                    sid_dict.update({"lan": groups["lan"]})
                    sid_dict.update({"pro": groups["pro"]})
                    sid_dict.update({"neighbor": groups["neighbor"]})
                    sid_dict.update({"interface": groups["interface"]})

        return ret_dict
