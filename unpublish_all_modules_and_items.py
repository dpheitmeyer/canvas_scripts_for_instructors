from canvasapi import Canvas
from dotenv import load_dotenv
import os


def print_modules_and_items(course):
    modules = course.get_modules()
    for module in modules:
        print(f"Module\tPublished:{module.published}\t{module.name} ({module.id})")
        items = module.get_module_items()
        for item in items:
            print(f"Item\tPublished:{item.published}\t{item.title} ({item.id}, {item.type})")

def unpublish_modules_and_items(course):
    modules = course.get_modules()
    for module in modules:
        if module.published:
            module.edit(module={'published': False})
        items = module.get_module_items()
        for item in items:
            # Most item types (Page, Assignment, Quiz, etc.) can be unpublished via 'published': False
            # However, some types (like 'ExternalUrl', 'ExternalTool') may not support unpublishing or may behave differently.
            # The Canvas API will raise an error if unpublishing is not supported for a given item type.
            try:
                if item.published:
                    if item.type == "File":
                        print(f"skipping file module item - {item.title}")
                    else: 
                        item.edit(module_item={'published': False})                    
            except Exception as e:
                print(f"Could not unpublish item {item.title} ({item.id}, {item.type}): {e}")


if __name__ == "__main__":
    load_dotenv()
    CANVAS_URL = os.getenv("CANVAS_URL")
    CANVAS_API_TOKEN = os.getenv("CANVAS_API_TOKEN")
    CANVAS_COURSE_ID = int(os.getenv("CANVAS_COURSE_ID"))

    canvas = Canvas(CANVAS_URL, CANVAS_API_TOKEN)
    course = canvas.get_course(CANVAS_COURSE_ID)

    print(f"Course: {course.name}")
    print(f"URL: {CANVAS_URL}/courses/{course.id}/")

    
    print_modules_and_items(course)

    confirm = input("Are you sure you want to unpublish\nALL modules and items for this course?\nType 'yes' to continue: ")
    if confirm.lower() != 'yes':
        print("Operation cancelled.")
        exit()
    else:
        print("Unpublishing modules and items")
        unpublish_modules_and_items(course)

    print("\nAfter unpublishing:")
    print_modules_and_items(course)


