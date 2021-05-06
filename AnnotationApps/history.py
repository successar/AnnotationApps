import random
from collections import defaultdict
from typing import Dict, List

import AnnotationApps.dbserver.api as dbapi
from AnnotationApps.dbserver.models import create_table, exist_table

if not exist_table("history") :
    create_table("history", { "username" : str, "id" : str, "value" : int })

def get_all_usernames() :
    rows: List[dict] = dbapi.filter_rows(tablename="history", keys={})
    usernames = sorted(list(set([row["username"] for row in rows])))
    return usernames

def get_history(dataset_ids: List[str], username: str) -> Dict[str, bool]:
    dataset_ids = set(dataset_ids)

    # Get Existing Assignments of this user
    rows: List[dict] = dbapi.filter_rows(tablename="history", keys={"username" : username})

    # Convert them to a dictionary with key = assignment id and value = if it was completed by the user.
    assignments: Dict[str, bool] = {}
    for row in rows :
        # Check to see if the assignment is in current dataset_ids list. 
        if row["id"] in dataset_ids :
            assignments[row["id"]] = row["value"] == 1

    # Check if the user has a incomplete assignment
    need_new_assignment = False not in list(assignments.values())

    # If not,
    if need_new_assignment :
        # Find all ids that have been assigned to *some* user.
        find_all_assignments: List[dict] = dbapi.filter_rows(tablename="history", keys={})

        # Convert to a dictionary with key = assignment id and value = to how many user it has been assigned.
        num_assignments: Dict[str, int] = defaultdict(int)
        for row in find_all_assignments :
            num_assignments[row["id"]] += 1

        # Find annotation ids, not assigned to anyone
        remaining_assigments = dataset_ids - set(num_assignments.keys())

        # If there exist such an annotation id,
        if len(remaining_assigments) != 0:
            # Select one randomly
            new_assignment_id: str = random.choice(list(remaining_assigments))

            # Assign it to current user.
            assignments[new_assignment_id] = False

            # Add the assignment to db with value = 0 (=> that assignment is incomplete)
            dbapi.add(tablename="history", keys={"username" : username, "id" : new_assignment_id}, value=0)

    # Return all assignments to this user (completed and incomplete)
    assignments = {**{k: v for k, v in assignments.items() if not v}, **{k: v for k, v in assignments.items() if v}}
    return assignments

def mark_as_completed(assignment_id: str, username: str) :
    dbapi.add(tablename="history", keys={"username" : username, "id" : assignment_id}, value=1)
    
