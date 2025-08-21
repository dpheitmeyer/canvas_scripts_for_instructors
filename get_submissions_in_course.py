from canvasapi import Canvas
from dotenv import load_dotenv
import os
import datetime
import csv
import re
import argparse

def get_submissions_in_course(course):
    users = {}
    mycourse_id = course.id
    courseusers = course.get_users()
    for user in courseusers:
        users[user.id] = user
    timestampstr = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    resultData = [];
    myfile = f"./assignments_to_check-{course.id}-{timestampstr}.csv"
    resultFile = open(myfile,'w')
    wr = csv.writer(resultFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ["Assignment Name","AssignmentID","Due At","UserID","Student","Submitted At","Late",
    "Score","Grade Matches Current Submission","Workflow State","Speed Grader URL","URL"]
    wr.writerow(header)
    assignments = course.get_assignments()
    print("#===== ASSIGNMENTS =====#")
    subcount = 0
    for assgn in assignments:
        submissions = {}
        a = course.get_assignment(assgn.id)
        submissions = a.get_submissions()
        print(f"{assgn.id}\t{a.name}")
        for s in submissions:
            myrow = []
            subcount += 1
            #print(a.name,"\t",s.assignment_id,"\t",s.user_id,"\t",s.grader_id,"\t",s.score,"\t",s.grade_matches_current_submission,"\t",s.workflow_state)
            if (not(ONLY_NEEDS_CHECK) or s.grade_matches_current_submission is False or not(s.workflow_state in ['graded','unsubmitted']) ):
                speedgraderurl = f"{CANVAS_URL}/courses/{mycourse_id}/gradebook/speed_grader?assignment_id={s.assignment_id}&student_id={s.user_id}"
                studentname = ''
                if s.user_id in users:
                    myuser = users[s.user_id]
                    studentname  = myuser.sortable_name
                myrow.append(a.name)
                myrow.append(s.assignment_id)
                myrow.append(a.due_at)
                myrow.append(s.user_id)
                myrow.append(studentname)
                myrow.append(s.submitted_at)
                myrow.append(s.late)
                myrow.append(s.score)
                myrow.append(s.grade_matches_current_submission)
                myrow.append(s.workflow_state)
                myrow.append(speedgraderurl)
                myrow.append(s.url)
                wr.writerow(myrow)
                resultData.append(myrow)
    print("total submissions:  ",subcount)
    print(f"Submission data in {myfile}")




if __name__ == "__main__":
    load_dotenv()
    CANVAS_URL = os.getenv("CANVAS_URL")
    CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
    CANVAS_COURSE_ID = int(os.getenv("CANVAS_COURSE_ID"))

    canvas = Canvas(CANVAS_URL, CANVAS_API_TOKEN)
    course = canvas.get_course(CANVAS_COURSE_ID)
    parser = argparse.ArgumentParser(description="Get Canvas course submissions.")
    parser.add_argument(
        "--only-needs-check",
        action="store_true",
        help="Only output submissions that need to be checked."
    )
    args = parser.parse_args()

    ONLY_NEEDS_CHECK = args.only_needs_check
    print(f"Course: {course.name}")
    print(f"URL: {CANVAS_URL}/courses/{course.id}/")
    get_submissions_in_course(course)
    exit()