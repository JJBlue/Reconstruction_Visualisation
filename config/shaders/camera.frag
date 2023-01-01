#version 460

in vec3 color;

uniform int project_id;
uniform int sub_project_id;
uniform int object_id;

layout (location=0) out vec4 out_color;
layout (location=1) out vec4 mouse_picker;

void main() {
	unsigned int max_value = 4294967295;

	out_color = vec4(color, 1.0);
	mouse_picker = vec4(project_id, ((sub_project_id << 16) + object_id), 0, max_value);
}
