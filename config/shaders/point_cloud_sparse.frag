#version 430

in vec3 color;
flat in int v_id;

layout (location=0) out vec4 out_color;
layout (location=1) out vec4 mouse_picker;

void main() {
	unsigned int max_value = 4294967295;

	unsigned int b = v_id & max_value;
	unsigned int g = (v_id >> 32) & max_value;
	unsigned int r = (v_id >> 64) & max_value;

	mouse_picker = uvec4(r, g, b, max_value);
	out_color = vec4(color, 1.0);
}
