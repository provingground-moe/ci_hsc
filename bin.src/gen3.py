#!/usr/bin/env python

# This file is part of ci_hsc.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import logging
import argparse

import lsst.log
from lsst.log import Log
from lsst.ci.hsc import gen3, Gen3ButlerWrapper

from lsst.obs.subaru.gen3.hsc import HyperSuprimeCam


def main(config=None):
    gen3wrapper = Gen3ButlerWrapper(config=config)
    registry = gen3wrapper.getRegistry()
    datastore = gen3wrapper.getDatastore(registry)
    walker = gen3.walk()
    gen3.write(walker, registry, datastore)
    HyperSuprimeCam().writeCuratedCalibrations(gen3wrapper.getButler("calib"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert ci_hsc data repos to Butler Gen 3.")
    parser.add_argument("-v", "--verbose", action="store_const", dest="logLevel",
                        default=Log.INFO, const=Log.DEBUG,
                        help="Set the log level to DEBUG.")
    parser.add_argument("-c", "--config",
                        help="Path to a butler configuration file to be used instead of the default"
                             " ci_hsc configuration.")
    args = parser.parse_args()
    log = Log.getLogger("lsst.daf.butler")
    log.setLevel(args.logLevel)

    # Forward python logging to lsst logger
    lgr = logging.getLogger("lsst.daf.butler")
    lgr.setLevel(logging.INFO if args.logLevel == Log.INFO else logging.DEBUG)
    lgr.addHandler(lsst.log.LogHandler())

    main(config=args.config)
