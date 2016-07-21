info = load('/home/aditya/data/cars/raw/annotations.mat');

class_names = fopen('/home/aditya/projects/image_dataset_preprocessing/output/class_names.txt', 'w');

for c = info.class_names
	fprintf(class_names, '%s\n', char(c));
end

fclose(class_names);

annotations = fopen('/home/aditya/projects/image_dataset_preprocessing/output/annotations.csv', 'w');
fprintf(annotations, 'rel_img_path,x1,y1,x2,y2,class,is_test_image\n');

for entry = info.annotations
	% The coordinates of the bounding box are saved in 0-indexed format since they will be
	% processed using Python, but the class index is kept in 1-indexed format since it will be
	% used in Torch.
	fprintf(annotations, '%s,%d,%d,%d,%d,%d,%d\n', char(entry.relative_im_path), ...
		entry.bbox_x1 - 1, entry.bbox_y1 - 1, entry.bbox_x2 - 1, entry.bbox_y2 - 1, ...
		entry.class, entry.test);
end

fclose(annotations);
