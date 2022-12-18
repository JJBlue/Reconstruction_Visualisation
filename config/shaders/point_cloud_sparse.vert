#version 430

layout (location=0) in vec3 pos;
layout (location=1) in vec3 in_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

uniform float point_size;

out vec3 color;
flat out unsigned int v_id;

void main() {
	gl_Position = proj * view * model * vec4(pos, 1.0);
	gl_PointSize = point_size;

	color = in_color;
	v_id = gl_VertexID;
}
