from extraction_pipeline.execute_pipeline import Executor


if __name__ == "__main__":
    job_post_ids=[1,367,363,369,372,374,376,377,378,420,437,364,366,415,1374,6,7,368,365,371,397,370]
    executor = Executor(job_post_ids)
    executor.execution_stage()