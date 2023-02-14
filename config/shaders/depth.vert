#version 430

layout (location=0) in vec2 uv;
layout (location=1) in float depth;
layout (location=2) in vec3 color;

uniform mat4 extrinsics;
uniform mat3x4 intrinsics;

uniform mat4 view;
uniform mat4 proj;

out vec3 col;

void main() {
	vec4 pos = depth * extrinsics * mat4(intrinsics) * vec4(uv.x, uv.y, 1.0, 1.0/depth);
	//vec4 pos = extrinsics * mat4(intrinsics) * vec4(uv.x, uv.y, 1.0, 1.0); // Direkt in Camera Plane gezeichnet

	//pos = vec4(uv.x, uv.y, 0.0, 1.0);
	//pos = vec4(pos.x, -pos.y, -pos.z, pos.w);
	gl_Position = proj * view * pos;

	col = color;
}
