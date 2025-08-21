# Python Scripts for Canvas I've Used as an Instructor

These are some scripts I've found useful as an instructor of a course that uses the Canvas LMS. See the last part of this README for dependencies and `.env` information needed.  

## Unpublish all items and modules

I've found this script useful when copying a previous course site into a new course site and want to start the course with things unpublished.  Canvas used to make this difficult, particularly when copying from an old course. Now the experience is improved from a UI perspective, but this script still may be helpful!

Warning: this script will *unpublish* all modules and items in the course!

```
python ./unpublish_all_modules_and_items.py
```

## Get all submissions in a course

This script produces a CSV file of data about submissions for a specific Canvas course site.

I've found this useful to grab all the submissions in the course to make sure everything is graded and accounted for.  In particular, I've found resubmissions tricky in Canvas, so there's a field in the output for "Grade Matches Current Submission" -- if this is true, check that submission out!  The CSV produced also includes a link directly to the Canvas Speed Grader for that particular submission.

With the `--only-needs-check` flag, only the submissions that are ungraded or have had resubmissions are included. 
```
python ./get_submissions_in_course.py --only-needs-check
```
If you want information about all the submissions, then run it without the flag. 
```
python ./get_submissions_in_course.py
```
### Python install dependencies and setup script environment

Install dependences
```
pip install -r requirements.txt
```
Create a `.env` file based on `.env.sample`
```
CANVAS_API_TOKEN=<your canvas token here>
CANVAS_URL=https://canvas.<DOMAIN>.edu
CANVAS_COURSE_ID=<course id>
```
Now you can run the scripts!