################################################################################
#                                                                              #
# Copyright (c) 2015 Cisco Systems                                             #
# All Rights Reserved.                                                         #
#                                                                              #
#    Licensed under the Apache License, Version 2.0 (the "License"); you may   #
#    not use this file except in compliance with the License. You may obtain   #
#    a copy of the License at                                                  #
#                                                                              #
#         http://www.apache.org/licenses/LICENSE-2.0                           #
#                                                                              #
#    Unless required by applicable law or agreed to in writing, software       #
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT #
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the  #
#    License for the specific language governing permissions and limitations   #
#    under the License.                                                        #
#                                                                              #
################################################################################
"""NX Toolkit module for physical objects
"""
import datetime
from .nxbaseobject import BaseNXObject, BaseNXPhysModule, BaseInterface
from .nxConcreteLib import *
from .nxsession import Session
from .nxcounters import InterfaceStats
import logging
import re
import copy
from .nxSearch import Searchable



class Linecard(BaseNXPhysModule):
    """ class for a linecard of a switch   """

    def __init__(self, slot=None, parent=None):
        """Initialize the basic object.  It will create the
        name of the linecard and set the type
        before calling the base class __init__ method.
        If arg1 is an instance of a Node, then pod,
        and node are derived from the Node and the slot_id
        is from arg0.  If arg1 is not a Node, then arg0
        is the pod, arg1 is the node id, and slot is the slot_id

        In other words, this Linecard object can either be initialized by

        `>>> lc = Linecard(slot_id)`

        or

        `>>> lc = Linecard(slot_id, parent_switch)`

        :param slot: slot_id if arg1 is node_id Not required if arg1 is a Node
        :param parent: parent switch of type Node.  Not required if arg1 is 
               used instead.

        :returns: None
        """
        self.type = 'linecard'
        self.check_parent(parent)
        super(Linecard, self).__init__(slot, parent)
        self.name = 'lcslot-' + '/'.join([slot])

    @classmethod
    def _get_switch_classes(cls):
        """
        Get the Switch classes used by this nxtoolkit class.

        :returns: list of strings containing Switch class names
        """
        resp = ['eqptLC']

        return resp

    @staticmethod
    def _get_parent_class():
        """
        Gets the nxtoolkit class of the parent object

        :returns: class of parent object
        """
        return Node

    @staticmethod
    def _get_children_classes():
        """
        Get the nxtoolkit class of the children of this object.

        This is meant to be overridden by any inheriting classes that have 
        children.
        If they don't have children, this will return an empty list.
        :return: list of classes
        """
        return [Interface]

    @classmethod
    def get(cls, session, parent=None):
        """Gets all of the linecards from the Switch.  If parent is
        specified, it will only get linecards that are
        children of the the parent.  The linecards will also
        be added as children to the parent Node.

        The lincard object is derived mostly from the Switch 'eqptLC' class.

        :param session: Switch session
        :param parent: optional parent of class Node

        :returns: list of linecards
        """
        return cls.get_obj(session, cls._get_switch_classes(), parent)

    def _populate_from_attributes(self, attributes):
        """Fills in an object with the desired attributes.
           Overridden by inheriting classes to provide the specific attributes
           when getting objects from the Switch.
        """
        self.serial = str(attributes['ser'])
        self.model = str(attributes['model'])
        self.descr = str(attributes['descr'])
        self.num_ports = str(attributes['numP'])
        self.hardware_version = str(attributes['hwVer'])
        self.hardware_revision = str(attributes['rev'])
        self.type = str(attributes['type'])
        self.oper_st = str(attributes['operSt'])
        self.dn = str(attributes['dn'])
        self.modify_time = str(attributes['modTs'])

    @staticmethod
    def get_table(linecards, super_title=''):
        """
        Will create table of line card information
        :param super_title:
        :param linecards:
        """
        result = []

        headers = ['Slot', 'Model', 'Ports',
                   'Firmware', 'Bios', 'HW Ver', 'Hw Rev',
                   'Oper St', 'Serial', 'Modify Time']
        table = []
        for module in sorted(linecards, key=lambda x: x.slot):
            table.append([module.slot,
                          module.model,
                          module.num_ports,
                          module.firmware,
                          module.bios,
                          module.hardware_version,
                          module.hardware_revision,
                          module.oper_st,
                          module.serial,
                          module.modify_time])

        result.append(Table(table, headers, title=super_title + 'Linecards'))
        return result


class Supervisorcard(BaseNXPhysModule):
    """Class representing the supervisor card of a switch
    """

    def __init__(self, slot, parent=None):
        """ Initialize the basic object.  This should be called by the
            init routines of inheriting subclasses.

            :param slot: slot id
            :param parent: optional parent object
        """
        self.type = 'supervisor'
        self.check_parent(parent)
        super(Supervisorcard, self).__init__(slot, parent)
        self.name = 'supslot-' + '/'.join([slot])

    @classmethod
    def _get_switch_classes(cls):
        """
        Get the Switch classes used by this nxtoolkit class.

        :returns: list of strings containing Switch class names
        """
        resp = ['eqptSupC']

        return resp

    @staticmethod
    def _get_parent_class():
        """
        Gets the nxtoolkit class of the parent object

        :returns: class of parent object
        """
        return Node

    @classmethod
    def get(cls, session, parent_node=None):
        """Gets all of the supervisor cards from the Switch.
        If parent is specified, it will only get the
        supervisor card that is a child of the the parent Node.
        The supervisor will also be added as a child to the parent Node.

        The Supervisorcard object is derived mostly from the
        Switch 'eqptSupC' class.

        If `parent_node` is a str, then it is the Node id of the switch
        for the supervisor.

        :param session: Switch session
        :param parent_node: optional parent switch of class Node or the node
               id of a switch

        :returns: list of linecards
        """

        return cls.get_obj(session, cls._get_switch_classes(), parent_node)

    def _populate_from_attributes(self, attributes):
        """Fills in an object with the desired attributes.
           Overridden by inheriting classes to provide the specific attributes
           when getting objects from the Switch.
        """
        self.serial = str(attributes['ser'])
        self.model = str(attributes['model'])
        self.dn = str(attributes['dn'])
        self.descr = str(attributes['descr'])
        self.type = str(attributes['type'])
        self.num_ports = str(attributes['numP'])
        self.hardware_version = str(attributes['hwVer'])
        self.hardware_revision = str(attributes['rev'])
        self.oper_st = str(attributes['operSt'])
        self.modify_time = str(attributes['modTs'])

    @staticmethod
    def get_table(modules, super_title=''):
        """
        Will create table of supervisor information
        :param super_title:
        :param modules:
        """
        result = []

        headers = ['Slot', 'Model', 'Ports', 'Firmware', 'Bios',
                   'HW Ver', 'Hw Rev', 'Oper St', 'Serial', 'Modify Time']
        table = []
        for module in sorted(modules, key=lambda x: x.slot):
            table.append([module.slot,
                          module.model,
                          module.num_ports,
                          module.firmware,
                          module.bios,
                          module.hardware_version,
                          module.hardware_revision,
                          module.oper_st,
                          module.serial,
                          module.modify_time])

        result.append(Table(table, headers, title=super_title + 'Supervisors'))
        return result


class Fantray(BaseNXPhysModule):
    """Class for the fan tray of a node"""

    def __init__(self, slot, parent=None):
        """ Initialize the basic object.  It will create
        the name of the fan tray and set the type
        before calling the base class __init__ method
        :param slot: slot id
        :param parent: optional parent object
        """
        self.type = 'fantray'
        self.status = None
        self.check_parent(parent)
        super(Fantray, self).__init__(slot, parent)
        self.name = 'FT-' + '/'.join([slot])

    @classmethod
    def _get_switch_classes(cls):
        """
        Get the Switch classes used by this nxtoolkit class.

        :returns: list of strings containing Switch class names
        """
        resp = ['eqptFt']

        return resp

    @staticmethod
    def _get_parent_class():
        """
        Gets the nxtoolkit class of the parent object

        :returns: class of parent object
        """
        return Node

    @staticmethod
    def _get_children_classes():
        """
        Get the nxtoolkit class of the children of this object.
        
        This is meant to be overridden by any inheriting classes that 
        have children. If they don't have children, this will return
        an empty list.
        :return: list of classes
        """
        return [Fan]

    @classmethod
    def get(cls, session, parent=None):
        """Gets all of the fantrays from the Switch.

        If parent is specified, it will only get fantrays that are
        children of the the parent.  The fantrays will
        also be added as children to the parent Node.

        The fantray object is derived mostly from the Switch 'eqptFt' class.

        :param session: Switch session
        :param parent: optional parent switch of class Node

        :returns: list of fantrays
        """

        fans = cls.get_obj(session, cls._get_switch_classes(), parent)
        return fans

    def _populate_from_attributes(self, attributes):
        """Fills in an object with the desired attributes.
           Overridden by inheriting classes to provide the specific attributes
           when getting objects from the Switch.
        """
        self.serial = str(attributes['ser'])
        self.model = str(attributes['model'])
        self.dn = str(attributes['dn'])
        self.descr = str(attributes['descr'])
        self.oper_st = str(attributes['operSt'])
        self.name = str(attributes.get('fanName', 'None'))
        self.status = str(attributes['status'])
        self.modify_time = str(attributes['modTs'])

    @staticmethod
    def _get_firmware(dist_name):
        """ Returns None for firmware and bios revisions"""
        return None, None

    @staticmethod
    def get_table(modules, title=''):
        """
        Will create table of fantry information
        :param title:
        :param modules:
        """
        result = []

        headers = ['Slot', 'Model', 'Name', 'Tray Serial',
                   'Fan ID', 'Oper St', 'Direction', 'Speed', 'Fan Serial']
        table = []
        for fantray in sorted(modules, key=lambda x: x.slot):
            fans = fantray.get_children(Fan)

            first_fan = sorted(fans, key=lambda x: x.id)[0]
            table.append([fantray.slot,
                          fantray.model,
                          fantray.name,
                          fantray.serial,
                          'fan-' + first_fan.id,
                          first_fan.oper_st,
                          first_fan.direction,
                          first_fan.speed,
                          first_fan.serial])
            for fan in sorted(fans, key=lambda x: x.id):
                if fan != first_fan:
                    table.append([fantray.slot,
                                  fantray.model,
                                  fantray.name,
                                  fantray.serial,
                                  'fan-' + fan.id,
                                  fan.oper_st,
                                  fan.direction,
                                  fan.speed,
                                  fan.serial])

        result.append(Table(table, headers, title=title + 'Fan Trays'))
        return result


