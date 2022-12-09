#version 440

layout (location=0) in vec3 pos;
layout (location=3) in vec2 uv;

out vec2 tex_uv;

void main() {
	gl_Position = vec4(pos, 1.0);
	tex_uv = uv;
}
