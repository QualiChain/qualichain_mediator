import csv
import json
import re
import math
import requests


API_ENDPOINT = "http://qualichain.epu.ntua.gr:9006/annotate"


class JobPosting:

    def __init__(self, job_title: str, job_requirements: str, job_text: str) -> None:
        self.job_title = job_title
        self.job_requirements = job_requirements
        self.job_text = job_text


class SkillAnnotationTask:

    def __init__(self, label: str, job_description: str) -> None:
        self.label = label
        self.jobDescription = job_description


class JobPostSkillExtractor:

    def __init__(self, job_posts) -> None:
        self.job_posts = job_posts
        self.tasks = self.create_tasks_from_job_posts(posts_per_task=5)
        self.batches = self.create_batches_of_tasks(tasks_per_batch=5)
        self.skill_annotation_input = [self.create_skill_annontation_input(batch) for batch in self.batches]
        self.skill_annotation_output = [self.send_skill_extraction_request(inp) for inp in self.skill_annotation_input]
        print(self.skill_annotation_output)

    def create_tasks_from_job_posts(self, posts_per_task=5):
        num_of_tasks = math.ceil(len(self.job_posts) / posts_per_task)
        label = ""
        tasks = []
        for i in range(1, num_of_tasks+1):
            task_text = ""
            for p in self.job_posts[(i-1) * posts_per_task: i*posts_per_task]:
                task_text += " "
                task_text += p.job_text

            task = SkillAnnotationTask(label, task_text)
            tasks.append(task)
        return tasks

    def create_batches_of_tasks(self, tasks_per_batch=5):
        num_of_batches = math.ceil(len(self.tasks)/tasks_per_batch)
        batches = []
        for i in range(1, num_of_batches+1):
            batch = self.tasks[(i-1)*tasks_per_batch: i*tasks_per_batch]
            batches.append(batch)
        return batches

    @staticmethod
    def create_skill_annontation_input(batch):
        json_inp = json.dumps({"tasks": [task.__dict__ for task in batch]}, indent=4)
        return json_inp

    @staticmethod
    def send_skill_extraction_request(skill_annotation_input):
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }

        r = requests.post(url=API_ENDPOINT, data=skill_annotation_input, headers=headers)
        response_text = r.text
        return response_text


def extract_job_postings_from_file(file_path: str):
    with open(file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=',')
        line_count = 0
        job_posts = []
        for row in csv_reader:
            if line_count != 0:
                job_title = row['job_title']
                job_title = re.sub(r"[^a-zA-Z0-9]+", ' ', job_title)
                job_text = row['full_text']
                job_text = re.sub(r"[^a-zA-Z0-9]+", ' ', job_text)
                job_requirements = row['job_requirements']
                job_requirements = re.sub(r"[^a-zA-Z0-9]+", ' ', job_requirements)
                job_posts.append(JobPosting(job_title, job_requirements, job_text))
            line_count += 1

        return job_posts


job_posts = extract_job_postings_from_file('data/jobs.csv')
skillExtractor = JobPostSkillExtractor(job_posts)