class Fan(BaseNXPhysModule):
    """Class for the fan of a fan tray"""

    def __init__(self, parent=None):
        """ Initialize the basic fan.

            :param identifier: fan id - optional
            :param parent: optional parent Fantray object
            """
        self.type = 'fan'
        if parent:
            super(Fan, self).__init__(parent.slot, parent)
        else:
            super(Fan, self).__init__(slot=None, parent=parent)
        self.descr = None
        self.oper_st = None
        self.direction = None
        self.speed = None
        self.id = None

    @classmethod
    def _get_switch_classes(cls):
        """
        Get the Switch classes used by this nxtoolkit class.

        :returns: list of strings containing Switch class names
        """
        resp = ['eqptFan']

        return resp

    @staticmethod
    def _get_parent_class():
        """
        Gets the nxtoolkit class of the parent object

        :returns: class of parent object
        """
        return Fantray

    @classmethod
    def get(cls, session, parent=None):
        """Gets all of the fans from the Switch.  If parent
        is specified, it will only get fantrays that are
        children of the the parent.  The fantrays will
        also be added as children to the parent Node.

        The fan object is derived mostly from the Switch 'eqptFan' class.

        :param session: Switch session
        :param parent: optional parent fantray of class Fantray

        :returns: list of fans
        """

        cls.check_session(session)
        cls.check_parent(parent)
        fans = []

        # get the total number of ports = number of power supply slots
        if parent:
            mo_query_url = '/api/mo/' + parent.dn + \
                           '.json?query-target=subtree&target-subtree-class=' + \
                           ','.join(cls._get_switch_classes())

        else:
            mo_query_url = ('/api/node/class/eqptFan.json?'
                            'query-target=self')

        ret = session.get(mo_query_url)
        node_data = ret.json()['imdata']
        if node_data:
            for fan_obj in node_data:
                fan = Fan()
                fan.dn = str(fan_obj['eqptFan']['attributes']['dn'])
                fan.id = str(fan_obj['eqptFan']['attributes']['id'])
                fan.descr = str(fan_obj['eqptFan']['attributes']['descr'])
                fan.oper_st = str(fan_obj['eqptFan']['attributes']['operSt'])
                fan.direction = str(fan_obj['eqptFan']['attributes']['dir'])
                fan.model = str(fan_obj['eqptFan']['attributes']['model'])
                fan.serial = str(fan_obj['eqptFan']['attributes']['ser'])

                # now get speed if it is being monitored
                mo_query_url = '/api/mo/' + fan.dn + \
                               '.json?rsp-subtree-include=stats&rsp-subtree-class=eqptFanStats5min'
                ret = session.get(mo_query_url)
                stat_data = ret.json()['imdata']
                fan.speed = 'unknown'
                if stat_data:
                    if 'eqptFan' in stat_data[0]:
                        if 'children' in stat_data[0]['eqptFan']:
                            if stat_data[0]['eqptFan']['children']:
                                if 'eqptFanStats5min' in stat_data[0]['eqptFan']['children'][0]:
                                    fan.speed = \
                                        str(stat_data[0]['eqptFan']['children'][0]['eqptFanStats5min']['attributes'][
                                                'speedLast'])

                if parent:
                    fan._parent = parent
                    parent.add_child(fan)
                fans.append(fan)
        return fans

    def __eq__(self, other):
        """compares two fans and returns True if they are the same.
        """
        if type(self) == type(other):
            if self.model == other.model:
                if self.id == other.id:
                    if self._parent == other._parent:
                        return True
        return False


class Powersupply(BaseNXPhysModule):
    """ class for a power supply in a node   """

    def __init__(self, slot, parent=None):
        """ Initialize the basic object.  It will create
        the name of the powersupply and set the type
        before calling the base class __init__ method
        :param slot: slot id
        :param parent: optional parent object
        """
        self.type = 'powersupply'
        self.check_parent(parent)
        super(Powersupply, self).__init__(slot, parent)
        self.status = None
        self.voltage_source = None
        self.fan_status = None
        self.name = 'PS-' + '/'.join([slot])

    @classmethod
    def _get_switch_classes(cls):
        """
        Get the Switch classes used by this nxtoolkit class.

        :returns: list of strings containing Switch class names
        """
        resp = ['eqptPsu']

        return resp

    @staticmethod
    def _get_parent_class():
        """
        Gets the nxtoolkit class of the parent object

        :returns: class of parent object
        """
        return Node

    @classmethod
    def get(cls, session, parent=None):
        """Gets all of the power supplies from the Switch.
        If parent is specified, it will only get power supplies that are
        children of the the parent.  The power supplies
        will also be added as children to the parent Node.

        The Powersupply object is derived mostly from the Switch 'eqptPsu' class.

        :param session: Switch session
        :param parent: optional parent switch of class Node

        :returns: list of powersupplies
        """
        return cls.get_obj(session, cls._get_switch_classes(), parent)

    def _populate_from_attributes(self, attributes):
        """Fills in an object with the desired attributes.
           Overridden by inheriting classes to provide the specific attributes
           when getting objects from the Switch.
        """
        self.serial = str(attributes['ser'])
        self.model = str(attributes['model'])
        self.dn = str(attributes['dn'])
        self.descr = str(attributes['descr'])
        self.oper_st = str(attributes['operSt'])
        self.fan_status = str(attributes['fanOpSt'])
        self.voltage_source = str(attributes['vSrc'])
        self.hardware_version = str(attributes['hwVer'])
        self.hardware_revision = str(attributes['rev'])
        self.status = str(attributes['status'])
        self.modify_time = str(attributes['modTs'])

    @staticmethod
    def _get_firmware(dist_name):
        """ The power supplies do not have a readable firmware or bios revision so
        this will return None for firmware and bios revisions"""

        return None, None

    @staticmethod
    def get_table(modules, super_title=''):
        """
        Will create table of power supply information
        :param super_title:
        :param modules:
        """
        result = []
        headers = ['Slot', 'Model', 'Source Power',
                   'Oper St', 'Fan State', 'HW Ver', 'Hw Rev', 'Serial', 'Uptime']

        table = []
        for pwr_sup in sorted(modules, key=lambda x: x.slot):
            # pwr_sup = modules[slot]
            table.append([pwr_sup.slot,
                          pwr_sup.model,
                          pwr_sup.voltage_source,
                          pwr_sup.oper_st,
                          pwr_sup.fan_status,
                          pwr_sup.hardware_version,
                          pwr_sup.hardware_revision,
                          pwr_sup.serial,
                          pwr_sup.modify_time])

        result.append(Table(table, headers, title=super_title + 'Power Supplies'))
        return result


