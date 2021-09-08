#!/usr/bin/env python3
import logging
from pathlib import Path
from Pegasus.api import *

props = Properties()
props["pegasus.mode"] = "development"
props.write()

inputFileName = "message.txt"
outputFileName = "result.txt"

inputFile = File(inputFileName).add_metadata(creator="sai")
rc = ReplicaCatalog().add_replica("local", inputFile, Path("/home/scitech/pegasus-workflows/Workflow4/input").resolve() / inputFileName)


tc = TransformationCatalog()

tools_container = Container(
                  "ubuntu-container",
                  Container.DOCKER,
                  image="docker:///vsai121/ubuntu_thumbs_up:latest",
                  arguments="--shm-size=2g",
                  bypass_staging=True
               )

tc.add_containers(tools_container)

add_thumbs_up = Transformation(
        "add_thumbs_up",
        site="local",
        pfn="/home/scitech/pegasus-workflows/Workflow4/bin/add_thumbs_up.py",
        is_stageable=True,
        container=tools_container
    )

tc.add_transformations(add_thumbs_up)

wf = Workflow("workflow4")

outputFile = File(outputFileName)
job_add_thumbs_up = Job(add_thumbs_up)\
                .add_args(inputFileName, outputFileName)\
                .add_inputs(inputFile)\
                .add_outputs(outputFile)


wf.add_jobs(job_add_thumbs_up)
wf.add_transformation_catalog(tc)
wf.add_replica_catalog(rc)

try:
    wf.plan(submit=True)\
        .wait()
except PegasusClientError as e:
    print(e)
