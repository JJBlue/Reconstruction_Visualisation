#version 440

in vec2 tex_uv;

uniform sampler2D tex;

out vec4 out_color;

float func(unsigned int v) {
	double x = v / double(4294967295);
	return -1.0 * sin(float(1.5 * x)) + 1.0;
}

void main() {
	vec4 tex_color = texture(tex, tex_uv).rgba;

	if(tex_color.x > 1 || tex_color.y > 1 || tex_color.z > 1 || tex_color.w > 1) {		// Colors are wrong
		unsigned int x = unsigned int(tex_color.x);
		unsigned int y = unsigned int(tex_color.y);
		unsigned int z = unsigned int(tex_color.z);
		unsigned int w = unsigned int(tex_color.w);

		out_color = vec4(func(x), func(y), func(z), func(w));
		out_color = vec4(1, 1, 1, 1);
	} else {		// Normal Output for Normal Texture
		out_color = vec4(tex_color);
	}
}