class Node(BaseNXPhysObject):
    """Node :  roughly equivalent to fabricNode """

    def __init__(self, name=None, role=None):
        """
        :param name: Name of the node
        :param parent: Parent pod object of the node.
        """
        if name:
            if not isinstance(name, str):
                raise TypeError("Name must be a string")

        valid_roles = [None, 'spine', 'leaf', 'controller', 'vleaf', 'vip', 'protection-chain', 'unsupported']
        if role not in valid_roles:
            raise ValueError

        self.role = role
        self._session = None
        self.fabricSt = None
        self.ipAddress = None
        self.tep_ip = None
        self.macAddress = None
        self.state = None
        self.mode = None
        self.operSt = None
        self.operStQual = None
        self.descr = None
        self.model = None
        self.dn = None
        self.vendor = None
        self.serial = None
        self.health = None
        self.firmware = None
        self.num_ps_slots = 0
        self.num_fan_slots = 0
        self.num_sup_slots = 0
        self.num_lc_slots = 0
        self.num_ps_modules = 0
        self.num_fan_modules = 0
        self.num_sup_modules = 0
        self.num_lc_modules = 0
        self.num_ports = 0
        self.inb_mgmt_ip = None
        self.oob_mgmt_ip = None
        self.system_uptime = None
        self.vpc_info = None
        self.v4_proxy_ip = None
        self.mac_proxy_ip = None
        self.dynamic_load_balancing_mode = None
        logging.debug('Creating %s %s', self.__class__.__name__, 'pod-' +
                      str(self.pod) + '/node-' + str(self.node))
        super(Node, self).__init__(name=name)

    @staticmethod
    def _get_parent_class():
        """
        Gets the nxtoolkit class of the parent object
        Meant to be overridden by inheriting classes.
        Raises exception if not overridden.

        :returns: class of parent object
        """
        return None

    @staticmethod
    def _get_children_classes():
        """
        Get the nxtoolkit class of the children of this object.
        This is meant to be overridden by any inheriting classes that have children.
        If they don't have children, this will return an empty list.
        :return: list of classes
        """
        return [Supervisorcard, Linecard, Powersupply, Fantray]

    @staticmethod
    def _get_children_concrete_classes():
        """
        Get the nxtoolkit class of the concrete children of this object.
        This is meant to be overridden by any inheriting classes that have children.
        If they don't have children, this will return an empty list.
        :return: list of classes
        """
        return [ConcreteArp, ConcreteAccCtrlRule, ConcreteBD, ConcreteOverlay,
                ConcretePortChannel, ConcreteEp, ConcreteFilter, ConcreteLoopback,
                ConcreteContext, ConcreteSVI, ConcreteVpc]

    @classmethod
    def _get_switch_classes(cls):
        """gets list of all switch classes used to build this nxtoolkit class
        """
        resp = ['fabricNode','firmwareCardRunning', 'topSystem', 'vpcInst','vpcDom',
                'eqptCh','l1PhysIf','eqptFtSlot','eqptLCSlot','eqptPsuSlot',
                'eqptSupCSlot','topoctrlLbP',
                #'topoctrlVxlanP'
                ]
        return resp

    def get_role(self):
        """ retrieves the node role
        :returns: role
        """
        return self.role

    def getFabricSt(self):
        """ retrieves the fabric state.

        :returns: fabric state
        """
        return self.fabricSt

    @staticmethod
    def _parse_dn(dn):
        """Parses the pod and node from a
           distinguished name of the node.
        """
        name = dn.split('/')
        pod = name[1].split('-')[1]
        node = name[2].split('-')[1]
        return pod, node

    @classmethod
    def get(cls, session):
        """
        TODO: Currently not implemented fully
        :param session: Switch session
        :returns: list of Nodes
        """
        # need to add pod as parent
        cls.check_session(session)

        return Node

    def get_firmware(self, working_data):
        """
        retrieves firmware version
        """
        if self.role != 'controller':
            dn = self.dn + '/sys/ch/supslot-1/sup/running'
            data = working_data.get_object(dn)
            if data:
                if 'firmwareCardRunning' in data:
                    self.firmware = data['firmwareCardRunning']['attributes']['version']

    def get_health(self):
        """
        This will get the health of the switch node
        """
        if self.role != 'controller':
            mo_query_url = '/api/mo/' + self.dn + \
                           '/sys.json?&rsp-subtree-include=stats&rsp-subtree-class=fabricNodeHealth5min'
            ret = self._session.get(mo_query_url)
            data = ret.json()['imdata']
            if data:
                if 'topSystem' in data[0]:
                    if 'children' in data[0]['topSystem']:
                        if 'fabricNodeHealth5Min' in data[0]['topSystem']['children'][0]:
                            self.health = data[0]['topSystem']['children'][0]['fabricNodeHealth5min']\
                                ['attributes']['healthLast']

    def _add_vpc_info(self, working_data):
        """
        This method only runs for leaf switches.  If
        the leaf has a VPC peer, the VPC information will be populated
        and the node.vpc_present flag will be set.

        check for vpcDom sub-object
        and if it exists, then create the entry as a dictionary of values.

        Will first check vpc_inst to see if it is enabled
        then get vpcDom under vpcInst

        peer_present is true if vpcDom exists
        
        From vpcDom get :
            domain_id
            system_mac
            local_mac
            monitoring_policy
            peer_ip
            peer_system_mac
            peer_version
            peer_state
            vtep_ip
            vtep_mac
            oper_role
            
        """
        partial_dn = 'topology/pod-{0}/node-{1}/sys/vpc/inst'.format(self.pod, self.node)

        vpc_admin_state = 'disabled'
        data = working_data.get_object(partial_dn)
        if data:
            if 'vpcInst' in data:
                vpc_admin_state = data['vpcInst']['attributes']['adminSt']

        result = {'admin_state': vpc_admin_state}
        if vpc_admin_state == 'enabled':
            result['oper_state'] = 'inactive'
            data = working_data.get_subtree('vpcDom', partial_dn)
            if data:
                if 'vpcDom' in data[0]:
                    result['oper_state'] = 'active'
                    vpc_dom = data[0]['vpcDom']['attributes']
                    result['domain_id'] = vpc_dom['id']
                    result['system_mac'] = vpc_dom['sysMac']
                    result['local_mac'] = vpc_dom['localMAC']
                    result['monitoring_policy'] = vpc_dom['monPolDn']
                    result['peer_ip'] = vpc_dom['peerIp']
                    result['peer_mac'] = vpc_dom['peerMAC']
                    result['peer_version'] = vpc_dom['peerVersion']
                    result['peer_state'] = vpc_dom['peerSt']
                    result['vtep_ip'] = vpc_dom['virtualIp']
                    result['vtep_mac'] = vpc_dom['vpcMAC']
                    result['oper_role'] = vpc_dom['operRole']

        else:
            result['oper_state'] = 'inactive'
        self.vpc_info = result

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return (self.pod == other.pod) and \
               (self.node == other.node) and \
               (self.name == other.name) and \
               (self.role == other.role)

    def _populate_from_attributes(self, attributes):
        """Fills in an object with the desired attributes.
        """
        self.serial = attributes['serial']
        self.model = attributes['model']
        self.dn = attributes['dn']
        self.vendor = attributes['vendor']
        self.fabricSt = attributes['fabricSt']
        self.modify_time = attributes['modTs']

    def _get_topsystem_info(self, working_data):
        """ will read in topSystem object to get more information about Node"""

        node_data = working_data.get_object(self.dn+'/sys')
        if node_data is not None:
            if 'topSystem' in node_data:

                self.ipAddress = str(node_data['topSystem']['attributes']['address'])
                self.tep_ip = self.ipAddress
                self.macAddress = str(node_data['topSystem']['attributes']['fabricMAC'])
                self.state = str(node_data['topSystem']['attributes']['state'])
                self.mode = str(node_data['topSystem']['attributes']['mode'])
                self.oob_mgmt_ip = str(node_data['topSystem']['attributes'].get('oobMgmtAddr'))
                self.inb_mgmt_ip = str(node_data['topSystem']['attributes'].get('inbMgmtAddr'))
                self.system_uptime = str(node_data['topSystem']['attributes'].get('systemUpTime'))

                # now get eqptCh for even more info
                node_data = working_data.get_object(self.dn+'/sys/ch')
                if node_data:
                    if 'eqptCh' in node_data:
                        self.operSt = str(node_data['eqptCh']['attributes']['operSt'])
                        self.operStQual = str(node_data['eqptCh']['attributes']['operStQual'])
                        self.descr = str(node_data['eqptCh']['attributes']['descr'])

                # get the total number of ports = number of l1PhysIf
                node_data = working_data.get_subtree('l1PhysIf', self.dn+ '/sys')
                if node_data:
                    self.num_ports = len(node_data)

                # get the total number of ports = number of fan slots
                node_data = working_data.get_subtree('eqptFtSlot', self.dn+'/sys')
                if node_data:
                    self.num_fan_slots = len(node_data)

                self.num_fan_modules = 0
                if node_data:
                    for slot in node_data:
                        if slot['eqptFtSlot']['attributes']['operSt'] == 'inserted':
                            self.num_fan_modules += 1

                # get the total number of ports = number of linecard slots
                node_data = working_data.get_subtree('eqptLCSlot', self.dn + '/sys/ch')
                self.num_lc_slots = len(node_data)
                self.num_lc_modules = 0
                if node_data:
                    for slot in node_data:
                        if slot['eqptLCSlot']['attributes']['operSt'] == 'inserted':
                            self.num_lc_modules += 1

                # get the total number of ports = number of power supply slots
                node_data = working_data.get_subtree('eqptPsuSlot', self.dn + '/sys/ch')
                self.num_ps_slots = len(node_data)
                self.num_ps_modules = 0
                if node_data:
                    for slot in node_data:
                        if slot['eqptPsuSlot']['attributes']['operSt'] == 'inserted':
                            self.num_ps_modules += 1

                # get the total number of ports = number of supervisor slots
                node_data = working_data.get_subtree('eqptSupCSlot', self.dn + '/sys/ch')
                self.num_sup_slots = len(node_data)
                self.num_sup_modules = 0
                if node_data:
                    for slot in node_data:
                        if slot['eqptSupCSlot']['attributes']['operSt'] == 'inserted':
                            self.num_sup_modules += 1

                # get dynamic load balancing config
                self.dynamic_load_balancing_mode = 'unknown'

                lb_data = working_data.get_subtree('eqptSupCSlot', self.dn + '/sys')
                for lb_info in lb_data:
                    if 'topoctrlLbP' in lb_info:
                        self.dynamic_load_balancing_mode = lb_info['topoctrlLbP']['attributes']['dlbMode']

                # get vxlan info
                self.ivxlan_udp_port = 'unknown'

                #node_data = working_data.get_subtree('topoctrlVxlanP', self.dn + '/sys')
                #for info in node_data:
                #    if 'topoctrlVxlanP' in info:
                #        self.ivxlan_udp_port = info['topoctrlVxlanP']['attributes']['udpPort']

    def populate_children(self, deep=False, include_concrete=False):
        """Will populate all of the children modules such as
        linecards, fantrays and powersupplies, of the node.

        :param deep: boolean that when true will cause the entire
                     sub-tree to be populated. When false, only the
                     immediate children are populated
        :param include_concrete: boolean to indicate that concrete objects should also be populated

        :returns: List of children objects
        """

        session = self._session
        for child_class in self._get_children_classes():
            child_class.get(session, self)

        if include_concrete and self.role != 'controller':
            # todo: currently only have concrete model for switches - need to add controller
            query_url = '/api/mo/topology/pod-' +self.pod + '/node-' + self.node + \
                        '/sys.json?'

            working_data = WorkingData(session, Node, query_url, deep=True, include_concrete=True)
            for concrete_class in self._get_children_concrete_classes() :
                concrete_class.get(working_data, self)

        if deep:
            for child in self._children:
                child.populate_children(deep, include_concrete)

        return self._children

    def get_chassis_type(self):
        """Returns the chassis type of this node.  The chassis
        type is derived from the model number.
        This is a chassis type that is compatible with
        Cisco's Cable Plan XML.

        :returns: chassis type of node of type str
        """
        if self.model:
            fields = re.split('-', self.model)
            chassis_type = fields[0].lower()
        else:
            chassis_type = None

        return chassis_type

    @staticmethod
    def get_table(switches, title=''):
        """
            Creates report of basic switch information
            :param switches: Array of Node objects
            :param title: optional title for this table
            """
        headers = ['Name',
                   'Pod ID',
                   'Node ID',
                   'Serial Number',
                   'Model',
                   'Role',
                   'Fabric State',
                   'State',
                   'Firmware',
                   'Health',
                   'In-band managment IP',
                   'Out-of-band managment IP',
                   'Number of ports',
                   'Number of Linecards (inserted)',
                   'Number of Sups (inserted)',
                   'Number of Fans (inserted)',
                   'Number of Power Supplies (inserted)',
                   'System Uptime',
                   'Dynamic Load Balancing']
        table = []
        for switch in sorted(switches, key=lambda x: x.node):
            table.append([switch.name,
                          switch.pod,
                          switch.node,
                          switch.serial,
                          switch.model,
                          switch.role,
                          switch.fabricSt,
                          switch.state,
                          switch.firmware,
                          switch.health,
                          switch.inb_mgmt_ip,
                          switch.oob_mgmt_ip,
                          switch.num_ports,
                          str(switch.num_lc_slots) + '(' + str(switch.num_lc_modules) + ')',
                          str(switch.num_sup_slots) + '(' + str(switch.num_sup_modules) + ')',
                          str(switch.num_fan_slots) + '(' + str(switch.num_fan_modules) + ')',
                          str(switch.num_ps_slots) + '(' + str(switch.num_ps_modules) + ')',
                          switch.system_uptime,
                          switch.dynamic_load_balancing_mode])
        if len(table) > 7:
            table_orientation = 'horizontal'
        else:
            table_orientation = 'vertical'

        if len(table) > 3:
            columns = 1
        else:
            columns = 2
        result = [Table(table, headers,
                        title=str(title) + '' if (title != '') else '' + 'Basic Information',
                        table_orientation=table_orientation, columns=columns)]
        return result

    def _define_searchables(self):
        """
        Create all of the searchable terms

        :rtype : list of Searchable
        """
        result = []

        if self.name:
            result.append(Searchable('name', self.name))
            result.append(Searchable('switch', self.name))
            result.append(Searchable('node', self.name))
        if self.node:
            result.append(Searchable('switch', self.node))
            result.append(Searchable('node', self.node))
        if self.serial:
            result.append(Searchable('serial', self.serial))
        if self.model:
            result.append(Searchable('model', self.model))
        if self.firmware:
            result.append(Searchable('firmware', self.firmware))
        if self.role:
            result.append(Searchable('role', self.role))

        return result


