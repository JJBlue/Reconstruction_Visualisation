#version 430

in vec3 color;
flat in int v_id;

layout (location=0) out vec4 out_color;
layout (location=1) out vec4 mouse_pick_color;

void main() {
	float a = (v_id & 0xFF) / 255.0;
	float b = ((v_id >> 8) & 0xFF) / 255.0;
	float g = ((v_id >> 16) & 0xFF) / 255.0;
	float r = ((v_id >> 24) & 0xFF) / 255.0;

	mouse_pick_color = vec4(r, g, b, a);
	out_color = vec4(color, 1.0);
}
