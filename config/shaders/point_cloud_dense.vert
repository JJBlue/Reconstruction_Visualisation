#version 430

layout (location=0) in vec3 pos;
layout (location=1) in vec3 in_normal;
layout (location=2) in vec3 in_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

uniform float point_size;

out vec3 color;

void main() {
	vec4 eye_pos = view * model * vec4(pos, 1.0);
	gl_Position = proj * eye_pos;

	float size = (1 / length(eye_pos.xyz));

	if(size < 1.0) {
		size = 1.0;
	}

	gl_PointSize = size * point_size;
	//gl_PointSize = point_size;

	color = in_color;
}
