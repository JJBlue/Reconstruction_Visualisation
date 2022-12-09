#version 430

layout (location=0) in vec3 pos;
layout (location=1) in vec3 in_normal;
layout (location=2) in vec3 in_color;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;

uniform float point_size;

out vec3 normal;
out vec3 color;
flat out int v_id;

void main() {
	gl_Position = proj * view * model * vec4(pos.x, -pos.y, -pos.z, 1.0);
	gl_PointSize = point_size;

	normal = in_normal;
	color = in_color;
	v_id = gl_VertexID;
}
