#version 440

in vec2 tex_uv;

uniform sampler2D tex;

out vec4 out_color;

void main() {
	vec4 tex_color = texture(tex, tex_uv).rgba;
	out_color = tex_color;
}
