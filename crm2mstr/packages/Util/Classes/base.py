import logging

from sqlalchemy import (MetaData, create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (sessionmaker)

class Crm2mstrBase(object):
    def __init__(self, gateway_connect, crm_connect):
        self.gw_meta= MetaData()
        self.crm_meta= MetaData()

        gatewayEngine = create_engine(gateway_connect)
        self.gw_meta.reflect(bind=gatewayEngine)
        self.gw_session= sessionmaker(bind=gatewayEngine)()

        crmEngine = create_engine(crm_connect)
        self.crm_meta.reflect(bind=crmEngine, only=['phs_job_classExtensionBase', 'AccountExtensionBase'])
        self.crm_session= sessionmaker(bind=crmEngine)()

        self.logContext= {'feature':'Feature'}
        self.log= logging.LoggerAdapter(logging.getLogger('feature'), self.logContext)

