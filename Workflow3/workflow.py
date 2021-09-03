#!/usr/bin/env python3
import logging
from pathlib import Path
from Pegasus.api import *
import os

props = Properties()
props["pegasus.mode"] = "development"
props.write()

rc = ReplicaCatalog()

fileList = []
for filename in os.listdir("/home/scitech/pegasus-workflows/Workflow3/input/"):
    inputFileName = filename
    inputFile = File(inputFileName).add_metadata(creator="sai")
    fileList.append(inputFile)
    rc.add_replica("local", inputFile, Path("/home/scitech/pegasus-workflows/Workflow3/input/").resolve() / inputFileName)


tc = TransformationCatalog()

separate = Transformation(
        "separate",
        site="local",
        pfn="/home/scitech/pegasus-workflows/Workflow3/bin/separate.py",
        is_stageable=True
    )

count = Transformation(
        "count",
        site="local",
        pfn="/home/scitech/pegasus-workflows/Workflow3/bin/count.py",
        is_stageable=True
    )

tar = Transformation(
        "tar",
        site="condorpool",
        pfn="/bin/tar",
        is_stageable=False
    )

tc.add_transformations(separate)
tc.add_transformations(count)
tc.add_transformations(tar)
tc.write()


wf = Workflow("workflow3")

evenFileName = "even_nums.txt"
oddFileName = "odd_nums.txt"

evenFile = File(evenFileName)
oddFile = File(oddFileName)

job_separate = Job(separate)\
                .add_inputs(*fileList)\
                .add_outputs(evenFile, oddFile)

evenCountFilename = "even_count.txt"
evenCountFile = File(evenCountFilename)
job_count1 = Job(count)\
                .add_args(evenFileName, evenCountFilename)\
                .add_inputs(evenFile)\
                .add_outputs(evenCountFile)

oddCountFilename = "odd_count.txt"
oddCountFile = File(oddCountFilename)
job_count2 = Job(count)\
                .add_args(oddFileName, oddCountFilename)\
                .add_inputs(oddFile)\
                .add_outputs(oddCountFile)


result = File("result.tar.gz")
job_tar = Job(tar)\
                .add_args("-czvf", "result.tar.gz", evenCountFile, oddCountFile)\
                .add_inputs(evenCountFile, oddCountFile)\
                .add_outputs(result)


wf.add_jobs(job_separate, job_count1, job_count2, job_tar)
wf.add_transformation_catalog(tc)
wf.add_replica_catalog(rc)

try:
    wf.plan(submit=True)\
        .wait()
except PegasusClientError as e:
    print(e)
