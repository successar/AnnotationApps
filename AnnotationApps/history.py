import AnnotationApps.dbserver.api as dbapi
from AnnotationApps.dbserver.models import create_table, exist_table
from collections import defaultdict
from typing import Dict, List
import random

if not exist_table("history") :
    create_table("history", { "username" : str, "idx" : str, "value" : int })

def get_history(dataset_idx: List[str], username: str) -> Dict[str, bool]:
    rows: List[dict] = dbapi.filter_rows(tablename="history", keys={"username" : username})
    assignments: Dict[str, bool] = {}
    for row in rows :
        assignments[row["idx"]] = row["value"] == 1

    need_new_assignment = False not in list(assignments.values())

    if need_new_assignment :
        find_all_assignments: List[dict] = dbapi.filter_rows(tablename="history", keys={})
        num_assignments: Dict[str, int] = defaultdict(int)
        for row in find_all_assignments :
            num_assignments[row["idx"]] += 1

        remaining_assigments = set(dataset_idx) - set(num_assignments.keys())
        if len(remaining_assigments) != 0:
            new_assignment_idx: str = random.choice(list(remaining_assigments))
            assignments[new_assignment_idx] = False
            dbapi.add(tablename="history", keys={"username" : username, "idx" : new_assignment_idx}, value=0)

    assignments = {**{k: v for k, v in assignments.items() if not v}, **{k: v for k, v in assignments.items() if v}}
    return assignments

def update_history(assignment: str, username: str) :
    dbapi.add(tablename="history", keys={"username" : username, "idx" : assignment}, value=1)
    
