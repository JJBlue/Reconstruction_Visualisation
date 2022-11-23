#version 440

layout (location=0) in vec3 pos;
layout (location=1) in vec3 in_color;

uniform mat4 view;
uniform mat4 proj;

out vec3 color;

void main() {
	gl_Position = proj * view * vec4(pos, 1.0);
	color = in_color;
}
