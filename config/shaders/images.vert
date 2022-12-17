#version 440

layout (location=0) in vec3 pos;
layout (location=1) in vec3 normals;
layout (location=2) in vec2 uv;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec2 texCoord;

void main() {
	gl_Position = proj * view * model * vec4(pos, 1.0);
	texCoord = uv;
}
