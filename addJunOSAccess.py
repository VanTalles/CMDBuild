from django.utils.text import slugify
from django.contrib.contenttypes.models import ContentType
from tenancy.models import Tenant
from dcim.choices import DeviceStatusChoices, SiteStatusChoices
from dcim.models import Device, DeviceRole, DeviceType, Manufacturer, Site, Rack, Interface
from ipam.models import Aggregate, IPAddress, Prefix, RIR, Role, Service, VLAN, VLANGroup, VRF
from extras.scripts import *
from extras.models import CustomField
from utilities.forms import (
    APISelect, APISelectMultiple, add_blank_choice, BootstrapMixin, BulkEditForm, BulkEditNullBooleanSelect,
    ColorSelect, CommentField, CSVChoiceField, CSVModelChoiceField, CSVModelForm,
    DynamicModelChoiceField, DynamicModelMultipleChoiceField, ExpandableNameField, form_from_model, JSONField,
    NumericArrayField, SelectWithPK, SmallTextarea, SlugField, StaticSelect2, StaticSelect2Multiple, TagFilterField,
    BOOLEAN_WITH_BLANK_CHOICES,
)
from CMDBuild import CMDBuildNLMK as cmdb

class createSGJuniperSwitch(Script):
    class Meta:
        name = 'Create Juniper switch for SG sites'
        description = 'Create Juniper switch for SG sites'
        field_order = ['site','rack','sw_name','sw_int_name','sw_int_ip']

    SERVICESLIST = (
        ('s2','SSHv2'),
        ('s1','SSHv1'),
        ('t','Telnet'),
        ('y','YANG'),
        ('r','REST'),
    )

    location = StringVar(
        description = 'Location place',
        label = 'Location',
        required = False
    )

    inventory = StringVar(
        description = 'Inventory number',
        label = 'Inventory number',
        required = False
    )

    sticker = StringVar(
        description = 'Stick number',
        label = 'Stick number',
        required = False
    )


    dev_name = StringVar(
        description = 'Switch name',
        label = 'Device name'
    )

    dev_serial = StringVar(
        description = 'Serial number',
        label = 'Serial number'
    )

    dev_model = ObjectVar(
        model = DeviceType,
        label = 'Device model',
        description = 'Device model',
        display_field = 'model',
        query_params = {
            'manufacturer_id' : '21'
        }
    )

    site = ObjectVar(
        model = Site,
        description = 'Site',
        display_field = 'name',
        query_params = {
            'tenant' : 'sg'
        }
    )


    mgmt_int_name = StringVar(
        description = 'MGMT vlan name',
        label = 'MGMT virtual interface name'

    )

    mgmt_int_ip = StringVar(
        description = 'with CIDR, example 10.1.1.1/24',
        label = 'MGMT ip address'


    )

    monitoring = BooleanVar(
        description = 'Set to monitoring',
        default = 'True'
    )

    backup = BooleanVar(
        description = 'Set to backup',
        default = 'True'

    )

    services = MultiChoiceVar(label = 'Services', description = 'multiselect allow', choices=SERVICESLIST)


    def run(self,data,commit):

        services_list = [
            {'id_s':'s2','port':22,'name':'SSHv2','protocol':'tcp'},
            {'id_s':'s1','port':22,'name':'SSHv1','protocol':'tcp'},
            {'id_s':'t','port':23,'name':'Telnet','protocol':'tcp'},
            {'id_s':'y','port':443,'name':'YANG','protocol':'tcp'},
            {'id_s':'r','port':443,'name':'REST','protocol':'tcp'},
        ]


        dev_role = DeviceRole.objects.get(slug = 'access-switch')
        device_new = Device(
            name = data['dev_name'],
            device_type = data['dev_model'],
            site = data['site'],
            device_role = dev_role,
            serial = data['dev_serial'],
        )

        # It is an incomplete script. Here is not a custom_field' part, a management interface' part and ip' part.
        
        device_new.save()

        self.log_success(f"Created new Juniper device: {device_new}")

        c1 = cmdb(username="",password="")
        r1 = c1.connect()
        self.log_success(f"CMDB connect: {r1}")
  
        r2 = c1.get_ProductsInfo(bname = device_new.device_type.model)       
        new_card = {
            "Code": device_new.name,
            "Hostname": device_new.name,
            "Availability":72,
            "State":121,
            "SerialNumber": device_new.serial,
            "Model": r2['data'][0]['_id'],
            "Brand": r2['data'][0]['Brand'],
            "Notes":"access-switch; JunOS; Juniper",
        }

        r4 = c1.insert_card_NetworkBox(card_data = new_card)

        self.log_success(f"CMDB connect: {r4}")

        r2 = c1.close()

        self.log_success(f"CMDB disconnect: {r2}")


        return 'OK'