class ExternalSwitch(BaseNXPhysObject):
    """External Node.  This class is for switch nodes that are
    connected to the pod, but are not
    NX nodes, i.e. are not under control of the Switch.
    Examples would be external layer 2 switches,
    external routers, or hypervisor based switches.

    This class will look as much as possible like the Node
    class recognizing that not as much information
    is available to the Switch about them as is available
    about NX nodes.  Nearly all of the information used
    to create this class comes from LLDP.
    """

    def __init__(self, parent=None):
        super(ExternalSwitch, self).__init__(name='', parent=parent)
        self.name = None

        self.check_parent(parent)
        self._parent = parent

        self._role = None
        self.dn = None
        self.name = None
        self.ip = None
        self.mac = None
        self.id = None
        self.pod = None
        self.status = None
        self.oper_issues = None
        self.fabric_st = 'external'
        self.role = 'external_switch'
        self.descr = None
        self.type = None
        self.state = None
        self.guid = None
        self.oid = None

    @classmethod
    def _get_parent_class(cls):
        """
        Gets the nxtoolkit class of the parent object
        Meant to be overridden by inheriting classes.
        Raises exception if not overridden.

        :returns: class of parent object
        """
        raise NotImplementedError

    @classmethod
    def _get_switch_classes(cls):
        """
        returns list of all switch classes used to build this toolkit class
        :return:
        """
        return ['fabricLooseNode', 'compHv', 'fabricLooseLink', 'pcAggrIf',
                'fabricProtLooseLink', 'pcRsMbrIfs', 'lldpAdjEp']

    def getRole(self):
        """ retrieves the node role
        :returns: role
        """
        return self.role

    @property
    def role(self):
        """
        Getter for role.
        :return: role
        """
        return self._role

    @role.setter
    def role(self, value):
        """
        Setter for role.  Will check that only valid roles are used
        :param value: role
        :return:None
        """
        valid_roles = [None, 'external_switch']
        if value not in valid_roles:
            raise ValueError("role must be one of " + str(valid_roles) + ' found ' + str(value))
        self._role = value

    @classmethod
    def _get_physical_switches(cls, session, parent):
        """Look for loose nodes and build an object for each one.
        """

        # if parent:
        # if not isinstance(parent, Topology):
        # raise TypeError('An instance of Topology class is required')
        lnode_query_url = ('/api/node/class/fabricLooseNode.json?'
                           'query-target=self')
        lnodes = []
        ret = session.get(lnode_query_url)
        lnode_data = ret.json()['imdata']

        for switch_node in lnode_data:
            if 'fabricLooseNode' in switch_node:
                external_switch = cls()
                external_switch._populate_physical_from_attributes(switch_node['fabricLooseNode']['attributes'])
                external_switch._get_system_info(session)

                if parent:
                    if isinstance(parent, cls._get_parent_class()):
                        external_switch._parent = parent
                        external_switch._parent.add_child(external_switch)

                lnodes.append(external_switch)

        return lnodes

    def _populate_physical_from_attributes(self, attr):
        self.dn = str(attr['dn'])
        self.name = str(attr['sysName'])
        self.id = str(attr['id'])
        self.status = str(attr['status'])
        self.oper_issues = str(attr['operIssues'])
        self.descr = str(attr['sysDesc'])

    @classmethod
    def _get_virtual_switches(cls, session, parent):
        """will find virtual switch nodes and return a list of such objects.
        """

        class_query_url = '/api/node/class/compHv.json?query-target=self'
        vnodes = []
        ret = session.get(class_query_url)
        vnode_data = ret.json()['imdata']

        for switch_node in vnode_data:

            if 'compHv' in switch_node:
                external_switch = cls()
                external_switch._populate_virtual_from_attributes(switch_node['compHv']['attributes'])
                external_switch._get_system_info(session)

                if parent:
                    if isinstance(parent, cls._get_parent_class()):
                        external_switch._parent = parent
                        external_switch._parent.add_child(external_switch)

                vnodes.append(external_switch)

        return vnodes

    def _populate_virtual_from_attributes(self, attr):

        self.dn = str(attr['dn'])
        self.name = str(attr['name'])
        self.descr = str(attr['descr'])
        self.type = str(attr['type'])
        self.state = str(attr['state'])
        self.guid = str(attr['guid'])
        self.oid = str(attr['oid'])

    @classmethod
    def get(cls, session, parent=None):
        """Gets all of the loose nodes from the Switch.

        :param session: Switch session
        :param parent: optional parent object of type Topology
        :returns: list of ENodes
        """
        cls.check_session(session)
        cls.check_parent(parent)

        enodes = cls._get_physical_switches(session, parent)
        enodes.extend(cls._get_virtual_switches(session, parent))
        return enodes

    @staticmethod
    def _get_dn(session, dn):
        """
        Will get the object that dn refers to.
        """
        mo_query_url = '/api/mo/' + dn + '.json?query-target=self'
        ret = session.get(mo_query_url)
        node_data = ret.json()['imdata']
        return node_data

    @staticmethod
    def _get_dn_children(session, dn):
        """
        Will get the children of the specified dn
        """

        mo_query_url = '/api/mo/' + dn + '.json?query-target=children'
        ret = session.get(mo_query_url)
        node_data = ret.json()['imdata']
        return node_data

    def _get_system_info(self, session):
        """This routine will fill in various other attributes of the loose node
        :param session:
        """
        mo_query_url = '/api/mo/' + self.dn + '.json?query-target=children'
        ret = session.get(mo_query_url)
        node_data = ret.json()['imdata']
        lldp_dn = None
        for node_info in node_data:
            if 'fabricLooseLink' in node_info:
                dn = node_info['fabricLooseLink']['attributes']['portDn']
                name = dn.split('/')
                pod = name[1].split('-')[1]
                node = str(name[2].split('-')[1])
                if 'phys' in name[4]:
                    result = re.search('phys-\[(.+)\]', dn)
                    lldp_dn = 'topology/pod-' + pod + '/node-' + \
                              node + '/sys/lldp/inst/if-[' + result.group(1) + ']/adj-1'
                else:
                    agg_port_data = ExternalSwitch._get_dn(session, dn)
                    if agg_port_data:
                        if 'pcAggrIf' in agg_port_data[0]:
                            port = agg_port_data[0]['pcAggrIf']['attributes']['lastBundleMbr']
                            lldp_dn = 'topology/pod-' + pod + '/node-' + \
                                      node + '/sys/lldp/inst/if-[' + port + ']/adj-1'

            if 'fabricProtLooseLink' in node_info:
                dn = node_info['fabricProtLooseLink']['attributes']['portDn']
                name = dn.split('/')
                pod = name[1].split('-')[1]
                node = str(name[2].split('-')[1])
                lldp_dn = 'topology/pod-' + pod + '/node-' + node + '/sys/lldp/inst/if-['
                if dn:
                    link = ExternalSwitch._get_dn_children(session, dn)
                    for child in link:
                        if 'pcRsMbrIfs' in child:
                            port = child['pcRsMbrIfs']['attributes']['tSKey']
                            lldp_dn = lldp_dn + port + ']/adj-1'

        if lldp_dn:
            lldp_data = ExternalSwitch._get_dn(session, lldp_dn)
        else:
            lldp_data = []

        if lldp_data:
            if 'lldpAdjEp' in lldp_data[0]:
                self.ip = str(lldp_data[0]['lldpAdjEp']['attributes']['mgmtIp'])
                self.name = str(lldp_data[0]['lldpAdjEp']['attributes']['sysName'])

                chassis_id_t = lldp_data[0]['lldpAdjEp']['attributes']['chassisIdT']
                if chassis_id_t == 'mac':
                    self.mac = str(lldp_data[0]['lldpAdjEp']['attributes']['chassisIdV'])
                else:
                    self.mac = str(lldp_data[0]['lldpAdjEp']['attributes']['mgmtPortMac'])

        self.state = 'unknown'

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.name == other.name


