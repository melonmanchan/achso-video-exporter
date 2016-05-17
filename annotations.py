

def get_annotations_added_duration(annotations):
    duration = 0
    for annotation in annotations:
        duration += get_annotation_duration(annotation)
    return duration


def get_annotation_duration(annotation):
    return (len(annotation["text"]) * 0.4)


def sort_annotations_by_time(annotations):
    return sorted(annotations, key=lambda k: k["time"])
