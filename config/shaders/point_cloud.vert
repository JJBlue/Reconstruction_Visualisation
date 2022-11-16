#version 430

layout (location=0) in vec3 pos;
layout (location=1) in vec3 in_normal;
layout (location=2) in vec3 in_color;

uniform mat4 view;
uniform mat4 proj;

out vec3 normal;
out vec3 color;

void main() {
	gl_Position = proj * view * vec4(pos, 1.0);

	normal = in_normal;
	color = in_color;
}
