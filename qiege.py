import cv2
import os


def parse_annotation(annotation_path):
    with open(annotation_path, 'r') as f:
        lines = f.readlines()

    annotations = []
    for line in lines:
        line = line.strip().split()
        class_id = int(line[0])
        x_center = float(line[1])
        y_center = float(line[2])
        width = float(line[3])
        height = float(line[4])
        annotations.append((class_id, x_center, y_center, width, height))

    return annotations


def crop_person_objects(image_path, annotation_path, save_dir, min_object_size=(32, 32)):
    annotations = parse_annotation(annotation_path)
    image = cv2.imread(image_path)
    image_name = os.path.splitext(os.path.basename(image_path))[0]

    for idx, (class_id, x_center, y_center, width, height) in enumerate(annotations):
        if class_id == 0:  # Check if object is "person"
            x1 = int((x_center - width / 2) * image.shape[1])
            y1 = int((y_center - height / 2) * image.shape[0])
            x2 = int((x_center + width / 2) * image.shape[1])
            y2 = int((y_center + height / 2) * image.shape[0])

            person_crop = image[y1:y2, x1:x2]
            # Split person crop into smaller images
            h, w, _ = person_crop.shape
            num_rows = h // min_object_size[0]
            num_cols = w // min_object_size[1]

            for r in range(num_rows):
                for c in range(num_cols):
                    small_person_crop = person_crop[r * min_object_size[0]: (r + 1) * min_object_size[0],
                                        c * min_object_size[1]: (c + 1) * min_object_size[1]]
                    if small_person_crop.shape[0] >= min_object_size[0] and small_person_crop.shape[1] >= \
                            min_object_size[1]:
                        save_path = os.path.join(save_dir, f"{image_name}_person_object{idx}_row{r}_col{c}.jpg")
                        cv2.imwrite(save_path, small_person_crop)


if __name__ == "__main__":
    image_dir = "path/to/your/image_directory"
    annotation_dir = "path/to/your/annotation_directory"
    save_dir = "path/to/save/directory"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    image_files = os.listdir(image_dir)
    for image_file in image_files:
        image_path = os.path.join(image_dir, image_file)
        annotation_path = os.path.join(annotation_dir, f"{os.path.splitext(image_file)[0]}.txt")
        crop_person_objects(image_path, annotation_path, save_dir)
