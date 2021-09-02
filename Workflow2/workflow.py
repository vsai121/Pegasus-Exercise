#!/usr/bin/env python3
import logging
from pathlib import Path
from Pegasus.api import *

props = Properties()
props["pegasus.mode"] = "development"
props.write()

inputFileName = "input.txt"
outputFileName = "result.txt"

inputFile = File(inputFileName).add_metadata(creator="sai")
rc = ReplicaCatalog().add_replica("local", inputFile, Path("/home/scitech/pegasus-workflows/Workflow2/input").resolve() / inputFileName)


tc = TransformationCatalog()

increment = Transformation(
        "increment",
        site="local",
        pfn="/home/scitech/pegasus-workflows/Workflow2/bin/increment.py",
        is_stageable=True,
        arch=Arch.X86_64,
        os_type=OS.LINUX
    )

tc.add_transformations(increment)
tc.write()


wf = Workflow("workflow2")

outputFile = File(outputFileName)
job_increment = Job(increment)\
                .add_args(inputFileName, outputFileName)\
                .add_inputs(inputFile)\
                .add_outputs(outputFile)


wf.add_jobs(job_increment)
wf.add_transformation_catalog(tc)
wf.add_replica_catalog(rc)

try:
    wf.plan(submit=True)\
        .wait()
except PegasusClientError as e:
    print(e)