class Link(BaseNXPhysObject):
    """Link class, equivalent to the fabricLink object in Switch"""

    def __init__(self, parent=None):
        """
            :param parent: optional parent object

        """
        super(Link, self).__init__(parent=parent)
        self.node1 = None
        self.slot1 = None
        self.port1 = None
        self.node2 = None
        self.slot2 = None
        self.port2 = None
        self.linkstate = None
        self.linkstatus = None
        self.pod = None
        self.link = None
        self.descr = None
        if isinstance(parent, str):
            raise TypeError("Parent object can't be a string")
        self.type = 'link'
        self._session = None
        logging.debug('Creating %s %s', self.__class__.__name__,
                      'pod-%s link-%s' % (self.pod, self.link))
        # self._common_init(parent)

    @staticmethod
    def _get_parent_class():
        """
        Gets the nxtoolkit class of the parent object
        Meant to be overridden by inheriting classes.
        Raises exception if not overridden.

        :returns: class of parent object
        """
        raise NotImplementedError

    @classmethod
    def _get_switch_classes(cls):
        """
        Get the Switch classes used by this nxtoolkit class.

        :returns: list of strings containing Switch class names
        """
        resp = ['fabricLink']

        return resp

    @classmethod
    def get(cls, session, parent_pod=None, node_id=None):
        """
        Currently Notimplemented

        :param session: Switch session
        :returns: list of links
        """
        cls.check_session(session)
        links = []
        return links

    def _populate_from_attributes(self, attributes):
        """ populate various additional attributes """

        self.linkstate = attributes['linkState']
        self.linkstatus = attributes['status']
        self.dn = str(attributes['dn'])
        self.modify_time = str(attributes['modTs'])
        self.node1 = str(attributes['n1'])
        self.slot1 = str(attributes['s1'])
        self.port1 = str(attributes['p1'])
        self.node2 = str(attributes['n2'])
        self.slot2 = str(attributes['s2'])
        self.port2 = str(attributes['p2'])
        (pod, link) = Link._parse_dn(self.dn)
        self.pod = pod
        self.link = link

    def __str__(self):
        text = 'n%s/s%s/p%s-n%s/s%s/p%s' % (self.node1, self.slot1,
                                            self.port1, self.node2, self.slot2, self.port2)
        return text

    def __eq__(self, other):
        """ Two links are considered equal if their class type is the
        same and the end points match.  The link ids are not
        checked.
        """

        if type(self) is not type(other):
            return False
        return (self.pod == other.pod) and (self.node1 == other.node1) \
               and (self.slot1 == other.slot1) and (self.port1 == other.port1)

    def get_node1(self):
        """Returns the Node object that corresponds to the first
        node of the link.  The Node must be a child of
        the Pod that this link is a member of, i.e. it
        must already have been read from the Switch.  This can
        most easily be done by populating the entire
        physical heirarchy from the Pod down.

        :returns: Node object at first end of link
        """

        if not self._parent:
            raise TypeError("Parent pod must be specified in order to get node")

        nodes = self._parent.get_children(Node)
        for node in nodes:
            if node.node == self.node1:
                return node

    def get_node2(self):
        """Returns the Node object that corresponds to the
        second node of the link.  The Node must be a child of
        the Pod that this link is a member of, i.e. it must
        already have been read from the Switch.  This can
        most easily be done by populating the entire physical
        heirarchy from the Pod down.

        :returns: Node object at second end of link
        """

        if not self._parent:
            raise TypeError("Parent pod must be specified in order to get node")

        nodes = self._parent.get_children(Node)
        for node in nodes:
            if node.node == self.node2:
                return node
        return None

    def get_slot1(self):
        """Returns the Linecard object that corresponds to the
        first slot of the link.  The Linecard must be a child of
        the Node in the Pod that this link is a member of,
        i.e. it must already have been read from the Switch.  This can
        most easily be done by populating the entire physical
        heirarchy from the Pod down.

        :returns: Linecard object at first end of link
        """

        if not self._parent:
            raise TypeError("Parent pod must be specified in order to get node")
        node = self.get_node1()
        if node:
            linecards = node.get_children(Linecard)
            for linecard in linecards:
                if linecard.slot == self.slot1:
                    return linecard
        return None

    def get_slot2(self):
        """Returns the Linecard object that corresponds to the
         second slot of the link.  The Linecard must be a child of
        the Node in the Pod that this link is a member of,
        i.e. it must already have been read from the Switch.  This can
        most easily be done by populating the entire physical
        heirarchy from the Pod down.

        :returns: Linecard object at second end of link
        """

        if not self._parent:
            raise TypeError("Parent pod must be specified in order to get node")
        node = self.get_node2()
        if node:
            linecards = node.get_children(Linecard)
            for linecard in linecards:
                if linecard.slot == self.slot2:
                    return linecard
        return None

    def get_port1(self):
        """Returns the Linecard object that corresponds to the
        first port of the link.  The port must be a child of
        the Linecard in the Node in the Pod that this link is a
        member of, i.e. it must already have been read from the Switch.  This can
        most easily be done by populating the entire physical
        heirarchy from the Pod down.

        :returns: Interface object at first end of link
        """

        if not self._parent:
            raise TypeError("Parent pod must be specified in order to get node")
        linecard = self.get_slot1()
        if linecard:
            interfaces = linecard.get_children(Interface)
            for interface in interfaces:
                if interface.port == self.port1:
                    return interface
        return None

    def get_port2(self):
        """
        Returns the Linecard object that corresponds to the second port of
        the link. The port must be a child of the Linecard in the Node in
        the Pod that this link is a member of, i.e. it must already have been
        read from the Switch.  This can most easily be done by populating the
        entire physical heirarchy from the Pod down.

        :returns: Interface object at second end of link
        """
        if not self._parent:
            raise TypeError(("Parent pod must be specified in "
                             "order to get node"))
        linecard = self.get_slot2()
        if linecard:
            interfaces = linecard.get_children(Interface)
            for interface in interfaces:
                if interface.port == self.port2:
                    return interface
        return None

    def get_port_id1(self):
        """
        Returns the port ID of the first end of the link in the
        format pod/node/slot/port

        :returns: port ID string
        """
        return '{0}/{1}/{2}/{3}'.format(self.pod, self.node1, self.slot1, self.port1)

    def get_port_id2(self):
        """
        Returns the port ID of the second end of the link in the
        format pod/node/slot/port

        :returns: port ID string
        """
        return '{0}/{1}/{2}/{3}'.format(self.pod, self.node2, self.slot2, self.port2)

    @staticmethod
    def _parse_dn(dn):
        """Parses the pod and link number from a
           distinguished name of the link.

           :param dn: dn string of the link
           :returns: (pod, link)
        """
        name = dn.split('/')
        pod = str(name[1].split('-')[1])
        link = str(name[2].split('-')[1])

        return pod, link


