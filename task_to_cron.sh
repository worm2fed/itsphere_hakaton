#!/bin/bash
SHELL=/bin/bash
*/6 * * * * source /home/bbx/webapps/itsphere/env/bin/activate && /home/bbx/webapps/itsphere/itsphere_hakaton/manage post > /dev/null
