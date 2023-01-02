#version 430

in vec3 color;
flat in unsigned int v_id;

uniform int project_id;
uniform int sub_project_id;
uniform int object_id;

layout (location=0) out vec4 out_color;
layout (location=1) out uvec4 mouse_picker;

void main() {
	unsigned int max_value = 4294967295;

	out_color = vec4(color, 1.0);
	mouse_picker = uvec4(project_id, ((sub_project_id << 16) + object_id), v_id & max_value, max_value);
}