class Interface(BaseInterface):
    """This class defines a physical interface.
    """

    def __init__(self, if_name, parent=None, session=None, attributes=None):

        self._session = session
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = copy.deepcopy(attributes)
            
        if 'eth' in if_name:
            self.interface_type = 'eth'
            self.attributes['interface_type'] = self.interface_type
            self.id = if_name
            self.if_type = if_name[:3]
            (self.module, self.port)= if_name.replace('eth', '').split('/')
            self.if_name = if_name
            self.attributes['module'] = self.module
            self.attributes['port'] = self.port
            self.attributes['if_name'] = self.if_name
        else:
            raise TypeError ('ethernet interface expected')

        super(Interface, self).__init__(if_name, None)
        self.porttype = ''
        self._cdp_config = None
        self._lldp_config = None
        self.type = 'interface'
        self.attributes['type'] = 'interface'
        
        self._layer = None  # Layer2 or Layer3
        self._mode = 'access' # access, trunk, fex-fabric
        self._snmp_trap_st = 'default' # enable/disable/default
        self._adminstatus = None  # up or down
        self._speed = '10G'  # 100M, 1G, 10G or 40G
        self._mtu = '1500'
        self._link_log = 'default' # enable/disable/default
        self._trunk_log = 'default' #enable/disable/default
        self._duplex = 'auto' # auto/half/full
        self._access_vlan = None
        self._trunk_vlans = None
        self._native_vlan = None
        self._descr = ''
        
        self.object = 'l1PhysIf'

        self._parent = parent
        if parent:
            self._parent.add_child(self)

        self.stats = InterfaceStats(self, self.attributes.get('dist_name'))
        
    def set_descr(self, desc):
        self._descr = desc
    
    def get_descr(self):
        return self._descr
       
    def set_mode(self, mode):
        self._mode = mode
    
    def get_mode(self):
        return self._mode
    
    def set_layer(self, layer):
        if layer not in ['Layer2', 'Layer3']:
            raise TypeError ('Not a valid layer')
        self._layer = layer
        
    def get_layer(self):
        return self._layer
    
    def set_snmp_status(self, status):
        self._snmp_trap_st = status
    
    def get_snmp_status(self):
        return self._snmp_trap_st
    
    def set_admin_status(self, status):
        self._adminstatus = status
    
    def get_admin_status(self):
        return self._adminstatus

    def set_speed(self, speed=None):
        self._speed = speed
    
    def get_speed(self):
        return self._speed
    
    def set_mtu(self, mtu=None):
        self._mtu = mtu
        
    def get_mtu(self):
        return self._mtu
    
    def set_link_log(self, linklog=None):
        self._link_log = linklog
    
    def get_link_log(self):
        return self._link_log
    
    def set_trunk_log(self, trunklog=None):
        self._trunk_log = trunklog
    
    def get_trunk_log(self):
        return self._trunk_log
    
    def set_duplex(self, duplex=None):
        self._duplex = duplex
    
    def get_duplex(self):
        return self._duplex
    
    def set_access_vlan(self, access=None):
        """Set access and trunk vlans for the interface"""
        self._access_vlan = access
    
    def get_access_vlan(self):
        return self._access_vlan
    
    def set_native_vlan(self, trunk):
        """ Set native vlan"""
        # TODO this feature is not Implemented,
        # currently it is not supported
        raise NotImplementedError
    
    def get_native_vlan(self):
        return self._native_vlan

    def is_interface(self):
        """
        Returns whether this instance is considered an interface.

        :returns: True
        """
        return True

    def is_cdp_enabled(self):
        """
        Returns whether this interface has CDP configured as enabled.

        :returns: True or False
        """
        return self._cdp_config == 'enabled'

    def is_cdp_disabled(self):
        """
        Returns whether this interface has CDP configured as disabled.

        :returns: True or False
        """
        return self._cdp_config == 'disabled'

    def enable_cdp(self):
        """
        Enables CDP on this interface.
        """
        self._cdp_config = 'enabled'

    def disable_cdp(self):
        """
        Disables CDP on this interface.
        """
        self._cdp_config = 'disabled'

    def is_lldp_enabled(self):
        """
        Returns whether this interface has LLDP configured as enabled.

        :returns: True or False
        """
        return self._lldp_config == 'enabled'

    def is_lldp_disabled(self):
        """
        Returns whether this interface has LLDP configured as disabled.

        :returns: True or False
        """
        return self._lldp_config == 'disabled'

    def enable_lldp(self):
        """
        Enables LLDP on this interface.
        """
        self._lldp_config = 'enabled'

    def disable_lldp(self):
        """
        Disables LLDP on this interface.
        """
        self._lldp_config = 'disabled'

    def get_type(self):
        """
        getter method for object.type

        :return: the type
        """
        return self.type

    @staticmethod
    def get_serial():
        """
        getter for the serial number

        :return: None
        """
        return None
     
    def _get_attributes(self):
        """
        :return All the attributes of the switch to be configured
        """
        att = {}
        if self._access_vlan:
            att['accessVlan'] = self._access_vlan
        if self._trunk_vlans:
            att['trunkVlans'] = self._trunk_vlans
        if self._mtu:
            att['mtu'] = self._mtu
        if self._adminstatus:
            att['adminSt'] = self._adminstatus
        if self._speed:
            att['speed'] = self._speed
        if self._layer:        
            att['layer'] = self._layer
        if self._snmp_trap_st:
            att['snmpTrapSt'] = self._snmp_trap_st
        if self._descr:
            att['descr'] = self._descr
        if self._duplex:
            att['duplex'] = self._duplex
        if self._mode:
            att['mode'] = self._mode
        if self._link_log:
            att['linkLog'] = self._link_log
        if self._trunk_log:
            att['trunkLog'] = self._trunk_log

        att['id'] = self.id

        return att

    def get_url(self, fmt='json'):
        """
        Gets URLs for physical domain, fabric, and infra.

        :return: string: URL to configure interface
        """
        return '/api/mo/' + self._get_path() + '.' + fmt

    def _get_name_for_json(self):
        return '%s-%s-%s-%s' % (self.pod, self.node,
                                self.module, self.port)

    def get_json(self):
        """ Get the json for an interface
        """
        resp =  super(Interface, self).get_json(self.object,
                                        attributes=self._get_attributes())
        if self._native_vlan:
            # TODO need to find parameter for native vlan
            pass
        return resp
        
    def _get_path(self):
        """Get the path of this interface used when communicating with
           the Switch object model.
        """
        return 'sys/intf/phys-[eth%s/%s]' % (self.module, self.port)

    @staticmethod
    def parse_name(name):
        """Parses a name that is of the form:
        <type> <pod>/<mod>/<port>
        :param name: Distinguished Name (dn)
        """
        interface_type = name.split()[0]
        name = name.split()[1]
        (module, port) = name.split('/')
        return interface_type, module, port

    @staticmethod
    def _parse_physical_dn(dn):
        """
        Handles DNs that look like the following:
        sys/phys-[eth1/1]
        sys/intf/phys-[eth1/1] (For Image .551) 
        """
        name = dn.split('/')
        module = name[2].split('[')[1]
        interface_type = module[:3]
        module = module[3:]
        port = name[3].split(']')[0]

        return interface_type, module, port

    @staticmethod
    def _parse_path_dn(dn):
        """
        Handles DNs that look like the following:
        sys/phys-[eth1/1]
        """
        name = dn.split('/')
        module = name[1].split('[')[1]
        interface_type = module[:3]
        module = module[3:]
        port = name[2].split(']')[0]

        return interface_type, module, port

    @classmethod
    def parse_dn(cls, dn):
        """
        Parses the pod, node, module, port from a distinguished name
        of the interface.

        :param dn: String containing the interface distinguished name
        :returns: interface_type, pod, node, module, port
        """
        if 'sys' in dn.split('/'):
            return cls._parse_physical_dn(dn)
        else:
            return cls._parse_path_dn(dn)

    @staticmethod
    def _get_discoveryprot_policies(session, prot):
        """
        :param prot: String containing either 'cdp' or 'lldp'
        """
        prot_policies = {}
        if prot == 'cdp':
            prot_class = 'cdpIfPol'
        elif prot == 'lldp':
            prot_class = 'lldpIfPol'
        else:
            raise ValueError

        query_url = '/api/node/class/%s.json?query-target=self' % prot_class
        ret = session.get(query_url)
        prot_data = ret.json()['imdata']
        for policy in prot_data:
            if ('%s' % prot_class) in policy:
                attributes = policy['%s' % prot_class]['attributes']
                if prot == 'cdp':
                    prot_policies[attributes['name']] = attributes['adminSt']
                else:
                    prot_policies[attributes['name']] = attributes['adminTxSt']
        return prot_policies

    @staticmethod
    def _get_discoveryprot_relations(session, interfaces, prot, prot_policies):
        if prot == 'cdp':
            prot_relation_class = 'l1RsCdpIfPolCons'
            prot_relation_dn_class = '/cdpIfP-'
            prot_relation_dn = '/rscdpIfPolCons'
        elif prot == 'lldp':
            prot_relation_class = 'l1RsLldpIfPolCons'
            prot_relation_dn_class = '/lldpIfP-'
            prot_relation_dn = '/rslldpIfPolCons'
        else:
            raise ValueError

        query_url = ('/api/node/class/l1PhysIf.json?query-target=subtree&'
                     'target-subtree-class=%s' % prot_relation_class)
        ret = session.get(query_url)
        prot_data = ret.json()['imdata']
        for prot_relation in prot_data:
            if prot_relation_class in prot_relation:
                attributes = prot_relation[prot_relation_class]['attributes']
                policy_name = attributes['tDn'].split(prot_relation_dn_class)[1]
                intf_dn = attributes['dn'].split(prot_relation_dn)[0]
                #TODO search_intf = Interface(*Interface._parse_physical_dn(intf_dn))
                (if_type, module, port) = Interface._parse_physical_dn(intf_dn)
                if_name = if_type + module + '/' + port
                search_intf = Interface(if_name)
                for intf in interfaces:
                    if intf == search_intf:
                        if prot_policies[policy_name] == 'enabled':
                            if prot == 'cdp':
                                intf.enable_cdp()
                            else:
                                intf.enable_lldp()
                        else:
                            if prot == 'cdp':
                                intf.disable_cdp()
                            else:
                                intf.disable_lldp()
                        break
        return interfaces

    @classmethod
    def _get_parent_class(cls):
        """
        Gets the nxtoolkit class of the parent object
        Meant to be overridden by inheriting classes.
        Raises exception if not overridden.

        :returns: class of parent object
        """
        return Linecard

    @classmethod
    def _get_switch_classes(cls):
        """
        Get the Switch classes used by this nxtoolkit class.

        :returns: list of strings containing Switch class names
        """
        resp = ['l1PhysIf', 'ethpmPhysIf', 'l1RsCdpIfPolCons', 'l1RsLldpIfPolCons',
                'cdpIfPol', 'lldpIfPol']

        return resp

    @classmethod
    def get(cls, session, if_name=None):
        """
        Gets all of the physical interfaces from the Switch if no parent is
        specified. If a parent of type Linecard is specified, then only
        those interfaces on that linecard are returned and they are also
        added as children to that linecard.

        If the pod, node, module and port are specified, then only that
        specific interface is read.

        :param session: the instance of Session used for Switch communication
        :param pod_parent: Linecard instance to limit interfaces or pod\
                           number (optional)
        :param node: Node id string.  This specifies the switch to read.\
                     (optional)
        :param module: Module id string.  This specifies the module or\
                       slot of the port. (optional)
        :param port: Port number.  This is the port to read. (optional)

        :returns: list of Interface instances
        """
        if not isinstance(session, Session):
            raise TypeError('An instance of Session class is required')
        

        #if port:
        if if_name:
            #if not isinstance(port, str):
            if not isinstance(if_name, str):
                raise TypeError('When specifying a specific port, the port'
                                ' must be a identified by a string')

        cdp_policies = Interface._get_discoveryprot_policies(session, 'cdp')
        lldp_policies = Interface._get_discoveryprot_policies(session, 'lldp')

        if if_name:
            dist_name = 'sys/intf/phys-[{0}]'.format(if_name)
            # Below dist_name should be used if image version is below .541
            # dist_name = 'sys/phys-[{0}]'.format(if_name)
            interface_query_url = ('/api/mo/' + dist_name + '.json?query-target=self')
            eth_query_url = ('/api/mo/' + dist_name + '/phys.json?query-target=self')
        else:
            interface_query_url = '/api/node/class/l1PhysIf.json?query-target=self'
            eth_query_url = '/api/node/class/ethpmPhysIf.json?query-target=self'

        ret = session.get(interface_query_url)
        interface_data = ret.json()['imdata']

        # also get information about the ethernet interface
        eth_resp = session.get(eth_query_url)
        resp = []
        eth_data = eth_resp.json()['imdata']

        # re-index the ethernet port info so it can be referenced by dn
        eth_data_dict = {}
        for obj in eth_data:
            eth_data_dict[obj['ethpmPhysIf']['attributes']['dn']] = obj['ethpmPhysIf']['attributes']

        for interface in interface_data:
            if 'l1PhysIf' in interface:
                attributes = {}
                dist_name = str(interface['l1PhysIf']['attributes']['dn'])
                attributes['dist_name'] = dist_name
                porttype = str(interface['l1PhysIf']['attributes']['portT'])
                attributes['porttype'] = porttype
                adminstatus = str(interface['l1PhysIf']['attributes']['adminSt'])
                attributes['adminstatus'] = adminstatus
                speed = str(interface['l1PhysIf']['attributes']['speed'])
                attributes['speed'] = speed
                mtu = str(interface['l1PhysIf']['attributes']['mtu'])
                attributes['mtu'] = mtu
                identifier = str(interface['l1PhysIf']['attributes']['id'])
                attributes['id'] = identifier
                attributes['monPolDn'] = str(interface['l1PhysIf']['attributes']['monPolDn'])
                attributes['name'] = str(interface['l1PhysIf']['attributes']['name'])
                attributes['descr'] = str(interface['l1PhysIf']['attributes']['descr'])
                attributes['usage'] = str(interface['l1PhysIf']['attributes']['usage'])
                attributes['layer'] = str(interface['l1PhysIf']['attributes']['layer'])
                (interface_type, module, port) = Interface.parse_dn(dist_name)
                attributes['interface_type'] = interface_type
                attributes['module'] = module
                attributes['port'] = port
                phys_dist_name = dist_name + '/phys'
                if phys_dist_name in eth_data_dict.keys():
                    attributes['operSt'] = eth_data_dict[dist_name + '/phys']['operSt']
                else:
                    attributes['operSt'] = ''
                
                interface_obj = Interface(identifier, parent=None, session=session,
                                          attributes=attributes)
                
                
                interface_obj.porttype = porttype
                interface_obj.adminstatus = adminstatus
                interface_obj.speed = speed
                interface_obj.mtu = mtu
                if attributes['operSt']:
                    interface_obj.operSt = attributes['operSt']
                else:
                    interface_obj.operSt = '-'

                resp.append(interface_obj)

        resp = Interface._get_discoveryprot_relations(session, resp, 'cdp', cdp_policies)
        resp = Interface._get_discoveryprot_relations(session, resp, 'lldp', lldp_policies)
        return resp

    def __str__(self):
        items = [self.if_name, '\t', self.porttype, '\t',
                 self.adminstatus, '\t', self.speed, '\t',
                 self.mtu]
        ret = ''.join(items)
        return ret

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if (self.attributes['interface_type'] == other.attributes.get('interface_type') and
                    self.attributes['module'] == other.attributes.get('module') and
                    self.attributes['port'] == other.attributes.get('port')):
            return True
        return False


