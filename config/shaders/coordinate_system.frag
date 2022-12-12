#version 460

layout (location=0) out vec4 out_color;
layout (location=1) out vec4 mouse_picker;

in vec3 color;

void main() {
	out_color = vec4(color, 1.0);
	mouse_picker = vec4(0, 0, 0, 0);
}
