from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Or, Optional, ListOf
import re
# from genie.metaparser.util.schemaengine import Schema, Any, Optional, Or, ListOf, And,\
#                                          Default, Use


# ======================================================
# Schema for 'show ip nbar protocol-discovery protocol'
# ======================================================
class ShowIPNameServerSchema(MetaParser):
    '''
	Schema for:
	show ip name-servers
	show ip name-servers vrf {vrf}
	'''
    schema = {
        'vrf': {
             Any(): ListOf(str),
        },
    }


# ==============================
# Parser for 'show ip name-servers', 'show ip name-servers vrf {vrf}'
# ==============================
class ShowIPNameServer(ShowIPNameServerSchema):
    '''
    Parser for:
    show ip name-servers
    show ip name-servers vrf {vrf}
    '''
    cli_command = ['show ip name-servers',
        'show ip name-servers vrf {vrf}']
            
    def cli(self, vrf = '', output = None):
        if output is None:
            if vrf:
                out = self.device.execute(self.cli_command[1].format(vrf = vrf))
            else:
                out = self.device.execute(self.cli_command[0])
        else:
            out = output

        # Init vars
        parsed_dict = {}
        # 255.255.255.255 matching ipv4 address
        p1 = re.compile(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}")
        # ABCD:1234::1 matching ipv6 address
        p2 = re.compile(r"[a-fA-F\d\:]+")

        if not vrf:
            vrf = 'default'

        for line in out.splitlines():
            line = line.strip()

            # match the line with ipv4 address
            m1 = p1.match(line)      
            # match the line with ipv6 address
            m2 = p2.match(line)      
            if m1 or m2  :     
               ip_flow = parsed_dict.setdefault("vrf", {}).setdefault(
                    (vrf), []
               )
               ip_flow.append(line)
               continue
       
        return parsed_dict
    
