#version 430

in vec3 color;
flat in int v_id;

layout (location=0) out vec4 out_color;
layout (location=1) out vec4 mouse_picker;

void main() {
	float max_value = 4294967295.0;

	float a = (v_id & 0xFF) / max_value;
	float b = ((v_id >> 8) & 0xFF) / max_value;
	float g = ((v_id >> 16) & 0xFF) / max_value;
	float r = ((v_id >> 24) & 0xFF) / max_value;

	mouse_picker = vec4(r, g, b, a);
	out_color = vec4(color, 1.0);
}