class WorkingData(object):
    """
    This class will hold the entire json tree
    from topSystem down, for a switch.
    The attributes of a specific class can be retrieved
    in which case it will be as a list of objects.
    It will allow all children of an object to be retrieved
    result is list of objects
    It will allow an instance of a class to be retrieved returned
    as a single object.
    """

    def __init__(self, session = None, toolkit_class=None, url=None, deep=False, include_concrete=False):

        self.by_class = {}
        self.by_dn = {}
        self.vnid_dict = {}
        self.ctx_dict = {}
        self.bd_dict = {}
        self.rawjson = {}
        self.session = session
        self.add(session, toolkit_class, url, deep, include_concrete)

    def add(self, session = None, toolkit_class=None, url=None, deep=False, include_concrete=False):

        """

        :param session:
        :param toolkit_class:
        :param url:
        :param deep:
        :param include_concrete:
        :return:
        """
        self.session = session
        if session is None:
            return

        if deep:
            switch_classes = toolkit_class.get_deep_switch_classes(include_concrete=include_concrete)
        else:
            switch_classes = toolkit_class._get_switch_classes()
        query_url = url + 'query-target=subtree&target-subtree-class='+','.join(switch_classes)

        ret = session.get(query_url)
        ret._content = ret._content.replace('\n', '')
        data = ret.json()['imdata']

        if data:
            self.rawjson = ret.json()['imdata']
        else:
            self.rawjson = None

        if 'error' not in self.rawjson:
            self._index_objects()

            self.build_vnid_dictionary()

    def _index_objects(self):
        """
        Will index the json by dn and by class for easy reference
        """
        for item in self.rawjson:
            for switch_class in item:
                if switch_class != u'error':
                    self.by_dn[item[switch_class]['attributes']['dn']] = item
                    if switch_class not in self.by_class:
                        self.by_class[switch_class] = []

                    # fix apparent bug in Switch where multiple nodes are returned for the Switch node
                    if switch_class == 'fabricNode':
                        if item[switch_class]['attributes']['role'] in ['leaf', 'spine']:
                            self.by_class[switch_class].append(item)
                        else:
                            if (item[switch_class]['attributes']['role'] == 'controller') \
                                    and (item not in self.by_class[switch_class]):

                                # look through all the objects in 'fabricNode' class and only insert if
                                # this controller not already there.
                                found = False
                                for item_in_class in self.by_class[switch_class] :
                                    if item[switch_class]['attributes']['dn'] == item_in_class[switch_class]['attributes']['dn']:
                                        found = True
                                        break
                                if not found:
                                    self.by_class[switch_class].append(item)

                    else:
                        self.by_class[switch_class].append(item)


    def get_class(self, class_name):
        """
        returns all the objects of a given class
        :param class_name: The name of the class you are looking for.
        """
        result = self.by_class.get(class_name)
        if not result:
            return []
        return result

    def get_subtree(self, class_name, dname):
        """
        will return list of matching classes and their attributes

        It will get all classes that
        are classes under dn.
        :param class_name: name of class you are looking for
        :param dname: Distinguished Name (dn)
        """
        result = []

        classes = self.get_class(class_name)
        if classes:
            for class_record in classes:
                for class_id in class_record:
                    obj_dn = class_record[class_id]['attributes']['dn']
                    if obj_dn[0:len(dname)] == dname:
                        result.append(class_record)
        return result

    def get_object(self, dname):
        """
        Will return the object specified by dn.
        :param dname: Distinguished Name (dn)
        """
        # start at top
        result = self.by_dn.get(dname)
        if not result:
            return None
        return result

    def build_vnid_dictionary(self):
        """
        Will build a dictionary that is indexed by
        vnid and will return context or bridge_domain
        and the name of that segment.
        :param self:
        """

        # pull in contexts first
        ctx_data = self.get_class('l3Inst')[:]
        ctx_data.extend(self.get_class('l3Ctx')[:])
        for ctx in ctx_data:
            if 'l3Ctx' in ctx:
                class_id = 'l3Ctx'
            else:
                class_id = 'l3Inst'

            if '-' in ctx[class_id]['attributes']['encap']:
                vnid = str(ctx[class_id]['attributes']['encap'].split('-')[1])
            else:
                vnid = str(ctx[class_id]['attributes']['encap'])
            name = str(ctx[class_id]['attributes']['name'])
            record = {'name': name, 'type': 'context'}
            self.vnid_dict[vnid] = record

            # and opposite dictionary
            self.ctx_dict[name] = vnid
        # pull in bridge domains next
        bd_data = self.get_class('l2BD')
        for l2bd in bd_data:
            vnid = str(l2bd['l2BD']['attributes']['fabEncap'].split('-')[1])
            name = str(l2bd['l2BD']['attributes']['name'].split(':')[-1])
            if not name:
                name = vnid
            dname = str(l2bd['l2BD']['attributes']['dn'])
            fields = dname.split('/')
            context_dn = '/'.join(fields[0:-1])
            ctx_data = self.get_object(context_dn)
            if 'l3Ctx' in ctx_data:
                context = str(ctx_data['l3Ctx']['attributes']['name'])
            elif 'l3Inst' in ctx_data:
                context = str(ctx_data['l3Inst']['attributes']['name'])
            else:
                context = None

            record = {'name': name, 'type': 'bd', 'context': context}
            self.vnid_dict[vnid] = record

            # and opposite dictionary
            self.bd_dict[name] = vnid


