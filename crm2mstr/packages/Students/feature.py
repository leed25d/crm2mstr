##
import logging

from packages.Util import (funcs)
from packages.Util.Classes import (Crm2mstrBase)
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

class Feature(Crm2mstrBase):
    def __init__(self, gateway, crm):
        super(Feature, self).__init__(gateway, crm)
        self.logContext['feature']= 'Students'
        self.log.info('__init__ complete')

    def run(self):
        ##self.gw_session.query(self.gw_meta.tables['crm_job_classes']).delete(synchronize_session=False)
        self.log.info('Students start run')
        
        ##self.gw_session.commit()
        ##self.log.info('JobClass %d rows committed', row_count)
