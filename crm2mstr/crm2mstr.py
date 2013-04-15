#!/usr/bin/env python
import os
import sys

import argparse
import errno
import logging
import logging.config
import re
import urllib

import ConfigParser

class Crm2mstrArgs(object):
    def __init__(self, *args, **kwargs):
        self.parser= argparse.ArgumentParser(description='Import CRM data to the mstr database')

        self.parser.add_argument('--gateway_connect',
                            default=os.environ.get('GATEWAY_CONNECT', None),
                            help='Connection string for the input database (eg. oracle://www:426hemi@10.20.10.115:1521/XE)')

        self.parser.add_argument('--crm_connect',
                            default=os.environ.get('CRM_CONNECT', None),
                            help='Connection string for the crm database')

        self.parser.add_argument('--features',
                            default=os.environ.get('FEATURES', None),
                            help='comma separated list of feature plugins to run')

run_defaults= {
    'gateway_connect'  : 'oracle://mstr:blahblah@10.20.10.115:1521/XE',
    'crm_dsn'          : r'crmdatasource;UID=PHS\ldoolan;PWD=C0ltr@n3;DATABASE=CRM4_MSCRM;',
    'features'         : 'NoSuchFeature',
}
aDict= vars(Crm2mstrArgs().parser.parse_args())
cliArgs= {k:aDict[k] for k in list(aDict) if aDict[k] != None}

crm2mstr_ini = ConfigParser.ConfigParser(run_defaults)
crm2mstr_ini.read('crm2mstr.ini')
crm2mstr_ini.set('main', 'crm_connect', 'mssql+pyodbc:///?odbc_connect=' + urllib.quote_plus(crm2mstr_ini.get('main', 'crm_dsn', 0, cliArgs)))

logging.config.fileConfig('crm2mstr.ini')
log= logging.getLogger('crm2mstr')

class Main(object):
    def __init__(self):
        self.log= log
        self.log.info('=' * 72)
        self.log.info("gateway ===>> " + crm2mstr_ini.get('main', 'gateway_connect', 0, cliArgs))
        self.log.info("crm     ===>> " + crm2mstr_ini.get('main', 'crm_connect', 0, cliArgs))
        self.log.info("features     ===>> " + crm2mstr_ini.get('main', 'features', 0, cliArgs))
        self.log.info("main __init__ comlete")

        self.features= re.split(r',', crm2mstr_ini.get('main', 'features', 0, cliArgs))

        self.lockfile= ''

    def __lock_feature(self, feat):
        self.lockfile= '/tmp/CRM2MSTRFEATURE_' + feat
        self.lock_fd= os.open(self.lockfile, os.O_NONBLOCK|os.O_CREAT|os.O_EXCL|os.O_WRONLY)
        pid= os.getpid()

        os.write(self.lock_fd, '%d\n' % (pid))
        self.log.info('%s locked by pid= %d' % (self.lockfile, pid))

    def __unlock_feature(self):
        if self.lockfile != '':
            self.log.info('unclock %s' % (self.lockfile))
            os.unlink(self.lockfile)
            self.lockfile= ''

    def run(self):
        for feat in self.features:
            self.log.info("Feature %s" % (feat))
            try:
                self.__lock_feature(feat)
                try:
                    self.log.warn("Loading feature %s" % (feat))
                    exec("from packages.%s import feature as f" % (feat))
                    f.Feature(crm2mstr_ini.get('main', 'gateway_connect', 0, cliArgs), crm2mstr_ini.get('main', 'crm_connect', 0, cliArgs)).run()

                except Exception as e:
                    self.log.error("exception during feature %s.  error ===>> %s.  " % (feat, e))

            except OSError as e:
                if e.errno == errno.EEXIST:
                    self.log.warn("locked feature %s skipped.  error ===>> %s." % (feat, e))

                else:
                    self.__unlock_feature()
                    self.log.exception("feature %s weird OSError during lock.  error ===>> %s." % (feat, e))
                    raise

            except Exception as e:
                self.log.error("locking feature %s resulted in an exception.  error ===>> %s." % (feat, e))


            self.__unlock_feature()

if __name__ == '__main__':
    Main().run()
