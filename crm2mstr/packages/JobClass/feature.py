##
import logging
import unicodedata

from packages.Util import (funcs)
from packages.Util.Classes import (Crm2mstrBase)
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base

class Feature(Crm2mstrBase):
    def __init__(self, gateway, crm):
        super(Feature, self).__init__(gateway, crm)
        self.logContext['feature']= 'JobClass'
        self.log.info('__init__ complete')

    def run(self):
        self.gw_session.query(self.gw_meta.tables['crm_job_classes']).delete(synchronize_session=False)
        self.log.info('JobClass start run')
       
        jc= self.crm_meta.tables['phs_job_classExtensionBase']
        acct= self.crm_meta.tables['AccountExtensionBase']
        JobClass= funcs.make_tableclass('JobClass', declarative_base(metadata= self.gw_meta), __tablename__= 'crm_job_classes')
        try:
            row_count= 0
            for j in self.crm_session.query(jc, acct).filter(jc.c.phs_ac_jc_id == acct.c.AccountId):
                row_count += 1
                row= JobClass()
                row.crm_jc_id        =  j.phs_job_classId
                row.phs_ccode        =  j.phs_ccode
                row.phs_title        =  unicodedata.normalize('NFKD', j.phs_title).encode('ascii','ignore')
                row.parentcustomerid =  j.phs_ac_jc_id
                row.parent_oracle_id =  j.phs_oracle_id
                row.phs_enabled_flag =  j.phs_enabled_flag
                row.phs_oracle_jc_id =  j.phs_oracle_jc_id
                row.modifiedon       =  datetime.now()
                self.gw_session.add(row)

        except Exception:
            self.gw_session.rollback()
            raise
        
        self.gw_session.commit()
        self.log.info('JobClass %d rows committed', row_count)
