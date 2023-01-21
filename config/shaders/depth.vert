#version 430

layout (location=0) in vec2 uv;
layout (location=1) in float depth;
layout (location=2) in vec3 color;

uniform mat4 extrinsics;
uniform mat3x4 intrinsics;

uniform mat4 view;
uniform mat4 proj;

out vec3 col;
out float disc;

void main() {
	vec4 pos = extrinsics * vec4((intrinsics * vec3(uv.x, uv.y, depth / 50 )).xyz, 1.0);
	//pos = vec4(uv.x, uv.y, 0.0, 1.0);
	//pos = vec4(pos.x, -pos.y, -pos.z, pos.w);
	gl_Position = proj * view * pos;

	col = color;

	disc = 0.0; // valid
	//if(depth <= 1.0) {
	//	disc = 1.0;
	//}
}
