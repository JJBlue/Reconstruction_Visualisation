#version 430

in vec3 col;

out vec4 out_color;

void main() {
	//out_color = vec4(col, 1.0);
	out_color = vec4(col / 255.0, 1.0);
}
