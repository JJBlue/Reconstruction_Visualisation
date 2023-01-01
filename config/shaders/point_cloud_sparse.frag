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

	unsigned int b = v_id & max_value;
	unsigned int g = ((sub_project_id << 16) + object_id);
	unsigned int r = project_id;

	mouse_picker = uvec4(r, g, b, max_value);
	out_color = vec4(color, 1.0);
}
