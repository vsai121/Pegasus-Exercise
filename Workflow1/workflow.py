#! /usr/bin/env python3
import logging
from pathlib import Path
from Pegasus.api import *

props = Properties()
props["pegasus.mode"] = "development"
props.write()

 

rc = ReplicaCatalog()
tc = TransformationCatalog()

echo = Transformation(
        "echo",
        site="condorpool",
        pfn="/bin/echo",
        is_stageable=False,
    )

tc.add_transformations(echo)
tc.write()


wf = Workflow("workflow1")

outfile = File("stdout.txt")
job_echo = Job(echo)\
                .add_args("hello world")\
                .set_stdout(outfile)


wf.add_jobs(job_echo)
wf.add_transformation_catalog(tc)
wf.add_replica_catalog(rc)

try:
    wf.plan(submit=True, verbose=3)\
        .wait()
except PegasusClientError as e:
    print(e)
