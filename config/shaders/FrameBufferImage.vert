#version 440

layout (location=0) in vec3 pos;
// layout (location=1) in vec3 normal;
// layout (location=2) in vec3 colors;
layout (location=3) in vec2 uv;

out vec2 tex_uv;

void main() {
	gl_Position = vec4(pos, 0.0);
	tex_uv = uv;
}
