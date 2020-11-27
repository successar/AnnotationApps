import AnnotationApps.dbserver.api as dbapi
from collections import defaultdict
from typing import NamedTuple, Dict, List
import random


def get_history(dataset_idx: List[str], username: str) :
    rows: List[dict] = dbapi.filter_rows(tablename="history", keys={"username" : username})
    assignments: Dict[str, bool] = {}
    for row in rows :
        assignments[row["idx"]] = row["done"] == 1

    need_new_assignment = 0 not in list(assignments.values())

    if need_new_assignment :
        find_all_assignments: List[dict] = dbapi.filter_rows(tablename="history", keys={})
        num_assignments: Dict[str, int] = defaultdict(int)
        for row in find_all_assignments :
            num_assignments[row["idx"]] += 1

        remaining_assigments = set(dataset_idx) - set(num_assignments.keys())
        if len(remaining_assigments) != 0:
            new_assignment_idx: str = random.choice(list(remaining_assigments))
            assignments[new_assignment_idx] = False
            dbapi.add_or_delete(tablename="history", keys={"username" : username, "idx" : new_assignment_idx, "done": 0}, value=True)

    return assignments

def update_history(assignment: str, username: str) :
    dbapi.update(tablename="history", keys={"username" : username, "idx" : assignment}, update={"done": 1})
    
