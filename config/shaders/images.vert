#version 440

layout (location=0) in vec3 pos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

out vec2 texCoord;

void main() {
	gl_Position = proj * view * model * vec4(pos, 1.0);
	texCoord = vec2(pos.x, pos.y);
}