class Process(BaseNXPhysObject):
    """
    Class to hold information about a process running on a Switch
    """

    def __init__(self):
        """

        :return:
        """
        super(Process, self).__init__(name='', parent=None)
        self.id = None
        self.name = None
        self.oper_st = None
        self.cpu_execution_time_ave = None
        self.cpu_invoked = None
        self.cpu_execution_time_max = None
        self.cpu_usage_last = None
        self.cpu_usage_avg = None
        self.mem_alloc_avg = None
        self.mem_alloc_last = None
        self.mem_alloc_max = None
        self.mem_used_avg = None
        self.mem_used_last = None
        self.mem_used_max = None

    @classmethod
    def get(cls, session, node):
        """

        :param session:
        :param parent:
        :return:
        """
        cls.check_session(session)

        result = []

        node_query_url = ('/api/mo/sys/procsys.json?query-target=children&'
                          'rsp-subtree-include=stats&rsp-subtree-class='
                          'statsCurr')

        ret = session.get(node_query_url)
        processes = ret.json()['imdata']
        for child in processes:
            if child['procProc']:
                process = Process()
                process._populate_from_attributes(child['procProc']['attributes'])
                process._populate_stats(child['procProc']['children'])
                result.append(process)
        return result

    def _populate_from_attributes(self, attr):
        """

        :param attr:
        :return:
        """
        self.id = attr['id']
        self.name = attr['name']
        self.oper_st = attr['operSt']
        self.dn = attr['dn']

    def _populate_stats(self, children):
        """
        Will read the most current stats and populate parameters accordingly
        :param children:
        :return:
        """
        for child in children:

            if 'procProcCPU5min' in child:
                attr = child['procProcCPU5min']['attributes']
                self.cpu_avg_execution_time_avg = attr['avgExecAvg']
                self.cpu_avg_execution_time_max = attr['avgExecMax']
                self.cpu_avg_execution_time_last = attr['avgExecLast']
                self.cpu_max_execution_time_avg = attr['maxExecAvg']
                self.cpu_max_execution_time_max = attr['maxExecMax']
                self.cpu_max_execution_time_last = attr['maxExecLast']
                self.cpu_invoked_avg = attr['invokedAvg']
                self.cpu_invoked_max = attr['invokedMax']
                self.cpu_invoked_last = attr['invokedLast']
                self.cpu_usage_avg = attr['usageAvg']
                self.cpu_usage_max = attr['usageMax']
                self.cpu_usage_last = attr['usageLast']

            if 'procProcMem5min' in child:
                attr = child['procProcMem5min']['attributes']
                self.mem_alloc_avg = attr['allocedAvg']
                self.mem_alloc_max = attr['allocedMax']
                self.mem_alloc_last = attr['allocedLast']
                self.mem_used_avg = attr['usedAvg']
                self.mem_used_max = attr['usedMax']
                self.mem_used_last = attr['usedLast']

    @staticmethod
    def get_table(nx_objects, title='Process'):
        """

        :param nx_objects: list of process objects to build table for
        :param title: Title of the table
        :return: Table
        """
        result = []

        headers = ['Name', 'id', 'Oper State', 'Avg CPU Exec Avg', 'Avg CPU Exec Last',
                   'CPU Usage Avg', 'CPU Usage Last', 'Mem Alloc Avg', 'Mem Alloc Last',
                   'Mem Used Avg', 'Mem Used Last']

        table = []
        for nx_object in nx_objects:
            table.append([
                nx_object.name,
                nx_object.id,
                nx_object.oper_st,
                nx_object.cpu_avg_execution_time_avg,
                nx_object.cpu_avg_execution_time_last,
                nx_object.cpu_usage_avg,
                nx_object.cpu_usage_last,
                nx_object.mem_alloc_avg,
                nx_object.mem_alloc_last,
                nx_object.mem_used_avg,
                nx_object.mem_used_last
            ])

        table = sorted(table, key=lambda x: (x[0], x[1]))
        result.append(Table(table, headers, title=title + 'Process CPU and MEM'))

        return result


class PhysicalModel(BaseNXObject):
    """
    This is the root class for the physical part of the network.  It's corrolary is the LogicalModel class.
    It is a container that can hold all of physical model instances.  Initially this is only an instance of Pod.

    From this class, you can populate all of the children classes.
    """

    def __init__(self, session=None, parent=None):
        """
        Initialization method that sets up the Fabric.
        :return:
        """
        if session:
            assert isinstance(session, Session)

        if parent:
            assert isinstance(parent, System)

        super(PhysicalModel, self).__init__(name='', parent=parent)

        self.session = session

    @staticmethod
    def _get_children_classes():
        """
        Get the nxtoolkit class of the children of this object.
        This is meant to be overridden by any inheriting classes that have children.
        If they don't have children, this will return an empty list.
        :return: list of classes
        """
        return [Node]

    @classmethod
    def get(cls, session=None, parent=None):
        """
        Method to get all of the PhysicalModels.  It will get one and return it in a list.
        :param session:
        :param parent:
        :return: list of PhysicalModel
        """
        physical_model = PhysicalModel(session=session, parent=parent)
        return [physical_model]


class System(BaseNXObject):
    """
    This is the root class for the nxtoolkit.  It is a container that
    can hold all of the other instances of the nxtoolkit classes.

    From this class, you can populate all of the children classes.
    """

    def __init__(self, session=None, name=None):
        """
        Initialization method that sets up the Fabric.
        :return:
        """
        if session:
            assert isinstance(session, Session)
        if not name:
            name = ''
        super(System, self).__init__(name=name, parent=None)

        self._session = session
   
    def get_url(self, fmt='json'):
        return '/api/mo/sys.' + fmt
    
    @staticmethod
    def _get_children_classes():
        """
        Get the nxtoolkit class of the children of this object.
        This is meant to be overridden by any inheriting classes that have children.
        If they don't have children, this will return an empty list.
        :return: list of classes
        """
        return [PhysicalModel, NX.LogicalModel]

    @classmethod
    def get(cls, session=None):
        """ Get System info
        
        :param Session object co communicate with switch
        :reutrn System object
        """
        if not isinstance(session, Session):
            raise TypeError('An instance of Session class is required')
        
        query_url = '/api/mo/sys.json'
        resp = session.get(query_url).json()['imdata']
        for system in resp:
            dev_name = str(system['topSystem']['attributes']['name'])
            print dev_name
            return System(session=session, name=dev_name)


class Ethpm(BaseNXObject):
    """
    This class defines ethpm
    """
    
    def __init__(self, name=None, session=None, ):
        
        if not name:
            name = ''
        super(Ethpm, self).__init__(name=name)
        
        self._session = session
        self.unsuported_sft = None
        self.default_admin_st = None
        self.default_layer = None
        self.jumbo_mtu = None
        self.object = 'ethpmInst'
    
    def set_unsupported_transceiver(self, supp_sft=None):
        self.unsuported_sft = supp_sft
    
    def get_unsupported_transceiver(self):
        return self.unsuported_sft
    
    def set_default_admin_st(self, admin_st=None):
        self.default_admin_st = admin_st
    
    def get_default_admin_st(self):
        return self.default_admin_st
    
    def set_default_layer(self, layer=None):
        self.default_layer = layer
    
    def get_default_layer(self):
        return self.default_layer
    
    def set_jumbomtu(self, mtu=None):
        self.jumbo_mtu = mtu
    
    def get_jumbomtu(self):
        return self.jumbo_mtu
    
    def _get_attributes(self):
        att = {}
        if self.unsuported_sft:
            att['allowUnsupportedSfp'] = self.unsuported_sft
        if self.default_admin_st:
            att['systemDefaultAdminSt'] = self.default_admin_st
        if self.default_layer:
            att['systemDefaultLayer'] = self.default_layer
        if self.jumbo_mtu:
            att['systemJumboMtu'] = self.jumbo_mtu
        return att

    def get_json(self):
        att = self._get_attributes()
        return super(Ethpm, self).get_json(self.object, attributes=att)
    
    def get_url(self, fmt='json'):
        return '/api/mo/sys/ethpm/inst.' + fmt
    
    @classmethod
    def get(self, session=None):
        """
        Get ethpm details
        :param session: A Session instance to communicate with Switch
        """
        if not isinstance(session, Session):
            raise TypeError('An instance of Session class is required')
        
        query_url = '/api/mo/sys/ethpm/inst.json'
        
        ethpms = session.get(query_url).json()['imdata']
        for ethpm in ethpms:
            
            ethpm_obj = Ethpm(session=session)
            
            adminst = str(ethpm['ethpmInst']['attributes']['systemDefaultAdminSt'])
            layer = str(ethpm['ethpmInst']['attributes']['systemDefaultLayer'])
            mtu = str(ethpm['ethpmInst']['attributes']['systemJumboMtu'])
            sfp = str(ethpm['ethpmInst']['attributes']['allowUnsupportedSfp'])
            
            ethpm_obj.set_default_admin_st(admin_st=adminst)
            ethpm_obj.set_default_layer(layer=layer)
            ethpm_obj.set_jumbomtu(mtu=mtu)
            ethpm_obj.set_unsupported_transceiver(supp_sft=sfp)
            
            return ethpm_obj