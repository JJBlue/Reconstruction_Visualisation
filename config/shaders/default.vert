#version 430

layout (location=0) in vec3 pos;
layout (location=0) in vec3 in_normal;

uniform mat4 view;
uniform mat4 proj;

out vec3 normal;

void main() {
	gl_Position = proj * view * vec4(pos, 1.0);
	//gl_Position = vec4(pos, 1.0);

	normal = in_normal;
}
