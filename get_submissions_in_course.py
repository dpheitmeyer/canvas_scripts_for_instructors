from canvasapi import Canvas
from dotenv import load_dotenv
import os
import datetime
import csv
import re
import argparse

def prompt_create_env():
    print("It doesn't look like you have these scripts fully configured in a .env file.")
    resp = input("Would you like some help creating one? (y/n): ").strip().lower()
    if resp != "y":
        print("Exiting. Please set up your .env file and rerun the script.")
        exit(1)
    canvas_url = input("Enter your Canvas course URL (e.g., https://canvas.harvard.edu/courses/12345): ").strip()
    match = re.match(r"(https?://[^/]+)/courses/(\d+)", canvas_url)
    if not match:
        print("Could not parse Canvas URL. Please ensure it matches the format above.")
        exit(1)
    url, course_id = match.group(1), match.group(2)
    print("To create an API token, go to:")
    print(f"{url}/profile/settings")
    print("and click '+ New Access Token'")
    api_token = input("Paste your Canvas API token here: ").strip()
    timestamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    # Check if .env exists and back it up if so
    if os.path.exists(".env"):
        backup_name = f".env-bak-{timestamp}"
        print(f"Existing .env found. Backing up to {backup_name}")
        os.rename(".env", backup_name)
    with open(".env", "w") as f:
        f.write(f"## ------------------------------------\n")
        f.write(f"#  .env file created {timestamp}\n")
        f.write(f"## ------------------------------------\n")        
        f.write(f"CANVAS_URL={url}\n")
        f.write(f"CANVAS_API_TOKEN={api_token}\n")
        f.write(f"CANVAS_COURSE_ID={course_id}\n")
    print("Wrote .env file. Please rerun the script.")
    exit(0)
    
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
    CANVAS_COURSE_ID = os.getenv("CANVAS_COURSE_ID")

    if not (CANVAS_URL and CANVAS_API_TOKEN and CANVAS_COURSE_ID):
        prompt_create_env()

    CANVAS_COURSE_ID = int(CANVAS_COURSE_ID)
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